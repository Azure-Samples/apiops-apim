import os
import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.factory import BuilderFactory
from deployment.logger import get_logger

logger = get_logger()


def delete_resources(deleted_files, builder_factory):
    unique_resources = set()

    for line in deleted_files:
        path = line.strip().split("environments/")[1]
        parts = path.split("/")
        resource_type, resource_name = parts[2], parts[3]
        unique_resources.add((resource_type, resource_name))

    for resource_type, resource_name in unique_resources:
        builder = builder_factory.get_builder(resource_type)
        builder.delete(resource_name)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--deleted-files",
            help="Path to the file containing deleted files list",
            default="deleted_files.txt",
        )
        args = parser.parse_args()

        environment = os.getenv("ENVIRONMENT", "dev")
        apim_instance = os.getenv("APIM_INSTANCE", "apim-apimpgs-dev-eastus")
        resource_group = os.getenv("RESOURCE_GROUP", "rg-apimpgs-dev-eastus")
        subscription_id = os.getenv(
            "SUBSCRIPTION_ID", "1640ab47-b036-4934-bdcb-937d79e45473"
        )
        
        logger.info(f"Starting deployment for {environment} {apim_instance} {resource_group} {subscription_id}" )

        if not all([environment, apim_instance, resource_group, subscription_id]):
            raise ValueError("One or more required environment variables are missing")

        credential = DefaultAzureCredential()
        client = ApiManagementClient(credential, subscription_id)

        builder_factory = BuilderFactory(client, resource_group, apim_instance)

        # Handle deleted resources
        if args.deleted_files:
            logger.info("Deleted files list provided. Deleting resources.")
            if os.path.exists(args.deleted_files):
                logger.info(f"Reading deleted files from {args.deleted_files}")
                with open(args.deleted_files) as f:
                    deleted_files = f.readlines()
                logger.info(f"Deleting {len(deleted_files)} resources")
                delete_resources(
                    deleted_files,
                    builder_factory,
                )
            else:
                print(f"The file {args.deleted_files} does not exist.")
        # Deploy resources
        builders = [
            "apis",
            "policy_fragments",
            # "products",
            "operation_policy",
            "external_policy",
        ]
        for builder_type in builders:
            builder = builder_factory.get_builder(builder_type)
            builder.create(environment)

        logger.info("Deployment completed successfully.")
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise
