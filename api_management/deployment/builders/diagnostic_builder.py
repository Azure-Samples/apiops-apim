import os
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.utils import load_json_file
from deployment.logger import get_logger
from deployment.builders.builder_base import BuilderBase

logger = get_logger()


class DiagnosticBuilder(BuilderBase):
    def create(self, environment):
        diagnostics_folder = os.path.join(
            "environments", environment, self.apim_instance, "diagnostics"
        )
        try:
            for diagnostic_name in os.listdir(diagnostics_folder):
                diagnostic_path = os.path.join(diagnostics_folder, diagnostic_name)
                diagnostic_info = load_json_file(
                    os.path.join(diagnostic_path, "diagnostic_information.json")
                )

                response = self.client.diagnostic.create_or_update(
                    resource_group_name=self.resource_group,
                    service_name=self.apim_instance,
                    diagnostic_id=diagnostic_name,
                    parameters=diagnostic_info,
                )
                logger.info(f"Successfully deployed diagnostic {diagnostic_name}")
        except Exception as e:
            logger.error(f"Error deploying diagnostic {diagnostic_name}: {e}")
            raise

    def delete(self, resource_name: str):
        try:
            self.client.diagnostic.delete(
                resource_group_name=self.resource_group,
                service_name=self.apim_instance,
                diagnostic_id=resource_name,
                if_match="*",
            )
            logger.info(f"Deleted diagnostic {resource_name}")
        except Exception as e:
            logger.error(f"Error deleting diagnostic {resource_name}: {e}")
            raise
