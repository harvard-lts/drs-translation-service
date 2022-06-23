from dataclasses import dataclass


@dataclass
class MqConnectionParams:
    mq_host: str
    mq_port: str
    mq_user: str
    mq_password: str
