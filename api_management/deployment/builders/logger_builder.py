import os
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.utils import load_json_file
from deployment.logger import get_logger
from deployment.builders.builder_base import BuilderBase

logger = get_logger()


class LoggerBuilder(BuilderBase):
    def create(self, environment):
        loggers_folder = os.path.join(
            "environments", environment, self.apim_instance, "loggers"
        )
        try:
            for logger_name in os.listdir(loggers_folder):
                logger_path = os.path.join(loggers_folder, logger_name)
                logger_info = load_json_file(
                    os.path.join(logger_path, "logger_information.json")
                )

                response = self.client.logger.create_or_update(
                    resource_group_name=self.resource_group,
                    service_name=self.apim_instance,
                    logger_id=logger_name,
                    parameters=logger_info,
                )
                logger.info(f"Successfully deployed logger {logger_name}")
        except Exception as e:
            logger.error(f"Error deploying logger {logger_name}: {e}")
            raise

    def delete(self, resource_name: str):
        try:
            self.client.logger.delete(
                resource_group_name=self.resource_group,
                service_name=self.apim_instance,
                logger_id=resource_name,
                if_match="*",
            )
            logger.info(f"Deleted logger {resource_name}")
        except Exception as e:
            logger.error(f"Error deleting logger {resource_name}: {e}")
            raise
