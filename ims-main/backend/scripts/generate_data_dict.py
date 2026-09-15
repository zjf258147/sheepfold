#!/usr/bin/env python3
"""自动生成数据字典 Markdown 文档。

遍历所有 SQLAlchemy Model 类，按 MRO 提取含继承的全部字段，
按模块分组输出为 Markdown 表格。

用法：
    cd backend
    python scripts/generate_data_dict.py
    python scripts/generate_data_dict.py --output ../docs/附录/数据字典.md
"""

import argparse
import importlib
import inspect
import os
import pkgutil
import sys
from datetime import datetime
from pathlib import Path

_backend_dir = Path(__file__).resolve().parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from sqlalchemy import Column, Integer as SAInteger, inspect as sa_inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import (
    BigInteger, Boolean, Date, DateTime, Enum, Float,
    Numeric, SmallInteger, String, Text, Time,
)

from app.db.base import Base, TimestampMixin

# ---------- 模块归属配置 ----------

FILE_MODULE_MAP: dict[str, str] = {
    "incoming":       "主线A - 采购来料管理",
    "inbound":        "主线A - 采购来料管理",
    "raw_material":   "主线A - 采购来料管理",
    "rma":            "主线B - 成品返厂维修",
    "outbound":       "主线C - 出货管理",
    "shipment":       "主线C - 出货管理",
    "bom":            "主线D - BOM与生产准备",
    "product":        "基础数据 - 商品SKU",
    "partner":        "基础数据 - 往来单位",
    "customer":       "基础数据 - 客户管理",
    "sequence":       "基础数据 - 编号序列",
    "user":           "支撑模块 - 用户与权限",
    "audit_log":      "支撑模块 - 审计日志",
    "system_config":  "支撑模块 - 系统设置",
    "inventory":              "库存管理",
    "station":                "二期 - 场站管理",
    "device_ledger":          "二期 - 设备台账",
    "stocktake":              "二期 - 盘点管理",
    "inventory_adjustment":   "二期 - 库存调整",
    "enums":                  None,
}

TABLE_OVERRIDE: dict[str, str] = {}

# TimestampMixin 定义的列名
_TS_COLUMN_NAMES: set[str] = {"created_at", "updated_at"}

# ---------- 类型映射 ----------

_SQLA_TYPE_MAP: dict[type, str] = {
    BigInteger:   "BIGINT",
    Boolean:      "BOOLEAN",
    Date:         "DATE",
    DateTime:     "DATETIME",
    Float:        "FLOAT",
    SAInteger:    "INT",
    Numeric:      "DECIMAL",
    SmallInteger: "SMALLINT",
    String:       "VARCHAR",
    Text:         "TEXT",
    Time:         "TIME",
    Enum:         "ENUM",
}


def _type_to_str(col_type) -> str:
    t = type(col_type)
    base = _SQLA_TYPE_MAP.get(t, t.__name__.upper())
    if isinstance(col_type, String) and col_type.length:
        return f"VARCHAR({col_type.length})"
    if isinstance(col_type, Numeric):
        p = col_type.precision
        s = col_type.scale
        if p is not None and s is not None:
            return f"DECIMAL({p},{s})"
    if isinstance(col_type, Enum):
        vals = [repr(v) for v in col_type.enums]
        return f"ENUM({', '.join(vals)})"
    return base


def _get_module_name(model_cls: type) -> str:
    table = getattr(model_cls, "__tablename__", "")
    if table in TABLE_OVERRIDE:
        return TABLE_OVERRIDE[table]
    mod = model_cls.__module__
    parts = mod.split(".")
    filename = parts[-1] if len(parts) > 1 else mod
    result = FILE_MODULE_MAP.get(filename, "待归类")
    return result if result is not None else "待归类"


def _discover_models() -> list[type]:
    import app.models
    pkg_path = os.path.dirname(app.models.__file__)
    models: list[type] = []

    for _, name, is_pkg in pkgutil.iter_modules([pkg_path]):
        if is_pkg or name.startswith("_"):
            continue
        mapped = FILE_MODULE_MAP.get(name)
        if mapped is None and name != "enums":
            continue

        try:
            mod = importlib.import_module(f"app.models.{name}")
        except Exception:
            continue

        for _, obj in inspect.getmembers(mod, inspect.isclass):
            if obj is Base or obj is TimestampMixin or obj is DeclarativeBase:
                continue
            if not hasattr(obj, "__tablename__"):
                continue
            if issubclass(obj, Base):
                models.append(obj)

    return models


def _is_timestamp_mixin(cls: type) -> bool:
    return TimestampMixin in getattr(cls, "__mro__", [])


def _extract_columns(model_cls: type) -> list[dict]:
    try:
        mapper = sa_inspect(model_cls)
    except Exception:
        return []

    columns: list[dict] = []
    ts_inherited = _is_timestamp_mixin(model_cls)

    for col in mapper.columns:
        field_type = _type_to_str(col.type)
        is_pk = col.primary_key

        default_str = "—"
        if is_pk and getattr(col, "autoincrement", False) in (True, "auto"):
            default_str = "自增"
        elif col.server_default is not None:
            try:
                default_str = str(col.server_default.arg)
            except Exception:
                default_str = "DB默认"
        elif col.default is not None:
            try:
                default_str = str(col.default.arg)
            except Exception:
                default_str = "有默认值"

        is_ts = ts_inherited and col.name in _TS_COLUMN_NAMES
        type_str = field_type + "（继承）" if is_ts else field_type

        columns.append({
            "name":     col.name,
            "type":     type_str,
            "nullable": col.nullable if col.nullable is not None else True,
            "default":  default_str,
            "comment":  col.comment or "",
        })

    return columns


def _collect_tables(models: list[type]) -> list[dict]:
    tables: list[dict] = []
    for m in models:
        col_list = _extract_columns(m)
        if not col_list:
            continue
        doc = (m.__doc__ or "").strip().split("\n")[0].rstrip("。").rstrip(".")
        tables.append({
            "table_name": getattr(m, "__tablename__", m.__name__),
            "doc":        doc,
            "module":     _get_module_name(m),
            "columns":    col_list,
        })
    tables.sort(key=lambda t: (t["module"], t["table_name"]))
    return tables


# ---------- Markdown 渲染 ----------

def _render_table(info: dict) -> str:
    lines: list[str] = []
    lines.append(f"## 表：{info['table_name']}")
    if info["doc"]:
        lines.append("")
        lines.append(f"> 表注释：{info['doc']}")
    lines.append(f"> 所属模块：{info['module']}")
    lines.append("")
    lines.append("| 字段名 | 类型 | 必填 | 默认值 | 说明 |")
    lines.append("|--------|------|:---:|--------|------|")

    for col in info["columns"]:
        required = "✅" if not col["nullable"] else "❌"
        lines.append(
            f"| `{col['name']}` "
            f"| {col['type']} "
            f"| {required} "
            f"| {col['default']} "
            f"| {col['comment']} |"
        )
    lines.append("")
    return "\n".join(lines)


def _render_full(tables: list[dict], unclassified: set[str]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = []
    lines.append("# IMS 完整数据字典")
    lines.append("")
    lines.append(f"> 本文档由 `generate_data_dict.py` 自动生成，生成时间：{now}")
    lines.append("> 数据源：`backend/app/models/*.py`，禁止手动编辑。")
    lines.append("> 如需更新，修改 Model 的 `comment` 后重新运行脚本。")
    lines.append("")
    lines.append("---")
    lines.append("")

    prev_module = None
    for t in tables:
        if t["module"] != prev_module:
            lines.append(f"# {t['module']}")
            lines.append("")
            prev_module = t["module"]
        lines.append(_render_table(t))

    if unclassified:
        lines.append("---")
        lines.append("")
        lines.append("# 待归类表清单")
        lines.append("")
        lines.append("> 以下表未能自动匹配到业务模块，请手动补充到脚本的 `TABLE_OVERRIDE` 字典中。")
        lines.append("")
        for tbl in sorted(unclassified):
            lines.append(f"- `{tbl}`")

    return "\n".join(lines)


# ---------- 主入口 ----------

def main() -> None:
    parser = argparse.ArgumentParser(description="生成 IMS 数据字典 Markdown")
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出文件路径（默认：docs/附录/数据字典.md，相对于 backend 目录）",
    )
    args = parser.parse_args()

    output_path = args.output
    if output_path is None:
        output_path = os.path.join(_backend_dir, "..", "docs", "附录", "数据字典.md")
    output_path = os.path.abspath(output_path)

    print("发现 Model 类...")
    models = _discover_models()
    print(f"  找到 {len(models)} 个 Model 类")

    print("提取字段信息...")
    tables = _collect_tables(models)

    unclassified: set[str] = set()
    for t in tables:
        if t["module"] == "待归类":
            unclassified.add(t["table_name"])

    print("生成 Markdown...")
    md = _render_full(tables, unclassified)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md)

    total_cols = sum(len(t["columns"]) for t in tables)
    print(f"数据字典已生成：{output_path}")
    print(f"共 {len(tables)} 张表，{total_cols} 个字段")
    if unclassified:
        print(f"{len(unclassified)} 张表未归类，请查看文档末尾的待归类表清单")
    else:
        print("所有表均已归类")


if __name__ == "__main__":
    main()