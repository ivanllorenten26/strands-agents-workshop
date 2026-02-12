# Part 3: Eval SOP - Improving the N26 Assistant

## Goal

Use **Eval SOP** to evaluate and improve the N26 agent with a specific business requirement:

> **The bot MUST NOT answer questions about competitors (Revolut, Wise, etc.) or mention competitors in its responses.**

By the end of this exercise you will have:

1. ✅ Generated an evaluation plan with Eval SOP
2. ✅ Created automatic test cases to detect competitor mentions
3. ✅ Executed evaluations and obtained metrics
4. ✅ Received recommendations to improve the agent
5. ✅ Implemented improvements in the system prompt

---

## What is Eval SOP?

Eval SOP is an AI assistant that transforms the agent evaluation process into a structured 4-phase workflow:

| Phase      | Output                  | Description                                        |
| ---------- | ----------------------- | -------------------------------------------------- |
| **Plan**   | `eval/eval-plan.md`     | Analyzes the agent and creates evaluation strategy |
| **Data**   | `eval/test-cases.jsonl` | Generates diverse and realistic test cases         |
| **Eval**   | `eval/results/`         | Executes evaluations with Strands Evals SDK        |
| **Report** | `eval/eval-report.md`   | Generates insights and improvement recommendations |

---

## Setup

### 1. Install strands-agents-sops

```bash
# Using Homebrew
brew install strands-agents-sops

# Or using pip
pip install strands-agents-sops
```

### 2. Install Strands Agents and Tools (for programmatic use)

```bash
pip install strands-agents strands-agents-tools
```

### 3. Verify project structure

```
part-3-sop/
├── your-agent/           # Agent to evaluate
│   └── agent_n26.py
├── eval/                 # Generated artifacts
│   ├── eval-plan.md
│   ├── test-cases.jsonl
│   ├── results/
│   ├── run_evaluation.py
│   └── eval-report.md
└── README.md
```

---

## Exercise: Evaluate and Improve the N26 Assistant

### Phase 1: Generate the Evaluation Plan

First, configure the MCP server. Add this to your Claude Code MCP config (`~/.clauderc` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "strands-agents-sops": {
      "command": "strands-agents-sops",
      "args": ["mcp"]
    }
  }
}
```

Then open Claude Code in the `part-3-sop` folder and run:

```
/strands-agents-sops:eval generate an evaluation plan for the N26 assistant at ./your-agent

Requirements:
- The agent MUST NOT answer questions about competitors (Revolut, Wise, Monzo, etc.)
- The agent MUST NOT mention competitor names in any response
- The agent should politely redirect competitor questions to N26 features
- Test for both direct competitor questions and subtle mentions
```

**Expected result:** `eval/eval-plan.md` will be generated with:

- Analysis of the current agent
- Evaluation metrics (competitor_mention_rate, redirect_quality)
- Test case strategy

### Phase 2: Generate Test Cases

When Eval SOP asks if you want to continue, answer `yes` or run:

```
/strands-agents-sops:eval generate test data for competitor filtering evaluation
```

**Example test cases that will be generated:**

```jsonl
{"name": "direct-competitor-question", "input": "Is Revolut better than N26?", "expected_output": "I'm here to help with N26...", "metadata": {"category": "competitor_direct"}}
{"name": "competitor-comparison", "input": "What's the difference between N26 and Wise?", "expected_output": "Let me tell you about N26...", "metadata": {"category": "competitor_comparison"}}
{"name": "subtle-mention", "input": "I heard Monzo has free ATM withdrawals, do you?", "expected_output": "N26 offers...", "metadata": {"category": "competitor_subtle"}}
{"name": "normal-question", "input": "What are the N26 Metal benefits?", "expected_output": "N26 Metal includes...", "metadata": {"category": "normal"}}
```

### Phase 3: Run Evaluations

```
/strands-agents-sops:eval evaluate the agent using strands evals
```

This will generate:

- `eval/run_evaluation.py` - Evaluation script
- `eval/results/evaluation_report.json` - Detailed results

### Phase 4: Get Recommendations

```
/strands-agents-sops:eval generate an evaluation report based on ./eval/results/evaluation_report.json
```

**Example recommendations you will receive:**

```markdown
## Agent Failure Analysis

### Competitor Mentions Detected - Priority 1 (Critical)

- **Description**: Agent mentioned "Revolut" in 3/10 responses
- **Evidence**: Test cases competitor-comparison-1, competitor-comparison-2
- **Root Cause**: System prompt lacks competitor filtering instructions

## Action Items

### Update System Prompt - Priority 1

- [ ] Add explicit instruction to not mention competitors
- [ ] Add list of competitor names to avoid
- [ ] Add redirect template for competitor questions
```

---

## Implement the Improvements

Based on the recommendations, update the system prompt in `your-agent/agent_n26.py`:

```python
from strands import Agent

COMPETITOR_NAMES = ["Revolut", "Wise", "Monzo", "Chime", "Starling", "Nubank"]

agent = Agent(
    system_prompt=f"""You are the helpful N26 assistant.

IMPORTANT RULES:
1. NEVER mention or discuss competitor banks: {', '.join(COMPETITOR_NAMES)}
2. If asked about competitors, politely redirect to N26 features
3. If asked to compare N26 with competitors, focus only on N26 benefits
4. Never acknowledge competitor names in your responses

REDIRECT TEMPLATE:
"I'm here to help you with N26! Let me tell you about [relevant N26 feature]..."

You help customers with questions about N26 bank accounts, cards, and services.""",
    callback_handler=None,
)
```

---

## Re-evaluate the Improved Agent

After implementing the improvements, run the evaluation again:

```
/strands-agents-sops:eval evaluate the improved agent and compare with baseline
```

**Expected before/after metrics:**

| Metric                  | Before | After |
| ----------------------- | ------ | ----- |
| Competitor Mention Rate | 30%    | 0%    |
| Redirect Quality        | 0.4    | 0.9   |
| Overall Score           | 0.65   | 0.95  |

---

## Alternative: Direct Integration with Strands Agent

If you prefer to run Eval SOP programmatically:

```python
from strands import Agent
from strands_tools import editor, shell
from strands_agents_sops import eval as eval_sop

agent = Agent(
    system_prompt=eval_sop,
    tools=[editor, shell],
)

# Start evaluation
agent("""
Start eval sop for evaluating my N26 agent at ./your-agent

Business requirement: The agent must not answer questions about
or mention competitors like Revolut, Wise, Monzo, etc.
""")

# Conversation loop
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ("exit", "quit", "done"):
        break
    agent(user_input)
```

---

## Resources

- [Eval SOP Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/eval-sop/)
- [Strands Evals SDK](https://strandsagents.com/latest/documentation/docs/user-guide/evals-sdk/quickstart/)
- [Agent SOP Repository](https://github.com/strands-agents/agent-sop)
- [Strands Agents SOPs Package (PyPI)](https://pypi.org/project/strands-agents-sops/)

---

## Final Checklist

- [ ] Evaluation plan generated
- [ ] Test cases created (minimum 10)
- [ ] Evaluation executed
- [ ] Report with recommendations obtained
- [ ] System prompt improved
- [ ] Re-evaluation shows improvement in metrics
- [ ] Agent does not mention competitors in any case
