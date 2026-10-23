# 三重积分配图

配合 [三重积分](../../三重积分.md)，用解析几何展示积分限、切片和体积权重。

| 正文图号 | 文件主干 | 内容 |
| --- | --- | --- |
| 1 | fig-01-slices | 单位四面体：竖直线段、水平截面、截面积函数 |
| 2 | fig-02-order-split | 柱面与抛物面：换序后在 $z=1$ 处分段 |
| 3 | fig-03-cylindrical | 双抛物面：母线厚度与 $2\pi r$ 径向权重 |
| 4 | fig-04-spherical | 球与圆锥：子午截面及球坐标参数范围 |

## 重现

在本目录运行：

```powershell
python make_figures.py
```

[生成脚本](make_figures.py) 依赖 Python、NumPy、Matplotlib、Pillow；[本地样式](sci_style.py) 沿用本章已有的 sci-plot 样式副本，含 `tight=False` 扩展以保持精确画布尺寸。所有数据来自确定的解析公式，无随机数、测量数据或误差带。

每组输出 **178 × 95 mm** 的矢量 PDF、SVG 及 **600 dpi PNG**。脚本读取实际导出尺寸与 PNG 分辨率，检查二维文字不超出画布，三维刻度另经预览检查；结果记录于 [尺寸清单](figure_manifest.json)。正文嵌入 PNG，印刷可使用同名 PDF 或 SVG。

字体为 Microsoft YaHei，回退到 DejaVu Sans；正文 8 pt，三维刻度 7 pt，面板字母 10 pt。采用 Okabe–Ito 蓝色、朱红色与中性灰；颜色之外还用实/虚线、点标记、位置与文字区分对象。两色灰度亮度接近，因此请结合线型及标签阅读，见 [灰度预览](preview-gray.png)；[彩图预览](preview.png) 供整体检查。

所有坐标均无量纲，图中的 `dim.` 表示 dimensionless；角度以 rad 表示。三维图采用正交投影，三个空间轴保持相同长度尺度。母线区域和参数区域是二维表示，其平面面积不能直接当作三维体积；相应的 Jacobian 与整周角度因子见正文图注。
