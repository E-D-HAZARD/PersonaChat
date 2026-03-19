# PersonaChat Skill

> 类人聊天风格回复系统

## 功能

基于MBTI人格的类人聊天回复生成

## 人格类型

- **ENFJ** (主人公) - 温暖鼓励型
- **ENTP** (辩论家) - 俏皮幽默型
- **INFJ** (提倡者) - 温柔理解型
- **INTJ** (建筑师) - 理性简洁型
- **ESFP** (表演者) - 活泼热情型
- **ISTP** (鉴赏家) - 冷静慵懒型

## 使用方法

### 基本调用

```python
from persona import PersonaChat

chat = PersonaChat()
reply = chat.generate("今天天气真好", persona="ENFJ")
# 输出: "哇！今天天气真的很好呀！心情也跟着好起来了呢🎉"
```

### 指定行业

```python
reply = chat.generate("我要转账", persona="ENFJ", corpus="banking")
# 输出: "好的，马上帮您处理~💪"
```

### 自动识别人格

```python
reply = chat.generate("你好呀", persona="auto")
# 根据用户历史自动选择人格
```

## 配置

人格和语料定义在 `data/` 目录下：
- `personas.json` - MBTI人格定义
- `corpus/` - 行业语料库

## 触发场景

当用户表达：
- 希望聊天更有"人味"
- 需要特定风格回复
- 需要情感化客服回复
