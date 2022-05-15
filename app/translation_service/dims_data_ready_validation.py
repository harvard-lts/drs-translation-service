import os, os.path, json, jsonschema, logging

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

def validate_json_schema(json_data):

    app_path = os.path.abspath(os.path.dirname(__file__))
    schemasdir = os.path.join(app_path, "schemas")
    
    logging.debug("Schemas dir: {}".format(schemasdir))
    print("Schemas dir: {}".format(schemasdir))
    
    if json_data is None:
        raise Exception("Missing JSON data in validate_json_schema")
        
    try:
        with open('{}/{}.json'.format(schemasdir, 'dims-data-ready')) as json_file:
            json_model = json.load(json_file)
    except Exception as e:
        logging.exception("Unable to get json schema model.")
        raise e
        
    try:
        jsonschema.validate(json_data, json_model)
    except json.decoder.JSONDecodeError as e:
        logging.exception("Invalid JSON format")
        raise e
    except jsonschema.exceptions.ValidationError as e:
        logging.exception("Invalid JSON schema:")
        raise e
    except Exception as e:
        logging.exception("Unable to validate json model.")
        raise e

