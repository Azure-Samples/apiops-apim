# Overview

The APIOPS framework is designed to manage API operations in a controlled and efficient manner, adhering to best practices. It facilitates the creation and management of APIs, policies, diagnostics, loggers, policy fragments, and products through a Git-based approach. 

This methodology eliminates the need for manual changes through the API Management UI, ensuring consistency and robust version control.

## Project Structure

- `api_management/`: Contains the main API management code.

    -`builders/`: Contains builder classes for creating and managing APIs, policies,policy fragments, products etc.

    -`environments/`: Manage different environments such as development, integration testing, production etc.

    -`tests/integration/`: Contains integration tests for different components.

- `.vscode/launch.json` : Configuration file for debugging in Visual Studio Code.

## Getting Started

1. Clone this github repository into your local machine and open it in VS code.

2. **Setup environment variables**:  Create an environment file `.env` file by copying the contents from `env_template` file.

3. **Install the required dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the main application**:

    ```sh
    python main.py
    ```

    You will see that the builder gets deployed.

    **Note**: In `main.py`, there is a section for defining the builders and components that need to be deployed, with the sequence being important.

## Debugging the Application

To debug the application, follow these steps:

1. Open Run and Debug view by clicking on the icon in the Activity Bar on the side of the window.
2. Choose the configuration **`Python Debugger: Current File`** from the top of the Debug view and click on the green play button to start debugging.

## How to create API/Policy/Products

1. Navigate to the specific environment under `api_management/environments` of your choice.
2. You will see your APIM instance name. Under this, you have specific folders for creating APIs, policy fragments, and products.

## Running integration test

The project includes configuration in `.vscode/launch.json`:

**Python: Debug Pytest:** Runs and debugs the integration tests located in the `tests/integration` directory.

To use this configuration:

1. Open the Run and Debug view by clicking on the icon in the Activity Bar on the side of the window.
2. Select the configuration **`Python: Debug Pytest`** from the dropdown menu at the top of the Debug view.
3. Click the green play button to start running the tests.

## Continuous Integration/Continuous Deployment (CI/CD)

 Pipelines are integrated through github actions to automate testing and deployment.This ensures that changes are continuously tested and deployed to maintain application stability.