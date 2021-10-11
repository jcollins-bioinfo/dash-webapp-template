"""
WSGI
----
Web Service Gateway Interface

Deployment of the app in "production" mode.

"""

if __name__ == "__main__":

    import os
    import sys

    from deploy import server
    from seqapp import app


    gunicorn_wd = os.path.dirname(os.path.realpath(__file__))
    print(gunicorn_wd, file=sys.stderr)

    sys.path.append(gunicorn_wd)

    app.logger.info(
        "John Collins 2021 - Bioinformatics | dash-webapp-template :"
        " RUN SERVER (Production)"
    )
    server.run()