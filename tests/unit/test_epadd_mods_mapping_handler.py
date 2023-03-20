import jsonschema, json, pytest, sys
sys.path.append('app')
from translation_service.epadd_mods_mapping_handler import EpaddModsMappingHandler

def test_valid_json():
    '''Verifies that the supplied mods mapping file is valid'''
    
    try: 
        epadd_mods_handler = EpaddModsMappingHandler()
        epadd_mods_handler.validate_json_schema()
        assert True
    except Exception:
        assert False
        
def test_build_object_overrides():
    '''Verifies that the overrides are being built properly.'''
    
    try: 
        epadd_mods_handler = EpaddModsMappingHandler()
        expected = "identifier=eas-0001,titleInfoTitle=EAS Project Email Collection,abstract=Scope and content: EAS Test Scope and Content.Description: EAS Test Email Description.,Format version: MBOX version 1.2.13.Format name: MBOX.Overall unique attachment count: 2.,originInfoDateCreated=2012-05-16/2020-12-07,embargoGrantStart=2023-03-15,embargoDuration=2,embargoDurationUnit=years"
        overrides = epadd_mods_handler.build_object_overrides("/home/appuser/tests/data/samplemods/epaddobject", "epaddobject")
        assert overrides == expected
    except Exception:
        assert False