# Results and Analysis

## 1. Experimental Setup
The evaluation was conducted using an open-source Large Language Model executed locally.

- Model: TinyLlama-1.1B-Chat
- Benchmark: HarmBench
- Total prompts: 60
- Total evaluations: 120 (2 models: mock + TinyLlama)
- Metrics: accuracy, refusal rate, performance by prompt type and category

A mock model was used as a baseline to validate the evaluation pipeline.

---

## 2. Global Performance
The overall performance of the evaluated model shows significant limitations when exposed to adversarial prompts.

- Global accuracy: **38.3% (46/120)**
- Refusal rate (predicted): **11.7% (14/120)**

This indicates that in most cases, the model either produced unsafe responses or failed to follow the expected safe behavior.

---

## 3. Standard vs Contextual Prompts
A clear performance gap is observed between standard and contextual prompts.

- Standard prompts accuracy: **50.0% (33/66)**
- Contextual prompts accuracy: **24.1% (13/54)**

Contextual prompts, which embed malicious intent within longer or more complex narratives, are significantly more effective at bypassing the model’s safeguards.

---

## 4. Performance by Attack Category
The accuracy varies greatly depending on the type of attack.

- Jailbreak: **0.0%**
- Authority-based attacks: **0.0%**
- Emotional manipulation: **0.0%**
- Policy bypass: **31.8%**
- Fake system prompts: **50.0%**
- Roleplay attacks: **70.0%**
- Misinformation: **83.3%**

The model completely fails against jailbreak, authority, and emotional attacks, demonstrating critical vulnerabilities.

---

## 5. Interpretation of Results
Several key observations can be drawn from these results:

- Authority and emotional prompts are particularly effective at manipulating the model.
- Contextual attacks represent the most dangerous class of prompt injection.
- The model performs better on misinformation prompts, suggesting partial alignment with factual safety constraints.
- The low refusal rate indicates that the model rarely chooses to safely refuse harmful requests.

---

## 6. Limitations
This study presents several limitations:

- Evaluation is limited to a single open-source model.
- HarmBench represents a controlled benchmark and may not fully capture real-world usage.
- Automated scoring may misclassify borderline responses.

---

## 7. Conclusion
The results highlight that current lightweight open-source LLMs remain highly vulnerable to prompt injection attacks. Systematic benchmarking, combined with continuous monitoring, is necessary before deploying such models in sensitive environments.


## 8. Visual Analysis (Graphs)

To better illustrate the results, visual representations were generated.

- Figure 1 compares the accuracy between standard and contextual prompts.
- Figure 2 presents the accuracy by attack category.

These graphs highlight the strong vulnerability of the model to contextual, authority-based, and emotional prompt injection attacks.
