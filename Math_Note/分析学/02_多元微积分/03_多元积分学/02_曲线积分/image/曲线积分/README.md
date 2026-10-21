# 曲线积分配图

为[曲线积分](../../曲线积分.md)绘制的 9 组几何图，共 20 个分面，覆盖正文的原理、反例与计算例题。

## 图目与解释对象

| 图 | 几何内容 | 导出 |
| --- | --- | --- |
| 1 | 弧长、弦位移、切向方向与参数速率 | [PNG](fig-01-line-elements.png) · [PDF](fig-01-line-elements.pdf) |
| 2 | 半圆线密度、等弧长分段与质量的黎曼和 | [PNG](fig-02-scalar-accumulation.png) · [PDF](fig-02-scalar-accumulation.pdf) |
| 3 | 有向位移的坐标分解、场的正交切向投影 | [PNG](fig-03-two-projections.png) · [PDF](fig-03-two-projections.pdf) |
| 4 | 反向时弧长不变、做功反号 | [PNG](fig-04-reversal.png) · [PDF](fig-04-reversal.pdf) |
| 5 | 势函数例题的等势线、梯度场、两条路径与累积功 | [PNG](fig-05-potential.png) · [PDF](fig-05-potential.pdf) |
| 6 | 可收缩闭路与穿孔反例的局部、全局环量 | [PNG](fig-06-curl-topology.png) · [PDF](fig-06-curl-topology.pdf) |
| 7 | 环域的正向内外边界及有符号环量 | [PNG](fig-07-green-orientation.png) · [PDF](fig-07-green-orientation.pdf) |
| 8 | 小矩形上的环量密度与共享边的相消 | [PNG](fig-08-green-cancellation.png) · [PDF](fig-08-green-cancellation.pdf) |
| 9 | 非保守场例题的路径、功密度、旋度与竖切片 | [PNG](fig-09-worked-example.png) · [PDF](fig-09-worked-example.pdf) |

## 重现

在本目录运行，建议 Python 3.12 或更新版本：

~~~powershell
python -m pip install -r requirements.txt
python make_figures.py
~~~

- [make_figures.py](make_figures.py) 从确定的解析函数生成全部图形，不使用随机数或测量数据，无统计误差带。
- [sci_style.py](sci_style.py) 来自 sci-plot 技能；本地仅为 save() 增加 tight=False 选项，以保留精确的 178 mm 画布宽度。
- 中文字体采用 Microsoft YaHei，数学字体采用 DejaVu Sans；在其他环境重现相同排版需安装对应字体。
- [requirements.txt](requirements.txt) 固定本次实际使用的依赖版本。
- [figure_manifest.json](figure_manifest.json) 记录每组图的内容、实际 PDF 尺寸和 PNG 分辨率。

## 尺寸与阅读约定

所有图均为双栏宽 **178 mm**，高度 86–94 mm；图 9 为 173 mm 高的四分面图。正文嵌入 **600 dpi PNG**，配套 PDF 为矢量图，文字嵌入字体；坐标和示例量均无量纲，不对应实验测量单位。

几何坐标面保持等比例；参数图与累积图按其标注坐标阅读。蓝色实线与橙色虚线区分主要路径，结合箭头、文字和填充纹理，不依赖颜色单独传递含义；连续色带使用明度递增的 cividis。场箭头按面板内统一比例缩放；图 1 的单位切向方向与图 3A 的微元长度为示意缩放，图 3B 的向量长度按给定数值绘制。

脚本同时生成彩色和灰度联系表：preview-1.png 至 preview-3.png，对应 preview-1-gray.png 至 preview-3-gray.png。已核对方向、正负号、图注与正文公式；导出时自动核对宽度与文字是否超出画布。
