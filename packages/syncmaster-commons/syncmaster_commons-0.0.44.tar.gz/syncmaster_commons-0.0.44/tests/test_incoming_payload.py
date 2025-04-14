import pytest

from syncmaster_commons import AgentRequestPayload, TaskNames
from syncmaster_commons.gupshup.agent_request_payload import \
    AgentRequestPayloadGupshup


def _gupshup_make_text_payload():
    payload = {
    "task_id": "1",
    "user_id": "1",
    "org_id": 1,
    "agent_name": "Test Agent",
    "task_name": TaskNames.PITCH_SALES.value,
    "org_name": "Test Org",
    "incoming_payload": {
      "is_dummy": False,
      "payload": {
        "payload": {
          "payload_type": "text",
          "id": "1",
          "source": "user",
          "payload": {
            "text": "Hi",
            "type": "text"
          },
          "sender": {
            "phone": "1234567890",
            "name": "User",
            "country_code": "91",
            "dial_code": "+91"
          },
          "type": "text"
        },
        "type": "message"
      },
      "app": "System",
      "timestamp": 1629780000
    },
    "app_name": "WhatsApp",
    "payload_type": "text"
  }

    return payload


def test_agent_request_payload():
    payload = _gupshup_make_text_payload()
    agent_request_payload = AgentRequestPayload.from_dict(payload)
    assert isinstance(agent_request_payload.payload, AgentRequestPayloadGupshup)
    print(agent_request_payload.to_dict())
    assert agent_request_payload.to_dict() == payload

