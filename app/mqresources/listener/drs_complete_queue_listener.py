import os

from mqresources import mqutils
from mqresources.listener.mq_connection_params import MqConnectionParams
from mqresources.listener.stomp_listener_base import StompListenerBase


class DrsCompleteQueueListener(StompListenerBase):

    def _get_queue_name(self) -> str:
        return os.getenv('DRS_QUEUE_CONSUME_NAME')

    def _get_mq_connection_params(self) -> MqConnectionParams:
        return MqConnectionParams(
            mq_host=os.getenv('DRS_MQ_HOST'),
            mq_port=os.getenv('DRS_MQ_PORT'),
            mq_user=os.getenv('DRS_MQ_USER'),
            mq_password=os.getenv('DRS_MQ_PASSWORD')
        )

    def _handle_received_message(self, message_body: dict, message_id: str, message_subscription: str) -> None:
        self._logger.debug("************************ DRS COMPLETE LISTENER - ON_MESSAGE ************************")
        self._logger.debug(
            "Received message from DRS Queue. Message body: {}. Message id: {}".format(
                str(message_body),
                message_id
            )
        )
        try:
            # Send ingest status message to process queue
            # TODO - this will have to get pull the actual URN once it is available
            urn = "https://nrs-dev.lts.harvard.edu/URN-3:HUL.TEST:101113553"
            mqutils.notify_ingest_status_process_message(
                message_body["package_id"],
                message_body["batch_ingest_status"],
                urn
            )
        except Exception:
            mqutils.notify_ingest_status_process_message(message_body.get("package_id"), "failure")

        self._acknowledge_message(message_id, message_subscription)
