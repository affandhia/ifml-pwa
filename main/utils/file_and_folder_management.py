from pathlib import Path
import os
import logging
import shutil

logger_ff = logging.getLogger("utils.file_and_folder_management")

'''Still have a problem, if there are already existing file inside
still not yet handled
'''

DELIMITER = '/'


def create_new_file(filename, path, content):
    target_path = Path(path)
    file_with_target_path = target_path / filename
    if path_is_exist(file_with_target_path):
        logger_ff.error("FAILED creating {file}, already exists".format(
            file=str(file_with_target_path)))
        raise FileExistsError(
            "FAILED creating {file}".format(file=str(file_with_target_path)))
    else:
        f = open(file_with_target_path, 'w+')
        f.write(content)
        logger_ff.info(
            'CREATED {file}'.format(file=str(file_with_target_path)))


def create_new_directory(foldername, path):
    generated_folder_target = Path(path) / foldername
    try:
        if path_is_exist(path) and (not is_file(path)):
            os.mkdir(generated_folder_target)
            logging.debug('CREATED directory. ' + str(generated_folder_target))
    except OSError:
        logging.error(
            'FAILED creating directory. ' + str(generated_folder_target))
        raise FileExistsError(
            "FAILED creating {file}".format(file=str(generated_folder_target)))


def copy_file_to_target_folder(source_path, target_path):
    try:
        shutil.copyfile(source_path, target_path)
        logging.debug('SUCCESS copy into ' + target_path)
    except Exception as e:
        logging.error(str(e))


def is_directory(path):
    target_path = Path(path)
    return target_path.is_dir()


def is_file(path):
    target_path = Path(path)
    return target_path.is_file()


def path_is_exist(path):
    target_path = Path(path)
    return target_path.exists()


def directory_is_empty(path):
    target_path = Path(path)
    return os.listdir(target_path) == []


def path_joiner(path):
    final_path = ''
    if isinstance(path, list):
        final_path = DELIMITER.join(path)
    elif isinstance(path, str):
        final_path = path
    return final_path
