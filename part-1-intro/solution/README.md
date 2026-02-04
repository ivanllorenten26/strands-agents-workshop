# Part 1 Solution - Reference Implementation

This directory contains a complete, working implementation of the Part 1 exercise.

## What's Implemented

### ✅ Agent Initialization

- Loads environment variables from `.env` file
- Creates AWS Bedrock client for eu-central-1 region
- Configures Strands agent with Bedrock Nova Lite model
- Falls back to AWS CLI credentials if not in .env
- Sets up agent with custom instructions

### ✅ Terminal Loop

- Interactive command-line interface
- Handles user input and agent responses
- Supports exit commands (`exit`, `quit`, `bye`)
- Graceful error handling
- Keyboard interrupt handling (Ctrl+C)

### ✅ Error Handling

- Missing API key validation
- Empty input handling
- Runtime error management
- Helpful error messages

## Running the Solution

```bash
cd part-1-intro/solution

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your AWS credentials
# Or use: aws configure (if using AWS CLI)

# Run the agent
python agent.py
```

## Key Learning Points

### 1. Agent Configuration

# Create Bedrock client

bedrock_client = boto3.client(
'bedrock-runtime',
region_name='eu-central-1'
)

# Configure agent with Bedrock

agent = Agent(
name="Workshop Assistant",
instructions="Your agent's role and behavior",
model="us.amazon.nova-lite-v1:0",
client=bedrock_clientini",
api_key=api_key
)

````

### 2. Basic Agent Loop
```python
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
  AWS Bedrock client configuration
- Fallback to AWS CLI credentials
-       break
    response = agent.run(user_input)
    print(f"Agent: {response}")
````

### 3. Best Practices Demonstrated

- Environment variable management with `p and boto3
- AWS Bedrock client initialization
- Full implementation of `initialize_agent()` with Bedrock
- Clean code structure with functions
- User-friendly terminal interface
- Graceful shutdown handling

## Differences from Starter Code

The solution includes:

- Complete imports from Strands framework
- Full implementation of `initialize_agent()`
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
