# -*- coding:utf-8 -*-
import os
import sys
os.environ["USER_SETTINGS"] = "config.settings"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)



from src import script


if __name__ == '__main__':

    script.run()
