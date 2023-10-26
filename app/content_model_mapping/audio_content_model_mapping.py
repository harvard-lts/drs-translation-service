import os
import shutil
import glob
from content_model_mapping.content_model_mapping import ContentModelMapping

class AudioContentModelMapping(ContentModelMapping):
    def handle_directory_mapping(self, package_path, object_dir, aux_object_dir):
        '''Moves the audio into the audio directory'''
        self.logger.debug("Formatting for audio content model")
        audio_dir = os.path.join(object_dir, "audio")
        if not os.path.exists(audio_dir):
            os.mkdir(audio_dir)

        suffixes = ["wav", "mp3", "mp4", "aifc", "m2a", "zip", "xml"]

        self.logger.debug("globbing...")

        self.logger.debug("globbing...")
        for suffix in suffixes:
            for file in glob.glob(os.path.join(package_path, '*.' + suffix)):
                self.logger.debug("Found package: %s", file)
                filename = os.path.basename(file)
                if f".{suffix}" in filename:
                    shutil.copy2(file, os.path.join(audio_dir, filename))

        project_conf = os.getenv("AUDIO_PROJECT_CONF_TEMPLATE")        
        object_xml_template = os.getenv("AUDIO_OBJECT_XML_TEMPLATE")
        self._handle_project_conf_and_object_xml(package_path, aux_object_dir, project_conf, object_xml_template)

    def handle_single_file_directory_mapping(self, filename_path, target_filename, package_path, object_dir, aux_object_dir):
        content_dir = os.path.join(object_dir, "audio")
        if not os.path.exists(content_dir):
            os.mkdir(content_dir)
        shutil.copy2(filename_path, os.path.join(content_dir, os.path.basename(target_filename)))

        project_conf = os.getenv("AUDIO_PROJECT_CONF_TEMPLATE")        
        object_xml_template = os.getenv("AUDIO_OBJECT_XML_TEMPLATE")
        self._handle_project_conf_and_object_xml(package_path, aux_object_dir, project_conf, object_xml_template)