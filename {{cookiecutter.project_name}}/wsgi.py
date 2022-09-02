"""App entry point."""
from {{cookiecutter.app_name}} import create_app, db, models
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, "models": models}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
