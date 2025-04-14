from typing import override  # type: ignore

from syncmaster_commons.abstract.baseclass import OutgoingPayload, SMBaseClass

# https://docs.gupshup.io/docs/whatsapp-message-type-outbound-free-form


class PayloadGenerator(SMBaseClass):
    """
    PayloadGenerator class inherits from SMBaseClass and represents the payload for outgoing messages.

    Attributes:
        type_text (str): A property that should be implemented in subclasses to return the type of the payload as text.

    Methods:
        from_dict(cls, payload_dict: dict) -> "PayloadGenerator":
            Creates an PayloadGenerator object from a dictionary.

        to_dict(self) -> dict:
            Converts the object to a dictionary representation, including the object's attributes and type.
    """

    @property
    def type_text(self):
        raise NotImplementedError("`type_text` property not implemented.")

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "PayloadGenerator":
        """
        Creates a PayloadGenerator object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            PayloadGenerator: The PayloadGenerator object created from the dictionary.
        """
        payload_dict.pop("type", None)
        cls = cls(**payload_dict)                   
        return cls

    @override
    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation. Checks if the object has a `to_dict()` method and calls it.
        If the object does not have a `to_dict()` method, it raises a `NotImplementedError`. Also includes the object's
        attributes in the dictionary. If object is another class, it calls `to_dict()` on the related instance.

        Returns:
            dict: A dictionary containing the key-value pairs representing the object's attributes.
        """
        dict_json = super().to_dict()
        dict_json["type"] = self.type_text
        return dict_json


class TextPayload(PayloadGenerator):
    """TextPayload is a class responsible for handling text outgoing payloads for the Gupshup API."""

    body: str

    @property
    def type_text(self):
        return "text"


class FilePayload(PayloadGenerator):
    """FilePayload is a class responsible for handling file outgoing payloads for the Gupshup API."""

    url: str
    caption: str
    filename: str
    id: str

    @property
    def type_text(self):
        return "file"

class ImagePayload(PayloadGenerator):
    """ImagePayload is a class responsible for handling image outgoing payloads for the Gupshup API."""

    originalUrl: str
    caption: str
    id: str

    @property
    def type_text(self):
        return "image"

class AudioPayload(PayloadGenerator):
    """AudioPayload is a class responsible for handling audio outgoing payloads for the Gupshup API."""

    url: str
    fileName: str
    id: str

    @property
    def type_text(self):
        return "audio"

class VideoPayload(PayloadGenerator):
    """VideoPayload is a class responsible for handling video outgoing payloads for the Gupshup API."""

    url: str
    caption: str
    id: str

    @property
    def type_text(self):
        return "video"

class LocationPayload(PayloadGenerator):
    """LocationPayload is a class responsible for handling location outgoing payloads for the Gupshup API."""

    longitude: float
    latitude: float
    name: str
    address: str

    @property
    def type_text(self):
        return "location"

class GupshupOutgoingPayload(OutgoingPayload):
    """
    GupshupOutgoingPayload class represents the outgoing payload for Gupshup messaging service.
    Attributes:
        payload (PayloadGenerator): The payload generator object.
    Methods:
        app_name:
        from_dict:
    """
    payload: PayloadGenerator

    @property
    def app_name(self) -> str:
        """
        Returns the name of the application that the payload is associated with.
        """
        return "WhatsApp"
    
    @override
    def __call__(self, *args, **kwds):
        """
        This method allows the instance to be called as a function.
        
        Args:
            *args: Variable length argument list.
            **kwds: Arbitrary keyword arguments.
        
        Returns:
            The payload attribute of the instance.
        """
        return self.payload
    
    @classmethod
    def from_dict(cls, payload_dict: dict) -> "GupshupOutgoingPayload":
        """
        Creates a GupshupOutgoingPayload object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            GupshupOutgoingPayload: The GupshupOutgoingPayload object created from the dictionary.
        """
        # print(payload_dict, "<----")
        payload_dict = payload_dict.get("payload") if "payload" in payload_dict else payload_dict
        payload_type = payload_dict.get("type")
        if payload_type == "text":
            return cls(payload=TextPayload.from_dict(payload_dict))
        elif payload_type == "file":
            return cls(payload=FilePayload.from_dict(payload_dict))
        elif payload_type == "image":
            return cls(payload=ImagePayload.from_dict(payload_dict))
        elif payload_type == "audio":
            return cls(payload=AudioPayload.from_dict(payload_dict))
        elif payload_type == "video":
            return cls(payload=VideoPayload.from_dict(payload_dict))
        elif payload_type == "location":
            return cls(payload=LocationPayload.from_dict(payload_dict))
        else:
            raise NotImplementedError(f"Payload type '{payload_type}' is not supported.")

