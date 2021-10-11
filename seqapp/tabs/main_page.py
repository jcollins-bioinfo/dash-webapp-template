"""MAIN APP PAGE
Contains the principle tab of the application UI - where
the user uploads input files, launches analyses, and interprets
&/or downloads pipeline output QC results. This is the first tab
of the single-page UI (and therefore the default presentation
immediately upon loading the app), and the only one a user
will necessarily use. Remaining tabs provide supplemental info
or functionality.

Attributes:
    children (list): The whole page's worth of Dash components, ordered
    sequentially corresponding directly to displayed relative position
    in the app, from the very top to very bottom.
    components_list (list): Abstraction of `children` for the sake of diminishing
    excess whitespace indentation pushing the code too far to the right (i.e.,
    code wrap aesthetics).
    updates (list): Easy-access to one of the more permanently variable
    components - the app software version updates notifications displayed
    at top of main page just below the log in dialog.
    version (str): The config-imported automatically up-to-date software
    release version as queried via subprocess call `git describe --tags`.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from seqapp.config import *
from seqapp.utils import ljoin

version = VERSION
updates = UPDATES

app_logo = f'data:image/png;base64,{base64.b64encode(open(f"{APP_HOME}/{APP_NAME}/assets/images/dash-webapp-template-logo-light-web.png", "rb").read()).decode()}'


updates = [u.split("Date: ") for u in updates]
updates = [
    html.Details(
        [
            html.Ol(
                [
                    html.Li(
                        [
                            html.P(
                                commit_log[0],
                                style={"fontSize": "0.5rem", "fontWeight": 200},
                            ),
                            html.P(commit_log[1], style={"fontWeight": 400}),
                        ]
                    )
                    for commit_log in updates
                ],
                className="updates-list",
                reversed="reversed",
            ),
            html.Summary(html.Code("-UPDATES-", className="updates-header")),
        ],
        id="app-updates",
    )
]

navbar = [
    html.Td(html.Img(src=app_logo, style={"width": "80%"}), style={"width": "7%"}),
    html.Td(
        html.Div(
            [
                html.Div(
                    [
                        html.Span("[server/network/cmpny]: ", style={"color": "#878686", "fontSize": "0.5rem"}),
                        html.Span("[YOUR APP NAME]"),
                    ],  # ╦ ",
                    style={
                        "marginLeft": "-3%",
                        "cursor": "pointer",
                        "marginBottom": "0.5%",
                        "fontSize": "80%",
                    },
                ),
                html.Span(html.A("Top⏎", href="#back-to-top")),
                html.Span(" | "),
                html.Span(
                    html.A("Step One", href="#step-one", className="navbar-select")
                ),
                html.Span(" | "),
                html.Span(
                    html.A(
                        "Step Two (⮊Run🧬Pipeline)",
                        href="#step-two",
                        className="navbar-select",
                    )
                ),  # ⧉
                html.Span(" | "),
                html.Span(
                    html.A("Results", href="#mutation-calls", className="navbar-select")
                ),
                html.Span(" | "),
                html.Span(
                    html.A(
                        "Download Links",
                        href="#download-links",
                        className="navbar-select",
                    )
                ),  # (🖥⇉🗐)
                html.Span(" | "),
                html.Span(
                    html.A(
                        "Clear",
                        href="#pipeline-progress-disclaimer",
                        className="navbar-select",
                    )
                ),  # (∅🖺➡🗋)
                html.Div(
                    children=[
                        html.Span(
                            html.A(
                                ["⁂ Sign In"],
                                style={"fontSize": "80%", "color": "goldenrod", "width": "fit-content"},
                                href=f"#log-in-below",
                            )
                        )
                    ],
                    id="user-status",
                    style={"marginLeft": "1%"},
                ),
            ],
            style={"text-align": "left"},
        )
    ),
]

header = [html.Table(html.Tr(navbar)), html.Div(className="menubar-divider")]

download_options = [{"label": "—Select Output Type—", "value": "None"}] + sorted(
    [
        {"label": "Export [Streamlined] to Geneious (GENEIOUS)", "value": "GENEIOUS"},
        {
            "label": "Plasmid Maps [Full De Novo-Generated Archive] {ALL Putative TCR-α/β} (FASTA)",
            "value": "REF",
        },
        {
            "label": "Plasmid References [Current Session] (FASTA) {*plus*: Post-QC Consensus Sequence(s)}",
            "value": "CONSENSUS",
        },
        {"label": "Mutation Calls (Variant Call Format [VCF])", "value": "VCF"},
        {"label": "Reference Mapping Stats (TXT)", "value": "MAPSTATS"},
        {"label": "Raw Aggregated Input Sequences (ABI→FASTQ)", "value": "AGG_FQ"},
        {"label": "Quality Score QC Figures (PNG)", "value": "QUAL"},
        {
            "label": "Reference-Mapped Reads Assembly (Sequence Alignment Map [SAM])",
            "value": "SEQ_ALGN",
        },
        {
            "label": "Annotation Files [V(D)J-Specific De Novo Full Plasmid Map Features] (BED format)",
            "value": "ANNOT",
        },
        {
            "label": "Access LOGGING Records / Audit Trail [Current Session] (LOG)",
            "value": "LOGS",
        },
        {"label": "All Analysis Files", "value": "ALL"},
    ],
    key=lambda d: d["label"],
)

downloads = [
    dcc.Dropdown(
        id="download-dropdown",
        value=None,
        options=download_options,
        placeholder="—Select Output File Type—",
        style={"width": "80%", "marginLeft": "10%"},
    ),
    html.Button("Show Relevant Files", id="refresh-downloads-links", n_clicks=0),
]

components_list = [
    # NOTE:
    #         -----BROWSER MEMORY CACHING-----
    #
    #  Three types of storage (storage_type prop):
    #     1 - memory: default, keep the data as long the page is not refreshed.
    #     2 - local: keep the data until it is manually cleared.
    #     3 - session: keep the data until the browser/tab closes.
    #
    # [ For more info on `dcc.Store` browser caching, see:
    #    https://dash.plot.ly/dash-core-components/store  ]
    dcc.Store(id="memory", storage_type="session"),
    dcc.Store(id="local", storage_type="local"),
    dcc.Store(id="session", storage_type="session"),
    html.Div(id="back-to-top", style={"display": "hidden"}),
    html.Header(
        children=header,
        className="menubar",
        style={"width": "102%", "marginLeft": "-1%"},
    ),
    html.P(
        "Nex╬Gen Bi⌬informat🜾cs Web Apps",
        style={
            "lineHeight": "100%",
            "color": "#00000025",
            "textAlign": "left",
            "marginLeft": "-1%",
            "marginTop": "5px",
            "marginBottom": "-1%",
        },
    ),
    html.Div(
        [
            html.H2(
                "ℐ⌖ ℌ ℕ Collins — Bǁ◎IℕFO𓏢MA𓇰ICS",
                style={
                    "fontSize": "0.67rem",
                    "letterSpacing": "30px",
                    "lineHeight": "2.0rem",
                    "fontFamily": "'Cinzel', serif",
                    "color": "#8b8b8b",
                    "marginBottom": "-1%",
                    "textAlign": "center",
                    "marginLeft": "2.5%",
                },
                className="ml-title",
            ),
            html.Div(
                [
                    html.Pre(
                        "ୡ    ୡ        ୡୡ         ୡ         ୡ        ୡ  ୡ       ୡ     ୡ          ୡ",
                        style={
                            "color": "#d6d6d684",
                            "fontSize": "1.2rem",
                            "letterSpacing": "2px",
                            "marginBottom": "-0.3rem",
                        },
                    ),
                    html.Pre(
                        "◖𓇃𓇃𓇃𓏣🜾𓏣𓇃𓇃𓉽𓇃𓐩𓋥⸶⸷𓋥𓐩𓇃𓋏𓇃˥⎡𓇃𓇃࿅𓇃𓊢ꃊ𓊢𓇃𓇃𓇃ⴶ〰⸅‖⸄〰ж𓇃𓇃𓏟𓏞𓇃𓇃𓇃𓇃𓋅𓆬𓆬𓋅𓇃𓇃𓇊𓊢𓇊𓇃𓉽𓇃ண⎤꜒𓇃𓇃࿑◗",
                        style={
                            "filter": "blur(.4pt)",
                            "color": "#584e00a8",
                            "fontSize": "1.2rem",
                            "opacity": "0.85",
                            "marginBottom": "4%",
                            "marginTop": "6px",
                        },
                    ),
                    html.Pre(
                        "◖𓇃𓇃𓇃𓇃⸠⎫𓏉⎧⸡𓇃𓇃𓇃𓇃⸣⸠࿇⸡⸢𓇃𓇃𓇃𓇃⎨⎬𓇃𓇃𓇃𓉽𓋏𓉽𓇃𓇃ཥ⅌ཤ𓇃𓇃𓇃𓍰𓇃𓇃𓇃𓇃ཀཫ𓇃𓇃𓇃╗╔𓇃𓇃⦄༽⸶⸷༼⦃𓇃𓇃𓇃◗",
                        style={
                            "marginTop": "-1.5%",
                            "fontSize": "1.55rem",
                            "color": "#AEA46E",
                        },
                    ),
                ],
                style={
                    "letterSpacing": "-1px",
                    "fontFamily": "Roboto, sans-serif",
                    "textAlign": "center",
                    "overflow": "hidden",
                    "transform": "translate3d(0,0,0)",
                },
            ),
            html.Br(),
        ]
    ),
    html.H1(
        "Custom Web Apps — [dash-webapp-template]",
        style={
            "fontSize": "4rem",
            "fontColor": "#0d04a5f5",
            "lineHeight": "90%",
            "letterSpacing": "-8px",
            "marginTop": "-110px",
            "mixBlendMode": "multiply",
            "textAlign": "center",
            "cursor": "pointer",
            "zIndex": "1",
        },
    ),
    html.Div(id="log-in-below", style={"display": "hidden"}),
    html.Div(id="workflow-selection"),
    html.Span(className="fader-line-long"),
    html.H4("—Automated [Name/Function of Your App]—", style={"lineHeight": "80%"}),
    html.H5(
        "[Tagline-esque description for what this app does.]",
        className="title-description",
    ),
    html.Br(),
    # html.Div(
    #     [
    #         html.Video(
    #             src="../assets/animations/rotate_DNA_HD_HB.mp4",
    #             autoPlay=True,
    #             loop=True,
    #             controls=False,
    #             preload="true",
    #             muted=True,
    #             className="dna-login-animation"
    #         )
    #     ]
    # ),
    html.Div(
        [
            html.H4(
                "To Begin, Sign In Below",
                style={
                    "textAlign": "center",
                    "animation": "gradient-text-flow 40s infinite linear",
                    "mixBlendMode": "multiply",
                    "fontSize": "3.0rem",
                    # "marginTop": "15px!important",
                    "fontWeight": "300",
                    # "marginBottom": "1.1%",
                },
            ),
            html.Span(
                className="fader-line-short",
                style={"width": "112.5%", "marginLeft": "-6.25%"},
            ),
            dcc.RadioItems(
                options=[
                    {
                        "label": "[Team]",
                        "value": "XX-XXX | Name of process / workflow",
                        "disabled": True,
                    }
                ],
                value="XX-XXX | Name of process / workflow",
                labelStyle={
                    "display": "none",
                    "textAlign": "center",
                    "padding": "8px 20px 0px 20px",
                },
                id="workflow-id",
                # className="workflow-css",
            ),
        ],
        style={"position": "relative", "textAlign": "center"},
    ),
    html.Div(
        "Log In, Here!",
        className="H7",
        style={
            "textAlign": "center",
            "zIndex": "1000",
            "mixBlendMode": "color-dodge",
            "fontWeight": "600",
            "marginTop": "1.3%",
            "marginLeft": "-25%",
        },
    ),
    html.Div(
        [
            dcc.Dropdown(
                id="input-user-name",
                value="None",
                clearable=True,
                searchable=True,
                options=USERS,
                placeholder="—Select Your Name—",
            ),
            html.Div(
                [
                    html.Button("Sign In", id="sign-on-submit", n_clicks=0),
                    html.Button(
                        "Return",
                        id="log-back-in-submit",
                        className="submit-buttons",
                        n_clicks=0,
                    ),
                    html.Button(
                        "Log Out",
                        id="log-out-submit",
                        n_clicks=0,
                        style={"paddingRight": "3%"},
                    ),
                ],
                style={"display": "flow-root"},
            ),
            html.H6(
                [
                    "Current Version: ",
                    html.Br(),
                    html.Span(
                        f"{version}",
                        style={
                            "animation": "anim-text-flow-keys 25s infinite linear",
                            "fontSize": "133%",
                        },
                    ),
                ],
                className="version-tag",
            ),
        ],
        style={"marginLeft": "35%", "width": "30%", "marginBottom": "2px"},
    ),
    # html.Br(),
    html.Span(className="hr-style-2"),
    # html.Br(),
    html.Div(
        id="user-login-confirmation",
        children=updates,
        style={"position": "relative", "padding": "1%"},
    ),
    html.Br(),
    html.Div(id="accumulate-output-hidden", style={"display": "none"}),
    html.Hr(id="step-one"),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),
    html.H3(
        "Step One (1/2): [Simple instruction/Action command]",
        style={"textAlign": "center", "marginTop": "-10px"},
    ),
    html.H6("(subtitle / subdescription)", style={"marginTop": "-20px"}),
    html.H4(html.Div(["[Description of this tool]"])),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),
    html.H5(
        ["Some instructions of some kind (e.g., sample ID)"],
        style={"textAlign": "center"},
    ),
    html.Br(),
    html.Div(
        [
            html.Table(
                [
                    html.Tr(
                        [
                            html.P(
                                "Type to search.",
                                style={
                                    "textAlign": "left",
                                    "color": "#fff",
                                    "mixBlendMode": "darken",
                                },
                            ),
                            html.H6(
                                "ℹ | Clear selections before subsequent submissions.",
                                style={
                                    "textAlign": "left",
                                    "color": "#fff",
                                    "marginTop": "-4px",
                                },
                            ),
                            dcc.Dropdown(
                                id="dd1-dropdown",
                                value="None",
                                clearable=True,
                                searchable=True,
                                options=[
                                    {
                                        "label": "—🔍⤑Select by Schema Name/ID—",
                                        "value": "None",
                                    }
                                ]
                                + [
                                    {
                                        "label": f" 📃 : —{name}🔑{ent_id}— ",
                                        "value": f"{ent_id}-{name}",
                                    }
                                    for (name, ent_id) in sorted(
                                        zip(entity_schemas.index, entity_schemas.id),
                                        key=lambda x: x[0],  # reverse=True
                                    )
                                ],
                                style={
                                    "textAlign": "center",
                                    "backgroundColor": "rgba(0,0,0,0.25)",
                                    "zIndex": "3005",
                                    "color": "rgb(255, 255, 255)",
                                },
                                placeholder="—🔍⤑Search all Schemas—",
                            ),
                        ]
                    ),
                    html.Tr(
                        [
                            dcc.Dropdown(
                                id="dd2-dropdown",
                                clearable=True,
                                searchable=True,
                                options=[{"label": "—Select Field—", "value": "None"}],
                                style={
                                    "textAlign": "center",
                                    "backgroundColor": "rgba(0,0,0,0.25)",
                                    "zIndex": "3000",
                                    "color": "#00ffb8",
                                    "position": "relative!important",
                                },
                                placeholder="—Select Entity Field—",
                            )
                        ]
                    ),
                    html.Tr(
                        [
                            html.Br(),
                            html.Div(
                                [
                                    html.Button(
                                        "Submit", id="submit-selected-dds", n_clicks=0
                                    ),
                                    html.Button(
                                        "Clear Selections",
                                        id="clear-dd-selections",
                                        n_clicks=0,
                                    ),
                                ],
                                style={
                                    "textAlign": "center",
                                    "marginLeft": "10%",
                                    "width": "80%",
                                },
                            ),
                        ]
                    ),
                ],
                style={
                    "marginLeft": "50%",
                    "transform": "translateX(-50%)",
                    "width": "50%",
                },
            )
        ],
        id="crispr",
    ),
    html.Br(),
    html.Span(id="fader-line-short"),
    html.Br(),
    html.Br(),
    html.Div(id="submission-status"),
    html.Br(),
    html.Div(id="dd-selections", style={"textAlign": "left"}),
    html.Br(),
    html.Hr(),
    html.Br(id="step-two"),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),
    html.H3(
        "Step Two (2/2): Upload [insert expected file types (e.g., clinical data .xlsx files)].",
        style={"textAlign": "center", "marginTop": "-10px"},
    ),
    html.H2(
        "Click “Initiate Pipeline” to launch analysis.", style={"marginTop": "-0.75%"}
    ),
    html.H6('Uploading from multiple directories? Or after reset? ⮊ Click "✥ Append"'),
    html.Hr(style={"width": "50%", "marginLeft": "25%"}),
    dcc.Upload(
        id="upload-data",
        children=html.Div(
            [
                "Drag/Drop ⤓ file(s) here  ",
                html.Spacer(),
                "  —or—",
                html.A(
                    "📂 Select from your computer",
                    className="hvr-float-shadow",
                    style={"fontWeight": "400", "marginBottom": "5px"},
                ),
                html.H6(
                    "(Other Info/Note)",
                    style={
                        "textAlign": "center",
                        "letterSpacing": "1px",
                        "fontFamily": "'Cinzel', serif",
                        "fontSize": "70%",
                    },
                ),
                html.H6(
                    "(...Note details / description...)",
                    # NOTE - Overview of file formats
                    # ------------------------------------
                    # "FASTQ, C[/T]SV (Comma[/Tab]-Separated Values), "
                    # "XLS[X] (Excel), B[/S]AM (NGS alignments), "
                    # "VCF (Variant Call Format mutation/SN[P/V] files), "
                    # "BED ([track-based] annotations)",
                    style={
                        "textAlign": "center",
                        "letterSpacing": "4px",
                        "fontFamily": "'Cinzel', serif",
                        "marginTop": "-8px",
                    },
                ),
                html.Span(
                    html.H5(
                        "(Optional supplementary message...)",
                        style={
                            "width": "45%",
                            "marginLeft": "27.5%",
                            "fontSize": "80%",
                        },
                    )
                ),
            ],
            style={
                "borderWidth": "1px",
                "borderStyle": "solid",
                "borderRadius": "100px",
                "textAlign": "center",
                "margin": "2% 15%",
                "boxShadow": "0px 1px 5px 2px rgba(0, 0, 50, 0.16)",
                "borderColor": "transparent",
                "padding": "0.5%",
                "backgroundColor": "rgba(255,255,255,0.5)",
            },
        ),
        multiple=True,  # (Allow multiple files to be uploaded)
    ),
    html.Br(),
    html.Button(
        "✥ Append", id="append-uploads", className="refresh-files-button", n_clicks=0
    ),  # (📁+📁...)
    html.Button(
        "(↻ Refresh Uploads List)",
        id="refresh-uploads",
        className="refresh-files-button",
        n_clicks=0,
    ),
    html.Button(
        "❌Reset Uploads",
        id="clear-uploads",
        className="refresh-files-button",
        n_clicks=0,
    ),
    html.Br(),
    #####################
    ####    NOTE:    ####
    ##    PIPELINE     ##
    ###  O U T P U T  ###
    #####  INSERTS  #####
    ######  HERE:  ######
    html.Div(id="received-upload"),
    html.Div(id="saved-reports"),
    html.Div(id="output-data-upload"),
    #####################
    html.Div(
        [
            html.Button(
                "—Initiate Pipeline—",
                id="initiate-pipeline",
                n_clicks=0,
                className="hvr-float-shadow",
            ),
            html.Br(),
            html.Br(),
            html.H6(
                "⮩[Est.] Required Execution Time ≤ ≈ X s (per input sample)",
                style={"textAlign": "center", "color": "unset"},
            ),
            html.Br(),
        ],
        style={"textAlign": "center", "position": "relative"},
    ),
    html.H5(
        html.Div(
            [
                html.Blockquote(" ⚠ Cautionary notes / hints / advice / warnings - #1"),
                html.Blockquote(" ⚠ Cautionary notes / hints / advice / warnings - #2"),
            ]
        ),
        style={
            "fontSize": "0.85rem",
            "color": "#00000080",
            "width": "55%",
            "marginLeft": "22.5%",
            "textAlign": "justify",
        },
        id="pipeline-progress-disclaimer",
    ),
    html.Br(),
    html.Button("—Clear Current QC Results Output—", id="clear-pipeline", n_clicks=0),
    html.Br(),
    html.Br(),
    html.Div(
        [
            html.Span(
                "ℹ| Hint: Check the log! It may be very informative...",
                className="notes",
            ),
            html.Br(),
            html.Span(
                "(⮩️🚪: Refresh [by selecting] the 'Download Output Files'⤑'Log Files' option below for live updates of all ⌁backend⌁ app execution activity.)",
                className="notes",
                style={"fontSize": "0.75rem", "color": "gray"},
            ),
        ],
        style={"width": "33.3%", "marginLeft": "33.3%"},
    ),
    html.Br(),
    html.Div(
        [
            dcc.Input(
                placeholder="–Enter a Previous RUN ID–",
                type="text",
                value="",
                id="save-results-as",
                disabled=True,
            ),
            html.Div(
                [
                    html.Span(
                        html.Button(
                            "Gather Output from Saved History",
                            id="save-user-results",
                            n_clicks=0,
                            disabled=True,
                        )
                    ),
                    html.Span(
                        html.Button(
                            "(↻ 📖 Show Preview)",
                            id="refresh-user-history",
                            n_clicks=0,
                            disabled=True,
                        )
                    ),
                ]
            ),
        ],
        style={"display": "none"},
    ),
    html.Hr(id="download-links"),
    html.Br(),
    html.Div(dash_table.DataTable(data=[{}]), style={"display": "none"}),
    html.H1("Download Output Files ⬇💻"),
    html.Br(),
    html.Span(className="fader-line-short", style={"marginBottom": "-36px"}),
    html.H4("""Choose from the listed file types to limit downloads (or view all)"""),
    html.P("E.g., Select LOG to view the audit trail of your current session."),
    html.Div(
        downloads,
        style={"width": "60%", "marginLeft": "20%"},
        className="dash-custom-btn",
    ),
    html.Br(),
    html.H3("Output File(s) Download Links", style={"textAlign": "left"}),
    html.Ul(id="output-file-list", style={"textAlign": "left"}),
    html.Ul(id="download-all", style={"textAlign": "left"}),
    html.Button(
        ["Download All"],
        id="request-all-zipped",
        n_clicks=0,
        style={"fontFamily": "Roboto"},
    ),
    html.Hr(),
    html.Br(),
    html.P(
        f"\n\nJohn Collins | Bioinformatics\t{CURRENT_YEAR}\n",
        className="copyright",
        style={
            "fontSize": "1.1rem",
            "letterSpacing": "10px",
            "lineHeight": "2.0rem",
            "fontFamily": "'Cinzel', serif",
            "color": "#003b51",
            "marginBottom": "4.2rem",
            "textAlign": "center",
        },
    ),
    html.Img(src=app_logo, style={"width": "12.5%", "mixBlendMode": "screen"}),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.Br(),
]

children = [html.Div(components_list, style={"width": "98%", "marginLeft": "1%"})]
