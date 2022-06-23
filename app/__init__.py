import load_report_service.load_report_service as load_report_service
import mqresources.mqutils as mqutils
import werkzeug
from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump
from load_report_service.load_report_exception import LoadReportException
from requests import Response


# App factory
def create_app():
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

    return app


def disable_cached_responses(app: Flask) -> None:
    @app.after_request
    def add_response_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response
