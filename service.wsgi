activate_this = '/var/www/CL_LineBot/env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/CL_LineBot')

from botregister import app as application