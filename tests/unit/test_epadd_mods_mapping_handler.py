import jsonschema, json, pytest, sys
sys.path.append('app')
from translation_service.epadd_mods_mapping_handler import EpaddModsMappingHandler
from translation_service.translation_exceptions import MissingEmbargoBasisException

def test_valid_json():
    '''Verifies that the supplied mods mapping file is valid'''
    
    try: 
        epadd_mods_handler = EpaddModsMappingHandler()
        epadd_mods_handler.validate_json_schema()
        assert True
    except Exception:
        assert False
        
def test_build_object_overrides_with_embargo_basis():
    '''Verifies that the overrides are being built properly.'''
    
    try: 
        epadd_mods_handler = EpaddModsMappingHandler()
        expected = "identifier=eas-0001,titleInfoTitle=EAS Project Email Collection,abstract=Scope and content: EAS Test Scope and Content.Description: EAS Test Email Description.,Format version: MBOX version 1.2.13.Format name: MBOX.Overall unique attachment count: 2.,originInfoDateCreated=2012-05-16/2020-12-07,embargoBasis=Harvard policy,embargoGrantStart=2023-03-15,embargoDuration=2,embargoDurationUnit=years"
        embargoBasis="Harvard policy"
        overrides = epadd_mods_handler.build_object_overrides("/home/appuser/tests/data/samplemods/epaddobject", "epaddobject", embargoBasis)
        print(overrides)
        assert overrides == expected
    except Exception:
        assert False
        
def test_build_object_overrides_without_embargo_basis_with_embargo_data():
    '''Verifies that the overrides are being built properly.'''
    
    try: 
        epadd_mods_handler = EpaddModsMappingHandler()
        expected = "identifier=eas-0001,titleInfoTitle=EAS Project Email Collection,abstract=Scope and content: EAS Test Scope and Content.Description: EAS Test Email Description.,Format version: MBOX version 1.2.13.Format name: MBOX.Overall unique attachment count: 2.,originInfoDateCreated=2012-05-16/2020-12-07"
        embargoBasis=None
        with pytest.raises(MissingEmbargoBasisException):
            overrides = epadd_mods_handler.build_object_overrides("/home/appuser/tests/data/samplemods/epaddobject", "epaddobject", embargoBasis)
            assert overrides == expected
    except Exception:
        assert False