# DocuGraph
A lightweight pipeline that instantly converts Word documents into interactive knowledge graphs with a single command/一款轻量级流水线工具，只需一条命令即可把 Word 等办公文档自动转化为交互式知识图谱

DocuGraph 将传统办公文档一步自动转换为 **可交互知识图谱**。  
它包含三条串联的轻量模块：**格式转换 → 结构抽取 → 图谱渲染** 
让你在本地或服务器上只需一行命令，就能把 `.docx` 变成跨平台浏览器可视化结果。

![image](https://github.com/user-attachments/assets/096d4907-a129-4c23-949a-debe2c0f511c)

---

## Features

* **One-Command Pipeline** – `python main.py your.docx` 即可完成全部流程  
* **Large-Language-Model Extraction** – DeepSeek API 精准抽取实体 / 关系  
* **Zero Front-End Code** – `pyvis` + `networkx` 自动生成 HTML，窗口大小自适应  
* **可扩展** – 只需替换第一步转换脚本，即可支持 PDF、Excel 等多格式输入

---

## Quick Start

```bash
# 配置 DeepSeek Key（Windows 使用 $env:DEEPSEEK_API_KEY="sk-xxxx"）
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

python main.py /path/to/your.docx
````

运行完毕后，你会在同目录看到
`your__parsed__.json` — 结构化抽取结果
`your__parsed__kg.html` — 交互式知识图谱（浏览器打开查看）

---

## Architecture

```
       .docx
┌──────────────────┐
│     word2md      │
│    (mammoth)     │
└──────────────────┘
          │
          ▼
      Markdown
┌──────────────────┐
│    extractor     │
│    (DeepSeek)    │
└──────────────────┘
          │
          ▼
        JSON
┌──────────────────┐
│     build_kg     │
│    (pyvis+nx)    │
└──────────────────┘
          │
          ▼
        HTML
┌──────────────────┐
│     Browser      │
│     (viewer)     │
└──────────────────┘

```

1. **word2md.py** – 利用 *mammoth* 将 Word 转 Markdown
2. **extract\_json.py** – 拼接 `SCHEMA_NOTE` 调用 DeepSeek，解析干净 JSON
3. **build\_kg.py** – 把实体/关系喂给 *networkx*，用 *pyvis* 生成全屏自适应图谱
4. **main.py** – 串联三步，打印进度与输出路径

---

## Configuration

* **SCHEMA\_NOTE**：位于 `extract_json.py` 顶部，可按业务修改实体 / 关系 schema
* **网络代理**：如公司网络需代理，请在 `call_llm.py` 内部注入 `proxies` 参数
* **视觉主题**：更换节点颜色或布局，只需改 `build_kg.py` 中 `Network(...)` 参数

---

