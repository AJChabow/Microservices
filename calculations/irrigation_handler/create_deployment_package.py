import shutil
import os

source_dir = os.path.curdir
output_filename = "deployment_lam_package"

shutil.make_archive(output_filename, 'zip', source_dir)
