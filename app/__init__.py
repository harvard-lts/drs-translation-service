import logging
import os
from logging.handlers import RotatingFileHandler

import load_report_service.load_report_service as load_report_service
import mqresources.mqutils as mqutils
import werkzeug
from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump
from load_report_service.load_report_exception import LoadReportException
from mqresources.listener.process_ready_queue_listener import ProcessReadyQueueListener
from requests import Response

LOG_FILE_DEFAULT_PATH = os.getenv('LOGFILE_PATH', 'drs_translation_service')
LOG_FILE_DEFAULT_LEVEL = os.getenv('LOGLEVEL', 'WARNING')
LOG_FILE_MAX_SIZE_BYTES = 2 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 1


# App factory
def create_app():
    configure_logger()

    app = Flask(__name__)

    health = HealthCheck()
    envdump = EnvironmentDump()

    # add a check for the process mq connection
    def checkprocessmqconnection():
        connection_params = mqutils.get_process_mq_connection()
        if connection_params.conn is None:
            return False, "process mq connection failed"
        connection_params.conn.disconnect()
        return True, "process mq connection ok"

    # add a check for the drs mq connection
    def checkdrsmqconnection():
        connection_params = mqutils.get_drs_mq_connection()
        if connection_params.conn is None:
            return False, "drs mq connection failed"
        connection_params.conn.disconnect()
        return True, "drs mq connection ok"

    health.add_check(checkprocessmqconnection)
    health.add_check(checkdrsmqconnection)

    # add your own data to the environment dump
    def application_data():
        return {"maintainer": "Harvard Library Technology Services",
                "git_repo": "https://github.com/harvard-lts/drs-translation-service"}

    envdump.add_section("application", application_data)

    # Add a flask route to expose information
    app.add_url_rule("/healthcheck", "healthcheck", view_func=health.run)
    app.add_url_rule("/environment", "environment", view_func=envdump.run)

    @app.route('/loadreport', endpoint="loadreport")
    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def loadreport():
        args = request.args
        if ("filename" not in args):
            return 'Missing filename argument!', 400
        dryrun = False
        if ("dryrun" in args):
            dryrun = True
        try:
            load_report_service.handle_load_report(args['filename'], dryrun)
        except LoadReportException as lre:
            return "Handling of load report failed: {}".format(str(lre)), 400
        except Exception as e:
            return "Handling of load report failed: {}".format(str(e)), 500
        return "ok", 200

    @app.route('/failedBatch', endpoint="failedBatch")
    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def failedbatch():
        args = request.args
        if ("batchName" not in args):
            return 'Missing batchName argument!', 400
        dryrun = False
        if ("dryrun" in args):
            dryrun = True

        try:
            load_report_service.handle_failed_batch(args['batchName'], dryrun)
        except LoadReportException as lre:
            return "Handling of failed batch returned an error: {}".format(str(lre)), 400
        except Exception as e:
            return "Handling of failed batch returned an error: {}".format(str(e)), 500
        return "ok", 200

    disable_cached_responses(app)

    # Initializing queue listeners
    initialize_listeners()

    return app


def configure_logger():
    log_file_path = os.getenv('LOGFILE_PATH', LOG_FILE_DEFAULT_PATH)
    logger = logging.getLogger()

    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=LOG_FILE_MAX_SIZE_BYTES,
        backupCount=LOG_FILE_BACKUP_COUNT
    )
    logger.addHandler(file_handler)

    log_level = os.getenv('LOGLEVEL', LOG_FILE_DEFAULT_LEVEL)
    logger.setLevel(log_level)


def disable_cached_responses(app: Flask) -> None:
    @app.after_request
    def add_response_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response


def initialize_listeners():
    logging.debug("Creating Process Ready queue listener...")
    ProcessReadyQueueListener()
