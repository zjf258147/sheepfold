"""使用 pandoc 将 .md 转 .docx"""
import subprocess, sys, pathlib

PANDOC = r"C:\Users\25075\AppData\Local\Pandoc\pandoc.exe"
BASE = pathlib.Path(r"c:\Users\25075\Desktop\IMS生产物料与产品追溯管理系统\ims-main\docs")

tasks = [
    ("文档编写规范", BASE / "文档编写规范.md", BASE / "文档编写规范.docx"),
    ("系统说明书", BASE / "系统说明书" / "IMS系统说明书.md", BASE / "系统说明书" / "IMS系统说明书.docx"),
    ("用户操作手册", BASE / "用户操作手册" / "IMS用户操作手册.md", BASE / "用户操作手册" / "IMS用户操作手册.docx"),
    ("数据字典", BASE / "附录" / "数据字典.md", BASE / "附录" / "数据字典.docx"),
]

for name, src, dst in tasks:
    if not src.exists():
        print(f"  ❌ {name}: 源文件不存在 {src}", flush=True)
        continue
    sys.stdout.write(f"  {name} ... ")
    sys.stdout.flush()
    try:
        result = subprocess.run(
            [PANDOC, str(src), "-o", str(dst), "-f", "markdown", "-t", "docx"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            sz = dst.stat().st_size / 1024
            sys.stdout.write(f"✅ {sz:.1f} KB\n")
        else:
            sys.stdout.write(f"❌ rc={result.returncode} {result.stderr[:80]}\n")
        sys.stdout.flush()
    except subprocess.TimeoutExpired:
        sys.stdout.write("❌ 超时\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"❌ {e}\n")
        sys.stdout.flush()

print("完成", flush=True)