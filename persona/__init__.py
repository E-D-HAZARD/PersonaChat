"""
PersonaChat - 类人聊天风格回复系统
"""

import json
import random
from pathlib import Path
from typing import Optional, Dict, List, Any


class PersonaChat:
    """类人聊天风格回复生成器"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """初始化"""
        if data_dir is None:
            # 指向项目根目录的 data 文件夹
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        self.personas: Dict[str, Any] = {}
        self.corpus: Dict[str, Any] = {}
        self.emojis_map: Dict[str, List[str]] = {}
        
        # 加载人格定义
        try:
            with open(self.data_dir / "personas.json", "r", encoding="utf-8") as f:
                self.personas = json.load(f)
        except Exception as e:
            print(f"[{__name__}] Warning: Failed to load personas.json: {e}. Using fallback.")
            self.personas = {
                "ENFJ": {"name": "主人公", "prefix": ["没问题", "加油"], "emojis": ["💪", "❤️"]},
                "ENTP": {"name": "辩论家", "prefix": ["哈哈", "哎哟"], "emojis": ["😂", "🤔"]},
                "ESFP": {"name": "表演者", "prefix": ["太棒了", "哇"], "emojis": ["🎉"]},
                "ISTP": {"name": "鉴赏家", "prefix": ["嗯", "随便"], "emojis": ["😐"]},
                "INFJ": {"name": "提倡者", "prefix": ["我理解", "我懂"], "emojis": ["💜"]},
                "INTJ": {"name": "建筑师", "prefix": ["收到", "明白"], "emojis": ["🧠"]}
            }
        
        # 加载行业语料
        try:
            with open(self.data_dir / "corpus" / "industry.json", "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
        except Exception as e:
            print(f"[{__name__}] Warning: Failed to load corpus/industry.json: {e}")
            self.corpus = {}
            
        # 加载情绪表情映射
        try:
            with open(self.data_dir / "emojis.json", "r", encoding="utf-8") as f:
                self.emojis_map = json.load(f)
        except Exception as e:
            print(f"[{__name__}] Warning: Failed to load emojis.json: {e}")
            self.emojis_map = {}
    
    def generate(
        self, 
        message: str, 
        persona: str = "ENFJ", 
        corpus: Optional[str] = None,
        emotion: Optional[str] = None
    ) -> str:
        """
        生成类人回复
        
        Args:
            message: 用户消息
            persona: MBTI人格类型 (ENFJ/ENTP/INFJ/INTJ/ESFP/ISTP)
            corpus: 行业语料 (banking/medical/education)
            emotion: 情绪标签 (happy/sad/angry 等)
        
        Returns:
            str: 生成的回复
        """
        # 如果未提供情感，则通过关键词做极简的前置情感分析推断
        if not emotion and message:
            happy_words = ["开心", "哈哈", "棒", "好", "谢谢", "哇", "喜欢"]
            angry_words = ["生气", "太慢", "差", "投诉", "怎么回事", "气人"]
            sad_words = ["难过", "惨", "伤心", "心烦", "不行", "唉"]
            
            if any(w in message for w in happy_words):
                emotion = "happy"
            elif any(w in message for w in angry_words):
                emotion = "angry"
            elif any(w in message for w in sad_words):
                emotion = "sad"
            else:
                emotion = "neutral"

        # 识别和兼容 auto 人格
        if persona == "auto":
            import warnings
            warnings.warn("Memory module not connected. Falling back to ENFJ for 'auto' persona.", UserWarning)
            persona = "ENFJ"
            
        # 验证人格
        if persona not in self.personas:
            persona = "ENFJ"  # 默认
        
        # 获取人格配置
        persona_config = self.personas[persona]
        
        # 这里不再是无脑随机，加入基于 message 的初步匹配支持
        if corpus and corpus in self.corpus:
            examples = self.corpus[corpus]["examples"].get(persona, [])
            if examples:
                # 尝试找到和 message 有关键词碰撞的最佳句
                scored_examples: List[tuple] = []
                for ex in examples:
                    # 如果用户输入少于3个字，往往需要短句；如果长说明需要详情
                    len_diff = abs(len(ex) - len(message)) 
                    # 进行简单的相关性打分
                    score = sum(1 for char in message if char in ex) - (len_diff * 0.1)
                    scored_examples.append((score, ex))
                if scored_examples:
                    scored_examples.sort(reverse=True, key=lambda x: x[0])
                    # 取前两名进行随机，既有相关性又不至于死板
                    top_candidates = []
                    for i in range(min(2, len(scored_examples))):
                        top_candidates.append(scored_examples[i][1])
                    return random.choice(top_candidates)
                
                return random.choice(examples)
        
        # 使用通用模板生成
        return self._generate_from_template(persona_config, emotion)
    
    def _generate_from_template(
        self, 
        persona_config: Dict, 
        emotion: Optional[str] = None
    ) -> str:
        """从模板生成回复"""
        templates = persona_config.get("template", [])
        
        if not templates:
            # 基础组合：前缀 + 情绪emoji
            prefix = random.choice(persona_config.get("prefix", ["好"]))
            # 引入情绪对 emoji 的干预
            if emotion and emotion in self.emojis_map:
                emoji = random.choice(self.emojis_map[emotion])
            else:
                emoji = random.choice(persona_config.get("emojis", [""]))
            return f"{prefix}{emoji}"
        
        # 选择模板
        template = random.choice(templates)
        
        # 如果有 emotion，覆盖原有的静态 emoji 选择
        if emotion and emotion in self.emojis_map:
            emoji = random.choice(self.emojis_map[emotion])
        else:
            emoji = random.choice(persona_config.get("emojis", [""]))
        
        # 替换
        reply = template.replace("{emoji}", emoji)
        
        return reply
    
    def list_personas(self) -> List[str]:
        """列出所有可用人格"""
        return list(self.personas.keys())
    
    def list_corpus(self) -> List[str]:
        """列出所有可用行业语料"""
        return list(self.corpus.keys())
    
    def get_persona_info(self, persona: str) -> Dict:
        """获取人格详细信息"""
        return self.personas.get(persona, {})


def generate_reply(
    message: str, 
    persona: str = "ENFJ", 
    corpus: Optional[str] = None
) -> str:
    """便捷函数：生成回复"""
    chat = PersonaChat()
    return chat.generate(message, persona, corpus)


if __name__ == "__main__":
    # 测试
    chat = PersonaChat()
    
    print("可用人格:", chat.list_personas())
    print("可用语料:", chat.list_corpus())
    print()
    
    # 测试各种人格
    test_personas = ["ENFJ", "ENTP", "INFJ", "INTJ", "ESFP", "ISTP"]
    test_corpus = ["banking", "medical", "education"]
    
    for corpus in test_corpus:
        print(f"\n=== {corpus} ===")
        for p in test_personas:
            reply = chat.generate("我要转账", persona=p, corpus=corpus)
            print(f"{p}: {reply}")
