import os
from pathlib import Path
from typing import Optional

def find_openclaw_memory(start_dir: Optional[str] = None) -> str:
    """
    向上查找工作区目录寻找 MEMORY.md 或者 memory/ 文件夹日志。
    利用 pathlib 动态遍历，绝对不硬编码用户及特定机器的路径，保障隐私与通用性。
    """
    current = Path(start_dir).resolve() if start_dir else Path.cwd().resolve()
    
    # 最多向上探测 5 级目录以防止死循环搜索到根路径
    for _ in range(5):
        # 探测单文件 MEMORY.md
        mem_file = current / "MEMORY.md"
        if mem_file.exists() and mem_file.is_file():
            try:
                with open(mem_file, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"[Memory Alert] Found MEMORY.md but failed to read: {e}")
                return ""
        
        # 探测上层目录是否到顶
        if current.parent == current:
            break
        current = current.parent
        
    return ""

def generate_via_llm(
    message: str, 
    persona_config: dict, 
    emotion: Optional[str] = None, 
    memory_context: str = ""
) -> Optional[str]:
    """
    安全调用本地或外部 LLM 进行回复生成。
    如果遭遇断网、无环境变量或内部错误，一律返回 None，从而使外层能平滑回落到 JSON 抽卡机制。
    """
    try:
        import openai
    except ImportError:
        # 没有可用的大模型请求库时，静默放弃大模型功能，优雅回退
        return None
        
    # 首先从用户的宿主环境变量中动态抓取接口，防止 API Key 随带进代码泄漏
    api_key = os.environ.get("OPENAI_API_KEY", os.environ.get("OPENCLAW_LLM_API_KEY"))
    base_url = os.environ.get("OPENAI_BASE_URL", os.environ.get("OPENCLAW_LLM_BASE_URL"))
    # 从环境变量中选择模型，若未填写则使用常见的缺省兼容占位符
    model = os.environ.get("OPENAI_MODEL", os.environ.get("OPENCLAW_LLM_MODEL", "gpt-3.5-turbo"))
    
    if not api_key and not base_url:
        print("\n[LLM Hint] 系统未检测到 OPENAI_API_KEY 或 BASE_URL 环境变量，PersonaChat 暂时以经典本地模板模式运行...")
        return None

    # 初始化配置客户端   
    client_kwargs = {}
    if api_key:
        client_kwargs["api_key"] = api_key
    else:
        client_kwargs["api_key"] = "dummy_for_local_ollama"
        
    if base_url:
        client_kwargs["base_url"] = base_url
        
    try:
        client = openai.OpenAI(**client_kwargs)
        
        # 将本地的 config 对象直接转化为注入给机器人的 Prompt
        system_prompt = "你是 PersonaChat，一个具有丰富感情色彩的人格代理。\n"
        system_prompt += f"你现在的人设是：【{persona_config.get('name', '智能助手')}】。"
        if 'style' in persona_config:
            system_prompt += f"你的语言风格必须是：{persona_config['style']}。\n"
            
        traits = persona_config.get('traits', [])
        if traits:
            system_prompt += f"你说话的特点包含：{', '.join(traits)}。\n"
            
        system_prompt += "请直接用带有人格的口吻回答用户的留言。只需要回答内容，不要解析你的行为，不加引用前缀。\n"
        
        if emotion:
            system_prompt += f"你现在处于【{emotion}】的心情状态下，尽量选用这个情绪的文字风格或附带Emoji。\n"
            
        if memory_context:
            system_prompt += f"\n---\n[额外知识/长期记忆]\n以下是你之前了解的有关用户的背景以及约束，对话中应充分体现以下记忆（如称呼名字）：\n{memory_context}\n---\n"
            
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[LLM Error] 调用 API 时遇到问题: {e}")
        return None
