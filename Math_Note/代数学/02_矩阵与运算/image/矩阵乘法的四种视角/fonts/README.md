# 数学字体

本目录字体来自 KaTeX 0.16.22 的 `dist/fonts`，附带 [MIT 许可](./LICENSE-KaTeX.txt)。

配图使用 KaTeX_Main 的直立数字、KaTeX_Math 的斜体变量，以及 KaTeX_SansSerif 的直立转置字母。SVG 将字体转为路径，PDF 嵌入字体；阅读导出图不需要安装这些字体。

配图布局由 Matplotlib 生成；数学字符使用上述 KaTeX 字体。`figure_formulas.json` 保留实际绘图公式，`verify_katex.cjs` 使用 KaTeX 的严格解析模式检查这些公式。
