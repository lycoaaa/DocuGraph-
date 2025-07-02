import os, json, time, math, requests
from typing import List, Dict

# 基本参数
API_URL      = "https://api.deepseek.com/v1/chat/completions"
MODEL_NAME   = "deepseek-chat"
API_KEY      = os.getenv("DEEPSEEK_API_KEY", "").strip() or "YOUR_KEY" # 可直接填写 API KEY
TIMEOUT      = 300            # 单次请求超时（秒）
CHUNK_LEN    = 1000           # prompt 超长拆分阈值（按字符近似，不必太精确）
MAX_RETRIES  = 5              # 最多重试次数
BACKOFF_BASE = 2              # 指数退避基数

if not API_KEY:
    raise EnvironmentError("请先设置环境变量 DEEPSEEK_API_KEY")

def _split_prompt(text: str, limit: int = CHUNK_LEN) -> List[str]:
    """按字符长度切块，返回分段列表"""
    return [text[i : i + limit] for i in range(0, len(text), limit)]

# 底层请求
def _post_with_retry(payload: Dict) -> Dict:
    headers = {"Authorization": f"Bearer {API_KEY}",
               "Content-Type":  "application/json"}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(API_URL, headers=headers,
                                 json=payload, timeout=TIMEOUT, stream=True)
            resp.raise_for_status()

            # 手动按块读取，避免一次性加载 & “premature end”
            raw = b"".join(chunk for chunk in resp.iter_content(8192) if chunk)
            return json.loads(raw.decode())

        except (requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
                json.JSONDecodeError) as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"DeepSeek 请求连续失败 {MAX_RETRIES} 次：{e}") from None
            wait = BACKOFF_BASE ** attempt
            print(f"第 {attempt}/{MAX_RETRIES} 次失败，{wait}s 后重试…")
            time.sleep(wait)

# 主函数：外部仅调用这一层即可
def call_local_llm(prompt: str,
                   temperature: float = 0.2,
                   max_tokens: int = 4096) -> str:

    if not prompt.strip():
        raise ValueError("prompt 不能为空")

    parts = _split_prompt(prompt)

    sys_msg = {"role": "system",
               "content": "你是一名专业的结构信息抽取智能体。"}
    user_msgs = [
        {"role": "user",
         "content": f"【段 {idx+1}/{len(parts)}】\n{part}"}
        for idx, part in enumerate(parts)
    ]
    messages = [sys_msg] + user_msgs

    # DeepSeek
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False        # 禁用流式，拿一次性完整 JSON
    }
    data = _post_with_retry(payload)

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"DeepSeek 返回字段缺失：{data}")
