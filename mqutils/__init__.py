from flask import Flask
from healthcheck import HealthCheck, EnvironmentDump
import mqutils.mqutils as mqutils

'''This class is currently entirely for the purpose of providing
a healthcheck '''

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
    return app
