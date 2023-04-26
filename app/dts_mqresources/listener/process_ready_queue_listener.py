import os, traceback

import translation_service.translation_service as translation_service
from dts_mqresources import mqutils
from dts_mqresources.listener.mq_connection_params import MqConnectionParams
from dts_mqresources.listener.stomp_listener_base import StompListenerBase
from translation_service.translation_exceptions import TranslationException

import notifier.notifier as notifier


class ProcessReadyQueueListener(StompListenerBase):

    def _get_queue_name(self) -> str:
        return os.getenv('PROCESS_QUEUE_CONSUME_NAME')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('PROCESS_MQ_HOST'),
            mq_port=os.getenv('PROCESS_MQ_PORT'),
            mq_user=os.getenv('PROCESS_MQ_USER'),
            mq_password=os.getenv('PROCESS_MQ_PASSWORD')
        )

    def _handle_received_message(self, message_body: dict, message_id: str, message_subscription: str) -> None:
        self._logger.debug("************************ PROCESS READY LISTENER - ON_MESSAGE ************************")
        self._logger.debug(
            "Received message from Process Queue. Message body: {}. Message id: {}".format(
                str(message_body),
                message_id
            )
        )
        self._acknowledge_message(message_id, message_subscription)
        try:
            testing = False
            if "testing" in message_body:
                testing = True
            # This calls a method to handle prepping the batch for distribution to the DRS
            translation_service.prepare_and_send_to_drs(
                os.path.join(
                    message_body["destination_path"],
                    message_body["package_id"]
                ),
                message_body['admin_metadata'],
                message_body['application_name'],
                testing
            )
        except TranslationException as te:
            emails = message_body["admin_metadata"]["failureEmail"]
            if te.emailaddress:
                emails += "," + te.emailaddress
            exception_msg = traceback.format_exc()
            self.send_error_notifications(message_body, te, exception_msg, emails)
        except Exception as e:
            failureEmail = message_body["admin_metadata"]["failureEmail"]
            exception_msg = traceback.format_exc()
            self.send_error_notifications(message_body, e, exception_msg, failureEmail)
            
    def send_error_notifications(self, message_body, exception, exception_msg, emails):
        mqutils.notify_ingest_status_process_message(message_body.get("package_id"), "failure")
        msg = "Could not process export for DRSIngest for {}.  Error {}.".format(message_body.get("destination_path"), str(exception))
        failureEmail = message_body["admin_metadata"]["failureEmail"]
        notifier.send_error_notification(str(e), body, emails)
        