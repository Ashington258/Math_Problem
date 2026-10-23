"""Regenerate the chapter's clickable reference and backlink index."""
from collections import defaultdict
import os
from pathlib import Path
import re

from check_references import ROOT, links

MAP = ROOT / "关系图谱.md"


def relative(path):
    return Path(os.path.relpath(path, MAP.parent)).as_posix()


def generate():
    notes = sorted(p for p in ROOT.rglob("*.md") if p != MAP)
    titles, edges, back = {}, defaultdict(set), defaultdict(set)
    for note in notes:
        text = note.read_text(encoding="utf-8-sig")
        heading = re.search(r"(?m)^# (.+)$", text)
        title = heading.group(1).strip() if heading else note.stem
        if note.name.endswith(".converted.md"):
            title += "（导出转写稿）"
        titles[note] = title
        for raw, _ in links(text):
            if raw.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = (note.parent / raw.split("#")[0]).resolve()
            if target.suffix == ".md" and target != MAP:
                edges[note].add(target)
                back[target].add(note)

    def link(note):
        if note not in titles and note.is_file():
            heading = re.search(r"(?m)^# (.+)$", note.read_text(encoding="utf-8-sig"))
            titles[note] = heading.group(1).strip() if heading else note.stem
        title = titles.get(note, note.stem).replace("|", "／")
        return f"[{title}]({relative(note)})"

    lines = [
        "# 关系图谱", "",
        "主线图表示知识依赖；下方索引根据正文中的 Markdown 链接生成，列出每篇文档的引用与反向引用。章节入口、习题、配图说明及导出转写稿均纳入索引；图片文件由链接检查脚本单独核对。", "",
        "## 知识主线", "",
        "```mermaid", "flowchart TD",
        '  subgraph G["几何与代数基础"]',
        '    V["向量代数"] --> A["解析几何"]',
        '    A --> T["切矢量、弧长元素与面积元素"]', "  end",
        '  subgraph D["多元微分学"]',
        '    L["多元函数与极限"] --> D1["偏导数、全微分与可微性"]',
        '    D1 --> J["Jacobian 与链式法则"]',
        '    D1 --> H["Hessian 与二阶判别法"]',
        '    H --> E["驻点、极值与鞍点"]',
        '    D1 --> O["梯度、散度与旋度"]', "  end",
        '  subgraph I["多元积分学"]',
        '    M["积分元素"] --> I1["重积分与换元"]',
        '    M --> I2["曲线积分：坐标分解与切向投影"]',
        '    M --> I3["曲面积分：坐标投影与法向投影"]',
        '    I2 --> B["Green、Stokes 与 Gauss 定理"]',
        '    I3 --> B',
        '    I1 --> B',
        '    B --> F["保守场、势函数与守恒关系"]', "  end",
        "  T --> D1", "  T --> M", "  J --> M", "  O --> B",
        "  O --> F", "  I2 --> F", "```", "",
        "## 阅读入口与引用约定", "",
        "- [几何与代数基础](01_几何与代数基础/README.md)：从点积、叉积与参数化进入切空间。",
        "- [多元微分学](02_多元微分学/README.md)：[详解](02_多元微分学/02_微分与全微分/多元微分学详解.md) 负责推导，[速查](02_多元微分学/02_微分与全微分/多元微分学速查.md) 负责公式与条件。",
        "- [多元积分学](03_多元积分学/README.md)：由 [积分元素](03_多元积分学/01_重积分/积分元素.md) 进入各类积分，用 [速查](03_多元积分学/多元积分学速查.md) 选择方法。", "",
        "库内统一使用标准 Markdown 相对链接与 `/` 分隔符，目录链接指向 `README.md`。正文在概念衔接处说明前置或后续主题，速查回链详解；改名时同步更新正文、目录和绘图校验脚本。引用优先指向整篇文档，避免章节标题变化使锚点失效。", "",
        "## 完整引用与反向索引", "",
    ]
    for section in sorted({p.relative_to(ROOT).parts[0] for p in notes}):
        lines += [f"### {section.removesuffix('.md')}", "",
                  "| 文档 | 引用的文档 | 被哪些文档引用 |", "| --- | --- | --- |"]
        for note in notes:
            if note.relative_to(ROOT).parts[0] != section:
                continue
            outbound = "、".join(link(p) for p in sorted(edges[note])) or "—"
            inbound = "、".join(link(p) for p in sorted(back[note])) or "—"
            lines.append(f"| {link(note)} | {outbound} | {inbound} |")
        lines.append("")
    lines += ["## 更新与检查", "", "在本章目录运行：", "", "```powershell",
              "python tools/update_reference_map.py", "python tools/check_references.py",
              "python tools/check_references.py --git-ref HEAD", "```", "",
              "检查覆盖相对链接、图片目标及从总目录出发的文档可达性；`--git-ref HEAD` 直接读取提交内容，能够发现未纳入 Git 的依赖。关系图谱自身不参与反向索引统计，避免索引链接掩盖正文缺少交叉引用的问题。", "",
              "[返回多元微积分](README.md)"]
    MAP.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Indexed {len(notes)} Markdown documents.")


if __name__ == "__main__":
    generate()
