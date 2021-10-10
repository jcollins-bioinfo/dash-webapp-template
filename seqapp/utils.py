"""
U T I L S  |  app.utils
-------------
A general-use, application-agnostic (i.e., templatizable) 
   Python utilities module containing custom dataclasses, functions for 
   any/all variety of tasks expected to be very commonly required; 
   written non-specifically to any one project in *stand-alone* 
   fashion.

Attributes
----------
logger : logging.Logger
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from seqapp.config import *

logger = logging.getLogger(__name__)


def _verify_login():
    """Argon2-based user authentication cryptography (of sorts).

    Returns
    -------
    str
        secret
    """
    secret = f"{os.environ.get('DEFAULT_SECRET')}"
    if secret:
        h = argon2.hash(secret).encode()
        e = b64encode(f"{h}").decode("utf-8")
        s = e
    s = "Please enter your password."
    return s


def add_logfile(logfile, logger=logger):
    """Ensures creation of logging output file,
    via file handler addition to passed logger input.

    Parameters
    ----------
    logfile : str
        generated current session output logfile ID
    logger : logging.Logger
        current logger

    Returns
    -------
    logging.Logger
        logger with added file handler
    """
    import coloredlogs
    coloredlogs.install(level='INFO', logger=logger)
    logger.info(f"Creating logging `FileHandler({logfile})`...")
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s %(name)s %(processName)-12s %(module)s➜%(funcName)-40s↴\n%(asctime)s ⎙=%(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # if len(app.logger.handlers) < 1:
    #     app.logger.info("Adding logfile..")
    #     app.logger.addHandler(fh)
    #     app.logger.info("Added logfile..")
    return fh


def convert_html_to_dash(el, style=None):
    """[Quite] Conveniently auto-converts whole input HTML
    into the corresponding Python Dash HTML components. Uses
    Beautiful Soup to auto-parse into required HTML elements
    ('el') if given str input.

    Parameters
    ----------
    el : bs.element.NavigableString, str
        Accepts bs4 HTML 'element' object or raw html as string.
        (Input condition checked and converted by inner function)
        Beautiful Soup-parsed HTML element, by the tag (e.g., "<p>Hello</p>").
        If not already in bs4-format (just str instead), recursion is employed to simply
        auto bs4-parse the HTML into a `NavigableString` which can then be passed
        into the included Dash conversion.
    style : None, optional
        Style params for the HTML element.

    Returns
    -------
    Dash.html.Div()
        Where content (i.e. via attr 'children') is a list of Dash `html` components
        precisely mirroring the elements input as standard-format HTML.
    """
    ALLOWED_TAGS = {
        "a",
        "address",
        "b",
        "big",
        "blockquote",
        "br",
        "caption",
        "center",
        "cite",
        "div",
        "em",
        "font",
        "footer",
        "header",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "i",
        "img",
        "li",
        "ol",
        "option",
        "p",
        "pre",
        "s",
        "small",
        "span",
        "strong",
        "table",
        "td",
        "textarea",
        "th",
        "tr",
        "tt",
        "u",
        "ul",
    }

    def _extract_style(el):
        """Convert HTML-formatted style code into a
        format that can be passed to a Dash html object
        during instantiation, which underlies the
        conversion procedure herein.

        Parameters
        ----------
        el : bs.element.NavigableString

        Returns
        -------
        dict
            Dash-compatible style params
        """
        if not el.attrs.get("style"):
            return None
        return {
            k.strip(): v.strip()
            for k, v in [
                x.split(": ") for x in el.attrs["style"].split(";")
                if len(x) > 0
            ]
        }

    if type(el) is str:
        return convert_html_to_dash(bs.BeautifulSoup(el, "html.parser"))

    if type(el) == bs.element.NavigableString:
        return str(el)
    else:
        name = el.name
        style = _extract_style(el) if style is None else style
        contents = [convert_html_to_dash(x) for x in el.contents]
        if name.title().lower() not in ALLOWED_TAGS:
            return contents[0] if len(contents) == 1 else html.Div(contents)

    return getattr(html, name.title())(contents, style=style)



def convert_numerics(s):
    """Attempt to convert as many DataFrame columns
    into having numeric numpy/pandas dtypes as possible
    (e.g., `float64`, etc.).

    Parameters
    ----------
    s : pd.Series
        E.g., as supplied by an iterable/generator,
        say, via the Pandas apply method on the rows
        of a DataFrame:
        >>> pd.DataFrame.loc[:,col1].apply()

    Returns
    -------
    pd.Series
        dtype-transformed (possibly) input DataFrame
        sample [row] (or variate [col], i.e., if
        axis=1 for pd df operations)
    """
    try:
        s = pd.to_numeric(s.dropna().apply(float))
    except Exception as e:
        pass
    return s


def file_download_link(filename, get_all_zipped=False):
    """Generate properly formated (i.e. 'safe', etc.) URL allowing
    USER download of nearly any of the per-RUN generated output files.

    Parameters
    ----------
    filename : str
        Full path of file intended to be listed
        as a downloadable link.
    get_all_zipped : bool, optional

    Returns
    -------
    Dash.html.A()
        Url-safe-converted downloadable link.
    """
    if get_all_zipped:
        return html.A(
            re.sub(f"{RUN_OUTPUT_DIR}/", "", filename),
            href="/downloadZAll?value={}".format(urlsafe(filename)),
        )
    else:
        return html.A(
            re.sub(f"{RUN_OUTPUT_DIR}/", "", filename),
            href="/urlToDownload?value={}".format(urlsafe(filename)),
        )


def filesafe_ctime():
    """Returns a filename-safe (including accounting for
    accurate sorting behavior!) current timestamp.

    Returns
    -------
    str
        A current timestamp

    Examples
    --------
    >>> filesafe_ctime()
     '20191027_18101572230466'
    """
    return time.strftime("%Y%m%d_%H%m%s", time.gmtime())


def find_unique_ID(list_of_input_smpls):
    """Attempt to determine a unique ID shared among all input
    sample names/IDs, via a largest substring function performed
    combinatorially exhaustively pairwise among the input list.

    Parameters
    ----------
    list_of_input_smpls : list

    Returns
    -------
    list
        Unique set of all possible found shared uid's
    """
    if len(list_of_input_smpls) == 1:
        uid = list_of_input_smpls
    uid = list(
        set([
            largest_substr(a, b)
            for (a, b) in [*itl.combinations(list_of_input_smpls, 2)]
        ]))
    return uid


def now():
    """Microsecond-level timestamps.

    Returns
    -------
    str
        Underscore-delimited date, today, plus the current time
        as well down to sub-millisecond precision.
    """
    return re.sub("[ :.\-]", "", str(dt.datetime.now()))


def get_output_files(selected_filetypes,
                     final_output_dir=None):
    """List all files in the current RUN's output directory,
    as thus available for USER download.

    Parameters
    ----------
    selected_filetypes : []
        List of filename extensions representing the selected
        subset genre of output files (e.g., ['.bam', '.sam']
        for "Mapping" files).
    final_output_dir : None, optional str
        If given, should be the current user session `RUN_ID`
        full path; otherwise, if default <class 'NoneType'>,
        then looks up all files in the globally accumulated
        "Plasmids Archive".

    Returns
    -------
    list
        List of full filepaths for files to download.
    """
    files_to_dl = []
    if final_output_dir:
        dl_dir = final_output_dir
    else:
        dl_dir = PLASMIDS_ARCHIVE
    for topdir, currdir, files in os.walk(dl_dir):
        for filename in files:
            path = os.path.join(topdir, filename)
            if os.path.isfile(path):
                full_fn, ext = os.path.splitext(path)
                if ext in selected_filetypes:
                    files_to_dl.append(path)
    return files_to_dl


def initiate_logging(app=__name__, log_filename=None):
    """Add a 'FileHandler' to an input Logger() object.

    Parameters
    ----------
    app : str, optional
        Str name of current `app`; defaults to `__name__`
    log_filename : str, optional
        Provide to override default logfile name, which
        is the `__name__` of app (dash.Dash() or flask.Flask())
        dot timestamp dot log.

    Returns
    -------
    logging.Logger()
        Modified input with added FileHandler
    """
    if not log_filename:
        log_filename = f"{app}.{filesafe_ctime()}.log"
    logger = logging.getLogger(app)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    return logger


def largest_substr(s1, s2):
    """Determine and return the longest occurence of any
    possible substring of input string s2 located anywhere
    in input string s1.

    Parameters
    ----------
    s1 : str
        reference sequence to query
    s2 : str
        target sequence to find (in query)

    Returns
    -------
    str
        the largest found substring of s2 in s1

    Examples
    --------
    >>> largest_substr("GATTACA", "ATTACK")
    'ATTAC'
    """
    len1, len2 = len(s1), len(s2)
    ir, jr = 0, 0
    for i1 in range(len1):
        i2 = s2.find(s1[i1])
        while i2 >= 0:
            j1, j2 = i1 + 1, i2 + 1
            while j1 < len1 and j2 < len2 and s2[j2] == s1[j1]:
                if j1 - i1 > jr - ir:
                    ir, jr = i1, j1
                j1 += 1
                j2 += 1
            i2 = s2.find(s1[i1], i2 + 1)
    return s1[ir:jr + 1]


def ljoin(list_of_lists):
    """Flatten any n-multidimensional array of data & return
    a single list copy of it in only one dimension total.
    (Or in other words, take any aribtrarily nested list of
    lists [of lists, [...], etc.] and return a combined,
    single list.)
    
    Parameters
    ----------
    list_of_lists : list
        Multidimensional array. E.g.:
    >>> [['a', 'b', 'c'], [1, 2 3]]
    
    Returns
    -------
    list
        1-D array; e.g.:
    >>> ['a', 'b', 'c', 1, 2 3]
    """
    return [*itl.chain.from_iterable(list_of_lists)]


def make_randuid(salt="", n=8):
    """Generate an n-character ID drawn randomly from the 22-
    member string.hexdigits character set:
    >
    >    '0123456789abcdefABCDEF'
    >
    > Probability of uniqueness (for default length n=8 uid):
    >
    >    (1/22**8) = 1.822294453944271e-11

    Parameters
    ----------
    salt : str, optional
        Add salt to front of uid to
        mitigate non-uniqueness risk.
    n : int, optional
        Number of characters to randomly
        draw to create the uid.

    Returns
    -------
    str
        randomly generated hexdigits uid

    Examples
    --------
    >>> [make_randuid() for _ in range(3)]
    ['7eB5740b', 'B0B3e51a', 'C5E3941E']
    """
    return f"{salt}{''.join(random.choices(string.hexdigits, k=n))}"


def parallelized_dfapply_concat(
        file_list,
        jobs=((mp.cpu_count() * 2) + 1),
        drop_blank_cols=True,
        tab_delimited_input=True,
        max_cols=1000,
):
    """Parallelized dataframe concatenation via concomitant
    reading in of multiple files.

    Parameters
    ----------
    file_list : list
        List of <str> file paths.
    jobs : int, optional
        Number of workers in multiprocessing pool to spawn.
    drop_blank_cols : bool, optional
        Do not return entirely null column variates.
    tab_delimited_input : bool, optional
        Assumes tab separated data unless explicitly specified
        otherwise.
    max_cols : int, optional
        Cutoff to stop reading (horizontally) tabular input data

    Returns
    -------
    pd.DataFrame
        Single aggregated df

    """

    def df_reader(filename, max_cols=max_cols):
        """Read input data from an Excel (.xlsx) file,
        comma-separated raw text file; or else assumes
        tab-delimited raw text input.

        Parameters
        ----------
        filename : str
            Full path to file
        max_cols : int, optional
            Defaults to 1000

        Returns
        -------
        pd.DataFrame
        """
        if filename.endswith(".xlsx"):
            return pd.read_excel(filename, usecols=max_cols)
        elif filename.endswith(".csv") and not tab_delimited_input:
            return pd.read_csv(filename, usecols=max_cols)
        else:
            return pd.read_csv(filename, sep="\t", usecols=max_cols)

    with mp.Pool(jobs) as p:
        dfs = p.map(df_reader, file_list)
        df = pd.concat(dfs)

    if drop_blank_columns:
        df = df.dropna(axis=1, how="all")

    return df


def ntw(n):
    """Numbers to Words (ntw)
    -------------------------
    Convert integers less than 100 from numeric
    type to spelled-out words, as strings.
    
    Examples
    --------
    >>> ntw(44)
    >>> "XLIV"
    
    Parameters
    ----------
    n : int
        1 <= int(x) <= 99
    
    Returns
    -------
    str
        Roman Numeral equivalent
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


def today():
    """Current date in YYYYMMDD format.
    
    Examples
    --------
    >>> today()
    '20180924'
    
    Returns
    -------
    str
        pure alphanumeric date - today
    
    """
    return now()[:8]

  