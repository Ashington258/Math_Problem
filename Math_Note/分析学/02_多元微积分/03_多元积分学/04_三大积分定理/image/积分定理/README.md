# 积分定理配图

为 [积分定理：从内部微分到边界积分](../../积分定理：从内部微分到边界积分.md) 重绘的 9 组图。图像从区域维数、边界与定向出发，依次展示 Green、Stokes、Gauss 及适用范围。

## 生成

依赖 Python、NumPy、Matplotlib、Pillow。在本目录运行：

```powershell
python make_figures.py
```

[生成脚本](make_figures.py) 按自身目录读写文件；本地 `sci_style.py` 来自 sci-plot 技能。无需作者机器的绝对路径。全部数据由解析公式生成，无随机数、测量数据或误差带。

## 图目

| 图 | 文件主干 | 核心对照 |
| --- | --- | --- |
| 1 | `fig-01-domains-boundaries` | 平面区域—边界曲线；体积区域—边界曲面 |
| 2 | `fig-02-internal-cancellation` | 共享边的相反走向；共享面的相反外法向 |
| 3 | `fig-03-green-flux-circulation` | 径向场通量与旋转场环流 |
| 4 | `fig-04-green-orientation` | 孔洞定向；切向与外法向 |
| 5 | `fig-05-stokes-surfaces` | 同边界的圆盘与曲面帽 |
| 6 | `fig-06-stokes-tilted-disk` | 斜置圆盘及旋度三个分量的法向投影 |
| 7 | `fig-07-gauss-ball` | 三维径向场球面通量；常散度按体积累积 |
| 8 | `fig-08-gauss-surface-closure` | 有边缘曲面；补底后的完整封闭边界 |
| 9 | `fig-09-singularity-shell` | 奇点失效与挖孔后的完整内外边界 |

每图输出矢量 PDF、SVG 及 600 dpi PNG，宽度标称 **178 mm**，高度 **104 mm**；脚本核对实际宽度偏差小于 3%，结果见 `figure_manifest.json`。彩图、灰度总览分别为 `preview-1.png` 至 `preview-3.png` 及对应 `-gray.png`。

坐标及场量均无量纲，图中 `dim.` 为 dimensionless 的缩写。使用 DejaVu Sans、8 pt 正文字号、7 pt 三维刻度、Okabe–Ito 配色。箭头以颜色、线型、位置及文字共同区分场值、边界走向、法向和旋度；箭长作独立缩放，不跨图比较数值。三维视图为正交投影，面网格描述真实曲面；二维截面在正文图注中明确标记。
