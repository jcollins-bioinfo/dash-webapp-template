"""'Callbacks' are what enable the "reactive" functionality
of a Python Dash web application (literally, the react.js).
Every time a user interacts with a UI component on the web
app page in their browser, a callback with matching Input
(via the component's 'id' attribute) from this module is
activated, thus allowing customized programmed reactions
to any individual and/or series of any [possible combi-
nation of] user actions.


> dash-webapp-template
>    C a l l b a c k s
>          𝕄𝕠𝕕𝕦𝕝𝕖
> ண⎤꜒𓇃𓇃𓇃ཥ⅌ཤ𓇃𓇃𓇃𓋏ཀཫ𓋏𓇃𓇃𓇃╗╔𓇃𓇃𓆽⦄༽⸶⸷༼⦃𓆽𓇃𓇃𓇃𓇊𓊢ༀ࿐࿓𓇊࿑

## John Collins GitHub Public Repos — dash-webapp-template

To learn more about callbacks, see:
https://dash.plot.ly/getting-started-part-2

>                         ୡ      ୡୡ         ୡ
>                   ◖𓇃ⴶ〰⸅‖⸄〰ж𓇃𓇃𓇃𓇃⸠⎫𓏉⎧⸡𓇃𓇃𓇃𓏟𓏞𓇃𓇃╗╔𓇃𓇃𓇃𓐩𓋥⸶⸷𓋥𓐩◗
>         ୡ     ୡ                 ୡୡ
>      ◖𓇃𓇃𓇃𓏣🜾𓏣𓇃𓇃𓉽𓇃𓎸𓈌𓎹𓇃⎨⎬𓇃˥⎡𓇃𓇃࿅𓇃𓊢ꃊ𓊢𓇃𓇃𓇃◗

Attributes:
----------
    logger (logging.Logger):
        Current session log file
    version (str):
        Current git-committed source codebase version

               ____________________________
    ୡ
𓇃𓏣🜾𓏣𓇃࿑

"""
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from flask import Flask
from werkzeug.routing import Rule

from .config import *

from .utils import *
from seqapp import app

import config
from config import *

import bioinfo as bioinformatics
from bioinfo import pipeline, visualization
from bioinfo.pipeline import (
    parse_contents,
)

version = VERSION

logger = logging.getLogger(__name__)


########################################
#  S T A N D A R D  F U N C T I O N S  #
########################################
""" See the app.utils module & also the /app/config init file
    for some of the more general, non-reactive functions which may
    nonetheless be imported and used in the callbacks below.
"""


########################################
#    F L A S K  F U N C T I O N S      #
########################################
""" The dash.Dash() app object is itself at its core a flask app
    object, too; thus, all of the [vast] Flask source code
    functionalities are compatible as-is with Dash apps.
"""

app.server.url_map.add(Rule('/', endpoint='downloadZAll'))
app.server.url_map.add(Rule('/', endpoint='urlToDownload'))

@app.server.endpoint("/downloadZAll")
def download_all_selected():
    """Send path from directory to allow user to
    download zipped files as an attachment.

    Returns:
        File download directly to user's PC.
    """
    value = flask.request.args.get("value")
    fbn = f"{os.path.basename(value)}"
    app.logger.info(f"🗽| REQUEST TO DOWNLOAD: for [zipped] server file @ {value}")
    return flask.send_from_directory(
        directory=f"{os.path.dirname(value)}",
        filename=fbn,
        attachment_filename=fbn,
        as_attachment=True,
        mimetype="zip",
    )


@app.server.endpoint("/urlToDownload")
def download_file():
    """Send path from directory to allow user
       to download file as an attachment.

    Returns:
    """
    value = flask.request.args.get("value")
    fbn = f"{os.path.basename(value)}"
    app.logger.info(f"🗽| REQUEST TO DOWNLOAD: for server file @ {value}")
    mime = "text/plain" if "png" not in value else "image/png"
    return flask.send_from_directory(
        directory=f"{os.path.dirname(value)}",
        filename=fbn,
        attachment_filename=fbn,
        as_attachment=True,
        mimetype=mime,
    )


########################################
#  C A L L B A C K  F U N C T I O N S  #
########################################
""" Every callback function is preceded by a special `@app.callback`
    Python decorator function, which necessarily has an Output() and
    at least one Input() parameter (both objects from dash.dependencies).
    Optionally, a callback function decorator can also contain a
    State() parameter (also imported from dash.dependencies).

    Typically, the return of a callback function is an html.Div()
    object containing a list of updated components to be returned to
    the UI via the 'id' attribute indicated on the Output() object
    of callback decorator.

    For a helpful overview on Python decorators, see:
    https://realpython.com/primer-on-python-decorators/
"""

@app.callback(
    Output(f"user-login-confirmation", "children"),
    [
        Input(f"sign-on-submit", "n_clicks"),
        Input(f"input-user-name", "value"),
        Input(f"clear-pipeline", "n_clicks"),
        Input(f"session", "data"),
        Input(f"log-out-submit", "n_clicks")
    ],
    [State(f"sign-on-submit", "n_clicks_timestamp")],
)
def confirm_new_session(
    n_clicks,
    user_sign_on,
    clear_n_clicks,
    session_data,
    logout,
    login_timestamp,
):
    """Responsive components generation for user sign-on at top of app UI page.

    Parameters
    ----------
    n_clicks : int
        Total cumulative count of clicks 'submit' (sign-in) button
    user_sign_on : str
        Selected user name from sign on dropdown
    clear_n_clicks : int
        Total cumulative count of clicks clear pipeline button
    session_data : Dash.dcc.Store(type='session')
        Dash HTTP client-side memory caching, "Session" type (auto-cleared when
        browser tab closes [but *not* on Refresh's]).
    logout : int
        Total cumulative count of clicks logout button
    login_timestamp : int
        Timestamp at most recent sign on button click as integer
        (e.g., 1572843293129)

    """
    if user_sign_on == "None" and logout < 1:
        raise PreventUpdate

    if not user_sign_on:
        return [
            html.H6(
                "Please sign in to create a new session.",
                style={"fontSize": "1.2rem", "fontWeight": "300"},
            )
        ]

    try:
        enter_user = session_data["current_user"]
        user_proper = session_data["user_proper"]
        putat_user = user_sign_on[0] + user_sign_on.split("_")[0].lower()[1:]
        try:
            prev_user = session_data[f"SIGN_ON-№{n_clicks-1}"]
        except KeyError as e:
            prev_user = "NONE"
        app.logger.debug(f"Recorded user name: {enter_user} (Prev. user={prev_user})")
        if login_timestamp:
            submit_t_elapsed = tns() / 1e9 - login_timestamp / 1e3
            app.logger.debug(f"USER LOGIN : `submit_t_elapsed` = {submit_t_elapsed}")
        else:
            submit_t_elapsed = 0  # <1 ≡ No recent sign in!
        if (
            user_sign_on == enter_user
            or session_data["user_logged_in"] == "True"
        ) and submit_t_elapsed < 1:
            log_t_init = session_data["login_t_init"]
            session_log_file = session_data["session_log_file"]
            RUN_ID = session_data["RUN_ID"]
            app.logger.info(
                f"* C R E A T E D  N E W  'Current SESSION OUTPUT DIR' *\n{session_data['PATH_TO_SESSION_OUTPUT']}"
            )
            return html.Details(
                [
                    html.Div(
                        [
                            html.Span(
                                f"Active User Account — {enter_user.replace('_', ' ').title()}",
                                style={
                                    "fontSize": "1.2rem",
                                    "fontFamily": "'Open Sans', sans-serif",
                                    "fontWeight": "300",
                                    "color": "#304479",
                                },
                            ),
                            html.Span(
                                className="fader-line-short", style={"marginBottom": "20px"}
                            ),
                            html.P("You're all set!"),
                            html.H6(f"Sign-on Timestamp: {log_t_init.split('=')[1]}", style={"fontSize": "0.65rem"}),
                            html.P(
                                f"Session ID:\t{RUN_ID}",
                                style={
                                    "animation": "anim-text-flow-keys 60s infinite linear",
                                    "mixBlendMode": "difference",
                                    "fontSize": "0.7rem",
                                },
                            ),
                        ],
                        className="updates-list",
                    ),
                    html.Summary(
                        html.Code(
                            f"✔ LOGGED IN",
                            style={"color": "rgb(24, 230, 112)"},
                            className="updates-header",
                        )
                    ),
                ],
                id="logged-in-status",
            )
        elif n_clicks > 1 and prev_user != "None yet.." and enter_user != prev_user:
            return [
                html.Br(),
                html.H4(
                    f"{putat_user}, would you like to sign on [& log out {prev_user}]?",
                    style={"display": "block"},
                ),
                html.P(f"🧙🧠🗲⚛ 👌📓⬸📖🖊", style={"fontSize": "3rem"}),
            ]

    except Exception as e:
        user_proper = "⚠:[USER_UNKNOWN!]"
        app.logger.warning(f"Note: Exception raised during user sign on: {e}")

    return [
        html.Br(),
        html.H6("Sign In ( ⮩️🚪✨ ) to create a new, blank output directory for your analysis."),
    ]


@app.callback(
    Output(f"input-user-name", "value"),
    [
        Input(f"log-out-submit", "n_clicks"),
        Input(f"log-back-in-submit", "n_clicks"),
    ],
    [
        State(f"log-out-submit", "n_clicks_timestamp"),
        State(f"sign-on-submit", "n_clicks_timestamp"),
        State(f"log-back-in-submit", "n_clicks_timestamp"),
        State(f"sign-on-submit", "n_clicks"),
        State(f"local", "data"),
    ],
)
def log_out_or_comeback(
    logout,
    quick_logback,
    log_out_timestamp,
    sign_on_timestamp,
    logback_on_timestamp,
    signon,
    user_profile,
):
    """Enable USER "Log Out" functionality.

    Parameters
    ----------
    logout : int
        Total cumulative count of clicks log out button
    quick_logback : int
        Total cumulative count of clicks "Return" button
    log_out_timestamp : int
        Timestamp of last user click log out button
    sign_on_timestamp : int
        Timestamp of last user click sign-in button
    logback_on_timestamp : int
        Timestamp of last user click "Return" button
    signon : int
        Total cumulative count of clicks user sign-in button
    user_profile : Dash.dcc.Store(type='local')
        Browser-cached local app memory, containing stored saved
        user "profile" info / stats.
    """
    if not user_profile:
        raise PreventUpdate
    if logout < 1 and quick_logback < 1:
        raise PreventUpdate
    if quick_logback > 0:
        if signon > 0 and logout > 0:
            if logback_on_timestamp > max(log_out_timestamp, sign_on_timestamp):
                return user_profile["userAccount"]
        elif signon < 1:
            return user_profile["userAccount"]
    elif logout > 0 and signon > 0:
        if log_out_timestamp > sign_on_timestamp:
            return "None"


@app.callback(
    [
        Output(f"session", "data"),
        Output(f"local", "data"),
    ],
    [
        Input(f"sign-on-submit", "n_clicks"),
        Input(f"log-out-submit", "n_clicks"),
        Input(f"clear-pipeline", "n_clicks"),
    ],
    [
        State(f"input-user-name", "value"),
        State(f"session", "data"),
        State(f"local", "data"),
        State(f"initiate-pipeline", "n_clicks"),
        State(f"initiate-pipeline", "n_clicks_timestamp"),
        State(f"clear-pipeline", "n_clicks_timestamp"),
        State(f"sign-on-submit", "n_clicks_timestamp"),
        State(f"refresh-uploads", "n_clicks_timestamp"),
        State(f"log-out-submit", "n_clicks_timestamp"),
    ],
)
def record_user_name(
    login_n_clicks,
    logout_n_clicks,
    clear_pl_n_clicks,
    user_selection,
    data,
    local_cache,
    init_pl_n_clicks,
    initiate_pipeline_timestamp,
    clear_pipeline_timestamp,
    user_login_timestamp,
    refresh_uploads_timestamp,
    log_out_timestamp,
):
    """Upon user sign on (or sign off), correspondingly update the cached
    information describing the current user (e.g., name, proper name, sign
    in history, etc.) and create and store a new RUN ID for the current
    session, as applicable.

    Args:
        login_n_clicks (int):
            Total cumulative count of clicks user sign-in button
        logout_n_clicks (int):
            Total cumulative count of clicks log out button
        clear_pl_n_clicks (int):
            Total cumulative count of clicks clear results button
        user_selection (str):
            Selected value from user names dropdown in app log-in section
        data (Dash.dcc.Store):
            [Session] HTTP client-side memory cache
        local_cache (Dash.dcc.Store):
            [Local] HTTP client-side memory cache
        init_pl_n_clicks (int):
            Total cumulative count of clicks initiate step 2 pipeline button
        initiate_pipeline_timestamp (int):
            Timestamp of last user click initiate step 2 pipeline button
        clear_pipeline_timestamp (int):
            Timestamp of last user click clear results button
        user_login_timestamp (int):
            Timestamp of last user click sign-in button
        refresh_uploads_timestamp (int):
            Timestamp of last user click refresh uploads button
        log_out_timestamp (int):
            Timestamp of last user click log out button
    """
    app.logger.debug(f"sign on timestamp: {user_login_timestamp}")
    reset_session_data = {
        "SIGN_ON-№0": "None yet..",
        "RUN_ID": "NA",
        "current_user": "None",
        "user_logged_in": "False",
        "user_proper": "NA",
    }
    if login_n_clicks < 1 or user_selection == "None" or not user_selection:
        if not user_selection:
            return (
                reset_session_data,
                local_cache,
            )
        else:
            data = {"SIGN_ON-№0": "None yet.."}
            data["RUN_ID"] = "NA"
            data["current_user"] = user_selection
            data["login n_clicks"] = login_n_clicks
            data["user_logged_in"] = "False"
            data["user_proper"] = user_selection.replace("_", " ").title().split()[0]
            return data, local_cache

    login_t_elapse = tns() / 1e9 - user_login_timestamp / 1e3
    UUID = f"{''.join([*map(lambda x: x[:2], user_selection.split('_'))])}"
    logins = f"SIGN_ON-№{login_n_clicks}"
    data = data or {"SIGN_ON-№0": "None yet.."}
    data["UUID"] = UUID
    user_proper = user_selection[0] + user_selection.split("_")[0].lower()[1:]
    data["user_proper"] = user_proper
    data["current_user"] = user_selection
    data["login n_clicks"] = login_n_clicks

    if (login_n_clicks > logout_n_clicks and user_selection != "None") and login_t_elapse < 2:
        data["user_logged_in"] = "True"

    if logout_n_clicks > 0:
        if (tns() / 1e9 - log_out_timestamp / 1e3) < 2:
            return reset_session_data, local_cache

    if not user_selection:
        data["user_logged_in"] = "None"
        return data, local_cache

    # Proceed with apparent sign-in submission if this point reached:
    login_t_init = f"{tns()} = {now()}"
    data["login_t_init"] = login_t_init
    data[logins] = user_selection
    if "SIGN_ON-№1" in data.keys():
        data["prev_user"] = data[f"SIGN_ON-№{max(login_n_clicks-1,1)}"]

    RUN_ID = f"APP_RUNID_{now()}"
    SESSION_OUTPUT_DIR = f"{RUN_OUTPUT_DIR}/{today()}/{RUN_ID}/"
    data["RUN_ID"] = RUN_ID
    data["PATH_TO_SESSION_OUTPUT"] = SESSION_OUTPUT_DIR

    session_log_file = f"{SESSION_OUTPUT_DIR}{RUN_ID}_CurrentSession.log"
    os.makedirs(SESSION_OUTPUT_DIR, exist_ok=True)
    app.logger.debug(f"Number of logger handlers: {logger.handlers}")
    fh = add_logfile(logfile=session_log_file, logger=logger)
    app.logger.addHandler(fh)
    app.logger.debug(f"Number of logger handlers: {logger.handlers}")

    app.logger.info(f"USER SIGN ON @ {login_t_init}")
    app.logger.info(f"*** CURRENT APP APP SOFTWARE VERSION = {VERSION} ***")
    data["session_log_file"] = session_log_file
    data["SESSION_DATA"] = pd.DataFrame(
        [[RUN_ID, SESSION_OUTPUT_DIR, user_selection, session_log_file]],
        columns=["RUN_ID", "PATH_TO_SESSION_OUTPUT", "USER_ID", "LOG_FILE"],
    ).to_json(date_format="iso", orient="split")
    app.logger.info(f"USER: '{user_selection}' | RUN ID: {RUN_ID}")

    # Store basic user profile in browser local cache for  app:
    reset_local_cache = {
        "userName": user_proper,
        "userAccount": user_selection,
        "userProfileCreated": now(),
        "countUserLogIns": 0,
        "userRuns": {RUN_ID: data},
    }
    try:
        if local_cache["userAccount"] != user_selection:
            local_cache = reset_local_cache
        local_cache["countUserLogIns"] += 1
        local_cache["userRuns"][RUN_ID] = data
    except Exception as e:
        app.logger.info(
            f"Creating {user_proper}'s first local memory cache! (I.e., by which to remember them by! 😉)"
        )
        local_cache = reset_local_cache
        local_cache["countUserLogIns"] += 1

    return data, local_cache


@app.callback(
    Output(f"user-status", "children"),
    [
        Input(f"sign-on-submit", "n_clicks"),
        Input(f"refresh-user-history", "n_clicks"),
        Input(f"session", "data"),
    ],
    [State(f"input-user-name", "value"), State(f"local", "data")],
)
def show_user_in_menubar(
    sign_on_n_clicks, save_results_n_clicks, session_data, selected_username, local_data_cache
):
    """
    Parameters
    ----------
    sign_on_n_clicks
        int
    save_results_n_clicks
        int
    session_data
        Dash.dcc.Store(type='session')
    selected_username
        str
    local_data_cache
        Dash.dcc.Store(type='local')
    """
    log_in = [
        html.Span(
            html.A(["⁂ Sign In"], href=f"#log-in-below"),
            style={"fontSize": "80%", "color": "goldenrod"},
            id=f"log-in",
        )
    ]
    if session_data and sign_on_n_clicks > 0:
        if "session_log_file" in session_data:
            if session_data["current_user"] != "None":
                user = session_data["user_proper"]
                USER = session_data["current_user"]

                default = []
                history = {}
                try:
                    history = local_data_cache[f"{USER}_APP_Saved_History"]
                    app.logger.debug(str(local_data_cache), str(history))
                except Exception as e:
                    history = {}
                    default = [html.Li(f"You have no saved APP Results History, yet!\n")]
                return [
                    html.Details(
                        [
                            html.Summary(
                                [
                                    html.Span(
                                        f"👤Signed in as: {user}",
                                        style={
                                            "fontFamily": "Muli",
                                            "fontSize": "85%",
                                            "cursor": "pointer",
                                        },
                                        className="user-menu-summary",
                                    )
                                ]
                            ),
                            html.Div(
                                [
                                    html.Ul(
                                        [
                                            html.Li(f"Current RUN_ID: {session_data['RUN_ID']}"),
                                            html.Li(
                                                f"User Is Logged In: {session_data['user_logged_in']}",
                                                className="user-menu-action-items",
                                                style={"color": "rgb(37, 109, 210)"},
                                            ),
                                            html.Li(
                                                f"Signed On @ {session_data['login_t_init']}",
                                                className="user-menu-action-items",
                                                style={"color": "rgb(17, 199, 210)"},
                                            ),
                                            html.Li(
                                                [
                                                    html.A(
                                                        "Your Saved Analysis History",
                                                        href="#save-user-results",
                                                    ),
                                                    html.Ul(
                                                        [
                                                            html.Li(dcc.Link(f"{k}", href=f"/{k}"))
                                                            for k in history.keys()
                                                        ]
                                                        + default,
                                                        style={
                                                            "listStyle": "decimal-leading-zero",
                                                            "margin": "0!important",
                                                            "padding": "0!important",
                                                        },
                                                    ),
                                                ],
                                                className="user-menu-action-items",
                                                style={"color": "rgb(37, 149, 180)"},
                                            ),
                                            html.Li(
                                                [
                                                    html.A(
                                                        "Report an Issue/Bug",
                                                        href="mailto:jcollins.bioinformatics@gmail.com",
                                                    )
                                                ],
                                                className="user-menu-action-items",
                                                style={"color": "rgb(7, 69, 180)"},
                                            ),
                                        ]
                                    )
                                ],
                                className="user-menu",
                                style={"color": "rgb(199, 199, 199)"},
                            ),
                        ]
                    )
                ]
    return log_in


@app.callback(Output(f"workflow-selection", "children"), [Input(f"workflow-id", "value")])
def update_workflow_choice(workflow):
    """Update display at top of app based on USER's Worlflow selection
    (e.g., "Gene Editing: [...]", etc.)
    
    Args:
        workflow: str
    
    Returns:
        Array of H2 HTML Header element containing workflow text.
    """
    app.logger.debug(f"CALLBACK:::`update_workflow_choice` triggered with value: {workflow}")
    return [html.H2(f"{workflow}", style={"textAlign": "center"})]


@app.callback(Output("dd2-dropdown", "options"), [Input("dd1-dropdown", "value")])
def update_dropdown(dd1):
    """Update Dropdown for sample corresponding to USER-selected ID.
    
    Args:
        dd1 (Array of "label":"value" pairs dictionary containing the): Dropdown's options.
    
    Returns:
        Updated array matching form of input.
    """
    app.logger.debug(f"CALLBACK:::`update_dropdown` triggered with value: {dd1}")
    if dd1 and dd1 != "None":
        ent_id, ent_name, = dd1.split("-")
        try:
            wells = entity_schemas.loc[ent_name].columns #.unique()
        except KeyError as e:
            app.logger.info(f"WellID dropdown error in Plasmid Tool:\n{e}")
            return [{"label": "——N/A——", "value": "Error"}]
        # ⤑⟗αβ⟗⇒ *Trigger Ligation*
        return [{"label": " ✔ Confirm Well & EXP ID", "value": "None"}] + [
            {"label": w, "value": w}
            for w in wells
        ]
    else:
        return [{"label": "——N/A——", "value": "None"}]


@app.callback(
    Output("submission-status", "children"),
    [Input("submit-selected-dds", "n_clicks"), Input("clear-dd-selections", "n_clicks")],
    [State("dd1-dropdown", "value"), State("dd2-dropdown", "value")],
)
def trigger_dropdowns(submit_n_clicks, clear_n_clicks, dd1, dd2):
    """Initiate first analysis

    Args:
        submit_n_clicks: int
        clear_n_clicks: int
        dd1: str
        dd2: str

    Returns:
        Dash html component(s)
    """
    if clear_n_clicks == submit_n_clicks + 1:
        return html.Code(
            "⚠ | ℹ Overclicking clear *may* require compensatory submits! (I.e., Try clicking submit button >1 times, if submissions are not going through.)",
            style={
                "color": "red",
                "display": "flex",
                "flexFlow": "column wrap",
                "fontSize": "1.0rem",
                "margin": "0px 30% 20px 30%",
            },
        )
    if all(ui not in ("None", None) for ui in [dd1, dd2]):
        app.logger.info(
            f"-:!:- FUNCTION('trigger_dropdowns') has been activated, and now has value 'submit_n_clicks' = {submit_n_clicks}"
        )
        return [html.Code(f"SUBMISSION for: {dd1}, @Well{dd2}")]
    elif clear_n_clicks > submit_n_clicks + 1:
        app.logger.info(
            f"-:!:- FUNCTION('trigger_dropdowns') has been cleared, and now has value 'clear_n_clicks' = {clear_n_clicks}"
        )
        return html.Code(
            f"Submissions cleared: {clear_n_clicks}, [submissions_count={submit_n_clicks}].",
            style={"fontStyle": "normal", "color": "gray", "margin": "0px 30% 20px 30%"},
        )
    else:
        return html.Code("No submissions received, it seems...")



@app.callback(
    Output("dd-selections", "children"),
    [
        Input("dd1-dropdown", "value"),
        Input("dd2-dropdown", "value"),
        Input("submit-dds", "n_clicks"),
        Input("clear-dd-selections", "n_clicks"),
        Input("workflow-id", "value"),
    ],
    [State("session", "data"), State("submit-selected-dds", "n_clicks_timestamp")],
)
def display_generated_dd_output(
    dd1,
    dd2,
    submission,
    clear_submission,
    workflow,
    session_data,
    submission_timestamp,
):
    """Generic template for a paired dynamics set of dropdowns;
    such that the user selection in the first dropdown dynamically
    modifies live the possible options in the second dropdown.

    Args:
        dd1: str
        dd2: str
        submission: int
        clear_submission: int
        workflow: str
        session_data: Dash.dcc.Store(type='session')
        submission_timestamp: int
    """

    if (dd1 == "None" and dd2 == "None") or dd1 is None:
        return [
            html.Div(
                [
                    html.Span(
                        f"Make a new selection.",
                        style={"textAlign": "center", "fontFamily": "Muli", "fontSize": "1.5rem"},
                    ),
                    html.Span(
                        html.Img(
                            src="../assets/animations/dna-minimal-green.gif",
                            height="150",
                            style={
                                "transform": "translateY(-55px) translateX(5px)",
                                "filter": "hue-rotate(100deg) contrast(1.1) saturate(5)",
                                "position": "absolute",
                                "opacity": "0.5",
                                "borderRadius": "250px",
                            },
                        )
                    ),
                ],
                style={
                    "marginLeft": "25%",
                    "position": "relative",
                    "textAlign": "center",
                    "width": "50%",
                    "zIndex": "-1",
                },
            ),
            html.Div(
                [
                    html.Span("↪⦿"),
                    html.Img(
                        src="../assets/images/scope-unic.png",
                        width="80",
                        style={"marginTop": "15px", "marginBottom": "-25px", "cursor": "pointer"},
                    ),
                    html.Span("⥅♅"),
                ],
                style={
                    "textAlign": "center",
                    "fontSize": "1.75rem",
                    "animation": "animateGlow 45s infinite linear!important",
                    "cursor": "pointer",
                },
            ),
        ]
    elif any(ui == "Error" for ui in [dd1, dd2]):
        return
    elif dd1 != "None" and dd2 is None:
        return [
            html.H5(
                f"ℹ | Informational message to display.",
                style={"textAlign": "center", "marginLeft": "25%", "width": "50%"},
            )
        ]
    elif all(ui != "None" for ui in [dd1, dd2]):

        return html.Div(
            [
                html.Code(
                    f"♻ Cleared submission state: [total_clears={clear_submission}]",
                    style={"fontStyle": "italic", "fontSize": "0.9rem", "marginBottom": "5px"},
                ),
                html.Br(),
                html.Div(
                    [
                        html.H6(
                            [
                                html.P(f"⮊ Click ⬫Submit⬫ 𝑓𝗈𝓇⤑{dd2} ~ {dd1}"),
                                html.Span("to initiate "),
                                html.Span(
                                    f"in silico ",
                                    style={"fontStyle": "italic", "fontFamily": "'Times', serif"},
                                ),
                                html.Span("analysis of selections."),
                            ],
                            style={
                                "textAlign": "center",
                                "cursor": "pointer",
                                "color": "#ffffff6e",
                                "backgroundImage": "url(https://media.giphy.com/media/4HIOPSXOitJ2o/giphy.gif)",
                                "mozBackgroundClip": "text",
                                "webkitBackgroundClip": "text",
                                "fontWeight": "700",
                                "backgroundSize": "60%",
                            },
                        )
                    ],
                    style={
                        "position": "absolute",
                        "margin": """0.5% -5% -5% -5%""",
                        "textAlign": "center",
                        "display": "inline-block",
                        "mixBlendMode": "lighten",
                        "width": "200px",
                    },
                ),
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        html.Span("✂"),
                        html.Span("۝"),
                        html.Span("⭾"),
                        html.Span("α/β"),
                        html.Div(
                            [
                                html.Video(
                                    src=f"data:video/mp4;base64,{base64.b64encode(open(f'../assets/animations/T-Cell_TEM_4-3.mp4', 'rb').read()).decode()}",
                                    id="t-cell",
                                    autoPlay=True,
                                    loop=True,
                                    controls=False,
                                    preload="true",
                                    muted=True,
                                )
                            ],
                            style={"filter": "opacity(0.25)"},
                        ),
                    ],
                    style={
                        "textAlign": "center",
                        "fontSize": "2rem",
                        "width": "20%",
                        "marginLeft": "40.5%",
                        "mixBlendMode": "exclusion",
                    },
                    className="animate twirl",
                ),
            ],
            style={"textAlign": "center"},
        )


@app.callback(Output("dd1-dropdown", "value"), [Input("clear-dd-selections", "n_clicks")])
def clear_dd1_selection(n_clicks):
    """Clear Dropdown selections for Dropdown #1 (dd1)

    ( Dropdown to clear #1 of 2 )

    Args:
        n_clicks: int

    Returns:
        str: Resets selections to default, blank states.
    """
    if n_clicks > 0:
        app.logger.info(
            f"-:!:- FUNCTION('clear_dd1_selection') has been activated, and now has value 'n_clicks' = {n_clicks}"
        )
        return "None"


@app.callback(
    Output("dd2-dropdown", "value"),
    [Input("dd1-dropdown", "value"), Input("clear-dd-selections", "n_clicks")],
)
def clear_dd2_selection(val, n_clicks):
    """Clear Dropdown selections for Dropdown #2 (dd2)

    ( Dropdown to clear #2 of 2 )

    Args:
        val (str): cascading response via `clear_dd2_selection()` callback
        n_clicks: int

    Returns:
        str: Resets selections to default, blank states.
    """
    if n_clicks > 0:
        app.logger.info(
            f"-:!:- FUNCTION('clear_dd2_selection') has been activated, and now has value 'n_clicks' = {n_clicks} & 'val' = {val}"
        )
        if val == "None":
            return "None"
        else:
            return None


@app.callback(
    Output("memory", "data"),
    [
        Input("append-uploads", "n_clicks"),
        Input("clear-uploads", "n_clicks"),
        Input("refresh-uploads", "n_clicks"),
        Input("upload-data", "contents"),
    ],
    [
        State("session", "data"),
        State("memory", "data"),
        State("append-uploads", "n_clicks_timestamp"),
        State("refresh-uploads", "n_clicks_timestamp"),
        State("clear-uploads", "n_clicks_timestamp"),
        State("upload-data", "filename"),
        State("upload-data", "last_modified"),
    ],
)
def enable_combined_file_uploads(
    append_nclicks,
    clear_nclicks,
    refresh_nclicks,
    list_of_contents,
    session_data,
    clientside_memory_cache,
    append_nclicks_timestamp,
    refresh_nclicks_timestamp,
    clear_nclicks_timestamp,
    list_of_names,
    list_of_dates,
):
    """Management of app components and file upload States allowing for USER-
    toggled continuation of upload (i.e., as opposed to overwriting any previously
    received ABI files uploaded).
    
    Args:
        append_nclicks: int
        clear_nclicks: int
        refresh_nclicks: int
        list_of_contents: list of bytes
        session_data: Dash.dcc.Store(type='memory')
        clientside_memory_cache: Dash.dcc.Store(type='memory')
        append_nclicks_timestamp: int
        refresh_nclicks_timestamp: int
        clear_nclicks_timestamp: int
        list_of_names: list of str
        list_of_dates: list of int
    """
    memory_reset = {}
    if not session_data:
        raise PreventUpdate
    if clear_nclicks > 0:
        t_elapse = tns() / 1e9 - clear_nclicks_timestamp / 1e3
        app.logger.info(f"CLEAR UPLOAD UI ACTION DETECTED, W/ `t_elapse` = {t_elapse}")
        if t_elapse < 2:
            return memory_reset
    if append_nclicks > 0:
        LOG_FILE = session_data["session_log_file"]
        RUN_ID = session_data["RUN_ID"]
        SESSION_OUTPUT_DIR = session_data["PATH_TO_SESSION_OUTPUT"]
        app.logger.info(f"Append to Uploads in progress...")
        app.logger.info(f" ...Adding the following files: \n{list_of_names}")
        memory_reset = {f"{RUN_ID}-list_of_names": []}
        uploads_cache = clientside_memory_cache or memory_reset
        parsed_upload_children = [
            html.Details(
                [
                    parse_contents(c, n, d, SESSION_OUTPUT_DIR, session_log_file=LOG_FILE)
                    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
                ]
            )
        ]
        uploads_cache[f"{RUN_ID}-len_most_recent"] = len(parsed_upload_children)
        uploads_cache[f"{RUN_ID}-list_of_names"].extend(list_of_names)
        uploads_cache[f"{RUN_ID}-list_of_names"] = list(
            set(uploads_cache[f"{RUN_ID}-list_of_names"])
        )
        uploads_cache[f"{RUN_ID}-len_of_contents"] = len(uploads_cache[f"{RUN_ID}-list_of_names"])
        return uploads_cache
    else:
        return memory_reset


for n in range(1000):

    @app.callback(
        Output(f"cmds-dt-{n}", "style"),
        [Input(f"show-cmds-{n}", "n_clicks")],
        [State(f"cmds-dt-{n}", "style")],
    )
    def show_pipeline_commands(show_pl_cmds_n_clicks, style):
        """Enable dynamic reveal/hide functionality for showing
        the technical-heavy exact command line commands called 
        during the pipeline execution of processes.
        
        Args:
            show_pl_cmds_n_clicks: int
            style: <type>
        
        Returns:
            <type>
        
        Raises:
            PreventUpdate: Description
            PreventUpdate
        """
        if show_pl_cmds_n_clicks > 0:
            if (show_pl_cmds_n_clicks % 2) == 1:
                app.logger.info(f"show_pl_cmds clicked: {show_pl_cmds_n_clicks % 2}")
                return {"display": "block"}
            else:
                return {"display": "none"}
        else:
            raise PreventUpdate


@app.callback(
    Output("output-data-upload", "children"),
    [
        Input("upload-data", "contents"),
        Input("upload-data", "filename"),
        Input("upload-data", "last_modified"),
        Input("initiate-pipeline", "n_clicks"),
        Input("clear-pipeline", "n_clicks"),
        Input("append-uploads", "n_clicks"),
        Input("refresh-uploads", "n_clicks"),
        Input("clear-uploads", "n_clicks"),
        Input("memory", "data"),
        Input("sign-on-submit", "n_clicks"),
        Input("session", "data"),
    ],
    [
        State("workflow-id", "value"),
        State("initiate-pipeline", "n_clicks_timestamp"),
        State("clear-pipeline", "n_clicks_timestamp"),
        State("sign-on-submit", "n_clicks_timestamp"),
        State("refresh-uploads", "n_clicks_timestamp"),
        State("clear-uploads", "n_clicks_timestamp"),
    ],
)
def update_output(
    list_of_contents,
    list_of_names,
    list_of_dates,
    initiate_pipeline_n_clicks,
    clear_pipeline_n_clicks,
    append_uploads_n_clicks,
    refresh_uploads_n_clicks,
    clear_uploads_n_clicks,
    memory,
    user_login_n_clicks,
    session_data,
    workflow,
    initiate_pipeline_timestamp,
    clear_pipeline_timestamp,
    user_login_timestamp,
    refresh_uploads_timestamp,
    clear_uploads_timestamp,
):
    """Primary APP Pipeline function, as triggered by 'Initiate
    [APP] Pipeline' UI button (located in the "Step 2 (2/2)"
    section).
    
    Parameters
    ----------
    list_of_contents
        <list of str>
        Array containing user-uploaded ABI raw contents as
        binary strings (thus requiring decoding)
    list_of_names
        <list of str>
        Array containing user-uploaded ABI filenames
        (does not include the full path for security reasons)
    list_of_dates
        <list of int>
        Array containing user-uploaded ABI last modified timestamps
        (integers as seconds since 1970)
    initiate_pipeline_n_clicks
        <int>
        Total count of UI button clicks
    clear_pipeline_n_clicks
        <int>
        Total count of UI button clicks
    append_uploads_n_clicks
        <int> 
        Total count of UI button clicks
    refresh_uploads_n_clicks
        <int> 
        Total count of UI button clicks
    clear_uploads_n_clicks
        <int> 
        Total count of UI button clicks
    memory
        Dash.dcc.Store(type='session')
    user_login_n_clicks
        <int> 
        Total count of UI button clicks
    session_data
        Dash.dcc.Store(type='session')
    workflow
        <type>
    initiate_pipeline_timestamp
        <type>
    clear_pipeline_timestamp
        <type>
    user_login_timestamp
        <type>
    refresh_uploads_timestamp
        <type>
    clear_uploads_timestamp
        <type>
    
    """

    def show_list_of_names(USER, list_of_names):
        """Display the filenames for all successfully received 
        USER-uploaded ABI files.
        
        Args:
            USER: <str>
                Active user
            list_of_names: <list> 
                List of user-uploaded ABI filenames
        
        Returns:
            <html.Div([...])> 
                Reactive response to display after processing upload
        """
        if not all([fn.endswith(tuple([".csv",".xlsx"])) for fn in list_of_names]):
            return html.Div(
                [
                    html.Br(),
                    html.Code(
                        f"⚠ UPLOAD ERROR: Not all of the {len(list_of_names)} files are CSV or Excel files !",
                        style={"color": "red"},
                    ),
                    html.Br(),
                    html.Code(
                        f"⛔ | Please reset this upload & then perform a fresh upload of either .csv or .xlsx files."
                    ),
                ]
            )
        return html.Div(
            [
                html.Br(),
                html.Code(
                    f"✔ UPLOAD SUCCESSFUL (N={len(list_of_names)})", style={"color": "green"}
                ),
                html.Br(),
                html.Br(),
                html.Details(
                    [
                        html.Summary(
                            html.H3(
                                f"File(s) received (click to expand)",
                                style={"textAlign": "left", "fontSize": "120%"},
                            )
                        ),
                        html.Div(
                            [
                                html.Li(f"{'{:02d}'.format(i+1)})\t{abi}")
                                for (i, abi) in enumerate(sorted(list_of_names))
                            ],
                            id="files-received",
                            style={
                                "textAlign": "left",
                                "fontSize": "60%",
                                "columnCount": "3",
                                "paddingBottom": "2%",
                                "fontFamily": "'Roboto Mono', monospace",
                            },
                        ),
                        html.Hr(
                            style={
                                "borderTop": "1px solid",
                                "animation": "pact-gradient-text-flow 3s infinite linear",
                                "borderRadius": "5px",
                                "opacity": "0.67",
                                "width": "50%",
                                "marginLeft": "25%",
                            }
                        ),
                    ]
                ),
                html.Br(),
                html.Span(className="fader-line-short", style={"marginBottom": "20px"}),
            ],
            style={"width": "80%", "marginLeft": "10%"},
        )

    not_signed_in_msg = html.Div(
        [html.H6("Please log in to release the pipeline as ready for activation.")]
    )

    try:
        if session_data:  # ["user_logged_in"] == "True":
            RUN_ID = session_data["RUN_ID"]
            SESSION_OUTPUT_DIR = session_data["PATH_TO_SESSION_OUTPUT"]
            LOG_FILE = session_data["session_log_file"]
            USER = session_data["user_proper"]
            UUID = session_data["UUID"]

            if len(app.logger.handlers) < 1:
                app.logger.info(
                    f"Number logger handlers = {len(app.logger.handlers)}->{logger.handlers}"
                )
                app.logger.info("Adding log FileHandler...")
                fh = logging.FileHandler(LOG_FILE)
                fh.setLevel(logging.INFO)
                app.logger.addHandler(fh)
                app.logger.info(
                    f"Number logger handlers = {len(app.logger.handlers)}->{logger.handlers}"
                )
        else:
            return not_signed_in_msg

    except KeyError as e:
        app.logger.error(f"No user appears to be logged in (KeyError: {e})")
        return not_signed_in_msg

    ### UPON USER FILE UPLOAD(S):
    if list_of_contents is not None:

        if initiate_pipeline_n_clicks >= 1:
            init_t_elapse = tns() / 1e9 - initiate_pipeline_timestamp / 1e3
            app.logger.info(f"init_t_elapse = {init_t_elapse}; ")
            if init_t_elapse < 30:
                if (
                    clear_pipeline_n_clicks > 0
                    and refresh_uploads_n_clicks <= clear_pipeline_n_clicks
                ):
                    if all(
                        clear_pipeline_timestamp > ts
                        for ts in [initiate_pipeline_timestamp, user_login_timestamp]
                    ):
                        return [
                            html.H3(
                                f"Thanks, {USER}; the previous pipeline results have been cleared."
                            ),
                            html.H4(f"Current analysis output folder: {RUN_ID}"),
                            html.H5(
                                html.Div(
                                    [
                                        html.Span(f"Launch a new analysis."),
                                        html.Br(),
                                    ]
                                )
                            ),
                        ]
                elif clear_pipeline_n_clicks > 0:
                    if clear_pipeline_timestamp > initiate_pipeline_timestamp:
                        if refresh_uploads_n_clicks > 0:
                            if refresh_uploads_timestamp > clear_pipeline_timestamp:
                                return show_list_of_names(USER, list_of_names)
                        return html.Div(
                            html.H5(
                                f"(Pipeline results [{RUN_ID}] CLEARED)", style={"color": "red"}
                            )
                        )

                app.logger.info(
                    f"📟📶⌁⌁⌁📠Using the following as pipeline data input. \n{len(list_of_names)} USER UPLOADED FILE(S) : \n"
                    + "\n  📊⇢🧬 ".join(
                        [
                            "{:>03d})\t{:>50s}".format(i + 1, abi)
                            for i, abi in enumerate(sorted(list_of_names))
                        ]
                    )
                )

                app.logger.info(
                    f"INITIALIZING NEW PIPELINE LAUNCH:\n\n\t\t{SESSION_OUTPUT_DIR}"
                )

                start_time = tns()

                children = []
                parsed_upload_children = [
                    html.Details(
                        [
                            parse_contents(c, n, d, SESSION_OUTPUT_DIR, session_log_file=LOG_FILE)
                            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
                        ]
                    )
                ]
                # Generate (single!) TCR alpha/beta chain pair combinations
                # base pipeline reference files (e.g., agg'd fq, designated master
                # reference 'genome', DataFrames, log, etc.)
                try:
                    pipeline_output = ljoin(
                        [
                            r
                            for r in pipeline.run_pipeline(
                                RUN_ID,
                                SESSION_OUTPUT_DIR,
                                workflow=workflow,
                                session_log_file=LOG_FILE,
                            )
                        ]
                    )
                    args = [(*(x), i + 1) for i, x in enumerate(pipeline_output)]

                except Exception as e:
                    logs = []
                    report = None
                    with open(LOG_FILE, "r+") as log_file:
                        for line in log_file.readlines():
                            logs.append(line)
                    stderr = [
                        dcc.Textarea(
                            placeholder="(Main Sequence -- logger placeholder)",
                            value="\n".join(logs),
                            style={
                                "height": "400px",
                                "width": "50%",
                                "fontSize": "0.7rem",
                                "lineHeight": "0.9rem",
                                "fontFamily": "'Roboto Mono', monospace",
                            },
                            className="logger-text",
                            name="organization",
                            readOnly=True,
                        )
                    ]
                    fatal_crash = "⚠ ALERT: ERROR IN MAIN PIPELINE SEQUENCE"
                    app.logger.error(f"{fatal_crash}: \n\n{e}")
                    log_exc(app.logger)
                    return html.Div(
                        [
                            html.H2(fatal_crash, style={"color": "red"}),
                            html.P(f"App runtime was: {gtt(start_time)}"),
                            html.Code(f"Primary error message for crash:\n{e}"),
                            html.H4("See [end of] AUDIT LOG (below) for failure reason."),
                            html.H5(f"WEB SERVER SYSTEM LOG:", style={"color": "red"}),
                            html.Div(stderr),
                        ]
                    )

                ###   # # # # # # # # # #### # # # # # # # # #   ###
                children.append(
                    html.Div(
                        [
                            html.Hr(),
                            html.Br(),
                            html.H4("All files analyzed in most recent upload:"),
                        ]
                    )
                )
                """      ~ ◮ ~
                     S U M M A R Y
                 a  n  a  l  y  s  i  s
                     ~     ~     ~
                         ~ ◮ ~
                """
                if report:
                    summary_report = [
                        html.Div(
                            [
                                html.Br(),
                                html.H2(
                                    "Pipeline Output Summary",
                                    style={
                                        "fontSize": "80%",
                                        "letterSpacing": "1.33rem",
                                        "fontFamily": "Cinzel",
                                        "animation": "anim-text-flow-keys 120s infinite linear",
                                    },
                            ),
                                html.Hr(),
                            ],
                            style={"width": "90%", "marginLeft": "5%"},
                        )
                    ]
                else:
                    summary_report = [html.Div([html.H4(f"No final output found.")])]

                html_out = f"{SESSION_OUTPUT_DIR}{RUN_ID}_HTMLprops.tsv"
                pd.DataFrame(
                    [str(c.to_plotly_json()) for c in children], columns=["DashHTMLDivComponents"]
                ).to_csv(html_out, encoding="utf-8", sep="\t")
                app.logger.info("Processed & analzyed input files were:")
                app.logger.debug(parsed_upload_children)
                app.logger.info(",".join([str(type(x)) for x in parsed_upload_children]))
                total_exec_time = gtt(start_time)
                app.logger.info(
                    f"———COMPLETE——-\n\n \t ☆☆☆ Total EXECUTION TIME Required ☆☆☆\n\n \t\t = {total_exec_time} s \n\n"
                )
                show_exec_time = [
                    html.Div(
                        [
                            html.Hr(),
                            html.H3(
                                f"* ﾟ(>͂ ͡͡︒ ͜ ʖ ͡︒)>-｡ﾟ☆* :・ﾟ.☆ * ･ "
                            ),
                            html.H4(f"Total Execution Time Required = {total_exec_time} s"),
                            html.Hr(),
                            html.Br(),
                        ]
                    )
                ]

                if len(children) > 50:
                    full_report = [
                        html.Div(
                            [
                                html.H2(
                                    f"NOTICE: Due to an unusually large number of results in this analysis (N={len(children)}), full report display has been automatically disabled."
                                )
                            ]
                        )
                    ]
                else:
                    full_report = children

                children = (
                    show_exec_time
                    + TOC
                    + summary_report
                    + full_report
                    + parsed_upload_children
                    + [html.Div(html.Hr())]
                )

                app.logger.debug(",".join([str(type(x)) for x in children]))
                app.logger.debug(f"Number of html.Div elements in final layout: {len(children)}")

                return children

        elif initiate_pipeline_n_clicks > 15:
            return html.Div(
                [
                    html.H4(
                        "⚠ | ALERT ! : Un𝒇ortunately, you have over-activated the pipeline submissions check system. Please re𝒇resh the page, re-log in, and re-upload the set o𝒇 ABI 𝒇iles you would like analyzed.  🛠⎆ "
                    ),
                    html.H6("↺ Please Re𝒇resh the page. ↺"),
                ]
            )

        if clear_uploads_n_clicks > 0:
            t_elapsed = tns() / 1e9 - clear_uploads_timestamp / 1e3
            if t_elapsed < 2:
                for tcr_dir in os.listdir(SESSION_OUTPUT_DIR):
                    grouped_clone_fqs = f"{SESSION_OUTPUT_DIR}{tcr_dir}"
                    if os.path.isdir(grouped_clone_fqs):
                        shutil.rmtree(grouped_clone_fqs)
                return html.Div(
                    [
                        html.Code(f"UPLOADS CLEARED", style={"color": "red"}),
                        html.H5(
                            f'To continue, submit at least one new upload & click "✥ Append".'
                        ),
                    ]
                )

        if append_uploads_n_clicks > 0 or clear_uploads_n_clicks > 0:
            if len(list_of_names) > 0 and len(memory.items()) > 0:
                all_uploads = (
                    memory[f"{RUN_ID}-list_of_names"]
                    if len(memory[f"{RUN_ID}-list_of_names"]) > 0
                    else list_of_names
                )
                return show_list_of_names(USER, all_uploads)
            elif len(memory.items()) == 0:
                return html.Div(html.Code("NONE"))
        else:
            app.logger.info(
                f"{USER} uploaded the following {len(list_of_names)} file(s):"
                + "\n\t ◇ 📄 "
                + "\n\t ◇ 📄 ".join(sorted(list_of_names))
                + ".\n"
            )
            return show_list_of_names(USER, list_of_names)

    else:
        return html.Div(
            [html.Br(), html.H5(f"Logged in as: {USER}", style={"color": "rgb(32,92,188)"})]
        )




@app.callback(
    Output(f"output-file-list", "children"),
    [Input(f"refresh-downloads-links", "n_clicks")],
    [State(f"download-dropdown", "value"), State(f"session", "data")],
)
def update_link(refresh_n_clicks, value, session_data):
    """"Download Output Files" dropdown components suite.

    Allows user to choose from a list of file 'genres' (i.e.,
    subsets of similar bioinformatics datafile types) - and
    reacts by displaying all corresponding generated results
    files for the current session analysis up-to-now, which
    dual, and principally serve their purpose, as direct-to-
    desktop functional download links.

    Also capable of showing a full printout of the current cum-
    ulative state of the session logfile in via an HTML
    textarea Dash component.

    Finally, users are also presented (via HTML button comp)
    the option and ability to create a click-to-download link
    for a dynamically generated zipped archive of all curr-
    ently selected (& thus [reactively] displayed) results
    files.

    Args:
    -----
        refresh_n_clicks           :  int
        value                      :  str
        session_data (dcc.Store(   :  Dash HTTP client-side memory caching,
            type='session')        . "Session" type (auto-cleared when browser
                      )            .  tab closes [but *not* on Refresh's]).

    Returns:
    --------
        html.Div([html.Li's])      :  An array of download-enabling Dash HTML
                                      hyperlink components.

    """
    if value:
        if session_data:
            selection = output_filetype_genres[value]
            try:
                session_output = session_data["PATH_TO_SESSION_OUTPUT"]
            except KeyError as e:
                app.logger.info(
                    f"User attempting to access files when not yet logged in!\nError:\n{e}"
                )
                return [html.Li(f"(Please log in first!)")]
            if value == "LOGS":
                files = sorted(get_output_files(selection, session_output))
                logs = []
                for f in files:
                    with open(f, "r+") as log_file:
                        for line in log_file.readlines():
                            logs.append(line)
                    if len(app.logger.handlers) < 1:
                        app.logger.addHandler(add_logfile(f))
                        app.logger.info("Re-added logfile (post-log printout)")
                return [html.Li(file_download_link(filename)) for filename in files] + [
                    dcc.Textarea(
                        placeholder="(No logged activity yet.)",
                        value="\n".join(logs),
                        style={
                            "height": "550px",
                            "width": "60%",
                            "fontSize": "0.7rem",
                            "lineHeight": "0.9rem",
                            "fontFamily": "'Roboto Mono', monospace",
                        },
                        className="logger-text",
                        name="organization",
                        readOnly=True,
                    )
                ]
            elif value == "REF":
                return [
                    html.Li(
                        file_download_link(filename),
                        style={"fontFamily": "'Roboto Mono', monospace", "letterSpacing": "-1pt"},
                    )
                    for filename in sorted(get_output_files(selection))
                ]
            files = get_output_files(selection, session_output)
            if len(files) == 0:
                return [html.Li(f"No output files available for selection: {value}.")]
            else:
                return [
                    html.Li(
                        file_download_link(filename),
                        style={"fontFamily": "'Roboto Mono', monospace", "letterSpacing": "-1pt"},
                    )
                    for filename in sorted(files)
                ]
        else:
            return [html.Li(f"(Please log in first!)")]
    else:
        return [html.Li(f"[Select an output filetype(s) category.]")]


@app.callback(
    Output(f"download-all", "children"),
    [Input(f"request-all-zipped", "n_clicks")],
    [State(f"download-dropdown", "value"), State(f"session", "data")],
)
def zip_all_downloadables(getZipped_n_clicks, value, session_data):
    """Create a downloadable zip of USER selected set of output files.
    
    Args:
        getZipped_n_clicks: int
        value: str
        session_data: Dash.dcc.Store(type='session')
    
    Returns:
        html.Div([]): Dash HTML div component↦ itself an array of Dash HTML components
    """
    if getZipped_n_clicks > 0 and any(session_data):
        selection = output_filetype_genres[value]
        session_output = session_data["PATH_TO_SESSION_OUTPUT"]
        RUN_ID = session_data["RUN_ID"]
        source = session_output if value != "REF" else PLASMIDS_ARCHIVE
        files = get_output_files(selection, final_output_dir=source)
        zipped = re.sub("['\ \(\)]", "", f"{session_output}{RUN_ID}_{clock()[-4:]}.zip")
        for i, filename in enumerate(files):
            fbn = f"{os.path.basename(filename)}"
            app.logger.info(f"{i}: Adding file {filename} to new zipped archive: {fbn}...")
            with zipfile.ZipFile(zipped, "a") as zipf:
                zipf.write(filename, fbn)
        return html.Div(
            [
                html.H4(f"Zip⇝⇶🗃⇨Download All:"),
                html.H4([html.Li(file_download_link(zipped), className="zip-dl-link")]),
            ]
        )