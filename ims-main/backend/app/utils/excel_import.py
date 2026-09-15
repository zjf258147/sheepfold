"""通用 Excel 导入工具。"""
import io

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill


def parse_import_xlsx(content: bytes, skip_header: int = 1) -> list[list[str]]:
    """解析上传的 Excel 文件，返回数据行列表（每行为 list[str]）。

    Args:
        content: Excel 文件字节流
        skip_header: 跳过前 N 行（默认跳过第1行表头）
    """
    wb = load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb.active
    rows: list[list[str]] = []
    for i, row in enumerate(ws.iter_rows(values_only=True), 1):
        if i <= skip_header:
            continue
        if row is None or all(v is None or str(v).strip() == "" for v in row):
            continue
        rows.append([str(v).strip() if v is not None else "" for v in row])
    wb.close()
    return rows


def build_template_xlsx(
    headers: list[str],
    example_row: list[str] | None = None,
    sheet_title: str = "导入模板",
    col_widths: list[int] | None = None,
) -> bytes:
    """生成 Excel 导入模板（表头 + 示例行）。

    Args:
        headers: 表头列名列表
        example_row: 示例数据行（可选，放在第2行）
        sheet_title: Sheet 名称
        col_widths: 列宽列表（可选）
    """
    wb = load_workbook.__self__ if False else None  # noqa — just for import
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_title
    ws.append(headers)

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="67C23A")
    center = Alignment(horizontal="center", vertical="center")
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center

    if example_row:
        ws.append(example_row)

    if col_widths:
        for i, w in enumerate(col_widths, 1):
            letter = ws.cell(row=1, column=i).column_letter
            ws.column_dimensions[letter].width = w

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()