# 线性映射与四大子空间动态演示

Python + Manim Community + Plotly。**先观看 `R³ → R²`，再探索其余场景。** 输入端与输出端各有独立坐标系；所有子空间几何都来自 NumPy 的完整 SVD，不手写基向量。

## 直接查看已生成的成果

- [R³ → R² 交互演示](output/html/r3_to_r2.html)：三维旋转、核方向收缩、核平移平面与共同输出。
- [R² → R³ 交互演示](output/html/r2_to_r3.html)：二维网格抬升到 `z=x+y`。
- [四大子空间交互演示](output/html/four_subspaces.html)：切换两个非方阵案例和方阵反例。
- 第一幕正式视频：`output/videos/scene_02_r3_to_r2/1080p30/R3ToR2.mp4`。
- 其余场景视频：`output/videos/scene_0*/720p30/` 下的 MP4。

HTML 已内嵌 Plotly.js，可直接双击，离线可用，无需启动 Python 或联网。视频包含中文字幕与 LaTeX 公式，无配音。

## 安装与环境

在 VS Code Terminal 中进入本项目目录：

```powershell
cd linear-map-visualization
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

若 PowerShell 不允许执行激活脚本，可直接使用虚拟环境的解释器，无需改变系统执行策略：

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe build_interactive.py
```

Linux / macOS 激活：`source .venv/bin/activate`。建议 Python 3.11–3.13；本机实际验证使用 Python 3.13、Manim 0.21.0、NumPy 2.2.6、SciPy 1.15.3。

外部依赖：

- **LaTeX + dvisvgm**：用于 `MathTex`。Windows 可使用 TeX Live 或 MiKTeX，安装后确保 `latex --version` 与 `dvisvgm --version` 可运行。通常需要 `standalone`、`amsmath`、`amssymb` 等包；完整 TeX Live 包含这些包。
- **中文字体**：Windows 默认 `Microsoft YaHei`。其他系统安装中文字体后，用环境变量指定，例如 PowerShell：`$env:LINEAR_MAP_FONT='Noto Sans CJK SC'`；bash：`export LINEAR_MAP_FONT='Noto Sans CJK SC'`。
- Manim 0.21 使用 **PyAV** 编码视频；此项目的静音 MP4 渲染无需另装 FFmpeg 命令。若增加音频或使用其他处理工具，按其说明安装 FFmpeg。
- Windows 通常直接使用 Cairo、Pango 的二进制 wheels；Linux 从源码安装时可能需系统 Cairo/Pango 开发包，参见 [Manim 安装文档](https://docs.manim.community/en/stable/installation.html)。[Manim 0.19 的 PyAV 迁移说明](https://docs.manim.community/en/stable/changelog/0.19.0-changelog.html)解释了视频编码依赖的变化。

本机最初安装的新 SciPy 扩展被 Windows 应用控制拦截，换为上述固定版本后加载、渲染均正常；未修改系统安全设置。

只生成 HTML 时可用轻量环境：`python -m pip install numpy plotly`，不需要 Manim、SciPy 或 LaTeX。

## 渲染动画

先渲染核心场景（命令在项目根目录执行）：

```powershell
# 快速预览：480p / 15 FPS
manim -pql manim_scenes/scene_02_r3_to_r2.py R3ToR2

# 高清：1080p / 60 FPS（Manim high quality 默认）
manim -pqh manim_scenes/scene_02_r3_to_r2.py R3ToR2

# 1080p / 30 FPS，适合普通电脑
python -m manim -qh --fps 30 manim_scenes/scene_02_r3_to_r2.py R3ToR2

# 全部场景：默认 720p / 30 FPS，先渲染核心场景
python render_all.py

# 全部场景：1080p / 60 FPS
python render_all.py --quality h --fps 60
```

`-p` 会打开播放器，可去掉。`manim.cfg` 把输出放在 `output/videos/<场景文件名>/<分辨率与帧率>/`。使用默认 Cairo 渲染器；分屏投影相机为 Cairo 编写。

| 文件 | 类名 | 学习重点 |
| --- | --- | --- |
| `scene_01_domain_codomain.py` | `DomainCodomain` | m 行 n 列 → 从 Rⁿ 输入到 Rᵐ 输出 |
| `scene_02_r3_to_r2.py` | `R3ToR2` | 二维核方向收缩、原像平面、列空间与秩零度 |
| `scene_03_r2_to_r3.py` | `R2ToR3` | 单射网格抬升、像平面与三维输出空间 |
| `scene_04_four_subspaces.py` | `FourSubspaces` | 两端的正交分解、核映到零 |
| `scene_05_square_matrix_trap.py` | `SquareMatrixTrap` | 先识别坐标看重叠，再拆分两端纠正补空间错觉 |

其他场景可同样运行，例如：

```powershell
python -m manim -pqm manim_scenes/scene_03_r2_to_r3.py R2ToR3
```

## 生成交互页面

```powershell
python build_interactive.py
# 或独立生成
python interactive/r3_to_r2_plotly.py
python interactive/r2_to_r3_plotly.py
python interactive/four_subspaces_plotly.py
```

输出到 `output/html/`。网页提供空间/向量/标签勾选框、播放/暂停、重置、t 滑块与计算基展示。四大子空间页额外提供矩阵选择器。开关状态会在滑块变化时保留；相机可自由旋转。

## 动画为什么数学上成立

对矩阵 `A∈R^(m×n)`：

\[
\mathbb R^n=\operatorname{Row}(A)\oplus N(A),\qquad
\mathbb R^m=\operatorname{Col}(A)\oplus N(A^T).
\]

SVD 给出所有基，基向量作为二维数组的**列**存储。全空间 SVD 与统一容差计算秩、核、行、列、左核；计算函数始终检查 `rank + nullity == n` 和 `rank + left_nullity == m`。

### R³ → R²

\[
A=\begin{pmatrix}1&1&0\\0&0&0\end{pmatrix},\quad
A(x,y,z)^T=(x+y,0)^T.
\]

输入端核是 `x+y=0` 的二维平面；行空间是 `(1,1,0)` 的张成。输出端列空间是水平轴，左核是竖直轴。秩 1、核维数 2，因此 `3=2+1`。

矩形矩阵不能与单位矩阵直接相加。本项目在**输入端**演示：

\[
C_t=P_{\operatorname{Row}(A)}+(1-t)P_{N(A)},\quad
C_0=I_n,\quad C_1=P_{\operatorname{Row}(A)},\quad AC_tx=Ax.
\]

这不是 `A_t`，也不是把输入与输出混在同一个空间的矩阵插值。输入点云收缩到行空间，真实 `Ax` 单独出现在二维输出端。随后沿计算出的行空间方向移动输入标记，输出标记同步沿列空间移动，展示 `A(sv)=sAv`；这与沿核平移时输出不变形成对照。

对 `x₀=(1,0,0)`，由计算核基生成 `zᵢ`，验证 `A(x₀+zᵢ)=Ax₀=(1,0)`。全部原像恰为仿射平面 `x₀+N(A)`。输入端的一整个核平移平面对应一个输出；核的“两个方向”不是删掉两条坐标轴。

### R² → R³

\[
B=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\quad
B(x,y)^T=(x,y,x+y)^T.
\]

核为零、秩 2，故 `2=0+2`。输出空间是三维，像仅是二维平面。视觉抬升在输出端使用 `Hₜ(x,y)=(x,y,t(x+y))`，从平面嵌入 `H₀` 到真实映射 `H₁=B`。中间网格明确标为演示；真实映射点保持独立。

### 方阵反例

`A(x,y,z)=(y,0,0)` 时，输入核为 xz 平面，输出列空间为 x 轴。识别两端的标准坐标后，`Col(A)⊂N(A)`，因此交集非零，**不能写成直和**；普通和 `N(A)+Col(A)=N(A)≠R³`。动画先展示这个特殊坐标识别，再明确拆开输入与输出。正确分解仍是输入 `N(A)⊕Row(A)`、输出 `Col(A)⊕N(Aᵀ)`。

左核中的**非零**向量不可能成为 A 的输出；零向量属于两个输出子空间。

## 验证

```powershell
python -m unittest discover -s tests -v
```

测试涵盖三个指定矩阵、零矩阵、满秩/低秩非方阵、接近奇异矩阵；检查零空间残差、正交性、两端的完备分解、SVD 基正交归一、秩零度以及整个坍缩过程输出不变。

可选浏览器验收（开发依赖，无需纳入正常运行环境）：

```powershell
python -m pip install playwright
python tools/check_html.py
```

脚本使用已安装的 Chrome / Edge；若未安装，先运行 `python -m playwright install chromium`。浏览器检查覆盖页面加载、滑块端点、开关状态、三维旋转与三个矩阵切换；截图在 `output/qa/`。

颜色全项目统一：Kernel 粉色、Row 蓝色、Column 绿色、Left Null 黄色、普通向量浅灰。平面采用透明填充与清晰边界。

本次实际验收：五个场景均完成 MP4 渲染并解码检查关键帧；核心场景为 1080p / 30 FPS，其余为 720p / 30 FPS。四组数值测试通过；三个 HTML 在 Chrome 离线模式下通过空间/标签开关、t 端点、三维旋转、播放与重置检查，四大子空间页另验证全部矩阵切换。
