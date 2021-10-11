#!/usr/bin/env python3.7
"""APP PAGE LAYOUT - ALL COMPONENTS COMPRISING THE DOM
Contains the Dash Core Components (dcc) 'Tabs' components, which
collectively passes all application page layout components via
per-tab components-arrays bundled in 'dcc.Tab' components.

Attributes:
    children (list): dcc.Tabs singular component, comprised
    of all tabs for the single-page app UI, and which gets imported
    and passed to the `html.Div(id="page-content")` object in
    deploy.py.
    tabs (list): Dash Core Components - Tab objects
"""
from config import *
# from tabs.faq import children as faq_tab
# from tabs.howto import children as howto_tab
# from tabs.links import children as links_tab
from tabs.main_page import children as main_tab

tabs = [
    dcc.Tab(label="dash-webapp-template", children=main_tab),
    # dcc.Tab(label="HOWTO", children=howto_tab),
    # dcc.Tab(label="Links & Other Tools", children=links_tab),
    # dcc.Tab(label="Q&A / Help", children=faq_tab),
]

children = [dcc.Tabs(id="tabs", children=tabs)]