def handle_import(payload):
    return {"imported": len(payload)}


def dispatch(action, payload):
    return globals()["handle_" + action](payload)
