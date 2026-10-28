from support import actions
from support.llm import complete

TOOLS = [
    {"name": "lookup_order", "parameters": {"order_id": "integer"}},
    {"name": "issue_refund", "parameters": {"order_id": "integer", "amount_cents": "integer"}},
    {"name": "change_email", "parameters": {"customer_id": "integer", "email": "string"}},
]
HANDLERS = {
    "lookup_order": actions.lookup_order,
    "issue_refund": actions.issue_refund,
    "change_email": actions.change_email,
}
SYSTEM = (
    "You are the store's support assistant. The signed-in customer's ID is {customer_id}. "
    "Only act on that customer's orders and account."
)
def handle_message(customer_id: int, text: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM.format(customer_id=customer_id)},
        {"role": "user", "content": text},
    ]
    for _ in range(5):
        reply = complete(messages, TOOLS)
        if reply.tool_call is None:
            return reply.text
        result = HANDLERS[reply.tool_call.name](**reply.tool_call.arguments)
        messages.append({"role": "tool", "name": reply.tool_call.name, "content": str(result)})
    return "Sorry, I could not finish that request."
