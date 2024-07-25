import os
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.utils import load_json_file, load_text_file
from deployment.logger import get_logger

logger = get_logger()


class ApiBuilder:
    def __init__(
        self, client: ApiManagementClient, resource_group: str, apim_instance: str
    ):
        self.client = client
        self.resource_group = resource_group
        self.apim_instance = apim_instance

    def deploy(self, environment):
        api_folder_base = os.path.join(
            "environments", environment, self.apim_instance, "apis"
        )
        try:
            for api_name in os.listdir(api_folder_base):
                api_path = os.path.join(api_folder_base, api_name)
                api_info = load_json_file(
                    os.path.join(api_path, "api_information.json")
                )
                openapi_spec = load_text_file(
                    os.path.join(api_path, "openapispec.yaml")
                )
                api_info["value"] = openapi_spec

                response = self.client.api.begin_create_or_update(
                    resource_group_name=self.resource_group,
                    service_name=self.apim_instance,
                    api_id=f"{api_name};rev=1",
                    parameters=api_info,
                    if_match="*",
                ).result()

                logger.info(f"Successfully deployed API {api_name}")
        except Exception as e:
            logger.error(f"Error deploying API {api_name}: {e}")
            raise
