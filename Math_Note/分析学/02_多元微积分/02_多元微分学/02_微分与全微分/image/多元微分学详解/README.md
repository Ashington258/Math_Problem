# 多元微分学详解配图

为 [多元微分学详解](../../多元微分学详解.md) 提供可重现的解析示意图。

本文图 1–13 在本目录生成；图 14–15 复用 [积分元素配图](../../../../03_多元积分学/01_重积分/image/积分元素/README.md) 中的向量场作用与微分算子示意图。

## 生成

依赖 Python、NumPy、Matplotlib、Pillow；本次生成版本为 Python 3.13.13、NumPy 2.5.3、Matplotlib 3.11.2。在本目录运行：

```powershell
python make_figures.py
```

脚本从自身所在目录读写资源，与启动时工作目录无关。[make_figures.py](make_figures.py) 生成全套图像，[make_geometry_figures.py](make_geometry_figures.py) 提供曲面及几何图，[make_field_figures.py](make_field_figures.py) 提供配对的二维、三维散度与旋度场。`sci_style.py` 原样复制自 sci-plot 技能，不依赖作者机器的绝对路径。

## 图目

| 图号 | 文件主干 | 内容 |
| --- | --- | --- |
| 1 | `fig-01-partial-derivatives` | 三维坐标截线、切线与真实截面视图 |
| 2 | `fig-02-direction-derivative` | 输入方向、三维截线与距离—高度截面 |
| 3 | `fig-03-gradient-tangent-plane` | 二维梯度与三维图像切平面、叉积法向 |
| 4 | `fig-04-gradient-level-surface` | 三维等值面、梯度法向与切向方向 |
| 5 | `fig-05-total-differential` | 切平面上的分步增量与实际增量误差 |
| 6 | `fig-06-direction-counterexample` | 各方向可导仍不连续的反例 |
| 7 | `fig-07-flux-geometry` | 三维小盒子及其对面通量差 |
| 8 | `fig-08-divergence` | 二维与三维的源、汇和均匀场，六面板对照 |
| 9 | `fig-09-circulation-geometry` | 四边环流符号、空间回路与叉积定向 |
| 10 | `fig-10-curl` | 二维旋转/剪切；三维斜轴旋转与轴向输运 |
| 11 | `fig-11-vortex-domain` | 局部无旋与全局环流 |
| 12 | `fig-12-jacobian-decomposition` | 膨胀、旋转与形变 |
| 13 | `fig-13-physical-meaning` | 热流及质量守恒 |

每图输出同名矢量 PDF、SVG 和 600 dpi PNG。标称图宽为 **178 mm**，图高为 81–175 mm；实际尺寸由 `figure_manifest.json` 记录，并检查其宽度与标称值的偏差小于 3%。正文嵌入 PNG，导出或排版可使用矢量版。

`preview-1.png` 至 `preview-4.png` 是缩小的彩图总览；对应 `-gray.png` 为灰度总览。采用 8 pt 正文字号、7 pt 三维刻度、DejaVu Sans、Okabe–Ito 配色，主要曲线以线型、标记或方向文字区分。图中的 `dim.` 为 dimensionless（无量纲）的缩写。

所有数据由正文的解析公式生成，无随机数、测量数据或误差带。场箭头网格在各图内部统一缩放；梯度、切向量、法向等注释箭头采用便于阅读的独立缩放，不能跨图比较箭长。三维视图采用正交投影及不着色网格；二元图像的高度轴可单独缩放，斜率从配套的二维截面读取。等值椭球及其切平面采用相同坐标长度尺度。几何变形图使用精确流映射 $e^{tA}$，$t=0.35$。

图内数学标签遵循 [符号规范](../../../符号规范.md)：向量用粗体，算子写 $\nabla\cdot$、$\nabla\times$。matplotlib 的 mathtext 要求粗体写成 `\mathbf{...}`（必须带花括号）、平方根写成 `\sqrt{3}`；改标签后须重新运行 `python make_figures.py`。
