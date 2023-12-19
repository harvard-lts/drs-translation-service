from celery import Celery
import os

app1 = Celery()
app1.config_from_object('etdtestceleryconfig')

arguments = {"feature_flags": {
            'dash_feature_flag': "off",
            'alma_feature_flag': "off",
            'send_to_drs_feature_flag': "off",
            'drs_holding_record_feature_flag': "off"},
            "pqid": "30522803",
            "object_id": "123456789"}

res = app1.send_task('etd-alma-drs-holding-service.tasks.add_holdings',
                     args=[arguments], kwargs={},
                     queue=os.getenv("ETD_HOLDING_QUEUE_NAME"))
