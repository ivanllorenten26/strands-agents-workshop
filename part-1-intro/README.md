# Part 1: Introduction to Agents

Welcome to the first session of the Strands Agents Workshop! In this session, you'll learn the fundamentals of agent-based systems and get hands-on experience building your first agent.

## 📚 Learning Objectives

By the end of this session, you will:

- ✅ Understand what an agent is and how it works
- ✅ Learn about the Strands framework and its core concepts
- ✅ Understand the agent execution loop
- ✅ Build and run a basic agent locally
- ✅ Interact with your agent through a terminal-based UI

## 🎯 What is an Agent?

An **agent** is an autonomous software entity that:

- Perceives its environment through inputs
- Makes decisions based on its goals and available information
- Takes actions to achieve specific objectives
- Learns and adapts from interactions

Unlike traditional programs that follow fixed instructions, agents can reason, plan, and make dynamic decisions based on context.

## 🌊 What is Strands?

**Strands** is a powerful framework for building intelligent agents that:

- Provides high-level abstractions for agent development
- Handles the complexity of agent orchestration
- Offers built-in memory management
- Supports tool integration and custom capabilities
- Enables scalable multi-agent systems

## 🔄 The Agent Loop

The agent loop is the core execution cycle that every agent follows:

```
1. Receive Input → 2. Process/Reason → 3. Take Action → 4. Observe Result → [Repeat]
```

**Key components:**

- **Perception**: Agent receives input from users or environment
- **Reasoning**: Agent analyzes the situation using its capabilities and memory
- **Action**: Agent executes tools, generates responses, or triggers workflows
- **Learning**: Agent updates its state and memory based on outcomes

## 🛠️ Session Structure

### `/starter` Directory

Contains minimal boilerplate code to help you get started. You'll build upon this code during the hands-on exercises.

### `/solution` Directory

Contains a complete, working implementation that you can reference if you get stuck or want to compare your approach.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access in eu-central-1 region
- Teleport access configured for AWS credentials
- Bedrock Nova Lite model enabled in your AWS account

### Setup Instructions

1. Navigate to the starter directory:

```bash
cd part-1-intro/starter
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

4. Set up AWS credentials via Teleport:

```bash
# Use Teleport to get temporary AWS credentials
# Copy the export commands provided by Teleport and run them:
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_CA_BUNDLE="/path/to/ca-bundle.pem"
export HTTPS_PROXY="http://127.0.0.1:port"
```

5. Review the starter code and understand the basic structure

6. Follow along with the instructor to implement the missing pieces (look for TODOs in `agent.py`)

### Running Your First Agent

```bash
python agent.py
```

The agent will start an interactive terminal session where you can chat with it. Type `exit` or `quit` to end the conversation.

## 📖 Key Concepts to Explore

### Agent Configuration

- Setting up agent parameters
- Defining agent goals and capabilities
- Configuring the execution environment

### Terminal UI

- Building an interactive loop in Python
- Handling user input and agent responses
- Managing conversation flow

### Basic Agent Operations

- Initializing an agent
- Processing user queries
- Generating responses
- Graceful shutdown

## 💊 Knowledge Pill: BedrockModel Configuration

The `BedrockModel` class accepts many configuration parameters that allow you to fine-tune the model behavior. Here's a comprehensive reference:

### Constructor Parameters

| Parameter            | Type      | Description                                               |
| -------------------- | --------- | --------------------------------------------------------- |
| `model_id`           | `str`     | The Bedrock model ID (e.g., `"us.amazon.nova-lite-v1:0"`) |
| `region_name`        | `str`     | AWS region for Bedrock service (default: `"us-west-2"`)   |
| `boto_session`       | `Session` | Custom boto3 Session for AWS credentials                  |
| `boto_client_config` | `Config`  | Botocore config for retries, timeouts, etc.               |
| `endpoint_url`       | `str`     | Custom endpoint URL for VPC/PrivateLink                   |

### Generation Parameters

| Parameter        | Type        | Description                                                                       |
| ---------------- | ----------- | --------------------------------------------------------------------------------- |
| `temperature`    | `float`     | Controls randomness (0.0-1.0). Higher = more creative, lower = more deterministic |
| `top_p`          | `float`     | Nucleus sampling parameter. Alternative to temperature for controlling diversity  |
| `max_tokens`     | `int`       | Maximum number of tokens to generate in the response                              |
| `stop_sequences` | `list[str]` | Sequences that will stop generation when encountered                              |
| `streaming`      | `bool`      | Enable/disable streaming responses (default: `True`)                              |

### Caching Parameters

| Parameter      | Type          | Description                                                                                |
| -------------- | ------------- | ------------------------------------------------------------------------------------------ |
| `cache_config` | `CacheConfig` | Configuration for prompt caching. Use `CacheConfig(strategy="auto")` for automatic caching |
| `cache_tools`  | `str`         | Cache point type for tools                                                                 |
| `cache_prompt` | `str`         | _(Deprecated)_ Use `cache_config` instead                                                  |

### Guardrails Parameters

| Parameter                          | Type   | Description                                                |
| ---------------------------------- | ------ | ---------------------------------------------------------- |
| `guardrail_id`                     | `str`  | ID of the Bedrock guardrail to apply                       |
| `guardrail_version`                | `str`  | Version of the guardrail                                   |
| `guardrail_trace`                  | `str`  | Trace mode: `"enabled"`, `"disabled"`, or `"enabled_full"` |
| `guardrail_stream_processing_mode` | `str`  | Processing mode: `"sync"` or `"async"`                     |
| `guardrail_redact_input`           | `bool` | Redact input if guardrail triggers (default: `True`)       |
| `guardrail_redact_input_message`   | `str`  | Custom message when input is redacted                      |
| `guardrail_redact_output`          | `bool` | Redact output if guardrail triggers (default: `False`)     |
| `guardrail_redact_output_message`  | `str`  | Custom message when output is redacted                     |
| `guardrail_latest_message`         | `bool` | Send only latest user message to guardrails                |

### Advanced Parameters

| Parameter                         | Type             | Description                                         |
| --------------------------------- | ---------------- | --------------------------------------------------- |
| `additional_request_fields`       | `dict`           | Additional fields to include in the Bedrock request |
| `additional_response_field_paths` | `list[str]`      | Additional response field paths to extract          |
| `include_tool_result_status`      | `bool \| "auto"` | Include status field in tool results                |

### Example: Advanced Configuration

```python
from strands import Agent
from strands.models import BedrockModel
from botocore.config import Config as BotocoreConfig

# Create custom boto config for retries and timeouts
boto_config = BotocoreConfig(
    retries={"max_attempts": 3, "mode": "standard"},
    connect_timeout=5,
    read_timeout=60
)

# Create a fully configured Bedrock model
bedrock_model = BedrockModel(
    model_id="us.amazon.nova-lite-v1:0",
    region_name="eu-central-1",
    temperature=0.7,
    max_tokens=2048,
    top_p=0.9,
    streaming=True,
    boto_client_config=boto_config,
)

agent = Agent(model=bedrock_model)
```

### Runtime Configuration Updates

You can update model configuration at runtime using `update_config()`:

```python
# Update temperature for more creative responses
bedrock_model.update_config(temperature=0.9)

# Switch to a different model
bedrock_model.update_config(model_id="us.amazon.nova-pro-v1:0")
```

> 📚 **Reference**: [BedrockModel API Documentation](https://strandsagents.com/latest/documentation/docs/api-reference/python/models/bedrock/)

## 💊 Knowledge Pill: Anatomy of an Agent

An agent in Strands is more than just a model wrapper. Here's a visual overview of all the components you can configure:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              🤖 STRANDS AGENT                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   🧠 Model  │  │ 📝 System   │  │ 🔧 Tools    │  │ 📊 Structured       │ │
│  │             │  │   Prompt    │  │             │  │    Output           │ │
│  │ BedrockModel│  │             │  │ @tool       │  │                     │ │
│  │ OpenAI      │  │ Personality │  │ functions   │  │ Pydantic models     │ │
│  │ Anthropic   │  │ & behavior  │  │ & actions   │  │ for typed responses │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ 💾 State    │  │ 🔄 Session  │  │ 🪝 Hooks    │  │ 💬 Conversation     │ │
│  │             │  │ Management  │  │             │  │    Management       │ │
│  │ Persistent  │  │             │  │ Lifecycle   │  │                     │ │
│  │ data across │  │ Save/load   │  │ callbacks   │  │ Message history     │ │
│  │ invocations │  │ agent state │  │ & events    │  │ & context window    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quick Reference

| Component                   | Purpose                                  | We'll Cover In  |
| --------------------------- | ---------------------------------------- | --------------- |
| **Model**                   | The LLM that powers the agent            | Part 1 (today!) |
| **System Prompt**           | Defines personality and behavior         | Part 1 (today!) |
| **Tools**                   | Actions the agent can perform            | Part 2          |
| **State**                   | Persistent data across invocations       | Part 2          |
| **Session Management**      | Save and restore agent conversations     | Part 2          |
| **Hooks**                   | Lifecycle callbacks for observability    | Part 5          |
| **Structured Output**       | Type-safe responses with Pydantic        | Part 3          |
| **Conversation Management** | Control message history & context window | Part 2          |

### Minimal Agent (Today)

```python
agent = Agent(
    model=bedrock_model,
    system_prompt="You are a helpful assistant."
)
```

### Full-Featured Agent (Preview)

```python
agent = Agent(
    model=bedrock_model,
    system_prompt="You are a helpful assistant.",
    tools=[my_tool, another_tool],
    state={"user_preferences": {}},
    conversation_manager=SlidingWindowConversationManager(window_size=10),
    hooks=[LoggingHook(), MetricsHook()],
)
```

> 💡 **Don't worry!** In this first session we'll focus only on **Model** and **System Prompt**. We'll explore the other components in upcoming sessions.

## ✏️ Exercises

During this session, you'll complete the following exercises:

1. **Create a Basic Agent**: Set up a minimal agent that can respond to simple queries
2. **Implement the Terminal Loop**: Build an interactive command-line interface
3. **Add Conversation Flow**: Enable multi-turn conversations with your agent
4. **Handle Edge Cases**: Implement proper error handling and exit conditions

## 🔗 Helpful Resources

- [Strands Documentation](https://strandsagents.com/latest/documentation/docs/)
- [Agent Fundamentals](https://strandsagents.com/latest/documentation/docs/fundamentals)
- [Getting Started Guide](https://strandsagents.com/latest/documentation/docs/getting-started)

## 🎓 Next Steps

After completing this session:

- Experiment with different agent configurations
- Try modifying the terminal UI with additional features
- Explore the Strands documentation for advanced concepts
- Move on to Part 2: Agent Memory & Tools

## ❓ Common Issues

### Agent doesn't start

- Check that Strands is properly installed
- Verify your Python version (3.8+)
- Ensure all dependencies are installed

### Terminal loop crashes

- Check for proper error handling
- Verify input validation
- Review the solution code for comparison

### Import errors

- Activate your virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

---

**Questions?** Ask your instructor or check the solution code for reference!

Happy coding! 🚀
