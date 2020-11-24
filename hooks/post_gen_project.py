import logging
import os
import shutil
import sys

logger = logging.getLogger()
BASE_DIR = os.getcwd()


def clean_extra_package_management_files():
    """Removes either requirements files and folder or the Pipfile."""
    use_pipenv = "{{cookiecutter.use_pipenv}}"
    to_delete = []

    if use_pipenv == "yes":
        to_delete = to_delete + ["{{cookiecutter.project_name}}/requirements.txt", "{{cookiecutter.project_name}}/requirements"]
    try:
        for file_or_dir in to_delete:
            if os.path.isfile(file_or_dir):
                os.remove(file_or_dir)
            else:
                shutil.rmtree(file_or_dir)
    except OSError as error:
        logger.warning("Error: {0}".format(error))
        sys.exit(1)


def install_debug_tools():
    debug = "{{cookiecutter.debug}}"

    if int(debug):
        filenames = [os.path.join(BASE_DIR, "requirements_dev.txt")]
        try:
            with open(os.path.join(BASE_DIR, 'requirements.txt'), 'a') as outfile:
                #print(outfile.read())
                for fname in filenames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)
        except OSError as error:
            logger.warning("Error: {0}".format(error))
            sys.exit(1)


if __name__ == "__main__":
    pass
