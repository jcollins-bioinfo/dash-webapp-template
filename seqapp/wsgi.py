import os
import sys

gunicorn_wd = os.path.dirname(os.path.realpath(__file__))
print(gunicorn_wd, file=sys.stderr)

sys.path.append(gunicorn_wd)

from . import app
from deploy import server

if __name__ == "__main__":
    app.logger.info(
        "John Collins 2021 - Bioinformatics | dash-webapp-template : RUN SERVER (Production)"
    )
    server.run()