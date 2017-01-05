# settings to make the population scripts find the django application

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

SETUP_SETTINGS = ["DJANGO_SETTINGS_MODULE", "beauticart.settings"] # change to own applcation name.settings
