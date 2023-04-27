import os, os.path, logging, json, jsonschema, shutil
import xml.etree.ElementTree as ET
from pyunpack import Archive
from pathlib import Path
from translation_service.translation_exceptions import EpaddModsHandlingException
from translation_service.translation_exceptions import MissingEmbargoBasisException
from datetime import date

'''
Parses and assigns values using the associated mapping file
'''
class EpaddModsMappingHandler:
        
    def __init__(self):
        
        self.logger = logging.getLogger('dts')
        self.mapping_file_validated = False
        
        
        
    def build_object_overrides(self, project_path, object_name, embargoBasis, emailAddress=None):
        #validate if it hasn't been  validated yet
        if not self.mapping_file_validated:
            self.validate_json_schema()
            
        #Unzip the zip file
        extracted_path = self.__unzip_object(project_path)
        if extracted_path is None:
            self.logger.warning("Could not find a compressed file to extract for MODS data in {}.".format(project_path))
            return ""
        
        cm_file_path = self.__find_collection_metadata_file(extracted_path)     
        if cm_file_path is None:
            self.logger.warning("Could not find a collection_metadata.json file in {}.".format(extracted_path))
            
        premis_file_path = self.__find_premis_file(extracted_path)     
        if premis_file_path is None:
            self.logger.warning("Could not find a epaddPremis.json file in {}.".format(extracted_path))
        
        if cm_file_path is None and premis_file_path is None:
            return ""
        
        cm_overrides = {}
        premis_overrides = {} 
        for mapping in self.mapping_data["mapping"]:
            if (mapping['property-type'] == "object"):
                #Loop through the mapping details array and collect the overrides from each filetype
                for mapping_details in mapping['mapping-details']:
                    if mapping_details['epadd-file'] == 'collection-metadata':
                        if cm_file_path:
                            cm_overrides = self.__build_collection_metadata_overrides(mapping_details['mapping-values'], cm_file_path, embargoBasis, emailAddress)
                    elif mapping_details['epadd-file'] == 'epaddPremis':
                        if premis_file_path:
                            premis_overrides = self.__build_epadd_premis_overrides(mapping_details['mapping-values'], premis_file_path, emailAddress)
                    else: 
                        raise EpaddModsHandlingException("Data from {} is not implemented.".format(mapping_details['epadd-file']), emailAddress)
        override_dict = cm_overrides
        #Both cm and premis overrides
        if override_dict and premis_overrides:
            for premis_override_key in premis_overrides:
                if premis_override_key in override_dict:
                    override = override_dict[premis_override_key]
                    override += "," + premis_overrides[premis_override_key]
                    override_dict[premis_override_key] = override
                else:
                    override_dict[premis_override_key] = premis_overrides[premis_override_key]
        #only premis
        elif premis_overrides:
            override_dict = premis_overrides
        
        shutil.rmtree(extracted_path)
        overrides = ""
        delimiter = "" 
        
        for val in override_dict:  
            overrides += "{}{}={}".format(delimiter, val, override_dict[val])
            delimiter = ","    
        return overrides
            
                
    def __build_collection_metadata_overrides(self, mapping_values_array, cm_file_path, embargoBasis, emailAddress):
        with open(cm_file_path, 'r') as f:
            cm_json = json.load(f)
        
        override_dict = {}
        for mapping_values in mapping_values_array:
            epadd_value = mapping_values["epadd-field"]
            if epadd_value not in cm_json:
                continue
            
            #get the collection metadata value from the cm json
            cm_value = cm_json[epadd_value]
            
            if "date-format-field" in mapping_values:
                #Convert from ms to s 
                cm_value = int(cm_value)/1000
                cm_value = date.fromtimestamp(cm_value).isoformat()
            
            #Set the final value for now        
            final_val =  cm_value
            
            if "epadd-field-2" in mapping_values:
                epadd_value_2 = mapping_values["epadd-field-2"]
                cm_value2 = cm_json[epadd_value_2]
                if "date-format-field-2" in mapping_values:
                    #Convert from ms to s 
                    cm_value2 = int(cm_value2)/1000
                    cm_value2 = date.fromtimestamp(cm_value2).isoformat()

                if "concatenation-delimiter" in mapping_values:
                    delimiter = mapping_values["concatenation-delimiter"]
                    final_val = "{}{}{}".format(cm_value, delimiter, cm_value2)
                else:
                    final_val = "{}{}".format(cm_value, cm_value2)
                
            if "conditional" in mapping_values:
                cond_array = mapping_values["conditional"].split("=")
                if len(cond_array) != 2:
                    raise EpaddModsHandlingException("Conditional must be of format key=value.  Conditional supplied is {}.".format(mapping_values["conditional"]), emailAddress)
                cond_key = cond_array[0]
                cond_val = cond_array[1]
                for val in epadd_value:
                    if cond_key in cm_value and cm_value[cond_key] == cond_val:
                        if "value_field" in mapping_values:
                            final_val = cm_value[mapping_values["value_field"]]
                        else:
                            raise EpaddModsHandlingException("Value must be supplied if Collection Metadata conditional is set.  CM value: {} .".format(cm_value), emailAddress)             

            if "label" in mapping_values and final_val:
                final_val = mapping_values['label'] + ": " + final_val + "."
           
            
            #Embargo has to be parsed to two different BB fields and mapping wasn't straight forward.
            if epadd_value == "embargoDuration":
                #If not embargoBasis is supplied, fail the batch
                if not embargoBasis:
                    raise MissingEmbargoBasisException("embargoBasis was not set in drsConfig.txt but embargoDuration of {} is present in the collection-metadata.json file .".format(cm_value), emailAddress)  
                retval_dict = self.__format_embargo(cm_value)
                if len(retval_dict) == 2:
                    override_dict.update(retval_dict)
            else:
                if epadd_value == "embargoStartDate":
                    #If embargoBasis is not supplied, fail the batch
                    if not embargoBasis:
                        raise MissingEmbargoBasisException("embargoBasis was not set in drsConfig.txt but embargoStartDate of {} is present in the collection-metadata.json file .".format(cm_value), emailAddress)  
                    #Account for embargoBasis if it is supplied and there is a start date
                    else:
                        override_dict["embargoBasis"] = embargoBasis
                        
                bb_field = mapping_values["bb-field"]
                if bb_field in override_dict:
                    if final_val:
                        final_val = final_val + override_dict[bb_field] 
                    else:
                        final_val = override_dict[bb_field] 
                
                #As long as it isn't empty    
                if final_val:    
                    override_dict[bb_field] = final_val
            
        return override_dict
    
    def __format_embargo(self, embargoDuration):
        override_dict = {}
        embargo_array = embargoDuration.split()
        permitted_durations = ["day", "days", "month", "months", "year", "years"]
        if len(embargo_array) == 2:
            try:
                int(embargo_array[0])
                override_dict["embargoDuration"] = embargo_array[0]
                if embargo_array[1] in permitted_durations:
                    override_dict["embargoDurationUnit"] = embargo_array[1]
                else:
                    self.logger.error("Embargo duration unit {} must be one of {}".format(embargo_array[1], permitted_durations))
                    return {}
            except Exception:
                self.logger.error("Embargo duration {} must be an int".format(embargo_array[0]))
        else:
            self.logger.error("Embargo duration {} was not mapped because it does not meet the format of '# days|months|years'".format(embargoDuration))
        return override_dict 
    
    def __build_epadd_premis_overrides(self, mapping_values_array, premis_file_path, emailAddress):
        with open(premis_file_path, 'r') as f:
            tree = ET.parse(f)
            epaddpremisroot = tree.getroot()
        
        premis_ns = {"premis": os.getenv("PREMIS_NS", "http://www.loc.gov/premis/v3")}
        override_dict = {}
        for mapping_values in mapping_values_array:
            epadd_value = mapping_values["epadd-field"]
            search_field = ".//premis:{}".format(epadd_value)
            premis_value = epaddpremisroot.findall(search_field, premis_ns)
            final_val = ""
            for value in premis_value:
                if "conditional" in mapping_values:
                    value_field = ""
                    if "value_field" in mapping_values:
                        value_field = mapping_values["value_field"]
                    else:
                        raise EpaddModsHandlingException("Value must be supplied if Premis element has children.  Premis value: {} .".format(premis_value.tag), emailAddress) 
                    
                    cond_array = mapping_values["conditional"].split("=")
                    if len(cond_array) != 2:
                        raise EpaddModsHandlingException("Conditional must be of format key=value.  Conditional supplied is {}.".format(mapping_values["conditional"]), emailAddress)
                    
                    cond_key = cond_array[0]
                    cond_val = cond_array[1]
                    
                    cond_search_field = ".//premis:{}".format(cond_key)
                    child_cond_elt = value.find(cond_search_field, premis_ns)
                    if child_cond_elt is not None and cond_val == child_cond_elt.text:
                        value_search_field = ".//premis:{}".format(value_field)
                        value_elt = value.find(value_search_field, premis_ns)
                        if value_elt is not None:
                            final_val = value_elt.text
                else:
                    if "value_field" in mapping_values:
                        value_field = mapping_values["value_field"]
                        value_search_field = ".//premis:{}".format(value_field)
                        value_elt = value.find(value_search_field, premis_ns)
                        if value_elt is not None:
                            final_val = value_elt.text
                    else:
                        final_val = value.text       
                            

            if "label" in mapping_values and final_val:
                final_val = mapping_values['label'] + ": " + final_val + "."
           
            bb_field = mapping_values["bb-field"]
            if bb_field in override_dict:
                final_val = final_val + override_dict[bb_field] 
            
            #As long as it isn't empty    
            if final_val:    
                override_dict[bb_field] = final_val
            
        return override_dict
    
    
    def __find_collection_metadata_file(self, extracted_path):
        cm_file_name = os.getenv("EPADD_COLLECTION_METADATA_FILE_NAME")
        if cm_file_name is not None:
            for file in Path(extracted_path).rglob(cm_file_name):
                return file
        return None
                
    def __find_premis_file(self, extracted_path):
        premis_file_name = os.getenv("EPADD_PREMIS_FILE_NAME")
        if premis_file_name is not None:
            for file in Path(extracted_path).rglob(premis_file_name):
                return file
        return None
    
    def __unzip_object(self, project_path):
        for file in Path(project_path).rglob('*.7z'):
            logging.debug("Found file: %s", file)
            print("found {}".format(file))
            extracted_path = os.path.join(project_path, "extracted")
            Archive(file).extractall(extracted_path, True)
            return extracted_path

        for file in Path(project_path).rglob('*.zip'):
            logging.debug("Found file: %s", file)
            extracted_path = os.path.join(project_path, "extracted")
            Archive(file).extractall(extracted_path, True)
            return extracted_path
        
        for file in Path(project_path).rglob('*.gz'):
            logging.debug("Found file: %s", file)
            extracted_path = os.path.join(project_path, "extracted")
            Archive(file).extractall(extracted_path, True)
            return extracted_path
        return None
    
    def validate_json_schema(self):

        mapping_file = os.getenv("EPADD_MODS_MAPPING_FILE")
        with open(mapping_file) as user_file:
            file_contents = user_file.read()
  
        self.mapping_data = json.loads(file_contents)
        schema = os.getenv("MODS_MAPPING_SCHEMA")
        
        if not schema:
            raise Exception("Missing env definition: MODS_MAPPING_SCHEMA")
            
        try:
            with open(schema) as json_file:
                json_model = json.load(json_file)
        except Exception as e:
            raise e
            
        try:
            jsonschema.validate(self.mapping_data, json_model)
        except json.decoder.JSONDecodeError as e:
            raise e
        except jsonschema.exceptions.ValidationError as e:
            raise e
        except Exception as e:
            raise e
        
        self.mapping_file_validated = True