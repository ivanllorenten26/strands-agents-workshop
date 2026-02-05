# Part 2: Agent Memory & Tools


## 📚 Learning Objectives

By the end of this session, you will:

- ✅ Understand what an agent is and how it works
- ✅ Learn about the Strands framework and its core concepts
- ✅ Understand the agent execution loop
- ✅ Build and run a basic agent locally
- ✅ Interact with your agent through a terminal-based UI



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
cd part-2-memory-tools/starter
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
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

### Running Your Agent

```bash
python agent.py
```

The agent will start an interactive terminal session where you can chat with it. Type `exit` or `quit` to end the conversation.

## 📖 Key Concepts to Explore

