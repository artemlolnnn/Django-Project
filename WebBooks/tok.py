import os
from pathlib import Path


secret_password = open(os.path.join(Path(__file__).resolve().parent, 'NewApp/secret_password.txt'), 'r').readline()

token = secret_password