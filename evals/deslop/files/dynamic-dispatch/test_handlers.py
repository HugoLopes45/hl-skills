import json

import handlers


def test_every_configured_action_dispatches():
    for action in json.load(open("actions.json")):
        assert handlers.dispatch(action, [1, 2])
