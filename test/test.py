"""
PersonaChat 测试
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from persona import PersonaChat


def test_basic():
    """基础测试"""
    chat = PersonaChat()
    
    print("=" * 50)
    print("基础测试")
    print("=" * 50)
    
    # 测试人格列表
    print(f"\n可用人格: {chat.list_personas()}")
    print(f"可用语料: {chat.list_corpus()}")
    
    # 测试生成
    message = "你好"
    for persona in chat.list_personas():
        reply = chat.generate(message, persona=persona)
        print(f"{persona}: {reply}")


def test_corpus():
    """行业语料测试"""
    chat = PersonaChat()
    
    print("\n" + "=" * 50)
    print("行业语料测试")
    print("=" * 50)
    
    test_corpus = ["banking", "medical", "education"]
    test_message = "我要转账"
    
    for corpus in test_corpus:
        print(f"\n--- {corpus} ---")
        for persona in ["ENFJ", "ENTP", "ISTP"]:
            reply = chat.generate(test_message, persona=persona, corpus=corpus)
            print(f"{persona}: {reply}")


def test_message_relevance():
    """测试基于上下文和情绪的情境推断"""
    chat = PersonaChat()
    
    print("\n" + "=" * 50)
    print("上下文与情绪感知测试")
    print("=" * 50)
    
    messages = [
        "太棒了，谢谢你！",            # 走 happy 情绪并配发合适 emoji
        "怎么回事，太慢了我要投诉",    # 走 angry
        "心情有点难过唉",              # 走 sad
    ]
    
    for msg in messages:
        reply = chat.generate(msg, persona="ENFJ")
        print(f"用户: {msg}")
        print(f"回复: {reply}\n")


def test_auto_persona():
    """测试 auto 人格及异常处理"""
    chat = PersonaChat()
    
    print("\n" + "=" * 50)
    print("Auto 人格及兜底测试")
    print("=" * 50)
    
    reply = chat.generate("你好", persona="auto")
    print(f"提示中应有 Warning，自动回落-> {reply}")


def test_persona_info():
    """人格信息测试"""
    chat = PersonaChat()
    
    print("\n" + "=" * 50)
    print("人格信息")
    print("=" * 50)
    
    for persona in ["ENFJ", "INTJ", "ISTP"]:
        info = chat.get_persona_info(persona)
        print(f"\n{persona} ({info.get('name', '')}):")
        print(f"  风格: {info.get('style', '')}")
        print(f"  特点: {', '.join(info.get('traits', []))}")


if __name__ == "__main__":
    test_basic()
    test_corpus()
    test_message_relevance()
    test_auto_persona()
    test_persona_info()
    print("\n✅ 所有测试完成!")
