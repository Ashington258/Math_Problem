# 积分学配图

为总速查及五篇积分学笔记配套的 **22 幅数学示意图**，包含原理图、例题图及反例图。图形由公式或明确的几何对象生成；几何坐标无量纲，角度以弧度计，控制体示例的质量流率以 kg/s 计。空间图使用正交投影，法向与边界走向由几何条件确定。

积分定理正文已改用 [9 组专题重绘图](../../04_三大积分定理/image/积分定理/README.md)。下表涉及积分定理的旧图作为历史配图保留，其他文章的共享引用仍有效。

## 图目

| 图 | 内容 | 使用章节 |
| --- | --- | --- |
| fig-01-slicing | 同一区域的竖直与水平切片 | 重积分 |
| fig-02-polar-element | 参数矩形与环形扇区，Jacobian 的含义 | 重积分 |
| fig-03-curve-direction | 曲线反向：弧长不变，功积分变号 | 曲线积分 |
| fig-04-surface-flux | 斜面面积、投影面积与法向通量 | 曲面积分 |
| fig-05-internal-cancellation | 共享边、共享面的内部贡献相消 | 总速查、积分定理 |
| fig-06-stokes-surfaces | 同边界的圆盘与上半球，旋度通量一致 | 积分定理 |
| fig-07-gauss-hole | 奇点与挖孔，内外边界的定向 | 积分定理 |
| fig-08-potential-paths | 端点势差与穿孔平面的环流障碍 | 保守场与势函数 |
| fig-09-riemann-sum | 区域分割、取样点与黎曼柱体 | 总速查、重积分原理 |
| fig-10-radial-example | 同心薄环与径向加权积分 | 重积分例题 3 |
| fig-11-volume-slices | 四面体的竖直切片与投影 | 重积分例题 2 |
| fig-12-tangent-component | 位移微元与切向投影 | 曲线积分原理 |
| fig-13-surface-element | 参数矩形、切平行四边形与叉积 | 曲面积分原理 |
| fig-14-green-orientation | 含孔区域的定向与椭圆面积 | Green 原理及例题 1 |
| fig-15-gauss-sphere | 球面径向场与内部常散度积分 | Gauss 例题 3 |
| fig-16-cap-closure | 上半球与底面的法向及通量 | 曲面积分例题 2 |
| fig-17-continuity | 控制体的流入、流出与存量 | 质量守恒原理 |
| fig-18-gradient-example | 梯度场的两条路径及端点势差 | 曲线积分例题 2 |
| fig-19-field-comparison | 径向场与旋转场的微分性质 | 场论例题 2 |
| fig-20-ellipse-arc-chord | 椭圆弧补弦成闭路，弦上被积函数的奇偶分解 | 曲线积分例题 3 |
| fig-21-surface-coordinate-projections | 面元沿三个坐标轴的投影与有向投影面积 | 曲面积分：坐标投影视角 |
| fig-22-surface-normal-projection | 面元的法向定向与场的法向、切向分解 | 曲面积分：法向投影视角 |

## 重现

在本目录运行：

```powershell
python -m pip install -r requirements.txt
python make_figures.py
python make_principle_figures.py
python make_surface_projection_figures.py
```

已有依赖时可直接运行绘图脚本。`sci_style.py` 为所调用 sci-plot 技能的样式模块副本，脚本不依赖用户机器上的技能路径。

输出采用 **178 mm 双栏宽度、8 pt 基础字体、600 dpi PNG 与矢量 PDF**，统一 DejaVu Sans 字体和 Okabe–Ito 配色。虚实线、直接标注与箭头方向提供颜色以外的信息。PNG 用于笔记内嵌，PDF 用于排版和无损缩放。

新增投影图可单独运行 `make_surface_projection_figures.py` 重现，导出尺寸见 `figure_manifest_surface_projections.json`。面元均放大示意；坐标投影图用阴影线区分投影面元，法向分解图用虚线区分切向部分。脚本校验投影面积、方向余弦与向量的正交分解。

`figure_manifest.json` 与 `figure_manifest_extra.json` 分别记录基础图及新增图的实际导出尺寸。`preview-*.png` 为检查用总览，带 `-gray` 的文件用于灰度可读性检查。脚本验证投影、面积、四面体体积、径向积分、球面通量、端点势差及椭圆弧补弦等图文对应关系。
