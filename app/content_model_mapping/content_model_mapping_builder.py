import logging
from content_model_mapping.audio_content_model_mapping import AudioContentModelMapping
from content_model_mapping.document_content_model_mapping import DocumentContentModelMapping
from content_model_mapping.stillimage_content_model_mapping import StillImageContentModelMapping
from content_model_mapping.text_content_model_mapping import TextContentModelMapping
from content_model_mapping.etd_opaque_content_model_mapping import ETDOpaqueContentModelMapping
from subprocess import check_output
import os

class ContentModelMappingBuilder():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("ContentModelMappingBuilder initialized")

    def get_content_model_mapping(self, package_path, filename):

        content_model = None
        # get the content model from the package path
        # by inspecting mime type of the files
        # example code snippet:
        # https://github.huit.harvard.edu/LTS/etds/blob/ba9a05cbf2ed25ff9f50d28503b849edb9ceec8e/bin/etds2drs.py#L698
        content_model = self.__get_content_model(package_path, filename)
        
        if content_model == "text":
            return TextContentModelMapping()
        elif content_model == "image":
            return StillImageContentModelMapping()
        elif content_model == "document":
            return DocumentContentModelMapping()
        elif content_model == "audio":
            return AudioContentModelMapping()
        elif content_model == "opaque":
            return ETDOpaqueContentModelMapping("False")
        else:
            raise Exception("Unknown content model: " + content_model)
   
    def __get_content_model(self, package_path, filename):
        '''Get the content model from the package path'''
        mime_type = check_output(['file', '-b', '--mime-type', os.path.join(package_path, filename)]).strip().decode()

        try: 
            return {
				# this is not a complete list
				'application/pdf': 'document',
				'text/plain': 'text',
				'text/xml': 'text',
				'text/sgml': 'text',
				'image/jpeg': 'image',
				'image/jp2': 'image',
				'image/gif': 'image',
				'image/tiff': 'image',
				'image/x-photo-cd': 'image',
				'audio/x-aiff': 'audio',
				'audio/x-wave': 'audio',
				'audio/mpeg': 'audio',
				'audio/mp4': 'audio',
				'application/vnd.rn-realmedia': 'audio'
				}[mime_type]
        except:
            return 'opaque'