
import base64
import collections
import datetime as dt
import functools
import itertools as itl
import json
import logging
import multiprocessing as mp
import operator as op
import os
import os.path as path
import random
import re
import shlex
import shutil
import string
import subprocess
import sys
import textwrap
import threading
import time
import traceback
import warnings
import zipfile

from base64 import b64encode
from collections import ChainMap
from collections import Counter
from collections import defaultdict
from functools import partial
from multiprocessing import Pool
from sys import exc_info
from traceback import format_exception

import Bio
import Levenshtein as pylev
import argon2
import asyncio
import bs4 # Beautiful Soup
import dash
import dash_bio as dashbio
import flask
import ftfy
import io
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.io as pyio
import plotly.offline as poff
import plotly.tools as tls
import requests
import scipy
import scipy.stats as stats
import seaborn as sns
import sklearn

from Bio import Alphabet
from Bio import Emboss
from Bio import SeqIO
from Bio.Alphabet import IUPAC
from Bio.Data.IUPACData import ambiguous_dna_values
from Bio.GenBank.Record import Record
from Bio.Seq import Seq
from Bio.SeqFeature import FeatureLocation
from Bio.SeqFeature import SeqFeature
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import six_frame_translations
from Bio.SubsMat.MatrixInfo import blosum62
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
from dataclasses import dataclass
from flask import Flask
from io import BytesIO
from io import StringIO
from matplotlib.collections import LineCollection
from pathlib import Path
from six.moves.urllib import request as urlreq
from typing import Any
from typing import List
from urllib.parse import quote_plus as urlsafe
from urllib.parse import unquote_plus as unquote


# mpl.use('Qt5Agg')


###          I - C E N T R A L  F U N C T I O N S

def now():
    """Microsecond-level timestamps.

    Returns:
        str: (punctuation-stripped)
    """
    return re.sub("[ :.\-]", "", str(dt.datetime.now()))


def today():
    """Alphanumeric-sortable [current] date
    in YYYYMMDD format.

    Examples:
        >>> today()
        20180924

    Returns:
        <str> today
    """
    return now()[:8]


def ntw(n):
    """Numbers to Words (ntw):
    Convert integers less than 100 from numeric
    type to spelled-out words, as strings.

    Args:
        n (int): 1 <= int(x) <= 99

    Returns:
        str: number in roman numerals
    """
    numbers_to_words = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        6: "VI",
        7: "VII",
        8: "VIII",
        9: "IX",
        10: "X",
        20: "XX",
        30: "XXX",
        40: "XL",
        50: "L",
        60: "LX",
        70: "LXX",
        80: "LXXX",
        90: "XC",
        100: "C",
        0: "",
    }
    try:
        return numbers_to_words[n]
    except KeyError:
        try:
            return numbers_to_words[n - n % 10] + numbers_to_words[n % 10]
        except KeyError:
            return "[error:Number out of range]"


clock = lambda: now()[:14]
gtt = lambda start: str(time.strftime(str(dt.timedelta(seconds=(tns() - start) / 1e9))))
log_exc = lambda log: log.critical("".join(format_exception(*exc_info())))
ran_rec = lambda: "".join(random.choices([*RECEPTORS], k=random.randint(1, 3)))
rpunct = lambda x: re.sub(f"[{string.punctuation}]", "", x)
tns = lambda: time.time_ns()
url_safe = lambda u: re.sub("[:*\/]", "-", u)



###           I I  -  S T A T I C   G L O B A L   D A T A  
#                      (CONSTANTS - DO NOT CHANGE)

CURRENT_YEAR = dt.datetime.today().year

#
# APP  | ESTABLISHMENT OF PROPER RELATIVE PATH POSITIONING
#
APP_HOME = "/var/www/Apps/dash-webapp-template"
APP_NAME = "seqapp" # NOTE: Change this!
TOP_DIR = path.join(*path.split(APP_HOME)[:-1])
GUNICORN_STDERR = f"{APP_HOME}/{APP_NAME}/app/prod/gunicorn/logs/{today()}"
RUN_OUTPUT_DIR = f"{APP_HOME}/{APP_NAME}/app/prod/sessions"

entity_schemas = pd.read_csv(f"{APP_HOME}/{APP_NAME}/assets/data/entity-schemas.csv", sep='\t')
#
#  ----| FILE HEADERS (Useful for, e.g., common DataFrames.)
#
seqtk_header = [
    "chr", "length", "#A", "#C", "#G", "#T", "#2", "#3", "#4", "#CpG", "#tv",
    "#ts", "#CpG-ts",
]
vcf_header = ["#CHROM", "POS", "REF", "ALT", "QUAL", "Pr(FP|Mut)", "INFO"]
bed_header = ["chrom", "chromStart", "chromEnd", "name", "score", "strand"]

#
# | ENV  | THIRD-PARTY (EXT.) TOOLS PATH SETUP
#
my_env = os.environ.copy()  # (deprec.?)
PATH_TO_ANACONDA3_ON_SERVER = f"{TOP_DIR}/opt/anaconda3/bin/"
a3 = PATH_TO_ANACONDA3_ON_SERVER

#
# | LOG  | REALTIME AUTOMATIC UP-TO-DATE VERSIONING REPORTING
#          including the 20 latest commit messages reported to the
#          "UPDATES" main app tab component near app title.
#
# git_dir = TOP_DIR

v = subprocess.run(["git", "describe", "--tags"],
                   cwd=APP_HOME,
                   capture_output=True)
VERSION = v.stdout.decode("utf-8").rstrip()

u = subprocess.run(["git", "log", "-n 50"], cwd=APP_HOME, capture_output=True)
UPDATES = u.stdout.decode("utf-8").rstrip().split("\n\ncommit")
# Remove "commit" from only first item in array for consistency
UPDATES = [UPDATES[0][7:]] + UPDATES[1:]

#
#  ----| LOGGING OF ALL ACTIVITY & DATA GENERATION
#
DAILY_SESSIONS_DIR = f"{RUN_OUTPUT_DIR}/{today()}"
os.makedirs(DAILY_SESSIONS_DIR, exist_ok=True)
logging_level = logging.INFO

#
#  ----| APPLICATION OUTPUT-DOWNLOAD COMPONENT - FILE EXT.'S OPTIONS
# (NOTE:VARIABLE COMPONENT CONFIG)
#
uxui_hints = [html.Blockquote(tip) for tip in [
    "You can single-click to select individual cells and use your keyboard's arrow keys to navigate to any data.",
    "You can hold down the shift key while selecting two symmetrically opposite cells to select the entire intervening cells for any custom range of data.",
    "You can multi-sort tables by clicking on any column names. Hint: Notice the change in direction of the indicator arrow (up+down/up/down) to figure out complex sorts!",
    "You can click two cells while holding down Shift to select entire whole ranges. Use ⬫Ctrl-⬫c⇾⬫v to Copy➟Paste out multiple plasmids into your own text editor program, Benchling, or Geneious, etc.",
    "You can navigate to the 'Download Links' section. Then, select 'Plasmid Reference Files' from the dropdown options (among others), after launching Step One above or Two below, and download all relevant reference maps.",
    "All output files displayed in the Download Links section can be downloaded in one-click as a single zip-compressed archive. This can then easily be extracted on your local machine by double-clicking.",
    "If you ever see an empty Coverage QC plot (i.e. the ones that show 'Mean Read Depth') - where none of the data is showing, simply single-click any of the items in the legend to force the data to appear [re-single-click the same item to make it itself re-appear, too, if/as desired]! (The reason this sometimes happens is due to the use of WebGL graphics, which allows for significantly faster computational construction of the Plot.ly graph components)",
    "You can click the camera-icon in any of the custom QC data visualization Plot.ly plots to download a high-resolution PNG image file of the current view!"]
    ]

output_filetype_genres = {
    "ALL":
    tuple([
        ".ab1", ".airr", ".bam", ".bcf", ".bed", ".csv", ".fa", ".fasta", ".fastq",
        ".fq", ".gatk", ".gb", ".gff", ".gz", ".jpg", ".log", ".pdf", ".picard",
        ".png", ".sam", ".seqtk", ".tsv", ".txt", ".vcf", ".xlsx", ".zip", ".b64",
    ]),
    "AGG_FQ":
    tuple([".fq", ".fastq"]),
    "CONSENSUS":
    tuple([".fasta"]),
    "GENBANK":
    tuple([".gb"]),
    "GENEIOUS":
    tuple([".fa", ".ab1", ".sam", ".vcf", ".fq", ".gb", ".gff"]),
    "ANNOT":
    tuple([".bed", ".airr", ".gb"]),
    "LOGS":
    tuple([".log"]),
    "MAPSTATS":
    tuple([".txt", ".tsv", ".picard", ".gatk", ".seqtk"]),
    "QUAL":
    tuple([".png", ".jpg", ".pdf"]),
    "SEQ_ALGN":
    tuple([".sam"]),
    "VCF":
    tuple([".vcf"]),
    "REF":
    tuple([".fasta", ".gb"]),
}


###       I I I  -  D Y N A M I C   G L O B A L   D A T A
#             (VARIABLE - YOU MAY NEED TO CHANGE THESE)

#  ---| APP USER ACCOUNTS
# (NOTE:VARIABLE COMPONENT CONFIG)
#
USERS = sorted(
    [
        # {"label": "__(Add me!)", "value": "ADD_REQUEST"},
        {
            "label": "John C",
            "value": "JOHN_COLLINS"
        },
        {
            "label": "User A",
            "value": "USER_A"
        },
        {
            "label": "User B",
            "value": "USER_B"
        },
        {
            "label": "_Guest",
            "value": "ANON_GUEST"
        },
    ],
    key=lambda d: d["label"],
)
USERS_REALNAMES = {u["value"]: u["label"].split()[0] for u in USERS}

