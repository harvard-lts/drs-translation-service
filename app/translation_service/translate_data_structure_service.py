import os, os.path, logging, shutil

logfile=os.getenv('LOGFILE_PATH', 'drs_translation_service')
loglevel=os.getenv('LOGLEVEL', 'WARNING')
logging.basicConfig(filename=logfile, level=loglevel)

def translate_data_structure(package_path):
    #/package_path/extracted
    extracted_files_dir = os.path.join(package_path, "extracted")
    #/package_path/extracted/unsippeddir
    extracted_files = os.listdir(extracted_files_dir)
    if (len(extracted_files) != 1):
        raise Exception("{} directory expected 1 item but found {}".format(extracted_files_dir, len(extracted_files)))    
    
    data_dir = os.path.join(extracted_files_dir, extracted_files[0], "data")
    if os.path.exists(data_dir):
        print("Moving content for {}".format(data_dir))
        logging.debug("Moving content for {}".format(data_dir))
        content_path = os.path.join(package_path, "content")
        if not os.path.exists(content_path):
            os.mkdir(content_path)
        _move_content_files(data_dir, content_path)
    else:
        print("No contents exist in {}".format(data_dir))
        logging.debug("No contents exist in {}".format(data_dir))
        
    doc_path = os.path.join(package_path, "documentation")
    if not os.path.exists(doc_path):
        os.mkdir(doc_path)
    _move_document_files(os.path.join(extracted_files_dir, extracted_files[0]), doc_path)
    
    #Move the DDI file (ends in XML)
    for f in os.listdir(package_path):
        if os.path.isfile(os.path.join(package_path, f)):
            if f.endswith(".xml"):
                _move_files(package_path, os.path.join(package_path, f), doc_path)
    return True

def _move_content_files(data_dir, content_path):
    _move_files(data_dir, data_dir, content_path)
    return True

def _move_files(root, source, dest_dir):
    '''This method actually copies the files from source to destination rather than
    moves them to preserve the original structure and to aid in error handling'''
    if (os.path.isfile(source)):
        print("Moving {} to {}".format(os.path.join(root, source), os.path.join(dest_dir, source)))
        logging.debug("Moving {} to {}".format(os.path.join(root, source), os.path.join(dest_dir, source)))
        shutil.copy2(os.path.join(root, source), os.path.join(dest_dir, os.path.basename(source)))
    else:
        for root, subdirs, files in os.walk(source):
            for subdir in subdirs:
                print("Subdir {} to {}".format(os.path.join(root, subdir), dest_dir))
                _move_files(os.path.join(root, subdir), os.path.join(root, subdir), dest_dir)
            for filename in files:
                print("File {} to {}".format(os.path.join(root, filename), os.path.join(dest_dir, filename)))
                shutil.copy2(os.path.join(root, filename), os.path.join(dest_dir, filename))

def _move_document_files(extracted_dir, doc_path):
    #Move the files in the extracted directory (bag-it info, manifest info)
    for f in os.listdir(extracted_dir):
        print(os.path.join(extracted_dir, f))
        if os.path.isfile(os.path.join(extracted_dir, f)):
            _move_files(extracted_dir, os.path.join(extracted_dir, f), doc_path)
        
    md_dir = os.path.join(extracted_dir, "metadata")
    if os.path.exists(md_dir):
        logging.debug("Moving docs for {}".format(md_dir))
        #Move the files in the metadata directory
        _move_files(md_dir, md_dir, doc_path)
    else:
        logging.debug("No docs exist in {}".format(md_dir))
    md_dir = os.path.join(extracted_dir, "metadata")
    return True

    
        
        
