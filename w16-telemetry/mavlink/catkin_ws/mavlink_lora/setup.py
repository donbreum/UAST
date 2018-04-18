from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
  scripts=['scripts/mavlink_lora_get_param_list.py'],)
setup(**d)

