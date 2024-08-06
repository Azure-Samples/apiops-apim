import os
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from deployment.utils import load_json_file, load_text_file
from deployment.logger import get_logger
from deployment.builders.builder_base import BuilderBase

logger = get_logger()


class PolicyFragmentBuilder(BuilderBase):
    def create(self, environment):
        policy_fragments_folder = os.path.join(
            "environments", environment, self.apim_instance, "policy_fragments"
        )
        try:
            for fragment_name in os.listdir(policy_fragments_folder):
                fragment_path = os.path.join(policy_fragments_folder, fragment_name)
                fragment_info = load_json_file(
                    os.path.join(fragment_path, "policyFragmentInformation.json")
                )
                policy = load_text_file(os.path.join(fragment_path, "policy.xml"))

                response = self.client.policy_fragment.begin_create_or_update(
                    resource_group_name=self.resource_group,
                    service_name=self.apim_instance,
                    id=fragment_name,
                    parameters={
                        "properties": {
                            "description": fragment_info.get("description"),
                            "format": "rawxml",
                            "value": policy,
                        }
                    },
                ).result()
                logger.info(f"Successfully deployed policy fragment {fragment_name}")
            return {
                "status": "success",
                "message": "Successfully deployed all policy fragments",
            }
        except HttpResponseError as e:
            logger.error(
                f"HTTP response error while deploying policy fragment: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except Exception as e:
            logger.error(f"Error deploying policy fragment: {e}")
            return {"status": "error", "message": str(e)}

    def delete(self, resource_name: str):
        try:
            self.client.policy_fragment.delete(
                resource_group_name=self.resource_group,
                service_name=self.apim_instance,
                id=resource_name,
                if_match="*",
            )
            logger.info(f"Deleted policy fragment {resource_name}")
            return {
                "status": "success",
                "message": f"Deleted policy fragment {resource_name}",
            }
        except ResourceNotFoundError as e:
            logger.error(
                f"Resource not found error while deleting policy fragment {resource_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except HttpResponseError as e:
            logger.error(
                f"HTTP response error while deleting policy fragment {resource_name}: {e.message}"
            )
            return {"status": "error", "message": e.message}
        except Exception as e:
            logger.error(f"Error deleting policy fragment {resource_name}: {e}")
            return {"status": "error", "message": str(e)}
