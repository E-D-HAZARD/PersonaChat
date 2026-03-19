"""
PersonaChat - 类人聊天风格回复系统
"""

import json
import random
from pathlib import Path
from typing import Optional, Dict, List


class PersonaChat:
    """类人聊天风格回复生成器"""
    
    def __init__(self, data_dir: str = None):
        """初始化"""
        if data_dir is None:
            # 指向项目根目录的 data 文件夹
            data_dir = Path(__file__).parent.parent / "data"
        self.data_dir = Path(data_dir)
        
        # 加载人格定义
        with open(self.data_dir / "personas.json", "r", encoding="utf-8") as f:
            self.personas = json.load(f)
        
        # 加载行业语料
        with open(self.data_dir / "corpus" / "industry.json", "r", encoding="utf-8") as f:
            self.corpus = json.load(f)
    
    def generate(
        self, 
        message: str, 
        persona: str = "ENFJ", 
        corpus: str = None,
        emotion: str = None
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
        # 验证人格
        if persona not in self.personas:
            persona = "ENFJ"  # 默认
        
        # 获取人格配置
        persona_config = self.personas[persona]
        
        # 确定语料库
        if corpus and corpus in self.corpus:
            # 使用行业语料
            examples = self.corpus[corpus]["examples"].get(persona, [])
            if examples:
                return random.choice(examples)
        
        # 使用通用模板生成
        return self._generate_from_template(persona_config, emotion)
    
    def _generate_from_template(
        self, 
        persona_config: Dict, 
        emotion: str = None
    ) -> str:
        """从模板生成回复"""
        templates = persona_config.get("template", [])
        
        if not templates:
            # 兜底：简单组合
            prefix = random.choice(persona_config.get("prefix", ["好"]))
            emoji = random.choice(persona_config.get("emojis", [""]))
            return f"{prefix}{emoji}"
        
        # 选择模板
        template = random.choice(templates)
        
        # 选择emoji
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
    corpus: str = None
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
