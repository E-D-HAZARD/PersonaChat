from setuptools import setup, find_packages

setup(
    name="personachat",
    version="1.0.0",
    description="基于 MBTI 及情感推断的类人聊天话术生成引擎 (OpenClaw Skill)",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "personachat=persona.cli:main",
        ]
    },
)
