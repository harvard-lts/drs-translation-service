"""
This module defines a StompInteractor, which is an abstract class intended
to define common behavior for stomp-implemented MQ components.
"""
import logging
from abc import ABC, abstractmethod

import stomp
from mqresources.listener.mq_connection_exception import MqConnectionException
from mqresources.listener.mq_connection_params import MqConnectionParams


class StompInteractor(ABC):
    __STOMP_CONN_HEARTBEATS_MS = 40000
    __STOMP_CONN_TIMEOUT_MS = 5000

    def __init__(self) -> None:
        self._logger = logging.getLogger()

    def _create_mq_connection(self) -> stomp.Connection:
        """
        Creates a stomp.Connection to MQ.

        :raises MqConnectionException
        """
        mq_connection_params = self._get_mq_connection_params()

        mq_host = mq_connection_params.mq_host
        mq_port = mq_connection_params.mq_port
        mq_user = mq_connection_params.mq_user
        mq_password = mq_connection_params.mq_password

        self._logger.debug("Creating MQ connection... Host: " + mq_host + ", port: " + mq_port)
        try:
            connection = stomp.Connection(
                host_and_ports=[(mq_host, mq_port)],
                heartbeats=(self.__STOMP_CONN_HEARTBEATS_MS, self.__STOMP_CONN_HEARTBEATS_MS),
                keepalive=True
            )

            connection.set_ssl([(mq_host, mq_port)])

            connection.connect(
                mq_user,
                mq_password,
                wait=True,
                timeout=self.__STOMP_CONN_TIMEOUT_MS
            )

            self._logger.debug("MQ connection created. Host: " + mq_host + ", port: " + mq_port)
            return connection

        except Exception as e:
            self._logger.error(str(e))
            raise MqConnectionException(
                queue_host=mq_host,
                queue_port=mq_port,
                reason=str(e)
            )

    @abstractmethod
    def _get_mq_connection_params(self) -> MqConnectionParams:
        """
        Retrieves the MQ connection params necessary for creating the connection
        """

    @abstractmethod
    def _get_queue_name(self) -> str:
        """
        Retrieves the name of the queue to be interacted with
        """
