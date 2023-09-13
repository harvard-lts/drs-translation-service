import logging
from content_model_mapping.audio_content_model_mapping import AudioContentModelMapping
from content_model_mapping.document_content_model_mapping import DocumentContentModelMapping
from content_model_mapping.stillimage_content_model_mapping import StillImageContentModelMapping
from content_model_mapping.text_content_model_mapping import TextContentModelMapping


class ContentModelMappingBuilder():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("ContentModelMappingBuilder initialized")

    def get_content_model_mapping(self, package_path):

        content_model = None
        # get the content model from the package path
        # by inspecting mime type of the files
        # example code snippet:
        # https://github.huit.harvard.edu/LTS/etds/blob/ba9a05cbf2ed25ff9f50d28503b849edb9ceec8e/bin/etds2drs.py#L698
        
        if content_model == "text":
            return TextContentModelMapping()
        elif content_model == "stillimage":
            return StillImageContentModelMapping()
        elif content_model == "document":
            return DocumentContentModelMapping()
        elif content_model == "audio":
            return AudioContentModelMapping()
        else:
            raise Exception("Unknown content model: " + content_model)