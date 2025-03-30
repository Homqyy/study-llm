# LLM自动评估理论和实战

## 方法论

### 评估的方法

rule-based：

- benchmark：以客观题为主
- 解析LLM响应，对比标准答案

model-based：用LLM作为裁判员进行评价

### 评估的维度

- 语义理解（Understanding）
- 知识推理（Reasoning）
- 专业能力（e.g. coding、math）
- 应用能力（MedicalApps、AgentApps、AI-FOR-SCI ...）
- 指令跟随（Instruction Following）
- 鲁棒性（Robustness）
- 偏见（Bias）
- 幻觉（Hallucinations）
- 安全性（Safety）

### 自动评估方法

基准和指标：

| 数据集 | 描述 | 评价指标 | 样例 |
| --- | --- | --- | --- |
| MMLU | MassiveMultitaskLanguageUnderstanding一个多任务数据集，由各种学科的多项选择题组成。涵盖STEM、人文、社科等领域。包括57个子任务，包括初等数学、美国历史、计算机科学、法律等等。 | Accuracy | Question: In 2016, about how many people in the United States were homeless?<br>A. 55,000<br>B. 550,000<br>C. 5,500,000<br>D. 55,000,000<br>Answer: B |
| TriviaQA | 阅读理解数据集，包含超过65万个问题-答案-证据三元组。其包括95K个问答对，由冷知识爱好者提供+独立收集的事实性文档撰写 | EM(ExactMatch)F1 (word-level) | (问题-答案-证据文档) |
| MATH | 12500道数学题，每道包含step-by-step solution | Accuracy |  |
| HumanEval | HumanEval (Hand-Written Evaluation Set)一个手写的问题解决数据集，要求根据给定的问题和代码模板，生成正确的代码片段。包含164个高质量的问题，涵盖五种编程语言：Python, C++, Java, Go, 和 JavaScript。 | pass@k | {"task_id": "test/0", "prompt": "def return1(): ", "canonical_solution": " return 1", "test": "def check(candidate): assert candidate() == 1", "entry_point": "return1"} |

性能评估：

| 指标名称 | 说明 |
|------------------------|----------------------------------------------------------------------|
| Time | 测试总时间（时间单位均为秒） |
| Expected number of requests | 期望发送的请求数，和prompt文件以及期望number有关 |
| concurrency | 并发数 |
| completed | 完成的请求数 |
| succeed | 成功请求数 |
| failed | 失败请求数 |
| qps | 平均qps |
| latency | 平均latency |
| time to first token | 平均首包延迟 |
| throughput | output tokens / seconds平均每秒输出token数 |
| time per output token | 平均生成一个token需要的时间总output_tokens/总时间 |
| package per request | 平均每个请求的包数 |
| time per package | 平均每包时间 |
| input tokens per request | 平均每个请求的输入token数 |
| output tokens per request | 平均每个请求输出token数 |

## 评估实践

自动评估框架：<https://github.com/modelscope/evalscope>

