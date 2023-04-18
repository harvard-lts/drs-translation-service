import os, os.path, json, jsonschema, logging

logger = logging.getLogger('dts')
def validate_json_schema(json_data):

    app_path = os.path.abspath(os.path.dirname(__file__))
    schemasdir = os.path.join(app_path, "schemas")
    
    logger.debug("Schemas dir: {}".format(schemasdir))
    print("Schemas dir: {}".format(schemasdir))
    
    if json_data is None:
        raise Exception("Missing JSON data in validate_json_schema")
        
    try:
        with open('{}/{}.json'.format(schemasdir, 'dims-data-ready')) as json_file:
            json_model = json.load(json_file)
    except Exception as e:
        raise e
        
    try:
        jsonschema.validate(json_data, json_model)
    except json.decoder.JSONDecodeError as e:
        raise e
    except jsonschema.exceptions.ValidationError as e:
        raise e
    except Exception as e:
        raise e

