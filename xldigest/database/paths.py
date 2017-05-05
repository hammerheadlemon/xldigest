import os
import appdirs

APPNAME = 'xldigest'
APPAUTHOR = 'MRLemon'
USER_DATA_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
USER_HOME = os.path.expanduser('~')
DB_PATH = os.path.join(USER_DATA_DIR, 'db.sqlite')
