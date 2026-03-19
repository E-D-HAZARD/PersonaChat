import argparse
from persona import PersonaChat

def main():
    parser = argparse.ArgumentParser(description="PersonaChat CLI: 像人类一样对话回复")
    parser.add_argument("message", type=str, nargs="?", default="", help="用户输入的聊天内容")
    parser.add_argument("--persona", type=str, default="ENFJ", help="MBTI人格基调 (如 ENFJ, ENTP)")
    parser.add_argument("--corpus", type=str, default=None, help="专用行业语料库选择 (如 banking, medical)")
    parser.add_argument("--emotion", type=str, default=None, help="强制指定情绪基调而非通过 message 检测 (如 happy, sad, angry)")
    
    args = parser.parse_args()
    
    # 极简地调用生成功能并通过 std_out 返回
    try:
        chat = PersonaChat()
        reply = chat.generate(
            message=args.message, 
            persona=args.persona, 
            corpus=args.corpus,
            emotion=args.emotion
        )
        print(reply)
    except Exception as e:
        print(f"Error executing PersonaChat: {e}")

if __name__ == "__main__":
    main()
