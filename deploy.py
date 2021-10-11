#!/usr/local/bin/python3.9
""" ## Primary Application Deployment Script
       ------------------------------------

        >        𝕯𝖊𝖕𝖑𝖔𝖞𝖒𝖊𝖓𝖙
        _____

      ᵂʳⁱᵗᵗᵉⁿ ᵇʸ
          𝕁.ℂollin𝓈


    Purpose / Overview:
    ------------------
    It is from this script the WSGI Production- level   deployment   module  
    imports   the `deploy.server` object - itself imported & pulled from the
    `app` object — (i.e., the flask-derived [/`flask.Flask()`-esque]
    `dash.Dash()` main "app" [object]).For  Development-level  deployment ,
    simply run this script, like so:

        $ python deploy.py

            :   :   : ::::::: :   :   :

    Attributes:
    ----------
    quotes: list of (author, quote) tuples


        Code written by John Collins © 2021
          -------------------------------
"""
import logging
import random

from dash import dcc
from dash import html

from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from dash.exceptions import PreventUpdate

from seqapp import app # NOTE: `app.app` should be changed to `[your new app name].app` !
from seqapp import callbacks
from seqapp.layout import children as page_layout
from seqapp.utils import convert_html_to_dash


quotes = [("Carl Sagan", q) for q in [
    "Somewhere, something incredible is waiting to be known.",
    "For small creatures such as we, the vastness is bearable only through love.",
    "We're made of star stuff. We are a way for the cosmos to know itself.",
    "If you want to make an apple pie from scratch, you must first create the universe.",
    "Science is a way of thinking much more than it is a body of knowledge.",
    "Imagination will often carry us to worlds that never were. But without it we go nowhere.",
    "For me, it is far better to grasp the Universe as it really is than to persist in delusion, however satisfying and reassuring.",
    "We are like butterflies who flutter for a day and think it is forever.",
    "We live in a society exquisitely dependent on science and technology, in which hardly anyone knows anything about science and technology.",
    "Science is not only compatible with spirituality; it is a profound source of spirituality.",
]]

quotes += [("Frederick Sanger", q) for q in [
    "And indeed this theme has been at the centre of all my research since 1943,<br>both because of its intrinsic fascination and my conviction that a knowledge of sequences<br>could contribute much to our understanding of living matter.",
    "I and my colleagues here have been engaged in the pursuit of knowledge.",
]]

quotes += [("Albert Einstein", q) for q in [
    "What if one were to run after a ray of light? . . . What<br> if one were riding on the beam? . . . If one were to<br> run fast enough, would it no longer move at all? . . .",
    "I’ve completely solved the problem. My solution<br> was to analyze the concept of time. Time cannot be<br> absolutely defined, and there is an inseparable relation between time and signal velocity.",
]]

# quotes += [("[Your Idol]", q) for q in [
#     "Once said this interesting thing...",
# ]]


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"), Input("url", "href")],
    [State("page-content", "children")],
)
def display_page(pathname, href, current_page):
    """Activated upon url change, *react*ively returning new page components,
    as applicable. (I.e., User's browser tab does not actually reload when
    changing URL - unless of course it is the first load or a reload of the
    standard base application URL; applicable programmed changes are
    returned for certain expected non-standard, specific URL href path
    extensions.)


    Callbacks
    ---------
        ## Inputs
        pathname : str
            attr from `dcc.Location` | Current URL in user's browser tab address
            bar excluding the protocol [i.e. http], domain [i.e. localhost], &
            port [i.e. 9001 or 9999] and also any hash [i.e. '#[...]'] or
            search params [i.e. '?a=this&b=that']. E.g.,:
                >>> href.pathname
                >>> '/dash-webapp-template'
        href : str
            attr from `dcc.Location` | The complete URL currently in user's
            browser tab address bar (e.g.,
            'http://localhost:9001/dash-webapp-template/#log-in')

        ## States
        current_page : list
            components list attr from `html.Div` (id='page-content')
            Components list of what is currently displayed on UI page.
            Same callback parameter object as that returned. Required for
            checking if 'page-content' is empty or not (i.e., whether the
            callback is the first load vs. a subsequent URL change).

    Returns
    -------
    html.Div:
        Dash component App UI full main page's worth of components -
        arrayed via list attr 'children'

    Raises
    ------
    PreventUpdate
        Bypass any change in page components content when reacting
        to certain [URL] situations; for example in-page section
        links (i.e., enabling user-controlled rapid page scroll
        navigation)
    """

    # @cache.cached(timeout=TIMEOUT)
    def get_main_layout():
        """Function abstraction that returns unaltered main
        app layout of Dash-renderable to-be-React components.
        Useful for applying Flask Exstensions decorators,
        etc.

        Returns
        -------
        dash.html.Div: with param `children` = list of Dash components
        """
        return html.Div(page_layout, style={"textAlign": "center"})

    if not pathname:
        raise PreventUpdate
    if "#" in href and len(current_page) > 0:
        raise PreventUpdate
    elif any(
            tag in pathname.replace("/", "").lower()
            for tag in ["app", "dash-webapp-template"]): # allowed url href paths
        return get_main_layout()
    else:
        with open("static/error-pages/404.html") as error_404:
            parse_404 = "".join(error_404.readlines())
            author, quote, = random.choice(quotes)
            parse_404 = (
                parse_404 +
                f'<br><center><h6><i style="font-size: 80%; font-family: Montserrat, sans-serif; font-weight: 500">"{quote}"</i><br>—{author}</h6></center><br><br><br>'
            ).split("🌊")
            return html.Div([convert_html_to_dash(parse_404[0])] + [
                html.Img(
                    src="seqapp/assets/images/",
                    style={
                        "width": "40%",
                        "opacity": "0.75",
                        "borderRadius": "150px"
                    },
                )
            ] + [convert_html_to_dash(parse_404[1])] + [
                html.A(
                    "/dash-webapp-template/",
                    href="dash-webapp-template/",
                    style={"fontSize": "250%"})
            ] + [convert_html_to_dash(parse_404[2])])



app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content", children=[])
])


############################################
# #         D E P L O Y M E N T          # #
############################################

""" NOTE - Application Deployment:
 --------------------------------------
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   TWO PRINCIPAL MODES OF DEPLOYMENT AVAILABLE:
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  For best overview of details, see:
  - https://dash.plot.ly/deployment
  - http://docs.gunicorn.org/en/stable/deploy.html#nginx-configuration

  All new features are first developed in DEVELOPMENT mode!

  Successfully passed inspection following UI-based testing
  (including by non-developer end-user(s)) strictly required prior to
  any code changes (enhancements, bug fixes, package dependency version
  upgrades, etc.) being permitted to merge with master branch.

  Git link: https://github.com/jcollins-bioinfo/dash-webapp-template

  App app deployment as initiated herein is dependent on the
  following local absolute minimum .py files:
   [for: SERVER ACCESS]
   - app/wsgi.py
   - app/__init__.py
   - launch_gunicorn.sh
   [for: CONTENT DELIVERY] (reactively)
   - app/layout.py
   - app/callbacks.py

Feel free to reach out with any questions to:
    John C <jcollins.bioinformatics@gmail.com>
"""

############################################
# #  DEPLOYǂ MODE: DEVELOPMENT // DEBUG  # #
# # [ǂAs main (i.e.`python deploy.py`*)] # #
# # *Or:`python app`(see __main__.py) # #
############################################

logger = logging.getLogger(__name__)

logging.getLogger('matplotlib.font_manager').disabled = True



############################################
# #       DEPLOY* MODE: PRODUCTION       # #
# # [*WSGI import (e.g. Gunicorn+Nginx)] # #
############################################
if __name__ != "__main__":
    logging.basicConfig(
        format="%(asctime)s %(name)-12s %(module)s.%(funcName)s %(processName)s %(levelname)-8s %(relativeCreated)d %(message)s",
        level=logging.INFO)
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    app.logger.info(
        "Initializing dash-webapp-template (App) `app.server` for handoff..."
    )
    server = app.server