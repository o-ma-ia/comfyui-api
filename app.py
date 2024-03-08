from flask import Flask, abort, request, send_from_directory

app = Flask(__name__)

@app.route("/")
def hello_world():
    app_url = request.url_root
    return f"<h1>It's alive!</h1><p>Hello, World from {app_url}!</p>"

@app.route('/output/<path:path>')
def serve_output(path):
    return send_from_directory('output', path)

@app.post("/comfyui/<workflow>")
def comfyui(workflow):
    import json
    import random
    import importlib.util

    from utils.replace_placeholders import replace_placeholders
    from utils.execute_workflow import execute_workflow
    from utils.download_file import download_file

    # Get the post data
    post_data = request.json

    # Set the seed for the workflow
    seed = random.randint(1, 1000000000)

    # Dynamically import the workflow data module based on the workflow variable
    try:
        spec = importlib.util.spec_from_file_location("workflow_data", f"./comfyui-workflows/{workflow}_data.py")
        workflow_data_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(workflow_data_module)
    except FileNotFoundError:
        abort(500, description="Workflow data module not found")

    # Use the imported module
    variables_dict = workflow_data_module.get_data(post_data, seed)

    # Load workflow from file
    try:
        workflow_file = open(f"./comfyui-workflows/{workflow}.json", "r", encoding="utf-8")
    except OSError as e:
        print('open() failed', e)
        abort(500, description="Workflow file not found")
    with  workflow_file:
        workflow_data = workflow_file.read()

    workflow_json = json.loads(workflow_data)

    # Replace the placeholders in the workflow with the values from the variables_dict
    workflow_json = replace_placeholders(workflow_json, variables_dict)

    # Execute the workflow
    result = execute_workflow(workflow_json, seed)
    return {
        "variables": variables_dict,
        "workflow": workflow_json,
        "result": result    
    }