import os
import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.factory import BuilderFactory
from deployment.logger import get_logger
from deployment.utils import load_json_file

logger = get_logger()


def delete_resources(
    client, resource_group, apim_instance, deleted_files, builder_factory
):
    for line in deleted_files:
        path = line.strip().split("environments/")[1]
        parts = path.split("/")
        resource_type, resource_name = parts[2], parts[3]
        builder = builder_factory.get_builder(resource_type)
        builder.delete(resource_name)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--deleted-files",
            help="Path to the file containing deleted files list",
            default="deleted_resources.txt",
        )
        args = parser.parse_args()

        environment = os.getenv("ENVIRONMENT", "dev")
        apim_instance = os.getenv("APIM_INSTANCE", "apim-sharmaks")
        resource_group = os.getenv("RESOURCE_GROUP", "sitecore-sharmaks-rg")
        subscription_id = os.getenv(
            "SUBSCRIPTION_ID", "1640ab47-b036-4934-bdcb-937d79e45473"
        )

        if not all([environment, apim_instance, resource_group, subscription_id]):
            raise ValueError("One or more required environment variables are missing")

        credential = DefaultAzureCredential()
        client = ApiManagementClient(credential, subscription_id)

        builder_factory = BuilderFactory(client, resource_group, apim_instance)

        # Handle deleted resources
        if args.deleted_files:
            if os.path.exists(args.deleted_files):
                with open(args.deleted_files) as f:
                    deleted_files = f.readlines()
                delete_resources(
                    client, resource_group, apim_instance, deleted_files, builder_factory
                )
            else:
                print(f"The file {args.deleted_files} does not exist.")

        # Deploy resources
        builders = [
            "apis",
            "policy_fragments",
            "products",
            "operation_policy",
            "external_policy",
            "subscription",
        ]
        for builder_type in builders:
            builder = builder_factory.get_builder(builder_type)
            builder.create(environment)

        logger.info("Deployment completed successfully.")
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise
