"""
This module defines a StompListenerBase, which is an abstract class intended
to define common behavior for stomp-implemented MQ listener components.
"""
import json
import logging
from abc import abstractmethod, ABC

import stomp
from mqresources.listener.stomp_interactor import StompInteractor
from stomp.utils import Frame
from tenacity import retry, before_log, wait_exponential, stop_after_attempt


class StompListenerBase(stomp.ConnectionListener, StompInteractor, ABC):
    __STOMP_CONN_MIN_RETRY_WAITING_SECONDS = 2
    __STOMP_CONN_MAX_RETRY_WAITING_SECONDS = 10
    __STOMP_CONN_MAX_ATTEMPTS = 36

    __ACK_CLIENT_INDIVIDUAL = "client-individual"

    def __init__(self) -> None:
        super().__init__()
        self.__reconnect_on_disconnection = True
        self._connection = self.__create_subscribed_mq_connection()

    def on_message(self, frame: Frame) -> None:
        message_id = frame.headers['message-id']
        message_subscription = frame.headers['subscription']
        try:
            message_body = json.loads(frame.body)
            self._handle_received_message(message_body, message_id, message_subscription)
        except json.decoder.JSONDecodeError as e:
            self._logger.error(str(e))
            self._unacknowledge_message(message_id, message_subscription)

    def on_error(self, frame: Frame) -> None:
        self._logger.info("MQ error received: " + frame.body)

    def on_disconnected(self) -> None:
        self._logger.debug("Disconnected from MQ")
        if self.__reconnect_on_disconnection:
            self._logger.debug("Reconnecting to MQ...")
            self.reconnect()

    def reconnect(self) -> None:
        self.__reconnect_on_disconnection = True
        self._connection = self.__create_subscribed_mq_connection()

    def disconnect(self) -> None:
        self.__reconnect_on_disconnection = False
        self._connection.disconnect()

    @abstractmethod
    def _handle_received_message(self, message_body: dict, message_id: str, message_subscription: str) -> None:
        """
        Handles the received message by adding child listener specific logic.

        :param message_body: received message body
        :type message_body: dict
        :param message_id: received message id
        :type message_id: str
        :param message_subscription: received message subscription
        :type message_subscription: str
        """

    def _acknowledge_message(self, message_id: str, message_subscription: str) -> None:
        """
        Informs the MQ that the message was consumed

        :param message_id: message id
        :type message_id: str
        :param message_subscription: message subscription
        :type message_subscription: str
        """
        self._logger.info("Setting message with id {} as acknowledged...".format(message_id))
        self._connection.ack(id=message_id, subscription=message_subscription)

    def _unacknowledge_message(self, message_id: str, message_subscription: str) -> None:
        """
        Informs the MQ that the message was not consumed

        :param message_id: message id
        :type message_id: str
        :param message_subscription: message subscription
        :type message_subscription: str
        """
        self._logger.info("Setting message with id {} as unacknowledged...".format(message_id))
        self._connection.nack(id=message_id, subscription=message_subscription)

    @retry(
        wait=wait_exponential(
            multiplier=1,
            min=__STOMP_CONN_MIN_RETRY_WAITING_SECONDS,
            max=__STOMP_CONN_MAX_RETRY_WAITING_SECONDS
        ),
        stop=stop_after_attempt(__STOMP_CONN_MAX_ATTEMPTS),
        before=before_log(logging.getLogger(), logging.INFO)
    )
    def __create_subscribed_mq_connection(self) -> stomp.Connection:
        connection = self._create_mq_connection()
        connection.subscribe(destination=self._get_queue_name(), id=1, ack=self.__ACK_CLIENT_INDIVIDUAL)
        connection.set_listener('', self)
        return connection
