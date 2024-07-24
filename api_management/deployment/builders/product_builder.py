import os
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.utils import load_json_file
from deployment.logger import get_logger
from deployment.builders.builder_base import BuilderBase

logger = get_logger()


class ProductBuilder(BuilderBase):
    def create(self, environment):
        product_folder_base = os.path.join(
            "environments", environment, self.apim_instance, "products"
        )
        try:
            for product_name in os.listdir(product_folder_base):
                product_path = os.path.join(product_folder_base, product_name)
                product_info = load_json_file(
                    os.path.join(product_path, "product_information.json")
                )

                response = self.client.product.create_or_update(
                    resource_group_name=self.resource_group,
                    service_name=self.apim_instance,
                    product_id=product_name,
                    parameters=product_info,
                    if_match="*",
                )

                apis_folder = os.path.join(product_path, "apis")
                if os.path.exists(apis_folder):
                    for api_name in os.listdir(apis_folder):
                        self.client.product_api.create_or_update(
                            resource_group_name=self.resource_group,
                            service_name=self.apim_instance,
                            product_id=product_name,
                            api_id=api_name,
                        )
                logger.info(f"Successfully deployed product {product_name}")
        except Exception as e:
            logger.error(f"Error deploying product {product_name}: {e}")
            raise

    def delete(self, resource_name: str):
        try:
            self.client.product.delete(
                resource_group_name=self.resource_group,
                service_name=self.apim_instance,
                product_id=resource_name,
                if_match="*",
            )
            logger.info(f"Deleted product {resource_name}")
        except Exception as e:
            logger.error(f"Error deleting product {resource_name}: {e}")
            raise
