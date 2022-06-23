import os

import translation_service.translation_service as translation_service
from mqresources import mqutils
from mqresources.listener.mq_connection_params import MqConnectionParams
from mqresources.listener.stomp_listener_base import StompListenerBase


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
        try:
            # Trigger the mock services to 'run the drs ingest'
            mqutils.notify_mock_drs_trigger_message(message_body["package_id"])
            # This calls a method to handle prepping the batch for distribution to the DRS
            translation_service.prepare_and_send_to_drs(
                os.path.join(
                    message_body["destination_path"],
                    message_body["package_id"]
                ),
                message_body['admin_metadata']
            )
        except Exception:
            mqutils.notify_ingest_status_process_message(message_body.get("package_id"), "failure")
            self._logger.exception(
                "Could not translate data structure for {}".format(message_body.get("destination_path"))
            )

        self._acknowledge_message(message_id, message_subscription)
