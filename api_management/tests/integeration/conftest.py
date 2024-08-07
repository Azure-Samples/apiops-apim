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
    apim_instance = os.getenv("APIM_INSTANCE", "euw-int-ai-dev-genai-apim")
    resource_group = os.getenv("RESOURCE_GROUP", "rg-ai-euw-dev")
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

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_product(builder_factory):
    product_builder = builder_factory.get_builder("products")
    environment = os.getenv("ENVIRONMENT", "integration_test")
    api_id = "echo-api"
    
    # Create Product
    result = product_builder.create(environment)
    if result is None:
        pytest.fail("Product creation returned None")
    if result.get("status") == "error":
        pytest.fail(f"Product creation failed: {result.get('message', 'Unknown error')}")
    else:
        product_id = "basic"
        response = list(product_builder.client.product_api.list_by_product(
            builder_factory.resource_group, builder_factory.apim_instance, product_id
        ))
        assert response[0].name == product_id

    yield

    # Clean
    delete_result = product_builder.delete("basic")
    if delete_result["status"] == "error":
        pytest.fail(f"Product deletion failed: {delete_result['message']}")
    else:
        with pytest.raises(Exception):
            product_builder.client.product_policy.get(
                builder_factory.resource_group, builder_factory.apim_instance, product_id, api_id
            )