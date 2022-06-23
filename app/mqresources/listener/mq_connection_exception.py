from mqresources.listener.mq_exception import MqException


class MqConnectionException(MqException):
    def __init__(self, queue_host: str, queue_port: str, reason: str) -> None:
        message = f"An error occurred while connecting to MQ on host {queue_host}, port {queue_port}"
        if reason:
            message = message + f". Reason was: {reason}"
        super().__init__(message)
