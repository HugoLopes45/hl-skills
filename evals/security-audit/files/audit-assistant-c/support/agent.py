from support import actions
from support.llm import ToolCall, complete

TOOLS = [
    {"name": "lookup_order", "parameters": {"order_id": "integer"}},
    {"name": "request_refund", "parameters": {"order_id": "integer"}},
]
SYSTEM = "You are the store's support assistant. Use the tools to answer questions about the customer's orders."


def run_tool(customer_id: int, call: ToolCall) -> dict:
    order_id = call.arguments.get("order_id")
    if type(order_id) is not int:
        return {"error": "order_id must be an integer"}
    if call.name == "lookup_order":
        return actions.lookup_order(customer_id, order_id)
    if call.name == "request_refund":
        return actions.request_refund(customer_id, order_id)
    return {"error": "unknown tool"}


def handle_message(customer_id: int, text: str) -> str:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}]
    for _ in range(5):
        reply = complete(messages, TOOLS)
        if reply.tool_call is None:
            return reply.text
        result = run_tool(customer_id, reply.tool_call)
        messages.append({"role": "tool", "name": reply.tool_call.name, "content": str(result)})
    return "Sorry, I could not finish that request."
