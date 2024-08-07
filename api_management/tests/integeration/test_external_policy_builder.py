import pytest
import os

def test_create_external_policy(builder_factory, setup_and_teardown_api):
    external_policy_builder = builder_factory.get_builder("external_policy")
    environment = os.getenv("ENVIRONMENT", "integration_test")

    # Create external policy
    result = external_policy_builder.create(environment)

    # Verify the external policy was created
    if result and result.get("status") == "error":
        pytest.fail(f"External policy creation failed: {result['message']}")
    else:
        api_id = "echo-api"
        response = external_policy_builder.client.api_policy.get(
            builder_factory.resource_group,
            builder_factory.apim_instance,
            api_id,
            "policy",
        )
        assert response.value is not None

    # Clean up (Delete the external policy)
    delete_result = external_policy_builder.delete(api_id)
    if delete_result and delete_result.get("status") == "error":
        pytest.fail(f"External policy deletion failed: {delete_result['message']}")
    else:
        with pytest.raises(Exception):
            external_policy_builder.client.api_policy.get(
                builder_factory.resource_group,
                builder_factory.apim_instance,
                api_id,
                "policy",
            )
