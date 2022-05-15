import jsonschema, json, pytest, sys
sys.path.append('app')
import translation_service.dims_data_ready_validation as dims_data_ready_validation

def test_valid_json():
    msg_json = {
        "package_id": "12345",
        "application_name": "Dataverse",
        "destination_path": "/home/appuser/dropbox",
        "admin_metadata": {"original_queue": "myqueue", "retry_count":0}
    }
    
    try: 
        dims_data_ready_validation.validate_json_schema(msg_json)
        assert True
    except Exception:
        assert False

def test_valid_json_extra_admin_params():
    msg_json = {
        "package_id": "12345",
        "application_name": "Dataverse",
        "destination_path": "/home/appuser/dropbox",
        "admin_metadata": {"original_queue": "myqueue", "retry_count":0, "extra_admin_param": "should be valid"}
    }
    
    try: 
        dims_data_ready_validation.validate_json_schema(msg_json)
        assert True
    except Exception:
        assert False
    
def test_invalid_json_missing_param():
    with pytest.raises(jsonschema.exceptions.ValidationError):
        msg_json = {
            "package_id": "12345",
            "destination_path": "/home/appuser/dropbox",
            "admin_metadata": {"original_queue": "myqueue", "retry_count":0}
        }
    
        dims_data_ready_validation.validate_json_schema(msg_json)

def test_valid_json_extra_param():
    msg_json = {
         "package_id": "12345",
        "application_name": "Dataverse",
        "destination_path": "/home/appuser/dropbox",
        "extra_param": "should not fail",
        "admin_metadata": {"original_queue": "myqueue", "retry_count":0}
    }
    
    try: 
        dims_data_ready_validation.validate_json_schema(msg_json)
        assert True
    except Exception:
        assert False