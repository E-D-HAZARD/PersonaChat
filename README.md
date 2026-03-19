# PersonaChat (OpenClaw Skill)

基于 MBTI 人格字典和极简情绪关联推导的类人聊天话术生成引擎。它不仅仅是一套纯文本生成的 Python 框架代码，更是一个专门为 OpenClaw 等 AI Agent 平台设计的标准嵌套技能（Skill）。

## 🌟 核心特性
1. **情绪化推导调度**：不仅仅是盲目套用字符，它能基于传入的 `message` 上下文通过简单的关键词路由识别你的情绪（开心、难过、生气），并返回相匹配的语料及对应表情！
2. **极轻量容错装载**：不依赖庞大的数据与大模型，即使缺乏语料资源环境，也能自动降级（Fallback）运用系统内置的人格字典安全生成回复，拒接运行崩溃。
3. **支持 CLI 系统级嵌入**：为了兼容 Agent 的本地命令行工具操作习惯，我们提供了一句话直出的 CLI 调用。

---

## 🚀 安装指南

由于集成了支持 OpenClaw 生态的入口封装，推荐在你的环境中直接通过全局暴露 `personachat` 命令来进行拉取安装：

```bash
# 获取源码后，在项目根目录执行
pip install -r requirements.txt
pip install -e .
```

*如果你是作为 OpenClaw 工作区技能库，可以通过平台 `clawhub install` 命令加载 `_meta.json`。*

---

## 🛠️ 使用方法

### 方式一：作为 Agent 工具 (CLI 命令行调用)

安装完成后，你可以在系统的任何终端目录使用这个命令进行调度：

```bash
# 最简单的一句话聊天：
personachat "你好，今天真的太开心啦！" --persona ENFJ
# 终端将输出类似: "相信您一定可以的！🎉" (自动感知到了 happy 情绪关联表情)

# 使用完整的参数组合调用：
personachat "查一下余额谢谢" --persona INTJ --corpus banking --emotion neutral
```
**CLI 参数说明**
- `message` (可选)：用户对你说的话。脚本会从中萃取上下文匹配词以及基本的情感情感。
- `--persona`：MBTI 缩写 (如 `ENFJ`, `ENTP`, `ISTP` 等，详见下文)。默认为 `ENFJ`。
- `--corpus`：行业专用语料库指定（如 `banking` 银行业务, `medical` 医疗业务）。
- `--emotion`：若设定此值，将强行忽略 `message` 的感知，覆盖强制采用此处的情绪 (支持 `happy/sad/angry/neutral`)。

### 方式二：作为 Python 模块 (Python API)

如果在 Python 脚本或后端服务中，依旧保留了极其简单的随用即调代码：

```python
from persona import PersonaChat

chat = PersonaChat()

# 提供完整的 message 上下文生成
reply = chat.generate(message="怎么回事啊，太慢了！", persona="ENFJ")
print(reply)

# 便捷的单行函数
from persona import generate_reply
reply = generate_reply("收到", persona="ESFP", corpus="daily")
```

---

## 🎭 可用的人格预设 (Personas)
所有的预设可参考或自行修改 `data/personas.json`：
- **ENFJ** - 主人公 (温暖鼓励型)
- **ENTP** - 辩论家 (俏皮幽默型)
- **INFJ** - 提倡者 (温柔理解型)
- **INTJ** - 建筑师 (理性简洁型)
- **ESFP** - 表演者 (活泼热情型)
- **ISTP** - 鉴赏家 (冷静慵懒型)

*(注：如果指定 `persona="auto"`，系统会期待挂载至 OpenClaw Memory。若未检测到记忆模块环境，会自动友善降级为 `ENFJ`)*

## 🔬 本地化测试

项目不仅通过了完全静态类型的覆盖，也提供了长短句以及情感情境的路由测试，修改代码后可直接执行查验：

```bash
python test/test.py
```
