import sys, os, pytest, logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import mqutils as mqutils
import mqlistener as mqlistener

logging.basicConfig(format='%(message)s')

def test_get_mq_connection():
    mq_conn = None
    mq_conn = mqutils.get_mq_connection()
    assert mq_conn is not None

def test_drs_listener():
    mqlistener.initialize_drslistener()


if __name__ == "__main__":
    test_get_mq_connection()
    test_drs_listener()
    print("Everything passed")