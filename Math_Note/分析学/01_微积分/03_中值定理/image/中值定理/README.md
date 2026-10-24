# 中值定理配图

[中值定理](../../中值定理.md) 的八组解析几何图。目录内原有时间戳命名图片继续供旧例题和证明使用，本组使用独立的稳定文件名。

| 正文图号 | 文件主干 | 内容 |
| --- | --- | --- |
| 1 | fig-01-intermediate-values | 介值定理与零点定理 |
| 2 | fig-02-fermat | 费马引理及逆命题反例 |
| 3 | fig-03-differential-mvt | Rolle 水平切线与 Lagrange 平行切线 |
| 4 | fig-04-cauchy | 参数曲线端点弦、平行切线与辅助函数 |
| 5 | fig-05-taylor | 二阶 Taylor 多项式与拉格朗日余项界 |
| 6 | fig-06-integral-first | 等面积矩形与非负权重推广 |
| 7 | fig-07-integral-second | 单调函数、端点值阶梯与加权积分 |
| 8 | fig-08-darboux | 导数不连续但具有介值性 |

## 重现与规格

在本目录运行：

```powershell
python make_figures.py
```

[生成脚本](make_figures.py) 依赖 Python、NumPy、Matplotlib、Pillow。所有图来自解析函数，无测量数据或随机数；Taylor 图的阴影表示严格的确定性余项界。[本地样式](sci_style.py) 沿用 sci-plot 的本章样式副本，含 `tight=False` 以保持画布尺寸。

每组为 **178 × 92 mm** 的双面板图，输出矢量 PDF、SVG 和 **600 dpi PNG**；[尺寸清单](figure_manifest.json) 记录实际导出尺寸。采用 Microsoft YaHei 字体（回退 DejaVu Sans），正文 8 pt，图例 7 pt，面板字母 10 pt。坐标均无量纲，两面板的坐标范围可不同，见正文图注。

蓝色实线表示主要函数，橙色虚线通常表示切线、均值或替代函数，灰色点线表示端点连线或辅助线；圆、方、菱形标记进一步区分特殊点。蓝、橙在灰度中亮度接近，因此同时以线型、标记和位置编码。

- [彩图预览 1](preview-1.png)、[彩图预览 2](preview-2.png)
- [灰度预览 1](preview-1-gray.png)、[灰度预览 2](preview-2-gray.png)

脚本检查导出宽度、PNG 分辨率和文字是否超出画布；预览另用于核对标注遮挡、切线位置及灰度辨识。Darboux 图使用倒数变量均匀采样，解析呈现接近原点时越来越快的振荡；有限图像无法包含无穷多次振荡，原点导数单独标出。
