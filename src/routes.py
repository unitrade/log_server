import logging
from datetime import datetime, timedelta

from flask import abort

from flask import render_template, request as R, jsonify as J

from src import app

logger_success = logging.getLogger("to_info_file")
logger_fail = logging.getLogger("to_error_file")
log = [
    {"time": "2021-04-27 07:58:54,256", "level": "[INFO]", "msg": "Dumping current MySQL Servers structures for hostgroup ALL"},
    {"time": "2021-04-27 07:58:54,256", "level": "[DEBUG]", "msg": "Loading to runtime MySQL Users from peer proxysql-cluster.proxysql.svc.cluster.local:6032"},
    {"time": "2021-04-27 09:30:54,256", "level": "[ERROR]", "msg": "Error after 1009ms on server 10.0.1.72:3306 : timeout during ping"},
    {"time": "2021-04-28 10:30:54,256", "level": "[ERROR]", "msg": "Duplicate entry '6058-4006' for key 'interlocutors'"},
    {"time": "2021-04-29 10:30:54,256", "level": "[WARNING]", "msg": "1205, Lock wait timeout exceeded; try restarting transaction"}
]
filters = {
    1: "last_hour",
    2: "last_day",
    3: "last_week",
    4: "info",
    5: "debug",
    6: "warning",
    7: "error"
}

url = app.config["SERVER_NAME"]
nav = [
    {'name': 'Home', 'url': f"http://{url}"},
    {'name': 'Logs', 'url': f"http://{url}/api/v1/events"}
]


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
    if "application/json" in R.headers["Accept"]:
        return J(filters), 200


@app.route('/api/v1/filters', methods=["POST"])
def post_filters():
    pass


@app.route('/api/v1/events', methods=["POST"])
def post_events():
    if R.headers["Content-Type"] == "application/json":
        # if content length more 1MB
        if R.content_length > 1024 * 1024:
            abort(413, description="Content is too large")
        content = R.get_json()
        log.append(content)
        for i in log:
            logger_success.info(i)
        return 'Log has been added', 200
    else:
        return "Bad request", 400


@app.route('/api/v1/events', methods=["GET"])
def get_events():

    limit = R.args.get('limit', default=10, type=int)
    filter_id = R.args.getlist('filterID', type=int)
    filter_id.sort()
    result = []

    if "application/json" in R.headers["Accept"]:
        if filter_id:
            for items in filter_id:

                # last_hour
                if filters[items] == "last_hour":
                    last_hour_date_time = datetime.now() - timedelta(hours=1)
                    for dicts in log:
                        log_time = datetime.strptime(dicts["time"], "%Y-%m-%d %H:%M:%S,%f")
                        if log_time > last_hour_date_time:
                            result.append(dicts)

                # last_day
                if filters[items] == "last_day":
                    last_day_date_time = datetime.now() - timedelta(days=1)
                    for dicts in log:
                        log_time = datetime.strptime(dicts["time"], "%Y-%m-%d %H:%M:%S,%f")
                        if log_time > last_day_date_time:
                            result.append(dicts)

                # last_week
                if filters[items] == "last_week":
                    last_week_date_time = datetime.now() - timedelta(weeks=1)
                    for dicts in log:
                        log_time = datetime.strptime(dicts["time"], "%Y-%m-%d %H:%M:%S,%f")
                        if log_time > last_week_date_time:
                            result.append(dicts)

                # level
                if filters[items] == "info" \
                        or filters[items] == "debug" \
                        or filters[items] == "warning" \
                        or filters[items] == "error":
                    if not result:
                        result = log
                    for dicts in log:
                        if filters[items] not in dicts["level"].lower():
                            result.remove(dicts)
            return J(result[:limit], 200)
        else:
            return J(log[:limit]), 200
    elif "text/html" in R.headers["Accept"]:
        return render_template(
            "api/events.html",
            log=log[:limit],
            nav=nav
        ), 200
    else:
        return "Bad request", 400


@app.errorhandler(413)
def request_entity_too_large(error):
    return J(error=str(error)), 413
