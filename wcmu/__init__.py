from flask import Flask

def create_app(env):
    if env == "Development":
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_pyfile('config.py')

    elif env == "Production":
        app = Flask(__name__)
        app.config.from_pyfile('config.py')
        
    from .routes import wcmu_app
    app.register_blueprint(wcmu_app)
        
    return app