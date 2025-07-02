from pathlib import Path
import argparse
from word2md      import docx_to_markdown
from extract_json import markdown_to_json
from build_kg     import json_to_html

def run(docx_file: Path):
    md_path   = docx_to_markdown(docx_file)
    json_path = markdown_to_json(md_path)
    html_path = json_to_html(json_path)
    print(f"\n全流程完成！打开浏览器查看：{html_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word→Markdown→JSON→知识图谱 全流程脚本")
    parser.add_argument("docx", type=Path, help="待解析的 .docx 文件")
    args = parser.parse_args()
    run(args.docx.resolve())
