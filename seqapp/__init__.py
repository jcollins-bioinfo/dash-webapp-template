"""
# dash-webapp-template

`app`

## John Collins | Bioinformatics

A Custom [fill-in w/ description] Web Application
---------------------------------------------------
_Further description / overview_


Attributes
----------
app : dash.Dash
  app object
cache : flask_caching.Cache
  Flask caching object
logger : logging.Logger
    custom, thorough per-RUN ('session') logging
py_version : float
    Current Python version (must be 3.7+)
TIMEOUT : int
    default [browser-]cache timeout in seconds


Deleted Attributes
------------------
auth : HTTP BasicAuth supplemental security layer
ch : logging command-line streamer
server : Flask server object

             _____________________
                 ~John Collins~
                   © 2 0 2 1
                    ✧✵ ✺ ✵✧
                       ❉

"""
import os
import logging
import sys

# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import dash
# from flask_caching import Cache

logger = logging.getLogger(__name__)


# REQUIRES PYTHON 3.7+
py_version = float(".".join([str(x) for x in sys.version_info[:2]]))
print(f"Python version = {py_version}", file=sys.stderr)
if py_version < 3.7:
    raise Exception(
        f"Python3.7+ required! Current (wrong) version: {sys.version_info}")



########################################
#  A P P - S E R V E R  S T A R T U P  #
########################################

app = dash.Dash(
    __name__,
    index_string=
    """<!DOCTYPE html>\n<html>\n    <head>\n          <meta charset="UTF-8"><meta name="description" content="John Collins Plotly Dash Webapp Template Demonstration">  <meta name="keywords" content="John Collins, Bioinformatics, DNA Sequencing Analysis">  <meta name="author" content="John Collins, Bioinformatics"><meta name="viewport" content="width=device-width, initial-scale=1"> <meta name="theme-color" content="#317EFB"/>\n        <title>Dash Web App Template | John Collins Bioinformatics Pipelines - Web Apps | [Custom Title Here]</title>\n        {%favicon%}\n        {%css%}\n    </head>\n    <body>\n        {%app_entry%}\n        <footer>\n            {%config%}\n           {%scripts%} {%renderer%}\n        </footer>\n   </body>\n</html>""",
)


########################################
#        M E M O I Z A T I O N         #
########################################
# __Ref__ : __t(s)__
# 1K days = 86400000
# 90 days =  7776000
# 3 weeks =  1814400
# 7  days =   604800
# 1   day =    86400
# 4   hrs =    14400
# 1    hr =     3600
# 10  min =      600
# TIMEOUT = 50000
# cache = Cache(
#     app.server,
#     config={
#         "CACHE_TYPE": "filesystem",  # "memcached",
#         "CACHE_DIR": "./.flask-cache/",
#         "CACHE_DEFAULT_TIMEOUT": TIMEOUT,
#     },
# )


########################################
#     D A S H  A P P  C O N F I G      #
########################################

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config["suppress_callback_exceptions"] = True
