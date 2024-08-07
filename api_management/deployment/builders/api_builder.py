import os
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
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

                # Deploy diagnostics for the API
                diagnostics_folder = os.path.join(api_path, "diagnostics")
                if os.path.exists(diagnostics_folder):
                    for diagnostic_name in os.listdir(diagnostics_folder):
                        diagnostic_path = os.path.join(
                            diagnostics_folder, diagnostic_name
                        )
                        diagnostic_info = load_json_file(
                            os.path.join(diagnostic_path, "diagnostic_information.json")
                        )
                        diagnostic_response = (
                            self.client.api_diagnostic.create_or_update(
                                resource_group_name=self.resource_group,
                                service_name=self.apim_instance,
                                api_id=api_name,
                                diagnostic_id=diagnostic_name,
                                parameters=diagnostic_info,
                            )
                        )
                        logger.info(
                            f"Successfully deployed diagnostic {diagnostic_name} for API {api_name}"
                        )
            return {"status": "success", "message": "API deployed successfully"}

        except HttpResponseError as e:
            logger.error(
                f"HTTP response error while deploying API {api_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except Exception as e:
            logger.error(f"Error deploying API {api_name}: {e}")
            return {"status": "error", "message": str(e)}

    def delete(self, resource_name: str):
        try:
            # Delete diagnostics for the API
            diagnostic_list = self.client.api_diagnostic.list_by_service(
                resource_group_name=self.resource_group,
                service_name=self.apim_instance,
                api_id=resource_name,
            )
            for diagnostic in diagnostic_list:
                diagnostic_id = diagnostic.name
                self.client.api_diagnostic.delete(
                    resource_group_name=self.resource_group,
                    service_name=self.apim_instance,
                    api_id=resource_name,
                    diagnostic_id=diagnostic_id,
                    if_match="*",
                )
                logger.info(
                    f"Deleted diagnostic {diagnostic_id} for API {resource_name}"
                )

            # Delete the API
            self.client.api.delete(
                self.resource_group, self.apim_instance, resource_name, if_match="*"
            )
            logger.info(f"Deleted API {resource_name}")
            logger.info("Please ensure the linked API resources are also deleted.")
            return {"status": "success", "message": "API deleted successfully"}
        except ResourceNotFoundError as e:
            logger.error(
                f"Resource not found error while deleting API {resource_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except HttpResponseError as e:
            logger.error(
                f"HTTP response error while deleting API {resource_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except Exception as e:
            logger.error(f"Error deleting API {resource_name}: {e}")
            return {"status": "error", "message": str(e)}
