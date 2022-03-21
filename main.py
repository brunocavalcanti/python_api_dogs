import json
from flask import Flask, make_response, Response, jsonify
from flask_mongoengine import MongoEngine
from app.controller.dog import configure
from app.kafka.report.report_consumer import ReportConsumer
from threading import Thread
from werkzeug.exceptions import HTTPException, InternalServerError

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_exception(err):
    resp: Response = make_response("response")
    resp.content_type = 'application/json'
    if isinstance(err, HTTPException):
        resp.data = json.dumps({
            "code": err.code,
            "name": err.name,
            "description": err.description,
        })
        resp.status_code = err.code

    else:
        internal = InternalServerError()
        resp.data = json.dumps({
            "code": internal.code,
            "name": internal.name,
            "description": f"internal server error: {str(err)}",
        })
        resp.status_code = internal.code

    return resp


def create_app():
    app.config.update(
        API_TITLE='My application API',
        DEBUG=True,
        TRAP_HTTP_EXCEPTIONS=True,
        PROPAGATE_EXCEPTIONS=False,
        API_VERSION="v1",
        OPENAPI_VERSION="2.0",
        MONGODB_SETTINGS={
            'db': 'dogs',
            'host': 'localhost',
            'port': 27017
        }
    )
    db = MongoEngine()
    db.init_app(app)
    app.register_blueprint(configure())
    consumer = ReportConsumer()
    consumer_process = Thread(target=consumer.start, args=())
    consumer_process.start()
    app.run()

    return app


create_app()
