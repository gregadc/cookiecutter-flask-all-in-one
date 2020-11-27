import logging
import os
import shutil
import sys

logger = logging.getLogger()
BASE_DIR = os.getcwd()


def install_debug_tools():
    debug = "{{cookiecutter.debug}}"

    if int(debug):
        filenames = [os.path.join(BASE_DIR, "requirements_dev.txt")]
        try:
            with open(os.path.join(BASE_DIR, 'requirements.txt'), 'a') as outfile:
                for fname in filenames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)
        except OSError as error:
            logger.warning("Error: {0}".format(error))
            sys.exit(1)


if __name__ == "__main__":
    pass
