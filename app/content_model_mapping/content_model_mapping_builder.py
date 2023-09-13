import logging
from content_model_mapping.audio_content_model_mapping import AudioContentModelMapping
from content_model_mapping.document_content_model_mapping import DocumentContentModelMapping
from content_model_mapping.stillimage_content_model_mapping import StillImageContentModelMapping
from content_model_mapping.text_content_model_mapping import TextContentModelMapping


class ContentModelMappingBuilder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("ContentModelMappingBuilder initialized")

    def get_content_model_mapping(self, content_model):
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