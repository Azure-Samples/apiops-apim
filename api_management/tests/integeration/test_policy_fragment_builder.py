import pytest
import os


def test_create_policy_fragment(builder_factory, setup_and_teardown_api):
    policy_fragment_builder = builder_factory.get_builder("policy_fragments")
    environment = os.getenv("ENVIRONMENT", "integration_test")

    # Create policy fragment
    result = policy_fragment_builder.create(environment)

    # Verify the policy fragment was created
    if result and result.get("status") == "error":
        pytest.fail(f"Policy fragment creation failed: {result['message']}")
    else:
        fragment_name = "policy-fragment-test"
        response = policy_fragment_builder.client.policy_fragment.get(
            builder_factory.resource_group, builder_factory.apim_instance, fragment_name
        )
        assert response is not None
        assert response.name == fragment_name

    # Clean up (Delete the policy fragment)
    delete_result = policy_fragment_builder.delete(fragment_name)
    if delete_result and delete_result.get("status") == "error":
        pytest.fail(f"Policy fragment deletion failed: {delete_result['message']}")
    else:
        with pytest.raises(Exception):
            policy_fragment_builder.client.policy_fragment.get(
                builder_factory.resource_group,
                builder_factory.apim_instance,
                fragment_name,
            )
