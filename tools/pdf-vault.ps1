<#
.SYNOPSIS
    把 PDF（或任意文件）加密成"看不出是 PDF"的不透明容器；凭口令解回原文件。

.DESCRIPTION
    容器是纯二进制，没有 %PDF 文件头、没有 PDF 结构，云盘/网盘的预览与内容识别都认不出来。
    格式：
        magic(8) | ver(1) | kdf(1) | iters(4, 大端) | salt(16) | iv(16) | ciphertext(N) | hmac(32)

    算法：
        PBKDF2-HMAC-SHA256(口令, salt, iters) -> 64 字节
            前 32 字节 = AES-256 密钥
            后 32 字节 = HMAC 密钥
        AES-256-CBC + PKCS7 加密正文
        HMAC-SHA256 覆盖 magic 到 ciphertext 的全部字节（Encrypt-then-MAC）
        解密时先验 MAC：口令错误或被篡改都会直接失败，不会写出半截文件。

.PARAMETER Encrypt
    要加密的源文件，例如 .\考纲.pdf

.PARAMETER Decrypt
    要解密的容器文件，例如 .\考纲.dat（也接受 -Armor 生成的 Base64 文本）

.PARAMETER Out
    输出路径。默认：加密 -> 同名 .dat（加 -Armor 则为 .txt）；解密 -> 同名 .pdf

.PARAMETER Password
    口令。省略则交互输入；也可用 -PasswordFile 从文件读取（避免进命令历史）

.PARAMETER PasswordFile
    存放口令的文本文件（取首行）

.PARAMETER Armor
    输出 Base64 文本（每行 64 字符），在云盘里看起来只是一段普通文本

.PARAMETER Iterations
    PBKDF2 迭代次数，默认 200000

.PARAMETER Force
    输出文件已存在时覆盖

.EXAMPLE
    .\pdf-vault.ps1 -Encrypt .\考纲.pdf

.EXAMPLE
    .\pdf-vault.ps1 -Encrypt .\考纲.pdf -Armor -Out .\笔记备份.txt

.EXAMPLE
    .\pdf-vault.ps1 -Decrypt .\考纲.dat -Out .\考纲.pdf
#>
#Requires -Version 5.1
[CmdletBinding(DefaultParameterSetName = 'Encrypt')]
param(
    [Parameter(Mandatory, ParameterSetName = 'Encrypt', Position = 0)]
    [string]$Encrypt,

    [Parameter(Mandatory, ParameterSetName = 'Decrypt', Position = 0)]
    [string]$Decrypt,

    [string]$Out,
    [string]$Password,
    [string]$PasswordFile,
    [switch]$Armor,
    [int]$Iterations = 200000,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$script:Magic = [byte[]](0x4D, 0x44, 0x56, 0x4C, 0x54, 0x30, 0x31, 0x00)  # "MDVLT01\0"
$script:Version = [byte]1
$script:KdfPbkdf2Sha256 = [byte]1
$script:HeaderSize = 8 + 1 + 1 + 4 + 16 + 16   # 46
$script:MacSize = 32

function Resolve-FullPath {
    param([string]$Path, [switch]$MustExist)
    $p = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
    if ($MustExist -and -not (Test-Path -LiteralPath $p -PathType Leaf)) {
        throw "找不到文件: $p"
    }
    return $p
}

function Get-DefaultOutPath {
    param([string]$InPath, [switch]$Decrypting, [switch]$Armor)
    $dir = [IO.Path]::GetDirectoryName($InPath)
    if ($Decrypting) {
        return [IO.Path]::Combine($dir, [IO.Path]::GetFileNameWithoutExtension($InPath) + '.pdf')
    }
    $ext = if ($Armor) { '.txt' } else { '.dat' }
    return [IO.Path]::Combine($dir, [IO.Path]::GetFileNameWithoutExtension($InPath) + $ext)
}

function Get-PlainPassword {
    if ($Password) { return $Password }
    if ($PasswordFile) {
        $line = Get-Content -LiteralPath (Resolve-FullPath $PasswordFile -MustExist) -TotalCount 1
        if (-not $line) { throw "口令文件为空: $PasswordFile" }
        return $line
    }
    $sec = Read-Host -AsSecureString '输入口令'
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

function New-SubKey {
    param([string]$Password, [byte[]]$Salt, [int]$Iterations)
    $kdf = [System.Security.Cryptography.Rfc2898DeriveBytes]::new(
        $Password, $Salt, $Iterations, [System.Security.Cryptography.HashAlgorithmName]::SHA256)
    try {
        $material = $kdf.GetBytes(64)
    }
    finally { $kdf.Dispose() }

    $aesKey = [byte[]]::new(32)
    $macKey = [byte[]]::new(32)
    [Array]::Copy($material, 0, $aesKey, 0, 32)
    [Array]::Copy($material, 32, $macKey, 0, 32)
    [Array]::Clear($material, 0, $material.Length)
    return @{ Aes = $aesKey; Mac = $macKey }
}

function Get-Hmac {
    param([byte[]]$Key, [byte[]]$Data)
    $h = [System.Security.Cryptography.HMACSHA256]::new($Key)
    try { return $h.ComputeHash($Data) }
    finally { $h.Dispose() }
}

function Test-BytesEqual {
    param([byte[]]$A, [byte[]]$B)
    if ($null -eq $A -or $null -eq $B -or $A.Length -ne $B.Length) { return $false }
    $diff = 0
    for ($i = 0; $i -lt $A.Length; $i++) { $diff = $diff -bor ($A[$i] -bxor $B[$i]) }
    return ($diff -eq 0)
}

function New-Aes {
    param([byte[]]$Key, [byte[]]$Iv)
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aes.Key = $Key
    $aes.IV = $Iv
    return $aes
}

function Write-OutputFile {
    param([string]$Path, [byte[]]$Bytes, [switch]$Force)
    if ((Test-Path -LiteralPath $Path) -and -not $Force) {
        throw "输出文件已存在（加 -Force 覆盖）: $Path"
    }
    $dir = [IO.Path]::GetDirectoryName($Path)
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $fs = [IO.File]::Open($Path, [IO.FileMode]::Create, [IO.FileAccess]::Write)
    try { $fs.Write($Bytes, 0, $Bytes.Length) }
    finally { $fs.Dispose() }
}

function Invoke-Encrypt {
    $inPath = Resolve-FullPath $Encrypt -MustExist
    $outPath = if ($Out) { Resolve-FullPath $Out } else { Get-DefaultOutPath $inPath -Armor:$Armor }

    $plain = [IO.File]::ReadAllBytes($inPath)
    if ($plain.Length -eq 0) { throw "源文件为空: $inPath" }

    $pw = Get-PlainPassword
    if ([string]::IsNullOrEmpty($pw)) { throw '口令不能为空' }

    $salt = [byte[]]::new(16)
    $iv = [byte[]]::new(16)
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $rng.GetBytes($salt); $rng.GetBytes($iv) }
    finally { $rng.Dispose() }

    $keys = New-SubKey -Password $pw -Salt $salt -Iterations $Iterations
    try {
        $aes = New-Aes -Key $keys.Aes -Iv $iv
        try {
            $enc = $aes.CreateEncryptor()
            $cipher = $enc.TransformFinalBlock($plain, 0, $plain.Length)
        }
        finally { $aes.Dispose() }

        $iterBytes = [BitConverter]::GetBytes([uint32]$Iterations)
        if ([BitConverter]::IsLittleEndian) { [Array]::Reverse($iterBytes) }

        $body = [byte[]]::new($script:HeaderSize + $cipher.Length)
        [Array]::Copy($script:Magic, 0, $body, 0, 8)
        $body[8] = $script:Version
        $body[9] = $script:KdfPbkdf2Sha256
        [Array]::Copy($iterBytes, 0, $body, 10, 4)
        [Array]::Copy($salt, 0, $body, 14, 16)
        [Array]::Copy($iv, 0, $body, 30, 16)
        [Array]::Copy($cipher, 0, $body, $script:HeaderSize, $cipher.Length)

        $mac = Get-Hmac -Key $keys.Mac -Data $body
        $container = [byte[]]::new($body.Length + $script:MacSize)
        [Array]::Copy($body, 0, $container, 0, $body.Length)
        [Array]::Copy($mac, 0, $container, $body.Length, $script:MacSize)
    }
    finally {
        [Array]::Clear($keys.Aes, 0, $keys.Aes.Length)
        [Array]::Clear($keys.Mac, 0, $keys.Mac.Length)
    }

    if ($Armor) {
        $b64 = [Convert]::ToBase64String($container)
        $sb = [Text.StringBuilder]::new()
        for ($i = 0; $i -lt $b64.Length; $i += 64) {
            [void]$sb.AppendLine($b64.Substring($i, [Math]::Min(64, $b64.Length - $i)))
        }
        if ((Test-Path -LiteralPath $outPath) -and -not $Force) {
            throw "输出文件已存在（加 -Force 覆盖）: $outPath"
        }
        $dir = [IO.Path]::GetDirectoryName($outPath)
        if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
        [IO.File]::WriteAllText($outPath, $sb.ToString(), [Text.Encoding]::ASCII)
    }
    else {
        Write-OutputFile -Path $outPath -Bytes $container -Force:$Force
    }

    [pscustomobject]@{
        Action     = 'Encrypt'
        Input      = $inPath
        Output     = $outPath
        SizeIn     = $plain.Length
        SizeOut    = (Get-Item -LiteralPath $outPath).Length
        Iterations = $Iterations
        Armor      = [bool]$Armor
    }
}

function Invoke-Decrypt {
    $inPath = Resolve-FullPath $Decrypt -MustExist
    $outPath = if ($Out) { Resolve-FullPath $Out } else { Get-DefaultOutPath $inPath -Decrypting }

    $raw = [IO.File]::ReadAllBytes($inPath)
    $looksBinary = $raw.Length -ge $script:Magic.Length -and
        (Test-BytesEqual -A $raw[0..($script:Magic.Length - 1)] -B $script:Magic)

    if (-not $looksBinary) {
        # 不是二进制容器，按 Base64 文本（-Armor 输出）解码
        $text = [Text.Encoding]::ASCII.GetString($raw)
        $clean = $text -replace '[^A-Za-z0-9+/=]', ''
        try { $raw = [Convert]::FromBase64String($clean) }
        catch { throw "既不是本工具的二进制容器，也不是合法的 Base64 文本: $inPath" }
    }

    if ($raw.Length -lt $script:HeaderSize + $script:MacSize) { throw "容器长度不足，文件已损坏: $inPath" }
    if (-not (Test-BytesEqual -A $raw[0..7] -B $script:Magic)) { throw "不是本工具的加密容器（magic 不匹配）: $inPath" }
    if ($raw[8] -ne $script:Version) { throw "不支持的容器版本: $($raw[8])" }
    if ($raw[9] -ne $script:KdfPbkdf2Sha256) { throw "不支持的 KDF 标识: $($raw[9])" }

    $iterBytes = [byte[]]::new(4)
    [Array]::Copy($raw, 10, $iterBytes, 0, 4)
    if ([BitConverter]::IsLittleEndian) { [Array]::Reverse($iterBytes) }
    $iters = [int][BitConverter]::ToUInt32($iterBytes, 0)

    $salt = [byte[]]::new(16); [Array]::Copy($raw, 14, $salt, 0, 16)
    $iv = [byte[]]::new(16); [Array]::Copy($raw, 30, $iv, 0, 16)

    $bodyLen = $raw.Length - $script:MacSize
    $body = [byte[]]::new($bodyLen)
    [Array]::Copy($raw, 0, $body, 0, $bodyLen)
    $mac = [byte[]]::new($script:MacSize)
    [Array]::Copy($raw, $bodyLen, $mac, 0, $script:MacSize)

    $cipherLen = $bodyLen - $script:HeaderSize
    if ($cipherLen -le 0 -or ($cipherLen % 16) -ne 0) { throw "密文长度异常，文件已损坏: $inPath" }

    $pw = Get-PlainPassword
    $keys = New-SubKey -Password $pw -Salt $salt -Iterations $iters
    try {
        $calc = Get-Hmac -Key $keys.Mac -Data $body
        if (-not (Test-BytesEqual -A $calc -B $mac)) {
            throw '口令错误，或文件被篡改（HMAC 校验失败）'
        }

        $aes = New-Aes -Key $keys.Aes -Iv $iv
        try {
            $dec = $aes.CreateDecryptor()
            $plain = $dec.TransformFinalBlock($body, $script:HeaderSize, $cipherLen)
        }
        finally { $aes.Dispose() }
    }
    finally {
        [Array]::Clear($keys.Aes, 0, $keys.Aes.Length)
        [Array]::Clear($keys.Mac, 0, $keys.Mac.Length)
    }

    Write-OutputFile -Path $outPath -Bytes $plain -Force:$Force

    [pscustomobject]@{
        Action     = 'Decrypt'
        Input      = $inPath
        Output     = $outPath
        SizeIn     = $raw.Length
        SizeOut    = $plain.Length
        Iterations = $iters
        IsPdf      = ($plain.Length -ge 5 -and [Text.Encoding]::ASCII.GetString($plain, 0, 5) -eq '%PDF-')
    }
}

if ($PSCmdlet.ParameterSetName -eq 'Encrypt') { Invoke-Encrypt } else { Invoke-Decrypt }
