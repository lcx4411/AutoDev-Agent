# AutoDev-Agent 第二版 项目结构说明

```text
code-assistant-agent/
├── README.md                    # 项目说明文档
├── .gitignore                   # Git忽略文件
│
├── config/                     # 配置文件目录
│   ├── __init__.py
│   ├── config.yaml            # 主配置文件
│   ├── model_config.yaml      # 模型配置
│   └── prompt_templates.yaml  # 提示词模板
│
├── src/                        # 源代码目录
│   ├── __init__.py
│   ├── main.py                # 主入口文件
│   │
│   ├── cli/                # CLI接口
│   │   ├── __init__.py
│   │   ├── main.py     # CLI主程序
│   │
│   ├── core/                  # 核心逻辑
│   │   ├── __init__.py
│   │   ├── agent.py          # 主Agent类
│   │   ├── bugfix_agent.py   # 针对缺陷修复的Agent类
│   │   ├── plan_schema.py    # 任务结构定义（可拓展）
│   │   ├── planner.py        # 任务规划器
│   │   ├── code_generator.py # 代码生成器
│   │   ├── tester.py         # 测试生成器
│   │   ├── fixer.py          # Bug修复器
│   │   └── reflection.py     # 反思引擎
│   │ 
│   ├── evaluation/           # 评估模块
│   │   ├── __init__.py
│   │   ├── humaneval_eval.py     # humaneval代码生成评估
│   │   ├── mbpp_testgen_eval.py  # mbpp测试生成评估
│   │   └── swebench_fix_eval.py  # swebench代码修评估
│   │ 
│   ├── models/                # 模型相关
│   │   ├── __init__.py
│   │   ├── base_model.py     # 模型基类
│   │   └── qwen_model.py     # Qwen适配器
│   │
│   ├── tools/                 # 工具模块
│   │   ├── __init__.py
│   │   ├── base_tool.py      # 工具基类
│   │   └── python_repl.py    # Python执行器
│   │
│   ├── utils/                 # 工具函数
│   │   ├── __init__.py
│   │   ├── llm_utils.py      # LLM调用
│   │   └── config_utils.py   # 配置加载
│   
```

参考标准项目开发流程，构建规范的项目结构，便于后续开发与维护。已将第一版内容完成迁移。