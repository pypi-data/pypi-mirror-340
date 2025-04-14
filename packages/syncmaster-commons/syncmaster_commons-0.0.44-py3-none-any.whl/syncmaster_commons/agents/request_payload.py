from typing import Any, Union, override

from syncmaster_commons.abstract.baseclass import (
    SMBaseClass, ThirdPartyPayloadConsumedByAgent)
from syncmaster_commons.gupshup.agent_request_payload import \
    AgentRequestPayloadGupshup


class AgentRequestPayload(SMBaseClass):
    """
    AgentRequestPayload class is responsible for handling the payload associated with an agent's request. 
    It provides various properties to access specific attributes of the payload and methods to convert 
    the payload to and from a dictionary representation.
    Attributes:
        payload (Union[ThirdPartyPayloadConsumedByAgent, AgentRequestPayloadGupshup]): The payload associated with the agent's request.
    Properties:
        app_name (str): Returns the name of the application that the payload is associated with.
        org_id (int): Returns the organization id.
        user_id (str): Returns the user id.
        task_id (int): Returns the task id.
        task_name (str): Returns the task name.
        org_name (str): Returns the organization name.
        messages (dict): Returns the messages.
    Methods:
        to_dict(): Provides a dictionary representation of the current instance, extracted from the dictionary returned by the parent class.
        from_dict(request_payload: dict, client: str = None) -> "AgentRequestPayload": Creates an AgentRequestPayload object from a dictionary.
    """
    payload: Union[ThirdPartyPayloadConsumedByAgent,AgentRequestPayloadGupshup]

    @property
    def app_name(self) -> str:
        """
        Returns the name of the applicatio that the payload is associated with.
        """
        return self.payload.app_name

    @property
    def org_id(self) -> int:
        """
        Returns the organization id.
        """
        return self.payload.org_id
    
    @property
    def user_id(self) -> str:
        """
        Returns the user id.
        """
        return self.payload.user_id
    
    @property
    def task_id(self) -> int:
        """
        Returns the task id.
        """
        return self.payload.task_id
    
    @property
    def task_name(self) -> str:
        """
        Returns the task name.
        """
        return self.payload.task_name
    
    @property
    def org_name(self) -> str:
        """
        Returns the organization name.
        """
        return self.payload.org_name
    
    @property
    def messages(self) -> dict:
        """
        Returns the messages.
        """
        return self.payload.payload.get("messages", None)
    
    
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
    def from_dict(cls,request_payload: dict, client:str = None) -> "AgentRequestPayload":
        """
        Creates a AgentRequestPayload object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            AgentRequestPayload: The AgentRequestPayload object created from the dictionary.
        """
        app_name = request_payload.get("app_name", None)
        if client == "WhatsApp" or app_name == "WhatsApp":
            payload = AgentRequestPayloadGupshup.from_dict(request_payload) 
        else:
            raise ValueError(f"Client {client} is not supported.")
        return cls(
            payload=payload,
        )