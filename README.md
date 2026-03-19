# PersonaChat (OpenClaw Skill)

基于 MBTI 人格设定字典、大语言模型驱动与 OpenClaw 记忆外挂的类人聊天话术生成引擎。它是一个完美适配于各大平台 Agent 的标准智能组件。

## 🌟 核心突破特性
1. **大语言模型赋能 (LLM Driven)**：无需硬编码词条！只要配置了通用 `OPENAI_API_KEY`，系统会自动将 MBTI 人设信息转换为 `System Prompt`，生成自然、多变、极具人格色彩的一线对话回复！
2. **连接 OpenClaw 记忆库 (RAG & Memory)**：支持使用 `--persona auto` 指令或者显式传入 `--memory-dir` 进行向上扫描搜寻工作区中的 `MEMORY.md`。让你的 AI 机器人精准记得你的昵称与禁忌！
3. **极强生存降级能力 (Graceful Fallback)**：即使在断网状态下或是没有配置大模型密钥，它也不会让进程崩溃！系统会退回一套基于关键词和字长碰撞的内置容错 JSON 随机生成器，依旧能顺滑匹配你的 `emotion`。

---

## 🚀 安装指南

由于集成了支持 OpenClaw 生态的入口封装，极其推荐你在环境中直接进行全局安装挂载：

```bash
# 获取源码后，在项目根目录执行
pip install -r requirements.txt
pip install -e .
```

*若作为 OpenClaw 工作区的技能库，可以通过平台 `clawhub install` 命令自动读取 `_meta.json` 挂载。*

---

## 🛠️ 使用方法

### 方式一：终端命令行工具 (CLI 调用) - **推荐**

安装完毕后，在任意控制台均可直接使用：

**场景 1：基础闲聊与情绪覆盖**
```bash
personachat "你好，今天真的太开心啦！" --persona ENFJ
# 若未配置大模型，自动降级触发容错，匹配开心相关的 Emoji： "相信您一定可以的！🎉"
```

**场景 2：[全量态] 自动挂载记忆并请求大模型**
```bash
# 前置准备：配置环境变量
export OPENAI_API_KEY="sk-xxxx"
export OPENAI_BASE_URL="选填：如 http://localhost:11434/v1 支持本地或代理"

# 利用 auto 模式搜寻 Memory.md 并输出：
personachat "我今天实验跑完了！" --persona auto
# 输出: "Alex 真的太棒了！🎉 您的科研进展我很为您开心，赶快将数据存好休息一下吧！"
```

**CLI 参数字典**
- `message` (可选)：用户对你说的话。
- `--persona`：MBTI 缩写 (如 `ENFJ`, `ENTP` 等)。如果设为 `auto` 则开启上下文挂载记忆库及偏好继承。
- `--memory-dir`：强制指定查找 `MEMORY.md` 的根路径，不设则逐级往系统上层扫。
- `--corpus`：行业专用语料库指定（仅限降级在本地容错模版时生效）。
- `--emotion`：若设定此值，覆盖强制采用此处的情绪 (支持 `happy/sad/angry/neutral`)。

### 方式二：作为 Python 组件内嵌 (Python API)
在您的外部调度脚本里：

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-xxx"

from persona import PersonaChat

chat = PersonaChat()
reply = chat.generate(message="怎么回事啊，太慢了！", persona="ENFJ", memory_dir="../")
print(reply)
```

---

## 🎭 可用的人格预设 (Personas)
内涵极强扩展性，直接修改 `data/personas.json` 或 `emojis.json` 即可自创 AI 人设：
- **ENFJ** - 主人公 (温暖鼓励型)
- **ENTP** - 辩论家 (俏皮幽默型)
- **INTJ** - 建筑师 (理性简洁型)
... 等等。

## 🔬 测试

项目囊括了完整的情感情境降级路由以及模型请求容错测试。
```bash
python test/test.py
```
