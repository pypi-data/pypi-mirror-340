
from typing import Optional, override

from syncmaster_commons.abstract.baseclass import ThirdPartyOutgoingPayload
from syncmaster_commons.gupshup.outgoing_payloads import GupshupOutgoingPayload


class AgentResponsePayloadGupshup(ThirdPartyOutgoingPayload):
    """
    AgentResponsePayloadGupshup is a class that represents the payload for agent responses in the Gupshup integration.
    Attributes:
        outgoing_payload (GupshupOutgoingPayload): The outgoing payload object.
        task_id (str): The unique identifier for the task.

    Properties:
        app_name (str): Returns the name of the application.
        payload_type (str): Returns the incoming payload’s payload type.
        payload (dict): Constructs and returns the payload dictionary.
    Methods:
        from_dict(cls, payload_dict: dict) -> "AgentResponsePayloadGupshup":
    """
    outgoing_payload: GupshupOutgoingPayload
    to: Optional[str] = None

    @property
    def messaging_product(self) -> str:
        """
        Returns the messaging product of the outgoing payload.

        :return: The messaging product.
        :rtype: str
        """
        return "whatsapp"
    
    @property
    def recipient_type(self) -> str:
        """
        Returns the recipient type of the outgoing payload.

        :return: The recipient type.
        :rtype: str
        """
        return "individual"
    
    
    
    @property
    def app_name(self) -> str:
        """
        Returns the name of the application.

        :return: The string 'gupshup'.
        :rtype: str
        """
        return self.outgoing_payload.app_name
    
    @property
    def payload_type(self) -> str:
        """
        Returns the incoming payload’s payload type.

        This property retrieves the type of the payload contained within the incoming payload,
        providing insight into how the payload should be processed or interpreted.

        Returns:
            str: The type of the payload.
        """
        return self.outgoing_payload.payload.type_text
    
    @property
    def type(self) -> str:
        """
        Returns the type of the outgoing payload.

        :return: The type of the outgoing payload.
        :rtype: str
        """
        return self.payload_type



    @property
    def payload(self) -> dict:
        """
        Constructs and returns the payload dictionary.
        This method retrieves the payload from the incoming payload object,
        converts it to a dictionary, and adds the payload type to the dictionary.
        Returns:
            dict: The payload dictionary with an added payload type.
        """
       
        payload = self.outgoing_payload.payload
        output_dict = {} 
        output_dict["type"] = self.payload_type
        _payload_dict = payload.to_dict()
        _payload_dict.pop("type")
        output_dict[self.payload_type] = _payload_dict
        output_dict["to"] = self.to
        output_dict["messaging_product"] = self.messaging_product
        output_dict["recipient_type"] = self.recipient_type
        if not self.type == "text":
            raise NotImplementedError("Only text type is supported")
        return output_dict

    @classmethod
    def from_dict(cls, payload_dict: dict, task_id: str) -> "AgentResponsePayloadGupshup":
        """
        Creates an instance of AgentResponsePayloadGupshup from a dictionary.
        Args:
            cls: The class itself.
            payload_dict (dict): A dictionary containing the payload data.
        Returns:
            AgentResponsePayloadGupshup: An instance of the class populated with data from the dictionary.
        Raises:
            KeyError: If 'task_id', 'user_id', or 'org_id' keys are missing in the payload_dict.
        """
        
        outgoing_payload = GupshupOutgoingPayload.from_dict(payload_dict)
        print("###")
        print(outgoing_payload)
        return cls(
            outgoing_payload=outgoing_payload,
            task_id=task_id
        )
    
    @override
    def to_dict(self):
        """
        Converts the object to a dictionary representation.
        This method converts the object to a dictionary representation, including the `type`,
        `recipient_type`, `messaging_product`, and `to` fields.
        Returns:
            dict: A dictionary containing the object's data, including the type,
                  recipient_type, messaging_product, and to fields.
        """
        _d:dict  = super().to_dict()
        _d["type"] = self.type
        _d["recipient_type"] = self.recipient_type
        _d["messaging_product"] = self.messaging_product
        _d["to"] = self.to
        return _d