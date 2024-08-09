import pytest
import os

def test_create_product(builder_factory, setup_and_teardown_product):
    product_builder = builder_factory.get_builder("products")
    environment = os.getenv("ENVIRONMENT", "integration_test")

    # Create product builder
    result = product_builder.create(environment)
    api_id = "echo-api"
    product_id = "basic-test"
    # Verify the product was created
    if result and result.get("status") == "error":
        pytest.fail(f"Product creation failed: {result['message']}")
    else:
        response = list(product_builder.client.product_api.list_by_product(
            builder_factory.resource_group,
            builder_factory.apim_instance,
            product_id
        ))
        assert response is not None
        assert response[0].name == api_id