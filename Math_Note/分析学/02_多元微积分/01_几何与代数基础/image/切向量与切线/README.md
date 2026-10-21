# 切向量与切线：配图说明

配套正文：[切向量与切线](../../切向量与切线.md)。

## 复现方法

在本目录运行：

```powershell
python make_figures.py
```

依赖为 Python、NumPy、Matplotlib、Pillow。本次运行版本为 Python 3.13.13、NumPy 2.5.3、Matplotlib 3.11.2、Pillow 12.3.0。`sci_style.py` 为 sci-plot 技能提供的样式文件本地副本，绘图不依赖原技能的安装位置。所有曲线来自正文中的解析公式，无外部数据和随机采样。

## 配图与规格

| 文件主干 | 内容 | PDF 实际导出尺寸 |
| --- | --- | --- |
| `fig-01-secant-limit` | 抛物线割线与切线，两个趋近阶段 | 179.1 × 92.3 mm |
| `fig-02-helix-tangent` | 三维螺旋线切线及其平面投影 | 179.1 × 99.3 mm |
| `fig-03-zero-derivative` | 零导数时的光滑图像与尖点 | 179.1 × 85.3 mm |

每组输出正文嵌入用的 600 dpi PNG，以及 PDF、SVG 矢量文件。名义宽度均为 178 mm，紧边界导出后的实际宽度约 179.1 mm，偏差小于 1%。PNG 物理宽度按 600 dpi 换算，与 PDF 的取整差异小于 0.1 mm。

坐标和参数均无量纲。所有二维坐标轴采用等比例显示，三维图通过 `set_box_aspect` 保持三方向数据单位尺度一致。图 1 两面板采用相同坐标范围；其他面板不要求相同物理缩放。图中的箭头表示向量或参数增大方向，正文图注分别说明。

颜色采用 Okabe–Ito 蓝、橙和深灰，并以实线、点划线、虚线、圆点、方点和箭头辅助区分。`grayscale_check` 检查了颜色亮度差异；`preview-*.png` 和 `preview-*-gray.png` 分别供彩图与灰度检查，正文使用原始高分辨率 PNG。脚本重新生成所有文件，不进行手工图像修饰。

## 公式与链接检查

`verify_note.cjs` 用 KaTeX 严格模式验证正文中的行内和块级公式，并检查正文相对链接及图片目标是否存在。校验依赖可安装在临时目录：

```powershell
$validatorDir = Join-Path $env:TEMP 'math-note-katex-check'
npm install --prefix $validatorDir katex@0.16.22 --no-audit --no-fund
node verify_note.cjs (Join-Path $validatorDir 'node_modules/katex')
```

正文公式采用 `$...$` 和 `$$...$$`，矩阵、分段式和推导使用 KaTeX 支持的环境。图中文字采用 Matplotlib MathText；正文解析检查与图形导出是独立步骤。

本次检查：正文重排后，278 处公式通过 KaTeX 0.16.22 严格解析；正文图片和相对链接目标全部存在。三组配图内容适用于重排后的正文，其彩图及灰度预览已逐一查看。
