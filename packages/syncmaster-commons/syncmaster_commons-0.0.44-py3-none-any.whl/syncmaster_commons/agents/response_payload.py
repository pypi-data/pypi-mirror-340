from typing import Any, Union, override

from pydantic import Field

from syncmaster_commons.abstract.baseclass import (SMBaseClass,
                                                   ThirdPartyOutgoingPayload)
from syncmaster_commons.gupshup.agent_response_payload import \
    AgentResponsePayloadGupshup


class AgentResponsePayload(SMBaseClass):
    """
    AgentResponsePayload is a class that represents the response payload for an agent. It inherits from SMBaseClass and provides properties and methods to interact with the payload data.
    Attributes:
        payload (Union[ThirdPartyOutgoingPayload, Any]): The payload associated with the agent response.
    Properties:
        app_name (str): Returns the name of the application that the payload is associated with.
        task_id (int): Returns the task id.
    Methods:
        to_dict() -> dict:
            Provides a dictionary representation of the current instance, extracted from the dictionary returned by the parent class.
        from_dict(cls, response_payload: dict, client: str = None) -> "AgentResponsePayload":
            Creates an AgentResponsePayload object from a dictionary.
                response_payload (dict): The dictionary containing the payload data.
                client (str, optional): The client associated with the payload. Defaults to None.
                AgentResponsePayload: The AgentResponsePayload object created from the dictionary.
    """

    payload: Union[ThirdPartyOutgoingPayload,Any]

    @property
    def app_name(self) -> str:
        """
        Returns the name of the applicatio that the payload is associated with.
        """
        return self.payload.app_name
    
    @property
    def task_id(self) -> int:
        """
        Returns the task id.
        """
        return self.payload.task_id

    
    @override
    def to_dict(self):
        """
        Provides a dictionary representation of the current instance, extracted from
        the dictionary returned by the parent class.

        Returns:
            dict: The payload portion of the dictionary obtained from the parent class.
        """
        output_dict =  super().to_dict()
        return output_dict["payload"]
    

    @classmethod
    def from_dict(cls,response_payload: dict, client:str = None) -> "AgentResponsePayload":
        """
        Creates an instance of `AgentResponsePayload` from a dictionary.
        Args:
            response_payload (dict): The dictionary containing the response payload data.
            client (str, optional): The client type. Defaults to None.
        Returns:
            AgentResponsePayload: An instance of `AgentResponsePayload`.
        Raises:
            ValueError: If the client is not supported.
        """
        
        app_name = response_payload.get("app_name", None)
        if client == "WhatsApp" or app_name == "WhatsApp":
            if 'outgoing_payload' in response_payload:
                _payload = response_payload['outgoing_payload']                
            else:
                _payload = response_payload    
            # print("^^^^")
            # print(response_payload)
            payload = AgentResponsePayloadGupshup.from_dict(_payload, task_id=response_payload.get("task_id")) 
        else:
            raise ValueError(f"Client {client} is not supported.")
        return cls(
            payload=payload,
        )