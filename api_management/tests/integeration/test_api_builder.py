import pytest


def test_create_api(builder_factory, setup_and_teardown_api):
    api_builder = builder_factory.get_builder("apis")

    # Verify the API was created
    api_id = "echo-api"
    response = api_builder.client.api.get(
        builder_factory.resource_group, builder_factory.apim_instance, api_id
    )
    assert response.name == api_id
    assert response.display_name == "Echo Test API"
