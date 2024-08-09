# deployment/builders/backend_builder.py
import os
import requests
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from deployment.utils import load_json_file
from azure.identity import DefaultAzureCredential
from deployment.logger import get_logger
from deployment.builders.builder_base import BuilderBase

logger = get_logger()


class BackendBuilder(BuilderBase):
    def get_access_token(self):
        credential = DefaultAzureCredential()
        token = credential.get_token("https://management.azure.com/.default")
        return token.token
    def create(self, environment: str):
        backend_folder_base = os.path.join(
            "environments", environment, self.apim_instance, "backends"
        )
        try:
            for backend_name in os.listdir(backend_folder_base):
                backend_path = os.path.join(backend_folder_base, backend_name)
                backend_info = load_json_file(
                    os.path.join(backend_path, "backend_information.json")
                )

                url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.ApiManagement/service/{self.apim_instance}/backends/{backend_name}?api-version=2023-09-01-preview"

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.get_access_token()}",
                }
                
                response = requests.put(url, json=backend_info, headers=headers)
                response.raise_for_status()

                if response.status_code == 201:
                    logger.info(f"Successfully created backend {backend_name}")
                else:
                    logger.info(f"Successfully updated backend {backend_name}")

            return {"status": "success", "message": "Backends deployed successfully"}

        except HttpResponseError as e:
            logger.error(
                f"HTTP response error while deploying backend {backend_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except Exception as e:
            logger.error(f"Error deploying backend {backend_name}: {e}")
            return {"status": "error", "message": str(e)}

    def delete(self, resource_name: str):
        try:
            url = f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.ApiManagement/service/{self.apim_instance}/backends/{resource_name}?api-version=2023-09-01-preview"

            headers = {
                "Authorization": f"Bearer {self.get_access_token()}",
            }

            response = requests.delete(url, headers=headers)
            response.raise_for_status()

            logger.info(f"Deleted backend {resource_name}")
            return {"status": "success", "message": "Backend deleted successfully"}

        except ResourceNotFoundError as e:
            logger.error(
                f"Resource not found error while deleting backend {resource_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except HttpResponseError as e:
            logger.error(
                f"HTTP response error while deleting backend {resource_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except Exception as e:
            logger.error(f"Error deleting backend {resource_name}: {e}")
            return {"status": "error", "message": str(e)}
