$root = Join-Path (Get-Location).Path 'Math_Note'
$files = Get-ChildItem -LiteralPath $root -Recurse -Filter *.md
$bad = New-Object System.Collections.ArrayList
foreach ($f in $files) {
    $t = [IO.File]::ReadAllText($f.FullName)
    $rel = $f.FullName.Replace((Get-Location).Path + '\', '')
    foreach ($m in [regex]::Matches($t, '\]\(([^)\s]+?\.md)(#[\w-]+)?\)')) {
        $target = $m.Groups[1].Value
        $frag = $m.Groups[2].Value
        if ($target -match '^https?:') { continue }
        $p = Join-Path $f.DirectoryName $target
        if (-not (Test-Path -LiteralPath $p)) {
            [void]$bad.Add("DEADFILE | $rel | $target")
        }
        elseif ($frag -and -not ([IO.File]::ReadAllText($p).Contains('{' + $frag + '}'))) {
            [void]$bad.Add("ANCHOR   | $rel | $target$frag")
        }
    }
    foreach ($m in [regex]::Matches($t, '\]\((\.\./|\./)*(?:[\w\u4e00-\u9fa5]+/)+\)')) {
        $target = $m.Groups[0].Value.TrimStart(']').TrimStart('(').TrimEnd(')')
        $p = Join-Path $f.DirectoryName $target
        if (-not (Test-Path -LiteralPath $p)) {
            [void]$bad.Add("DEADDIR  | $rel | $target")
        }
    }
}
"scanned md files: $($files.Count)"
"--- problems ---"
if ($bad.Count -eq 0) { "none" } else { $bad | ForEach-Object { $_ } }
"--- total: $($bad.Count) ---"
