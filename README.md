# ComfyUI-API

> :warning: **WARNING: This project is currently a work in progress.** The API and its features are under active development and may change. Please be aware that functionality might be unstable, and the documentation could be updated frequently as we make improvements.


## Overview

ComfyUI-API allows you to serve ComfyUI workflows through a web API, enabling easy integration and automation of ComfyUI's powerful UI workflows into web applications. By setting up this API, developers can programmatically interact with ComfyUI workflows, expanding the capabilities and reach of their ComfyUI-based applications.

## Prerequisites

Before proceeding with the installation and setup of ComfyUI-API, ensure the following requirements are met:

- **ComfyUI Installation**: ComfyUI must be installed and operational either on your local machine or a remote server. Knowledge of the IP address and port number used to connect to the ComfyUI web socket is essential.
- **Python**: A recent version of Python must be installed on your system to create a virtual environment and run the API.

## Installation

Follow these steps to set up the ComfyUI-API on your system:

### 1. Create a Python Virtual Environment

A virtual environment is recommended to manage dependencies and avoid conflicts with other Python projects.

```shell
python -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

Install all the necessary Python packages listed in the `requirements.txt` file.

```shell
pip install -r requirements.txt
```

## Configuration

To configure the API to serve your custom ComfyUI workflows, follow these steps:

### 1. Rename .env-default to .env
The project uses environment variables for configuration, which are set in a file named .env. Initially, you will find a file named .env-default in the project root.

- **Rename .env-default**: Before running the API, rename `.env-default` to `.env`. This file contains template environment variables that you should adjust according to your setup, such as the ComfyUI server address, port, and any other necessary configuration values.


### 2. Prepare Your Workflow JSON File

After creating your workflow in ComfyUI, download the workflow API JSON file.

- **Rename the JSON File**: The file name will determine the API endpoint. For example, renaming your workflow file to `example_workflow.json` will create an endpoint like `/comfyui/example_workflow`.
- **Move the File**: Place the renamed file into the `comfyui-workflows` directory.
- **Parameterize the Workflow**: Edit the workflow file, replacing specific values with placeholders in the format `"<PARAMETER>"` where you wish to inject API parameters dynamically.

Refer to the `comfyui-workflows/img2img.json` as an example.

### 3. Create and Configure the "_data.py" File

For each workflow JSON file, a corresponding `_data.py` file is required for parameter validation and management.

- **Create the File**: In the `comfyui-workflows` directory, create a Python file with the same base name as your workflow JSON file and append `_data.py` to it. For example, `example_workflow_data.py`.
- **Edit the File**: Implement validation for the API parameters, manage file uploads if necessary, and set up the replacement values for your workflow parameters.

See `comfyui-workflows/img2img_data.py` for an example setup.

Your `comfyui-workflows` directory should resemble the following structure:

```
comfyui-workflows/
- example_workflow.json      # Your workflow configuration file
- example_workflow_data.py   # Python file for parameter management and validation
```

## Running the API

With your workflows configured, you're ready to launch the API:

```shell
flask run
```

## Making API Calls

After starting the API, send POST requests to the URL provided by Flask. Use the endpoint format `/comfyui/<workflow_name>` to interact with specific workflows. For example, to use the `img2img` workflow:

```
POST <API_URL>/comfyui/img2img
```

Replace `<API_URL>` with the actual URL where your Flask app is running, typically `http://127.0.0.1:5000` for local development.
