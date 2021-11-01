import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 

print(ROOT_DIR)

CONFIG_PATH = os.path.join(ROOT_DIR, 'databases','config.py')
print(CONFIG_PATH) 