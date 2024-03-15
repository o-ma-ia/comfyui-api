import os

from flask import Flask, request, send_from_directory

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello
    @app.route("/")
    def hello_world():
        app_url = request.url_root
        return f"<h1>It's alive!</h1><p>Hello, World from {app_url}!</p>"

    # Serve the output folder
    @app.route('/output/<path:path>')
    def serve_output(path):
        return send_from_directory('output', path)

    from . import workflow
    app.register_blueprint(workflow.bp)

    return app