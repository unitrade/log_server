import logging
import os
from logging.config import dictConfig

from flask import Flask, render_template

from config.config import ProductionConfig, DevelopmentConfig, TestingConfig
from src.settings import LoggerConfig


def create_app(config: object):
    app = Flask(__name__)

    # Set Flask config from object
    app.config.from_object(config)

    print(f'ENV is set to: {app.config["ENV"]}')

    # Set logger config
    logging.config.dictConfig(LoggerConfig.dictConfig)

    logger_success = logging.getLogger("to_info_file")
    logger_fail = logging.getLogger("to_error_file")

    @app.route('/')
    def index():
        logger_success.info("OK")
        logger_fail.error("Error")
        return render_template("index.html")

    @app.route('/api/v1/hello')
    def hello_world():
        logger_success.info("OK Hello")
        logger_fail.error("Error Hello")
        return render_template("hello.html")

    return app


# Check environment and set config
if os.environ["FLASK_ENV"] == "production":
    app = create_app(ProductionConfig())
elif os.environ["FLASK_ENV"] == "development":
    app = create_app(DevelopmentConfig())
else:
    app = create_app(TestingConfig())
