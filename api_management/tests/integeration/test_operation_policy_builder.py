import pytest
import os

def test_create_operation_policy(builder_factory, setup_and_teardown_api):
    operation_policy_builder = builder_factory.get_builder("operation_policy")
    environment = os.getenv("ENVIRONMENT", "integration_test")

    # Create operation policy
    result = operation_policy_builder.create(environment)

    # Verify the operation policy was created
    if result and result.get("status") == "error":
        pytest.fail(f"Operation policy creation failed: {result['message']}")
    else:
        api_id = "echo-api"
        operation_id = "openai-all"
        response = operation_policy_builder.client.api_operation_policy.get(
            builder_factory.resource_group,
            builder_factory.apim_instance,
            api_id,
            operation_id,
            "policy",
        )
        assert response.value is not None

    # Clean up (Delete the operation policy)
    delete_result = operation_policy_builder.delete(environment)
    if delete_result and delete_result.get("status") == "error":
        pytest.fail(f"Operation policy deletion failed: {delete_result['message']}")
    else:
        with pytest.raises(Exception):
            operation_policy_builder.client.api_operation_policy.get(
                builder_factory.resource_group,
                builder_factory.apim_instance,
                api_id,
                operation_id,
                "policy",
            )
