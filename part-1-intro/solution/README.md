# Part 1 Solution - Reference Implementation

This directory contains a complete, working implementation of the Part 1 exercise.

## What's Implemented

### ✅ Agent Initialization

- Loads environment variables from `.env` file
- Imports BedrockModel from `strands.models`
- Creates BedrockModel instance with Nova Lite model ID
- Configures region as eu-central-1
- Creates Strands Agent with BedrockModel
- Sets up agent with system prompt

### ✅ Terminal Loop (Pre-implemented)

The terminal loop is **already complete** in both starter and solution code:

- Interactive command-line interface
- Handles user input and agent responses
- Supports exit commands (`exit`, `quit`, `bye`)
- Graceful error handling
- Keyboard interrupt handling (Ctrl+C)
- Empty input validation

## Running the Solution

```bash
cd part-1-intro/solution

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up AWS credentials via Teleport
# Copy the export commands provided by Teleport and run them:
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_CA_BUNDLE="/path/to/ca-bundle.pem"
export HTTPS_PROXY="http://127.0.0.1:port"

# Run the agent
python agent.py
```

## Key Learning Points

### 1. BedrockModel Configuration

```python
from strands.models import BedrockModel

# Create BedrockModel instance
bedrock_model = BedrockModel(
    model_id="us.amazon.nova-lite-v1:0",
    region_name="eu-central-1",
)
```

### 2. Agent Creation

```python
from strands import Agent

# Configure agent with BedrockModel
agent = Agent(
    model=bedrock_model,
    system_prompt="You are a helpful AI assistant."
)
```

### 3. Terminal Loop (Pre-implemented)

```python
# This is already complete in the starter code
def terminal_loop(agent):
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        response = agent(user_input)
        print(f"Agent: {response}")
```

### 3. Best Practices Demonstrated

- Using Strands native BedrockModel integration
- No need for manual boto3 client setup
- AWS credentials handled automatically via Teleport environment variables
- Clean code structure with separate functions
- User-friendly terminal interface (pre-implemented)
- Graceful shutdown handling

## Differences from Starter Code

The starter code includes:

- Complete imports structure (commented out as TODOs)
- Empty `initialize_agent()` function with TODO instructions
- **Complete and working** `terminal_loop()` function
- Complete `main()` function
- All supporting files (.env.example, requirements.txt, .gitignore)

The solution adds:

- Uncommented imports (`Agent`, `BedrockModel`)
- Full implementation of `initialize_agent()`:
  - BedrockModel instance creation
  - Agent configuration with model and system_prompt
  - Return statement with configured agent
- Working conversation loop in `terminal_loop()`
- Comprehensive error handling
- User-friendly messages and formatting
- Input validation

## Next Steps

After reviewing this solution:

1. Compare with your implementation
2. Test edge cases (empty input, invalid API key, etc.)
3. Experiment with different agent instructions
4. Try modifying the conversation flow
5. Prepare for Part 2: Memory & Tools

## Common Questions

**Q: Why use `agent.run()` instead of other methods?**  
A: `run()` is the simplest method for single-turn interactions. Later sessions will explore more advanced methods.

**Q: How can I customize the agent's behavior?**  
A: Modify the `instructions` parameter when creating the ABedrock model available in eu-central-1 (e.g., other Nova models, Claude modelsities.

**Q: What if I want to use a different model?**  
A: Change the `MODEL` variable in your `.env` file to any OpenAI model (e.g., `gpt-4`, `gpt-3.5-turbo`).

---

Need help? Compare your code line-by-line with this solution and identify the differences!
