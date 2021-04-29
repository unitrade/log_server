import logging
import os
from logging.config import dictConfig

from flask import Flask

from config.config import ProductionConfig, DevelopmentConfig, TestingConfig
from src.settings import LoggerConfig
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv(".env")


def create_app(config: object):
    app = Flask(__name__)

    # Set Flask config from object
    app.config.from_object(config)
    app.logger.info(f'ENV is set to: {app.config["ENV"]}')

    # print(f'ENV is set to: {app.config["ENV"]}')

    # Set logger config
    logging.config.dictConfig(LoggerConfig.dictConfig)

    return app


# Check environment and set config
if os.environ["FLASK_ENV"] == "production":
    app = create_app(ProductionConfig())
elif os.environ["FLASK_ENV"] == "development":
    app = create_app(DevelopmentConfig())
else:
    app = create_app(TestingConfig())

import src.routes
