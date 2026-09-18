"""Markdown → .docx 转换器 (纯标准库，零网络依赖)

将 Markdown 文件转换为格式规范、可直接交付的 .docx 文档。
.docx 本质是 ZIP 压缩包内含 Word XML，本模块用 xml.etree + zipfile 直接构建。

输出格式：
  - 标题行样式（Heading1~4）：黑体加粗
  - 正文：宋体 10.5pt，单倍行距
  - 代码块：Consolas 等宽 + 浅灰背景
  - 表格：标准边框
  - 分章分页
"""

from __future__ import annotations

import re
import io
import zipfile
from pathlib import Path
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
}

DOCUMENT_REL_TYPE = (
    "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
)

FONT_SONG = "宋体"
FONT_HEI = "黑体"
FONT_MONO = "Consolas"


def _qname(tag: str) -> str:
    return "{%s}%s" % (NS["w"], tag)


def _w(tag: str) -> str:
    return _qname(tag)


def _rpr(font: str, size: int, bold: bool = False, color: str = "000000") -> Element:
    """生成 run properties 元素。"""
    rpr = Element(_w("rPr"))
    rFonts = SubElement(rpr, _w("rFonts"))
    rFonts.set(_w("eastAsia"), font)
    rFonts.set(_w("ascii"), font)
    rFonts.set(_w("hAnsi"), font)
    sz = SubElement(rpr, _w("sz"))
    sz.set(_w("val"), str(size))
    szCs = SubElement(rpr, _w("szCs"))
    szCs.set(_w("val"), str(size))
    if bold:
        b = SubElement(rpr, _w("b"))
        bCs = SubElement(rpr, _w("bCs"))
    if color != "000000":
        c = SubElement(rpr, _w("color"))
        c.set(_w("val"), color)
    return rpr


def _para_style(style_id: str) -> Element:
    ppr = Element(_w("pPr"))
    pStyle = SubElement(ppr, _w("pStyle"))
    pStyle.set(_w("val"), style_id)
    return ppr


def _run(text: str, font: str = FONT_SONG, size: int = 22, bold: bool = False,
         color: str = "000000", mono: bool = False) -> Element:
    """生成单个 run 元素。21 = 10.5pt (半倍), 32 = 16pt (三号)"""
    r = Element(_w("r"))
    r.append(_rpr(FONT_MONO if mono else font, size, bold, color))
    t = SubElement(r, _w("t"))
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return r


def _para(runs: list[Element] | None = None, style: str | None = None,
          spacing_after: int = 120, spacing_line: int = 300,
          page_break_before: bool = False,
          align: str | None = None) -> Element:
    """生成段落元素。"""
    p = Element(_w("p"))
    ppr = SubElement(p, _w("pPr"))
    if style:
        pStyle = SubElement(ppr, _w("pStyle"))
        pStyle.set(_w("val"), style)
    spacing = SubElement(ppr, _w("spacing"))
    spacing.set(_w("after"), str(spacing_after))
    spacing.set(_w("line"), str(spacing_line))
    spacing.set(_w("lineRule"), "auto")
    if page_break_before:
        pb = SubElement(ppr, _w("pageBreakBefore"))
    if align:
        jc = SubElement(ppr, _w("jc"))
        jc.set(_w("val"), align)
    if runs:
        for run in runs:
            p.append(run)
    return p


def _table(headers: list[str], rows: list[list[str]], col_widths: list[int] | None = None) -> Element:
    """生成表格元素。"""
    tbl = Element(_w("tbl"))
    tblPr = SubElement(tbl, _w("tblPr"))
    tblStyle = SubElement(tblPr, _w("tblStyle"))
    tblStyle.set(_w("val"), "TableGrid")
    tblW = SubElement(tblPr, _w("tblW"))
    tblW.set(_w("w"), "9072")
    tblW.set(_w("type"), "dxa")
    borders = SubElement(tblPr, _w("tblBorders"))
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = SubElement(borders, _w(edge))
        b.set(_w("val"), "single")
        b.set(_w("sz"), "4")
        b.set(_w("color"), "999999")

    def _cell(text: str, is_header: bool, width: int | None = None) -> Element:
        tc = Element(_w("tc"))
        tcPr = SubElement(tc, _w("tcPr"))
        if width:
            tcW = SubElement(tcPr, _w("tcW"))
            tcW.set(_w("w"), str(width))
            tcW.set(_w("type"), "dxa")
        if is_header:
            shading = SubElement(tcPr, _w("shd"))
            shading.set(_w("val"), "clear")
            shading.set(_w("color"), "auto")
            shading.set(_w("fill"), "4472C4")
        p = Element(_w("p"))
        p.append(_run(text, font=FONT_HEI if is_header else FONT_SONG,
                       size=20 if is_header else 20,
                       bold=is_header, color="FFFFFF" if is_header else "000000"))
        tc.append(p)
        return tc

    for i, row in enumerate([headers] + rows):
        tr = Element(_w("tr"))
        for j, cell_text in enumerate(row):
            w = col_widths[j] if col_widths else None
            tr.append(_cell(cell_text, is_header=(i == 0), width=w))
        tbl.append(tr)
    return tbl


def _code_block(lines: list[str]) -> list[Element]:
    """代码块 → 浅灰背景段落列表。"""
    paras = []
    for line in lines:
        p = Element(_w("p"))
        ppr = SubElement(p, _w("pPr"))
        shading = SubElement(ppr, _w("shd"))
        shading.set(_w("val"), "clear")
        shading.set(_w("color"), "auto")
        shading.set(_w("fill"), "F2F2F2")
        spacing = SubElement(ppr, _w("spacing"))
        spacing.set(_w("line"), "260")
        spacing.set(_w("lineRule"), "auto")
        p.append(_run(line if line else " ", mono=True, size=18))
        paras.append(p)
    return paras


def _parse_inline(text: str, base_font: str = FONT_SONG, base_size: int = 22) -> list[Element]:
    """解析行内格式：**粗体**、*斜体*、`代码`、[链接]。
    返回 run 列表。"""
    if not text:
        return [_run("", font=base_font, size=base_size)]

    runs = []
    pattern = re.compile(
        r'(\*\*(.+?)\*\*)|'        # **bold**
        r'(\*(.+?)\*)|'            # *italic*
        r'(`(.+?)`)|'              # `code`
        r'(\[(.+?)\]\((.+?)\))'    # [text](url)
    )
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            runs.append(_run(text[last:m.start()], font=base_font, size=base_size))
        if m.group(2):  # **bold**
            runs.append(_run(m.group(2), font=base_font, size=base_size, bold=True))
        elif m.group(4):  # *italic*
            runs.append(_run(m.group(4), font=base_font, size=base_size))
        elif m.group(6):  # `code`
            runs.append(_run(m.group(6), mono=True, size=base_size))
        elif m.group(8):  # [text](url)
            runs.append(_run(m.group(8), font=base_font, size=base_size, color="0563C1"))
        last = m.end()
    if last < len(text):
        runs.append(_run(text[last:], font=base_font, size=base_size))
    return runs if runs else [_run(text, font=base_font, size=base_size)]


def _process_markdown_lines(lines: list[str]) -> list[Element]:
    """逐行解析 Markdown，返回 Word XML 元素列表。"""
    elements: list[Element] = []
    i = 0
    n = len(lines)
    in_code_block = False
    code_lines: list[str] = []
    in_table = False
    table_rows: list[list[str]] = []

    def flush_table():
        nonlocal in_table, table_rows
        if table_rows:
            headers = table_rows[0]
            rows = [[c.strip() for c in r] for r in table_rows[1:]]
            elements.append(_para(spacing_after=60))
            elements.append(_table(headers, rows))
            elements.append(_para(spacing_after=60))
            table_rows = []
            in_table = False

    def flush_code():
        nonlocal in_code_block, code_lines
        if code_lines:
            elements.extend(_code_block(code_lines))
            elements.append(_para(spacing_after=60))
            code_lines = []
            in_code_block = False

    while i < n:
        line = lines[i]
        raw = line

        # 代码块
        if line.strip().startswith("```"):
            if in_code_block:
                flush_code()
            else:
                flush_table()
                in_code_block = True
            i += 1
            continue
        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # 空行
        if not line.strip():
            flush_table()
            elements.append(_para(spacing_after=60))
            i += 1
            continue

        # 表格（以 | 开头的行）
        if line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # 跳过分隔行（如 |---|----|）
            if all(re.match(r'^:?-{2,}:?$', c.strip()) for c in cells):
                i += 1
                continue
            if not in_table:
                flush_code()
                in_table = True
            table_rows.append(cells)
            i += 1
            continue
        else:
            flush_table()

        # 分隔线 ---
        if re.match(r'^[-*_]{3,}\s*$', line.strip()):
            p = _para(spacing_after=60)
            pPr = p.find(_w("pPr"))
            pBdr = SubElement(pPr, _w("pBdr"))
            bottom = SubElement(pBdr, _w("bottom"))
            bottom.set(_w("val"), "single")
            bottom.set(_w("sz"), "6")
            bottom.set(_w("color"), "CCCCCC")
            elements.append(p)
            i += 1
            continue

        # 标题
        h_match = re.match(r'^(#{1,4})\s+(.+)$', line)
        if h_match:
            level = min(len(h_match.group(1)), 4)
            text = h_match.group(2).strip()
            style_map = {1: "Heading1", 2: "Heading2", 3: "Heading3", 4: "Heading4"}
            font_size_map = {1: 36, 2: 32, 3: 28, 4: 24}
            p = Element(_w("p"))
            ppr = SubElement(p, _w("pPr"))
            pStyle = SubElement(ppr, _w("pStyle"))
            pStyle.set(_w("val"), style_map[level])
            spacing = SubElement(ppr, _w("spacing"))
            spacing.set(_w("before"), "240")
            spacing.set(_w("after"), "120")
            if level == 1:
                pb = SubElement(ppr, _w("pageBreakBefore"))
            p.append(_run(text, font=FONT_HEI, size=font_size_map[level], bold=True, color="1F3864"))
            elements.append(p)
            i += 1
            continue

        # 引用 >
        if line.startswith(">"):
            text = line[1:].strip()
            p = Element(_w("p"))
            ppr = SubElement(p, _w("pPr"))
            ind = SubElement(ppr, _w("ind"))
            ind.set(_w("left"), "720")
            shading = SubElement(ppr, _w("shd"))
            shading.set(_w("val"), "clear")
            shading.set(_w("color"), "auto")
            shading.set(_w("fill"), "F5F5F5")
            p.extend(_parse_inline(text, base_size=20))
            elements.append(p)
            i += 1
            continue

        # 无序列表
        ul_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if ul_match:
            indent_level = len(ul_match.group(1)) // 2
            text = ul_match.group(2)
            p = Element(_w("p"))
            ppr = SubElement(p, _w("pPr"))
            ind = SubElement(ppr, _w("ind"))
            ind.set(_w("left"), str(720 + indent_level * 360))
            ind.set(_w("hanging"), "360")
            spacing = SubElement(ppr, _w("spacing"))
            spacing.set(_w("after"), "60")
            # 添加项目符号
            p.extend(_parse_inline(text))
            bullet_run = _run("\u2022 ", font=FONT_SONG, size=22)
            p.insert(0, bullet_run)
            elements.append(p)
            i += 1
            continue

        # 有序列表
        ol_match = re.match(r'^(\s*)\d+[.)]\s+(.+)$', line)
        if ol_match:
            indent_level = len(ol_match.group(1)) // 2
            text = ol_match.group(2)
            p = Element(_w("p"))
            ppr = SubElement(p, _w("pPr"))
            ind = SubElement(ppr, _w("ind"))
            ind.set(_w("left"), str(720 + indent_level * 360))
            ind.set(_w("hanging"), "360")
            spacing = SubElement(ppr, _w("spacing"))
            spacing.set(_w("after"), "60")
            num = str(i + 1) + ". "
            p.append(_run(num, font=FONT_SONG, size=22))
            p.extend(_parse_inline(text))
            elements.append(p)
            i += 1
            continue

        # 普通段落
        p = Element(_w("p"))
        ppr = SubElement(p, _w("pPr"))
        spacing = SubElement(ppr, _w("spacing"))
        spacing.set(_w("after"), "120")
        spacing.set(_w("line"), "300")
        spacing.set(_w("lineRule"), "auto")
        p.extend(_parse_inline(line))
        elements.append(p)
        i += 1

    flush_table()
    flush_code()
    return elements


def _build_styles_xml() -> bytes:
    """生成 styles.xml。"""
    root = Element(_w("styles"))
    root.set("xmlns:w", NS["w"])
    root.set("xmlns:mc", NS["mc"])
    root.set("xmlns:r", NS["r"])
    root.set("xmlns:w14", NS["w14"])

    defaults = SubElement(root, _w("docDefaults"))
    rPrDefault = SubElement(defaults, _w("rPrDefault"))
    rPr = SubElement(rPrDefault, _w("rPr"))
    rFonts = SubElement(rPr, _w("rFonts"))
    rFonts.set(_w("eastAsia"), FONT_SONG)
    rFonts.set(_w("ascii"), FONT_SONG)
    rFonts.set(_w("hAnsi"), FONT_SONG)
    sz = SubElement(rPr, _w("sz"))
    sz.set(_w("val"), "22")
    pPrDefault = SubElement(defaults, _w("pPrDefault"))
    pPr = SubElement(pPrDefault, _w("pPr"))
    spacing = SubElement(pPr, _w("spacing"))
    spacing.set(_w("line"), "300")
    spacing.set(_w("lineRule"), "auto")

    styles_def = [
        ("Normal", "Normal", None, None, None),
        ("Heading1", "heading 1", None, FONT_HEI, 36),
        ("Heading2", "heading 2", None, FONT_HEI, 32),
        ("Heading3", "heading 3", None, FONT_HEI, 28),
        ("Heading4", "heading 4", None, FONT_HEI, 24),
        ("TableGrid", "Table Grid", "table", None, None),
    ]

    for style_id, name, stype, font, sz_val in styles_def:
        style = SubElement(root, _w("style"))
        style.set(_w("type"), stype or "paragraph")
        style.set(_w("styleId"), style_id)
        name_el = SubElement(style, _w("name"))
        name_el.set(_w("val"), name)
        if stype == "table":
            tblPr = SubElement(style, _w("tblPr"))
            tblStyleRowBandSize = SubElement(tblPr, _w("tblStyleRowBandSize"))
            tblStyleRowBandSize.set(_w("val"), "1")
        if font or sz_val:
            rPr = SubElement(style, _w("rPr"))
            if font:
                rFonts = SubElement(rPr, _w("rFonts"))
                rFonts.set(_w("eastAsia"), font)
                rFonts.set(_w("ascii"), font)
                rFonts.set(_w("hAnsi"), font)
            if sz_val:
                sz = SubElement(rPr, _w("sz"))
                sz.set(_w("val"), str(sz_val))

    return tostring(root, encoding="utf-8", xml_declaration=True)


def _build_document_xml(elements: list[Element]) -> bytes:
    """生成 document.xml。"""
    root = Element(_w("document"))
    root.set("xmlns:w", NS["w"])
    root.set("xmlns:r", NS["r"])
    body = SubElement(root, _w("body"))
    # 文档属性
    sectPr = SubElement(body, _w("sectPr"))
    pgSz = SubElement(sectPr, _w("pgSz"))
    pgSz.set(_w("w"), "11906")
    pgSz.set(_w("h"), "16838")
    pgMar = SubElement(sectPr, _w("pgMar"))
    pgMar.set(_w("top"), "1440")
    pgMar.set(_w("right"), "1440")
    pgMar.set(_w("bottom"), "1440")
    pgMar.set(_w("left"), "1440")

    for el in elements:
        body.append(el)

    return tostring(root, encoding="utf-8", xml_declaration=True)


def _build_content_types() -> bytes:
    return b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''


def _build_rels() -> bytes:
    return b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''


def _build_doc_rels() -> bytes:
    return b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''


def convert_md_to_docx(md_path: str | Path, docx_path: str | Path | None = None) -> str:
    """将 Markdown 文件转换为 .docx。

    Args:
        md_path: Markdown 源文件路径
        docx_path: 目标 .docx 路径，默认同目录同名 .docx

    Returns:
        生成的 .docx 文件路径
    """
    md_path = Path(md_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown 文件不存在: {md_path}")

    if docx_path is None:
        docx_path = md_path.with_suffix(".docx")
    docx_path = Path(docx_path)

    # 读取 Markdown
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    elements = _process_markdown_lines(lines)

    # 构建 docx ZIP
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _build_content_types())
        zf.writestr("_rels/.rels", _build_rels())
        zf.writestr("word/_rels/document.xml.rels", _build_doc_rels())
        zf.writestr("word/styles.xml", _build_styles_xml())
        zf.writestr("word/document.xml", _build_document_xml(elements))

    with open(docx_path, "wb") as f:
        f.write(buf.getvalue())

    return str(docx_path)


# ============================================================
# 批量转换入口
# ============================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python md2docx.py <文件.md> [输出.docx]")
        print("       python md2docx.py --all  # 批量转换全部三份文档")
        sys.exit(0)

    if sys.argv[1] == "--all":
        base = Path(__file__).resolve().parents[3] / "docs"
        targets = [
            base / "系统说明书" / "IMS系统说明书.md",
            base / "用户操作手册" / "IMS用户操作手册.md",
        ]
        # 二次开发说明书：合并后转换
        dev_dir = base / "二次开发说明书"
        merged = dev_dir / "_merged_for_docx.md"
        parts = sorted(dev_dir.glob("*.md"))
        with open(merged, "w", encoding="utf-8") as out:
            out.write("# IMS 二次开发说明书\n\n")
            out.write(f"> 文档版本：v2.0 | 生成日期：{datetime.now().strftime('%Y-%m-%d')}\n\n")
            out.write("---\n\n")
            for p in parts:
                with open(p, "r", encoding="utf-8") as inf:
                    out.write(inf.read())
                    out.write("\n\n---\n\n")
        targets.append(merged)

        for t in targets:
            out_path = convert_md_to_docx(t)
            print(f"OK: {out_path}")

        # 清理临时文件
        if merged.exists():
            merged.unlink()
        print("\n全部转换完成！")
    else:
        src = sys.argv[1]
        dst = sys.argv[2] if len(sys.argv) > 2 else None
        out = convert_md_to_docx(src, dst)
        print(f"OK: {out}")