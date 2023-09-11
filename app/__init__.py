import logging, traceback
import os, os.path
from logging.handlers import TimedRotatingFileHandler
from load_report_service.load_report_service_builder import LoadReportServiceBuilder
from translation_service.translation_service_builder import TranslationServiceBuilder
import werkzeug
from flask import Flask, request
from healthcheck import HealthCheck, EnvironmentDump
from load_report_service.load_report_exception import LoadReportException
from translation_service.translation_exceptions import TranslationException
from requests import Response
import notifier.notifier as notifier

LOG_FILE_BACKUP_COUNT = 1
LOG_ROTATION = "midnight"


# App factory
def create_app():
    configure_logger()

    app = Flask(__name__)

    health = HealthCheck()
    envdump = EnvironmentDump()

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
        if ("dropbox" not in args):
            return 'Missing dropbox argument!', 400
        dryrun = False
        if ("dryrun" in args):
            dryrun = True
        try:
            builder = LoadReportServiceBuilder()
            load_report_service = builder.get_load_report_service(args['dropbox'])
            load_report_service.handle_load_report(args['filename'], dryrun)
        except LoadReportException as lre:
            msg = "Handling of load report failed: {}".format(str(lre))
            exception_msg = traceback.format_exc()
            body = msg + "\n" + exception_msg
            notifier.send_error_notification(str(lre), body)
            return msg, 400
        except Exception as e:
            msg = "Handling of load report failed: {}".format(str(e))
            exception_msg = traceback.format_exc()
            body = msg + "\n" + exception_msg
            notifier.send_error_notification(str(e), body)
            return msg, 500
        return "ok", 200

    @app.route('/failedBatch', endpoint="failedBatch")
    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def failedbatch():
        args = request.args
        if ("batchName" not in args):
            return 'Missing batchName argument!', 400
        if ("dropbox" not in args):
            return 'Missing dropbox argument!', 400
        dryrun = False
        if ("dryrun" in args):
            dryrun = True

        try:
            builder = LoadReportServiceBuilder()
            load_report_service = builder.get_load_report_service(args['dropbox'])
            load_report_service.handle_failed_batch(args['batchName'], dryrun)
        except LoadReportException as lre:
            msg = "Handling of failed batch returned an error: {}".format(str(lre))
            exception_msg = traceback.format_exc()
            body = msg + "\n" + exception_msg
            notifier.send_error_notification(str(lre), body)
            return msg, 400
        except Exception as e:
            msg = "Handling of failed batch returned an error: {}".format(str(e))
            exception_msg = traceback.format_exc()
            body = msg + "\n" + exception_msg
            notifier.send_error_notification(str(e), body)
            return msg, 500
        return "ok", 200
    
    @app.route('/reprocess_batches', endpoint="reprocess_batches")
    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def reprocess_batches():
        args = request.args
        logging.getLogger('dts').debug("Reprocess args")
        logging.getLogger('dts').debug(args)
        
        if ("unprocessed_exports" not in args):
            return 'Missing unprocessed_exports argument in data!', 400
        
        #Don't actually reprocess if it is a dryrun
        if ("dryrun" not in args):
            try: 
                unprocessed_exports = args.getlist('unprocessed_exports')
                for batch_path in unprocessed_exports:
                    logging.getLogger('dts').debug("Reprocessing {}".format(batch_path))
                    reprocess_batch(batch_path)
                
            except Exception as e:
                msg = "Reprocessing of data failed: {}".format(str(e))
                exception_msg = traceback.format_exc()
                body = msg + "\n" + exception_msg
                notifier.send_error_notification(str(e), body)
                return msg, 500
        return "ok", 200


    disable_cached_responses(app)

    return app


def configure_logger():
    log_level = os.getenv("LOGLEVEL", "WARNING")
    log_file_path = os.getenv("LOGFILE_PATH", "/home/appuser/epadd-curator-app/logs/dts.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when=LOG_ROTATION,
        backupCount=LOG_FILE_BACKUP_COUNT
    )
    logger = logging.getLogger('dts')
        
    logger.addHandler(file_handler)
    file_handler.setFormatter(formatter)
    logger.setLevel(log_level)
        


def disable_cached_responses(app: Flask) -> None:
    @app.after_request
    def add_response_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response

def reprocess_batch(batch_path):
    logging.getLogger('dts').debug("Reprocessing: " + batch_path)
    
    admin_metadata = {}
    batch_as_array = batch_path.split("/")
    dropbox_name = batch_as_array[-3]

    try:
        builder = TranslationServiceBuilder()
        translation_service = builder.get_translation_service(dropbox_name)
    except TranslationException as te:
        msg = "Handling of failed batch returned an error: {}".format(str(te))
        exception_msg = traceback.format_exc()
        body = msg + "\n" + exception_msg
        notifier.send_error_notification(str(te), body)
        return msg, 400
    except Exception as e:
        msg = "Handling of failed batch returned an error: {}".format(str(e))
        exception_msg = traceback.format_exc()
        body = msg + "\n" + exception_msg
        notifier.send_error_notification(str(e), body)
        return msg, 500
    drs_config_path = os.path.join(batch_path, "drsConfig.txt")
    admin_metadata = translation_service.get_admin_metadata(drs_config_path)

    # If errors were caught while trying to parse the drsConfig file
    # then move exit
    if not admin_metadata:
        return
    admin_metadata["dropbox_name"] = dropbox_name            
    # This calls a method to handle prepping the batch for distribution to the DRS
    translation_service.prepare_and_send_to_drs(
        batch_path,
        admin_metadata,
        False
    )


