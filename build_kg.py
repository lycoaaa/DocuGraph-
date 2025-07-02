from pathlib import Path
import json
import networkx as nx
from pyvis.network import Network

def json_to_html(json_path: Path) -> Path:

    # 读取 JSON
    data = json.loads(json_path.read_text(encoding="utf-8"))

    # 构建有向图
    G = nx.DiGraph()
    for ent in data.get("entities", []):
        G.add_node(
            ent["id"],
            label=ent.get("label", ent["id"]),
            title=ent.get("type", ""),
            group=ent.get("type", "")
        )
    for rel in data.get("relations", []):
        G.add_edge(
            rel["source"],
            rel["target"],
            label=rel.get("type", ""),
            title=rel.get("type", "")
        )

    # 使用pyvis 渲染
    net = Network(
        height="95vh",
        width="100%",
        bgcolor="#ffffff",
        directed=True,
        notebook=False
    )
    net.from_nx(G)
    net.force_atlas_2based()

    html_path = json_path.with_name(f"{json_path.stem}__kg.html")
    net.write_html(str(html_path))  # 转成 str，兼容 pyvis
    print(f"知识图谱 HTML 生成：{html_path}")
    return html_path

if __name__ == "__main__":
    import sys
    json_to_html(Path(sys.argv[1]))
