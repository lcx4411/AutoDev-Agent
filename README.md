# 大模型原理与技术作业仓库 - 第一版

---

## 一、整体架构设计

### 系统目标

构建一个 **AI 驱动的软件开发助手（Dev-Agent）**，支持：

* 需求理解（自然语言 → 开发任务）
* 码生成（函数 / 文件级）
* 单元测试自动生成
* Bug 定位与修复（基于错误信息或失败测试）
* 反思与迭代优化（Self-Reflection）

---

### 系统架构

```
        ┌──────────────┐
        │   用户需求   │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Task Planner │ ← 需求理解 / 任务拆解
        └──────┬───────┘
               ↓
     ┌─────────┴─────────┐
     ↓                   ↓
Code Generator     Test Generator
     ↓                   ↓
┌──────────────┐   ┌──────────────┐
│ 代码执行环境  │←→ │ 单元测试运行 │
└──────┬───────┘   └──────┬───────┘
       ↓                  ↓
   Error Trace      Test Failure
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Bug Fix Agent│ ← 反思 + 修复
        └──────────────┘
```

---

## 二、数据准备

### 使用数据集

| 数据集                | 用途       | 对应功能               |
|--------------------|----------|--------------------|
| **HumanEval**      | 函数级代码生成  | 验证 Code Generation |
| **MBPP**           | 带测试的简单任务 | 验证 Test Generation |
| **SWE-Bench Lite** | Bug 修复   | 验证 Bug Fix Agent   |

> 这里直接调用HuggingFace上的数据集

---

## 三、模型选择

### 1️⃣ 基础模型

| 模型                       | 用途            |
|--------------------------|---------------|
| **Qwen3-Coder-7B / 14B** | 代码生成 + Bug 修复 |
| DeepSeek-Coder-6.7B      | 轻量快速          |

> 在第一版中，目前只使用 Qwen3-Coder，因为其在代码生成任务上表现优异且支持多种编程语言。

---

### 2️⃣ 推理方式

* **Prompt + Tool-Calling**

---

## 四、核心 Agent 设计

### 1️⃣ Task Planner

**输入：**

```
需求：实现一个字符串压缩函数
```

**输出（结构化）：**

```json
{
  "task_type": "code_generation",
  "language": "python",
  "steps": [
    "理解函数语义",
    "生成函数实现",
    "生成测试用例",
    "执行并验证"
  ]
}
```

---

### 2️⃣ Code Generator Agent

**Prompt 模板**：

```text
You are a professional software developer.
Task:
{task_description}

Function signature:
{signature}

Requirements:
- Follow Python best practices
- Handle edge cases
- Do not include test code
```

---

### 3️⃣ Test Generator Agent

**Prompt 模板**：

```text
Given the following function specification and implementation,
generate Python unit tests using assert statements.

Focus on:
- Edge cases
- Invalid inputs
- Typical cases
```

---

### 4️⃣ Bug Fix Agent（SWE 核心）

**Prompt 模板**：

```text
The following code fails some tests.

Code:
{code}

Error:
{error_trace}

Please:
1. Analyze the root cause
2. Propose a fix
3. Output the corrected code
```

---

## 五、反思与迭代机制

### Self-Reflection Prompt

**Prompt 模板**：

```text
The previous attempt failed.

Analyze:
- Why did it fail?
- What assumptions were wrong?
- How should the solution be improved?
```

### 迭代流程

```python
for step in range(max_iter):
    code = generate_code()
    tests = generate_tests()
    result = run_tests(code, tests)
    if result.success:
        break
    code = fix_bug(code, result.error)
```

---

## 六、系统实现

在第一版中目前只实现了模拟数据流，后续版本会逐步完善各个 Agent 的调用和数据流转。

## 七、评估方案

### 指标设计

| 任务              | 指标     |
| --------------- | ------ |
| Code Generation | Pass@1 |
| Test Generation | 覆盖率    |
| Bug Fix         | 修复成功率  |
| Agent           | 平均迭代次数 |

---

### 示例结果

待实现

---

## 六、下一版任务

1. 完善各 Agent 的实现细节。
2. 完成各个 Agent 任务的评价指标计算。
3. 将各个 Agent 任务分隔开，可以单独实现。
4. 完成CLI工具的实现，方便用户交互使用。

