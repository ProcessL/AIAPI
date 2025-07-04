from langchain_openai import ChatOpenAI
import tiktoken

def estimate_tokens(text, model="deepseek-chat"):
    """估算文本的token数量"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        # 使用简单的估算方法作为备选
        return len(text) / 4

def generate_result(messages):
    # 配置 DeepSeek LLM
    llm = ChatOpenAI(
        openai_api_base="https://api.deepseek.com/v1",
        openai_api_key="sk-22df05dbda344a35830fb0e9f76a052b",
        model="deepseek-chat",
        temperature=0.7
    )

    # 估算输入token
    prompt_tokens = 0
    for message in messages:
        prompt_tokens += estimate_tokens(str(message.content))

    # 使用流式输出
    full_comment = ""
    for chunk in llm.stream(messages):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            full_comment += chunk.content
    
    # 估算输出token
    completion_tokens = estimate_tokens(full_comment)
    total_tokens = prompt_tokens + completion_tokens
    
    # 打印token使用情况
    print(f"\n\n使用了大约{total_tokens}个token (输入: {prompt_tokens}, 输出: {completion_tokens})")
    
    return full_comment, total_tokens