from pathlib import Path
import json
from call_llm import call_local_llm

# 可按需调整
SCHEMA_NOTE = """
你是一名结构抽取智能体（StructureExtractor），负责把 Markdown 文档中的关键信息转换成便于可视化的结构化 JSON。
禁止输出除 JSON 以外的任何字符（包括解释、Markdown、注释）。
输出示例：
{
  "entities": [
    {"id": "E1", "label": "主体A", "type": "公司"},
    {"id": "E2", "label": "主体B", "type": "产品"}
  ],
  "relations": [
    {"source": "E1", "target": "E2", "type": "生产"}
  ]
}
"""

def markdown_to_json(md_path: Path) -> Path:

    # 基础校验
    if not md_path.exists():
        raise FileNotFoundError(md_path)
    md_text = md_path.read_text(encoding="utf-8")
    prompt = f"{SCHEMA_NOTE}\n\n--------------\n文档内容：\n{md_text}"

    # 调用LLM
    json_str = call_local_llm(prompt).strip()

    # 解析并写盘
    data = json.loads(json_str)

    json_path = md_path.with_name(f"{md_path.stem}__parsed__.json")

    json_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"JSON 抽取完成：{json_path}")
    return json_path

if __name__ == "__main__":
    import sys
    markdown_to_json(Path(sys.argv[1]))
