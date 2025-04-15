# 🧠 Hive Intelligence Python SDK

The Hive Intelligence SDK lets you integrate real-time crypto and Web3 intelligence directly into your Python applications using simple prompt or message-based inputs.

## 🚀 Installation

Install the SDK and its dependencies using Poetry:

```bash
poetry add hive-intelligence 
```

Or with `pip` (if you're not using Poetry):

```bash
pip install hive-intelligence 
```

## 🔑 Setup

Set your Hive API key as an environment variable:

```bash
export HIVE_API_KEY=your_api_key_here 
```

On Windows CMD:

```cmd
set HIVE_API_KEY=your_api_key_here 
```

## 🧪 Example Usage

```python
import os
from hive_intelligence.client import HiveSearchClient
from hive_intelligence.types import HiveSearchRequest, HiveSearchMessage

# Get API key from environment
api_key = os.environ.get("HIVE_API_KEY")
if not api_key:
    raise ValueError("Please set the HIVE_API_KEY environment variable")

# Initialize the client
client = HiveSearchClient(api_key=api_key)

# 🟡 Example 1: Prompt-based query
prompt_request = HiveSearchRequest(
    prompt="What is the current price of Ethereum?"
)
response = client.search(prompt_request)
print("Prompt Response:", response.model_dump())

# 🟢 Example 2: Chat-style query
chat_request = HiveSearchRequest(
    messages=[
        HiveSearchMessage(role="user", content="Price of"),
        HiveSearchMessage(role="assistant", content="Price of what?"),
        HiveSearchMessage(role="user", content="BTC")
    ]
)
response = client.search(chat_request)
print("Chat Response:", response.model_dump())
```

## 📘 Request Options

- `prompt`: Plaintext question or query
- `messages`: For chat-style interaction
- Optional tuning parameters:
  - `temperature`: (e.g. 0.7) randomness of response
  - `top_k`: max tokens considered
  - `top_p`: nucleus sampling
  - `include_data_sources`: show source info

## ❗ Error Handling

The SDK raises `HiveSearchAPIError` for API errors with status code, message, and full response body.
