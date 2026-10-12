# 随机变量的数字特征配图

配套 [随机变量的数字特征](../../随机变量的数字特征.md#numerical-characteristics)。全部图形按分布公式生成，未模拟观测样本。

| 图 | 内容 |
| --- | --- |
| 01_weighted_mean | 离散概率权重与期望贡献 |
| 02_location_spread | 均值控制位置、标准差控制尺度 |
| 03_same_moments | 相同期望、方差下的不同分布 |
| 04_covariance_direction | 二维正态分布的正、负线性相关 |
| 05_uncorrelated_dependence | 非线性相依关系中的零相关 |
| 06_total_variance | 混合分布的组内与组间方差 |
| 07_continuous_expectation | 概率密度与求期望的加权函数 |

复现方式：

```powershell
python -m pip install -r requirements.txt
python plot_characteristics.py
```

已有依赖时可直接运行绘图脚本。样式模块 `sci_style.py` 为 sci-plot 技能的本地副本；中文字体优先使用 Microsoft YaHei。

输出为 178 mm 宽的矢量 PDF 与 600 dpi PNG。几何坐标无量纲，方差注明平方量纲；等密度椭圆表示分布结构，不表示置信区间。虚实线、阴影纹理与直接标注提供颜色以外的区分。

`figure_manifest.json` 记录实际尺寸，`preview-*.png` 为检查用总览，带 `-gray` 的文件用于灰度可读性检查。脚本核验离散矩、连续矩、零协方差、混合分布方差及椭圆公式。

[返回配套笔记](../../随机变量的数字特征.md#numerical-characteristics)
