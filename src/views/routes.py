import os
import logging
from logging.config import dictConfig
from flask import Flask, abort, render_template, request, jsonify, Response
from config import *
from src.filters.filters import *


def create_app(config: object):
    app = Flask(__name__, template_folder='templates')

    # Set Flask config from object
    app.config.from_object(config)

    # Set logger config
    logging.config.dictConfig(LoggerConfig.dictConfig)

    return app


# Check environment and set config
if os.environ["FLASK_ENV"] == "production":
    app = create_app(ProductionConfig())
elif os.environ["FLASK_ENV"] == "development":
    app = create_app(DevelopmentConfig())
elif os.environ["FLASK_ENV"] == "testing":
    app = create_app(TestingConfig())
elif os.environ["FLASK_ENV"] is None:
    app = ''

logger_success = logging.getLogger("to_info_file")
logger_fail = logging.getLogger("to_error_file")
log = [
    {"time": "2021-04-27 07:58:54,256", "level": "[INFO]",
     "msg": "Dumping current MySQL Servers structures for hostgroup ALL"},
    {"time": "2021-04-27 07:58:54,256", "level": "[DEBUG]",
     "msg": "Loading to runtime MySQL Users from peer proxysql-cluster.proxysql.svc.cluster.local:6032"},
    {"time": "2021-04-27 09:30:54,256", "level": "[ERROR]",
     "msg": "Error after 1009ms on server 10.0.1.72:3306 : timeout during ping"},
    {"time": "2021-04-28 10:30:54,256", "level": "[ERROR]",
     "msg": "Duplicate entry '6058-4006' for key 'interlocutors'"},
    {"time": "2021-04-29 10:30:54,256", "level": "[WARNING]",
     "msg": "1205, Lock wait timeout exceeded; try restarting transaction"}
]

url = app.config["SERVER_NAME"]
nav = [
    {'name': 'Home', 'url': f"http://{url}"},
    {'name': 'Logs', 'url': f"http://{url}/api/v1/events"}
]
filters = []


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="Track error reporting and related data in a centralized way.",
        description="Logging should be used in big applications and it can be put to use in smaller apps,\
         especially if they provide a crucial function.",
        nav=nav
    )


@app.route('/api/v1/filters', methods=["GET"])
def get_filters():
    if "application/json" in request.headers["Accept"]:
        return jsonify(filters), 200
    else:
        abort(400, description="Bad request")


@app.route('/api/v1/filters/<int:id>', methods=["GET"])
def get_filter_id(id):
    result = {}
    for item in filters:
        if item["id"] == id:
            result = item
    return jsonify(result)


@app.route('/api/v1/filters', methods=["POST"])
def post_filters():
    if not request.is_json:
        abort(400, description="Bad request")
    content = request.get_json()
    # {"filter_type": "FilterRange", "startDate": "2021-04-27", "endDate": "2021-04-28"}
    # {"filter_type": "FilterInfo"}
    if "filter_type" not in content:
        abort(400, description="Bad request, filter type not implemented")
    if content["filter_type"] not in ["FilterRange", "FilterInfo", "FilterDebug", "FilterWarning", "FilterError"]:
        abort(400, description="Bad request, filter type not valid")
    content["id"] = len(filters) + 1
    filters.append(content)
    response = Response("", 201, mimetype="application/json")
    response.headers["Location"] = "/api/v1/filters/{}".format(content["id"])
    return response


@app.route('/api/v1/filters/many', methods=["POST"])
def post_filters_many():

    def check_id(id) -> bool:
        for filter in filters:
            if id == filter["id"]:
                return True
        abort(400, description="Bad request, filter id not found")

    # {"filter_ids": ["1","2","3"]}
    if not request.is_json:
        abort(400, description="Bad request")
    filter_ids = request.get_json()
    for id in filter_ids["filter_ids"]:
        check_id(id)
    result = ""
    for id in filter_ids["filter_ids"]:
        for filter in filters:
            if id == filter["id"]:
                result = result + filter["filter_type"] + ","
    filter_many = {"filter_type": result[:-1]}
    filter_many["id"] = len(filters) + 1
    filters.append(filter_many)

    return jsonify({"msg": "Added Successfully"}), 200


@app.route('/api/v1/events', methods=["POST"])
def post_events():
    if not request.is_json:
        abort(400, description="Bad request")
    content = request.get_json()
    if request.content_length > int(app.config["CONTENT_LENGTH"]):
        abort(413, description="Content is too large")
    log.append(content)
    return jsonify({"msg": "Added Successfully"}), 200


@app.route('/api/v1/events', methods=["GET"])
def get_events():
    def get_filter(id) -> dict:
        find = {}
        for item in filters:
            if id in item.values():
                find = item
        return find

    limit = request.args.get('limit', default=10, type=int)
    filter_id = request.args.get('filterID', default=None, type=int)
    dict_filters = get_filter(filter_id)
    list_filters = dict_filters["filter_type"].split(",")
    for k, v in enumerate(list_filters):
        list_filters[k] = eval("{}()".format(v))
    result = []

    for item in log:
        if FilterDecorator(list_filters).evaluate(item):
            result.append(item)

    return jsonify(result[:limit])


@app.errorhandler(400)
def bad_request(error):
    logger_fail.error(error)
    return jsonify(error=str(error)), 400


@app.errorhandler(413)
def request_entity_too_large(error):
    logger_fail.error(error)
    return jsonify(error=str(error)), 413

#  curl --header "Content-Type: application/json" --request POST --data '{"username":"abc","password":"abc"}' http://0.0.0.0:8000/api/v1/events

#  curl -i -H "Accept: application/json" -X GET http://0.0.0.0:8000/api/v1/events\?limit\=1
#  curl -i -H "Accept: application/json" -X GET http://0.0.0.0:8000/api/v1/filters
