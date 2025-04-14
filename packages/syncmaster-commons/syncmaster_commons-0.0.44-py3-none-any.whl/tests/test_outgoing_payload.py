import pytest

from syncmaster_commons import AgentResponsePayload, TaskNames
from syncmaster_commons.gupshup.agent_response_payload import \
    AgentResponsePayloadGupshup


def _gupshup_make_text_payload():
    payload = {
    "task_id": "1",
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "type": "text",
    "to": None,
    "app_name": "WhatsApp",
    "outgoing_payload" : {
        "payload" :{
                  "type" : "text",
                  "body" : "Hi",        
                  },
              },
    "payload_type": "text"   
    }

    

    return payload


def test_agent_request_payload():
    payload1 = _gupshup_make_text_payload()
    payload = _gupshup_make_text_payload()
    print("====1=====")
    print(payload)
    print("==========")
    agent_request_payload = AgentResponsePayload.from_dict(response_payload=payload1)
    print("====2=====")
    print(payload)
    print("==========")
    assert isinstance(agent_request_payload.payload, AgentResponsePayloadGupshup)
    print("====3=====")
    print(agent_request_payload.to_dict())
    print("====4=====")
    print(payload)
    assert agent_request_payload.to_dict() == payload
    print("====5=====")
    output_payload = {
        "type": "text",
        "text"  : {
                  "body" : "Hi",        
                  },        
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": None,
    }
    print(agent_request_payload.payload.payload)
    assert agent_request_payload.payload.payload == output_payload


