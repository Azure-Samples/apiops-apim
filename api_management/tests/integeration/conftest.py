import os
import pytest
from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
from deployment.factory import BuilderFactory


@pytest.fixture(scope="session")
def api_management_client():
    subscription_id = os.getenv(
        "SUBSCRIPTION_ID", "1640ab47-b036-4934-bdcb-937d79e45473"
    )
    credential = DefaultAzureCredential()
    client = ApiManagementClient(credential, subscription_id)
    return client


@pytest.fixture(scope="session")
def builder_factory(api_management_client):
    apim_instance = os.getenv("APIM_INSTANCE", "apim-apimpgs-dev-eastus")
    resource_group = os.getenv("RESOURCE_GROUP", "rg-apimpgs-dev-eastus")
    factory = BuilderFactory(api_management_client, resource_group, apim_instance)
    return factory


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_api(builder_factory):
    api_builder = builder_factory.get_builder("apis")
    environment = os.getenv("ENVIRONMENT", "integration_test")

    # Create API
    result = api_builder.create(environment)
    if result["status"] == "error":
        pytest.fail(f"API creation failed: {result['message']}")
    else:
        api_id = "echo-api"
        response = api_builder.client.api.get(
            builder_factory.resource_group, builder_factory.apim_instance, api_id
        )
        assert response.name == api_id
        assert response.display_name == "Echo Test API"

    yield

    # Clean up (Delete the API)
    delete_result = api_builder.delete("echo-api")
    if delete_result["status"] == "error":
        pytest.fail(f"API deletion failed: {delete_result['message']}")
    else:
        with pytest.raises(Exception):
            api_builder.client.api.get(
                builder_factory.resource_group, builder_factory.apim_instance, api_id
            )
