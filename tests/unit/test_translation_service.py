import pytest, sys, os.path
sys.path.append('app')
import translation_service.translation_service as translation_service 

def test_translate_data_structure():
    assert translation_service.translation_data_structure()
    