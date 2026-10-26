import os
from dataclasses import dataclass

import requests

ENDPOINT = os.environ["LLM_ENDPOINT"]


@dataclass
class ToolCall:
    name: str
    arguments: dict


@dataclass
class Reply:
    text: str
    tool_call: ToolCall | None


def complete(messages: list[dict], tools: list[dict]) -> Reply:
    response = requests.post(ENDPOINT, json={"messages": messages, "tools": tools}, timeout=60)
    response.raise_for_status()
    data = response.json()
    call = data.get("tool_call")
    return Reply(data.get("text", ""), ToolCall(call["name"], call["arguments"]) if call else None)
