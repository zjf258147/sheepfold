"""文档下载 API"""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/docs", tags=["文档下载"])

DOCS_ROOT = Path(__file__).resolve().parents[3] / "docs"

DOCUMENTS = [
    {
        "id": "spec",
        "name": "系统说明书",
        "description": "系统架构、业务逻辑、数据规范、安全机制",
        "file": DOCS_ROOT / "系统说明书" / "IMS系统说明书.docx",
        "icon": "Document",
        "category": "用户文档",
    },
    {
        "id": "manual",
        "name": "用户操作手册",
        "description": "各角色日常操作步骤与常见问题",
        "file": DOCS_ROOT / "用户操作手册" / "IMS用户操作手册.docx",
        "icon": "Notebook",
        "category": "用户文档",
    },
    {
        "id": "dev",
        "name": "二次开发说明书",
        "description": "开发环境搭建、代码结构、后端/前端/数据库规范、部署运维",
        "file": DOCS_ROOT / "二次开发说明书" / "IMS二次开发说明书.docx",
        "icon": "Document",
        "category": "开发文档",
    },
    {
        "id": "style",
        "name": "文档编写规范",
        "description": "文档编写格式、风格与维护流程规范",
        "file": DOCS_ROOT / "文档编写规范.docx",
        "icon": "EditPen",
        "category": "开发文档",
    },
]


@router.get("")
def list_documents():
    """获取可下载的文档列表"""
    items = []
    for doc in DOCUMENTS:
        info = {
            "id": doc["id"],
            "name": doc["name"],
            "description": doc["description"],
            "icon": doc["icon"],
            "category": doc["category"],
            "downloadUrl": f"/api/v1/docs/download/{doc['id']}",
            "exists": doc["file"].exists(),
        }
        if doc["file"].exists():
            size_kb = round(doc["file"].stat().st_size / 1024, 1)
            info["size"] = f"{size_kb} KB"
        items.append(info)
    return {"items": items}


@router.get("/download/{doc_id}")
def download_document(doc_id: str):
    """下载指定文档"""
    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            if not doc["file"].exists():
                return {"detail": "文件不存在"}
            filename = f"{doc['name']}.docx"
            return FileResponse(
                path=str(doc["file"]),
                filename=filename,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
    return {"detail": "文档不存在"}