from pathlib import Path
import mammoth

def docx_to_markdown(docx_path: Path) -> Path:
    if not docx_path.exists():
        raise FileNotFoundError(docx_path)
    md_path = docx_path.with_suffix(".md")
    with open(docx_path, "rb") as fp:
        md = mammoth.convert_to_markdown(fp).value
    md_path.write_text(md, encoding="utf-8")
    print(f"Word → Markdown 已完成：{md_path}")
    return md_path
