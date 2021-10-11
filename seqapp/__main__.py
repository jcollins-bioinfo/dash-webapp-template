"""Development-level deployment ("DEBUG-MODE")

This file allows for the following execution:

	>$ python -m app

where `app` is the super package (top-level module) housed at:
	/var/www/Apps/dash-webapp-template

    (so in this case 'seqapp'):

    >$ python -m seqapp
.

"""
import logging

from deploy import app, server

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.logger.debug(
        "JCollins 2021 - Bioinformatics | dash-webapp-template Initialized [DEVELOPMENT - DEBUG MODE]."
    )
    app.run_server(
        host="0.0.0.0", port=9999, debug=True, dev_tools_hot_reload=True)