from .abstract_client import AbstractClient
from .DigitalAssistantOCR_pb2 import (
    OCRType,
    DigitalAssistantOCRRequest,
    DigitalAssistantOCRResponse,
)
from .DigitalAssistantOCR_pb2_grpc import DigitalAssistantOCRStub


class OCREnrichedClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantOCRStub(self._channel)

    def __call__(
        self,
        ocr_type_: OCRType,
        resource_id: str = None,
        request_id: str = "",
    ) -> tuple[str, str]:
        if resource_id is None:
            raise ValueError("Argument `resource_id` should be passed!")
        request = DigitalAssistantOCRRequest(
            ResourceId=resource_id, OCRType=ocr_type_, RequestId=request_id
        )
        response: DigitalAssistantOCRResponse = self._stub.GetTextResponse(request)
        return response.Text, response.ResourceId
