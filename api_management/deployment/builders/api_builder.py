import os
from deployment.utils import load_json_file, load_text_file
from deployment.logger import get_logger
from deployment.builders.builder_base import BuilderBase

logger = get_logger()


class ApiBuilder(BuilderBase):
    def create(self, environment: str):
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

    def delete(self, resource_name: str):
        try:
            self.client.api.delete(
                self.resource_group, self.apim_instance, resource_name, if_match="*"
            )
            logger.info(f"Deleted API {resource_name}")
        except Exception as e:
            logger.error(f"Error deleting API {resource_name}: {e}")
            raise
