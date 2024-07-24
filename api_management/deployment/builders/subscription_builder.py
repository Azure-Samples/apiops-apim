import os
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.utils import load_json_file
from deployment.logger import get_logger
from deployment.builders.builder_base import BuilderBase

logger = get_logger()


class SubscriptionBuilder(BuilderBase):
    def create(self, environment):
        subscriptions_folder = os.path.join(
            "environments", environment, self.apim_instance, "subscriptions"
        )
        try:
            for subscription_name in os.listdir(subscriptions_folder):
                subscription_path = os.path.join(
                    subscriptions_folder, subscription_name
                )
                subscription_info = load_json_file(
                    os.path.join(subscription_path, "subscriptionInformation.json")
                )

                response = self.client.subscription.create_or_update(
                    resource_group_name=self.resource_group,
                    service_name=self.apim_instance,
                    sid=subscription_name,
                    parameters=subscription_info,
                )
                logger.info(f"Successfully deployed subscription {subscription_name}")
        except Exception as e:
            logger.error(f"Error deploying subscription {subscription_name}: {e}")
            raise

    def delete(self, resource_name: str):
        try:
            self.client.subscription.delete(
                resource_group_name=self.resource_group,
                service_name=self.apim_instance,
                sid=resource_name,
                if_match="*",
            )
            logger.info(f"Deleted subscription {resource_name}")
        except Exception as e:
            logger.error(f"Error deleting subscription {resource_name}: {e}")
            raise
