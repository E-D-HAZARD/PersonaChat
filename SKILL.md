---
name: personachat
description: 基于 MBTI 及大语言模型情感推断的类人聊天引擎 (原生支持 OpenClaw Memory)
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["personachat"]},"env":["OPENAI_API_KEY","OPENAI_BASE_URL"]}}
---

# PersonaChat Skill

> 使用原生接入 LLM 与 Memory RAG 技术，能够根据语境感知并渲染情感的聊天风格处理器

## 设计初衷
当纯净的信息获取已经能由各大功能性 Agent 完成时，`PersonaChat` 能够在输出流末端为机器人赋予带有强烈“私人性格”与“历史回忆感”的沟通能力，让冰冷的终端交互更有“人味”。

## 平台级生态适配

### 大模型网络与参数支持
只要系统主环境拥有 `OPENAI_API_KEY` 或任意基于 OpenAI 标准协议的接口配置（含 Ollama 本地化部署等 `OPENAI_BASE_URL`），它将自动拉起模型去分析用户的字里行间并结合特有性格出词。
安全断网特性：如果无 API 支持，内部拥有完美的纯本地字典降级算法，无需额外配置，程序永不报错。

### OpenClaw Memory 联动
只需要一行简单的终端指令，它会智能向上探查所有工作区父级目录并截获 `MEMORY.md`（或手动 `memory_dir` 挂载）：

```bash
personachat "我要休假" --persona auto
# 会智能分析 Memory 中关于用户的记录（比如 Alex 您的职位与姓名）
# 辅以大模型的理解给出一句符合人设的温馨调侃...
```

## 数据配置替换支持
您不仅可以使用强悍的大模型驱动，还可以修改原本作为保命备份包位于 `data/` 下的文件作为企业或个人的快捷语料缓存地：
- `personas.json` - MBTI人格模板极其性格短句集
- `emojis.json` - 情绪映射图表
- `corpus/` - 特定领域（如医疗服务）垂直语料

这三者在无网络或无模型模式下同样极好地保障了程序的下限生成能力。
