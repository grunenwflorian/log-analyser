import pytest

from log_analyzer.steps import Action, ActionType, ActionsReifier


class FakeAction(Action):
    def __init__(self, name="DummyAction", action_type=ActionType.PROVIDER):
        Action.__init__(self, name, action_type)


def test_creating_action_register_it():
    dummy_action = FakeAction()
    assert dummy_action.name in ActionsReifier._actions
    assert FakeAction in ActionsReifier._actions.values()


def test_provider_reification():
    dummy_action = FakeAction("FileProvider")
    reifier = ActionsReifier({"file": "./logs.log"})

