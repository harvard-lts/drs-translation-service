import os, os.path, logging, shutil, glob
from pathlib import Path

logger = logging.getLogger('dts')


def translate_data_structure(package_path, supplemental_deposit_data, depositing_application):
    # Project name is the doi-name
    # Batch name doi-name-batch
    batch_name = os.path.basename(package_path) + "-batch"
    batch_dir = os.path.join(package_path, batch_name)
    # Object name is the doi-name
    object_name = os.path.basename(package_path)
    object_dir = os.path.join(batch_dir, object_name)

    aux_object_dir = os.path.join(package_path, "_aux", batch_name, object_name)
    os.makedirs(aux_object_dir, exist_ok=True)
    os.makedirs(object_dir, exist_ok=True)

    application_name = depositing_application
    is_extracted_package = "false"
    logger.debug("Depositing application: {}".format(depositing_application))
    if (application_name == "Dataverse"):
        is_extracted_package = os.getenv("EXTRACTED_PACKAGE_DVN", 'False').lower()
        content_model = os.getenv("DVN_CONTENT_MODEL", "opaque")
    elif (application_name == "ePADD"):
        content_model = os.getenv("EPADD_CONTENT_MODEL", "opaque_container")
    else:
        raise Exception("Unexpected application_name {}".format(application_name))
        
    if (content_model.lower() == "opaque"):
        __handle_opaque_directory_mapping(package_path, object_dir, aux_object_dir, is_extracted_package)
    elif (content_model.lower() == "opaque_container"):
        __handle_opaque_container_directory_mapping(package_path, object_dir, aux_object_dir)
    else:
        raise Exception("Content model {} is not yet supported".format(content_model))

    return batch_dir



def __handle_opaque_container_directory_mapping(package_path, object_dir, aux_object_dir):
    logger.debug("Formatting for opaque container content model")
    # Make object dir
    os.makedirs(object_dir, exist_ok=True)

    # Make content and documentation dirs
    content_dir = os.path.join(object_dir, "container")
    documentation_dir = os.path.join(object_dir, "documentation")
    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(documentation_dir, exist_ok=True)

    hascontent = False
    # Copy zip/gz/7z
    logger.debug("globbing...")

    for file in Path(package_path).glob('*.zip'):
        logging.debug("Found package: %s", file)
        filename = os.path.basename(file)
        if ".zip" in filename:
            shutil.copy2(file, os.path.join(content_dir, filename))
            hascontent = True

    for file in Path(package_path).glob('*.7z'):
        logging.debug("Found package: %s", file)
        filename = os.path.basename(file)
        if ".7z" in filename:
            shutil.copy2(file, os.path.join(content_dir, filename))
            hascontent = True
            
    for file in Path(package_path).glob('*.gz'):
        logging.debug("Found package: %s", file)
        filename = os.path.basename(file)
        if ".gz" in filename:
            shutil.copy2(file, os.path.join(content_dir, filename))
            hascontent = True
            
    __copy_project_conf_opaque_container(package_path)
    __copy_object_xml_and_rename_object(aux_object_dir, hascontent, True)





def __move_files(root_dir, source, dest_dir):
    '''This method actually copies the files from source to destination rather than
    moves them to preserve the original structure and to aid in error handling'''
    if (os.path.isfile(source)):
        logger.debug("Moving {} to {}".format(os.path.join(root_dir, source), os.path.join(dest_dir, source)))
        shutil.copy2(os.path.join(root_dir, source), os.path.join(dest_dir, os.path.basename(source)))
    else:
        for root, subdirs, files in os.walk(source):
            for subdir in subdirs:
                __move_files(os.path.join(root, subdir), os.path.join(root, subdir), dest_dir)
            for filename in files:
                shutil.copy2(os.path.join(root, filename), os.path.join(dest_dir, filename))


def __copy_project_conf_opaque(project_dir):
    project_conf = os.getenv("OPAQUE_PROJECT_CONF_TEMPLATE")
    shutil.copy2(project_conf, os.path.join(project_dir, "project.conf"))


def __copy_project_conf_opaque_container(project_dir):
    project_conf = os.getenv("OPAQUE_CONTAINER_PROJECT_CONF_TEMPLATE")
    shutil.copy2(project_conf, os.path.join(project_dir, "project.conf"))


def __copy_object_xml_and_rename_object(aux_object_dir, hascontent, is_opaque_container):
    if not hascontent:
        object_xml_template = os.getenv("OBJECT_XML_DOC_ONLY_TEMPLATE")
    elif is_opaque_container:
        object_xml_template = os.getenv("OPAQUE_CONTAINER_OBJECT_XML_TEMPLATE")
    else:
        object_xml_template = os.getenv("OPAQUE_OBJECT_XML_TEMPLATE")

    object_xml = os.path.join(aux_object_dir, "object.xml")
    object_name = os.path.basename(aux_object_dir)

    # Read in the template file
    with open(object_xml_template, 'r') as file:
        filedata = file.read()

    # Replace the object name
    filedata = filedata.replace('OBJECT_NAME', object_name)

    # Write the object.xml file out in the aux directory
    with open(object_xml, 'w') as file:
        file.write(filedata)
