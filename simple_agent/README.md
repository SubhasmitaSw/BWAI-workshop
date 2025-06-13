# Create a virtual environment

```bash
    python -m venv .venv
    # Activate (each new terminal)
    # macOS/Linux: source .venv/bin/activate
    # Windows CMD: .venv\Scripts\activate.bat
    # Windows PowerShell: .venv\Scripts\Activate.ps1
```

# Install dependencies

```bash
    pip install google-adk
    pip install ollama # if you don't have any other llm apikey available
    pip install litellm # if you want to use litellm as a client for ollama or other litellm supported models
```

# You will need to have a folder structure like this:

```
    parent_folder/
     agent_name/
        __init__.py
        agent.py
        .env
```

# Setup with ollama 

```bash
    ollama list # List models available locally to you
    ollama show <model name> # Show details of a specific model, make sure they have support for tools
    ollama run <model name> # run the model of your choice

```

# run the weather agent with adk

```bash
    adk run <point to the directory of the agent source code> # for interactive cli 
    adk web # for web interface
```