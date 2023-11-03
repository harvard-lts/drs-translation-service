from batch_builder_service.batch_builder_service import BatchBuilderService
from translation_service.translation_exceptions import TranslationException
import os


ROLE_THESIS = "THESIS"
SUPPLEMENT = "SUPPLEMENT"
ROLE_SUPPLEMENT = "THESIS_SUPPLEMENT"
ROLE_LICENSE = "LICENSE"
ROLE_DOCUMENTATION = "DOCUMENTATION"
FILE_ROLE_ARCHIVAL_MASTER = "ARCHIVAL_MASTER"
RELATIONSHIP_HAS_SUPPLEMENT = "has_supplement"
RELATIONSHIP_HAS_LICENSE = "license"
RELATIONSHIP_HAS_DOCUMENTATION = "has_documentation"
class ETDBatchBuilderService(BatchBuilderService):
    
    def build_command(self, project_path, batch_name, supplemental_deposit_metadata):
        bb_script_name = os.getenv("BB_SCRIPT_NAME")
        command = "sh " + bb_script_name + " -a build -p " + project_path + " -b " + batch_name
        batch_prop_overrides = self._build_batchprop_override_command(supplemental_deposit_metadata)
        if batch_prop_overrides is not None:
            command += batch_prop_overrides
                    
        dirs = os.listdir(os.path.join(project_path, batch_name))
        object_prop_overrides = ""
        dir_prop_overrides = ""
        # Stores the thesis object name to do last
        # to allow for addition of the relationships
        thesis = None
        # To store the relationship values so they can be added to the thesis value
        self.relationships = []
        for object_name in dirs:
            if object_name.startswith("ETD_"):
                role = self.__determine_role(object_name)
                # If it is the thesis, hold it until the end to add the relationships
                if role == ROLE_THESIS:
                    thesis = object_name
                else:
                    self.__add_relationship(object_name, role)
                    obj_prop_overrides = self.__build_objprop_override_command(role, object_name, supplemental_deposit_metadata)
                    if obj_prop_overrides:
                        object_prop_overrides += obj_prop_overrides
                    
                file_prop_overrids = self._build_dirprop_override_command(os.path.join(project_path, batch_name, object_name), role)
                if file_prop_overrids:
                    dir_prop_overrides += file_prop_overrids
        
        if thesis is None:
            raise TranslationException("No thesis found in {}".format(project_path), None)
        
        thesis_overrides = self.__build_objprop_override_command(ROLE_THESIS, thesis, supplemental_deposit_metadata, self.relationships)
        if thesis_overrides is not None:
                object_prop_overrides += thesis_overrides

        if object_prop_overrides:
            command += " -objectprop \"{}\"".format(object_prop_overrides)

        if dir_prop_overrides:
            command += " -dirprop \"{}\"".format(dir_prop_overrides)
        return command
    
    def __build_objprop_override_command(self, object_role, object_name, supplemental_deposit_metadata, relationships = None):
        '''Builds the etd specific objprop overrides'''
        delimiter = "" 
        command = ""
        overrides = "ownerCode={}".format(supplemental_deposit_metadata["ownerCode"].rstrip())
        delimiter = ","
        overrides += "{}billingCode={}".format(delimiter,supplemental_deposit_metadata["billingCode"].rstrip())
        overrides += "{}urnAuthorityPath={}".format(delimiter,supplemental_deposit_metadata["urnAuthorityPath"].rstrip())
        overrides += "{}role={}".format(delimiter,object_role)

        if "embargo_date" in supplemental_deposit_metadata:
            overrides += "{}embargoBasis=license,embargoGrantStart={}".format(delimiter, supplemental_deposit_metadata["embargo_date"])

        # Relationsihps
        if relationships is not None:
            for rel in relationships:
                overrides += "{}{}={}".format(delimiter,rel.relationship_type, rel.object_name)

        # Put it all together
        if overrides:
            command = "{}::{};".format(object_name, overrides);
        return command
    
    def _build_dirprop_override_command(self, object_path, role):
        '''Builds the -dirprop command'''
        dirs = os.listdir(object_path)
        for dir in dirs:
            if os.path.isdir(os.path.join(object_path, dir)):
                filerole = FILE_ROLE_ARCHIVAL_MASTER
                if role == ROLE_DOCUMENTATION or role == ROLE_LICENSE:
                    filerole = role
                overrides = "filerole={};".format(filerole)
                return "{}::{}::{}".format(os.path.basename(object_path), dir, overrides)
        return ""
    
    def __determine_role(self, object_name):
        '''The OSN will have been formatted before the DAIS pipeline so
        the role will be extracted from the OSN name.'''
        if ROLE_THESIS in object_name and SUPPLEMENT not in object_name:
            return ROLE_THESIS
        elif SUPPLEMENT in object_name:
            return ROLE_SUPPLEMENT
        elif ROLE_LICENSE in object_name:
            return ROLE_LICENSE
        elif ROLE_DOCUMENTATION in object_name:
            return ROLE_DOCUMENTATION
        return None
    
    def __add_relationship(self, object_name, role):
        rel = None
        if role == ROLE_SUPPLEMENT:
            rel = RELATIONSHIP_HAS_SUPPLEMENT
        elif role == ROLE_LICENSE:
            rel = RELATIONSHIP_HAS_LICENSE
        elif role == ROLE_DOCUMENTATION:
            rel = RELATIONSHIP_HAS_DOCUMENTATION
        if rel is not None:
            r = Relationship(object_name, rel)
            self.relationships.append(r)
    
class Relationship:

    def __init__(self, object_name, relationship_type):
        self.object_name = object_name
        self.relationship_type = relationship_type
