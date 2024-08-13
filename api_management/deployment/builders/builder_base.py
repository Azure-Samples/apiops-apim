from abc import ABC, abstractmethod
from azure.mgmt.apimanagement import ApiManagementClient


class BuilderBase(ABC):
    def __init__(
        self, client: ApiManagementClient, resource_group: str, apim_instance: str,subscription_id: str
    ):
        self.client = client
        self.resource_group = resource_group
        self.apim_instance = apim_instance
        self.subscription_id = subscription_id
        
    @abstractmethod
    def create(self, environment: str):
        pass

    @abstractmethod
    def delete(self, resource_name: str):
        pass
