# MinAgent

Agent is a wrapper on top of OpenAI chat completion and assistant API.
It handles `tool_call`, `file_search` within the class

## Features

Implemented

- Chat Completion API
- Assistant API

And tools

- Function call (Parallel execution)
- File search

## Usage

```
pip install minagent
```

### Create an Agent

```python
from openai import OpenAI
from minagent import Agent

openai_client = OpenAI(
    api_key="00000"
)

def current_utc_datetime(**args) -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()

clock = Agent(
    openai_client,
    name='clock',
    model='gpt-4o',
    instructions=['You are a time aware assistant.',],

    # optional: only add below if using assistant api
    openai_asst_id='asst_0000'

    # optional: tool for file_search, and function
    tools=[
        {
            'type': 'file_search',
        }, {
            'type': 'function',
            'function': {"name": 'current_utc_datetime'},
        },
    ],
    tool_functions={'current_utc_datetime': current_utc_datetime},
    tool_resources={'file_search': {'vector_store_ids': ['vs_0000']}},
)
```

### Use of Chat completion API

```python
response = clock.chat_completion(
    user='john',
    messages=[
        { 'role': 'user', 'content': 'what time is it now?' },
    ],
)
```

### Use of Assistant API

```python
thread = openai_client.beta.threads.create()
response = clock.ask_assistant(
    user='john',
    asst_thread_id=thread.id,
    message=[
        { 'role': 'user', 'content': 'what time is it now?' },
    ]
)
```

## Future

- Support for Response API
- Add test cases
- Release pipeline
