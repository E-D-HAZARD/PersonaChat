# PersonaChat

类人聊天风格回复系统 - OpenClaw Skill

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```python
from persona import PersonaChat

chat = PersonaChat()

# 指定人格
reply = chat.generate("你好", persona="ENFJ")

# 指定行业语料
reply = chat.generate("我要转账", persona="ENFJ", corpus="banking")

# 便捷函数
from persona import generate_reply
reply = generate_reply("谢谢", persona="ESFP")
```

## 人格

- **ENFJ** - 主人公 (温暖鼓励型)
- **ENTP** - 辩论家 (俏皮幽默型)
- **INFJ** - 提倡者 (温柔理解型)
- **INTJ** - 建筑师 (理性简洁型)
- **ESFP** - 表演者 (活泼热情型)
- **ISTP** - 鉴赏家 (冷静慵懒型)

## 行业/场景语料

- banking (银行)
- medical (医疗)
- education (教育)
- **daily (日常聊天)**

## 测试

```bash
python test/test.py
```
