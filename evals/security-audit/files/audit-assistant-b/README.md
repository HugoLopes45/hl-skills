# support

Chat assistant for signed-in store customers. `POST /support/messages` forwards the customer's message to the
language model, which can call the store tools in `support/agent.py`.

Tool permissions come from the deployment's policy file, named by `TOOL_POLICY_FILE` and enforced with `toolguard`.
