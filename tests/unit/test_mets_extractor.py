import sys
sys.path.append('app')
from translate_data_structure.mets_extractor import MetsExtractor


def test_mets_extraction():
    mets_extractor = MetsExtractor("/home/appuser/tests/data/etd-submission-2/mets.xml")
    amdid_mimetype = mets_extractor.get_amdid_and_mimetype(
        "TurkeyandtheEU-EuropeanSoftPowerandHowItHasImpactedTurkey.pdf")
    assert amdid_mimetype is not None
    assert amdid_mimetype.amdid == "amd_primary"
    assert amdid_mimetype.mimetype == "application/pdf"
    
    degree_date = mets_extractor.get_degree_date()
    expected_date = "2011"
    assert expected_date == degree_date

    identifier = mets_extractor.get_identifier()
    expected_identifier = "1496780"
    assert expected_identifier == identifier