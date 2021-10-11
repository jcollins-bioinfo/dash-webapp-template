#!/usr/bin/env python3.7
"""seqapp Core Bioinformatics Pipeline

Overview
--------
Contains the main seqapp functionality relies on for processing
(i.e., via a 'run' of the 'pipeline') user-uploaded inputt and returning 
transformed results.  These returned results data are displayed reactive-
ly via the UI and made available for direct file downloads via custom HTML-
transforming functions triggered by user callbacks and thus located in the
callbacks.py module.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from seqapp.config import *

from seqapp import app
from seqapp.utils import *


# logger = logging.getLogger(__name__)


def create_blank_df(header, index_name="NA"):
    """
    Function: create_blank_df
    Summary: InsertHere
    Examples: InsertHere
    Returns: InsertHere
    
    Args:
        header (TYPE): [...]
        index_name (str, optional): [...]
    
    Returns:
        TYPE: [...]
    """
    blank_entry = pd.DataFrame(
        [*itl.chain.from_iterable([[np.nan] for _ in range(len(header))])]
    ).T
    blank_entry.index = [f"{index_name}"]
    blank_entry.columns = header
    return blank_entry



def get_N_quals(df):
    """
    Parameters
    ----------
    df : pd.DataFrame
        Input df containing Sanger reads as rows w/ bases set to
        column 'seq' and corresponding quality score
    
    Returns
    -------
    pd.DataFrame
        Containing quality scores only for 'N' bases
    
    """
    bqs = []
    for n in range(df.shape[0]):
        bqs.append(
            [
                (b, q)
                for (b, q) in [*zip(df.iloc[n].seq, df.iloc[n].Q_arrays)]
                if b == "N"
            ]
        )
    N_quals = [q for (b, q) in [*itl.chain.from_iterable(bqs)]]
    df_NQs = pd.Series(N_quals)
    return df_NQs, df_NQs.describe()




def parse_contents(contents, filename, date, f_wout, session_log_file):
    """Parses user-uploaded input sequence files; namely, ABI Sanger
    Sequencing chromatogram 'trace' files. However, a variety of
    other bioinformatics sequence file types are also accepted.

    Args:
        contents (bytes): uploaded input file data via Dash uploads component
        filename (str): file name of the uploaded input
        date (int?): date modified of uploaded input
        f_wout (TYPE): file path of current session to write decoded sequence data
        session_log_file (str, optional): Deprecated [→No longer explicitly passing around log file paths.]

    Returns:
        list: Components array showing all uploaded files and displaying the 
              decoded FASTQ sequences and corresponding linear quality scores
    """
    # P A R S E   F I L E   U P L O A D  I N P U T S
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        ## READ IN : AB1 - SANGER
        # Chromatogram Sanger reads files
        if filename.endswith("ab1"):
            abi_decoded = io.BytesIO(decoded)
            df = abi2fastq(
                input_abi=filename,
                abi_contents=abi_decoded,
                f_wout=f_wout,
                abi_encoded=content_string,
            )
            if df.shape[0] < 1:
                return html.Div(
                    [
                        "There was an error processing this file.\n(\tTraceback:\n"
                        + f"{e}\n\t)."
                    ]
                )
        ## READ IN : FASTA - (ASSUME TCRα/β ligations)
        # TCR-alpha/beta allele-specific chain pairs sequences
        # i.e., Assume this is the refernce file already given by user.
        elif filename.endswith(tuple([".fa", ".fasta", ".FASTA"])):
            df, ref = parse_input_ref_fasta(
                input_fa=filename, fa_contents=io.StringIO(decoded.decode("utf-8"))
            )
        ## READ IN : FASTQ - (ASSUME TCRα/β ligations)
        # TCR-alpha/beta allele-specific chain pairs sequences
        elif filename.endswith(tuple([".fq", ".fastq", ".FASTQ"])):
            fastq = SeqIO.parse(io.StringIO(decoded), "fastq")
        ## READ IN : ARBITRARY DATA TABLES
        elif "csv" in filename:  # or "tsv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an Excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return html.Div(
            [
                f"⚠🤮:📄⤞🛇 There was an error processing this file: {filename}.\n(\tTraceback:\n"
                + f"{e}\n\t)."
            ]
        )
    return html.Div(
        [
            html.H5(filename),
            html.H6(now()),
            dash_table.DataTable(
                data=df.to_dict("rows"),
                columns=[{"id": c, "name": c} for c in df.columns],
                style_table={
                    "maxHeight": "600px",
                    "overflowY": "auto",
                    "overflowX": "auto",
                },
                style_cell={
                    "fontFamily": "Muli",
                    "fontSize": "0.7rem",
                    "whiteSpace": "normal",
                    "padding": "3px",
                    "textOverflow": "ellipsis",
                    "textAlign": "left",
                },
                style_header={
                    "fontWeight": "bold",
                    "fontSize": "0.8rem",
                    "cursor": "pointer",
                    "color": "rgba(0,0,180,0.75)",
                },
            ),
            html.Div("Raw Content"),
            html.Pre(
                contents[0:200] + "...",
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
            ),
        ]
    )


def q2p(phred_Sanger_Quality_score):
    """Quality [score] to probability (q2p)
    converter.
    
    Args:
        phred_Sanger_Quality_score (str): Input Q-Score as single-character string
    
    Returns:
        int: Output Q-Score as multi-character decimal probability.
    """
    Q = ord(phred_Sanger_Quality_score) - 33
    return round(10 ** (-Q / 10), 8)


def read_fasta(fa_contents, fa_out=None):
    """Parse input FASTA data.
    
    Args:
        fa_contents (TYPE): [...]
        fa_out (str, optional): [.fasta] output file path
    
    Returns:
        pd.DataFrame: Columnar tabulated FASTA data
    """
    fa_records = [*SeqIO.parse(fa_contents, "fasta")]
    app.logger.info(fa_records)
    reads = pd.concat(
        [
            pd.DataFrame(
                {x: str(getattr(seqr, x)) for x in ["id", "name", "seq", "[...]"]},
                index=[n],
            )
            for n, seqr in enumerate(fa_records)
        ]
    )
    reads.set_index("id", inplace=True)
    if fa_out:
        app.logger.info(f"Writing FASTA output for file: {fa_out}")
        SeqIO.write(fa_records, fa_out, "fasta")
        reads.to_csv(fa_out + ".DataFrame.tsv", sep="\t")
    return reads


def run_pipeline(
    RUN_ID, FINAL_OUTPUT_DIR, prefix_key="", exp="", well="", workflow="", session_log_file=""
):
    """Main parallelization of mapping & variant caller commands.

    Args:
        RUN_ID (str): Current RUN ID (e.g., SEQAPP_RUNID_20191103224547407862)
        FINAL_OUTPUT_DIR (str): local path to current session output directory
        exp (str, optional): Experiment ID
        well (str, optional): Plate Well ID
        workflow (str, optional): upstream process team 
        session_log_file (str, optional): path to current session log file
    """
    detected = [
        *filter(lambda dir: dir.startswith(prefix_key), os.listdir(FINAL_OUTPUT_DIR))
    ]
    app.logger.info(f"Samples detected: \n {detected}")
    with mp.Pool(processes=((mp.cpu_count() * 2) + 1)) as p:
        pipeline_stream = p.map(
            partial(
                run_sequence_alignment_with_sangerseqqc,
                RUN_ID=RUN_ID,
                FINAL_OUTPUT_DIR=FINAL_OUTPUT_DIR,
                exp=exp,
                well=well,
                workflow=workflow,
                session_log_file=session_log_file,
            ),
            (*(detected),),
        )
    return pipeline_stream


def wrap_seq_nucleic(seq, wrap=125):
    """Wraps input genetic sequence strings and returns
    tuple of 'wrap'-limited width with tuple zipped numeric
    indeces which can optionally be printed alongside each
    line of sequence code.

    Args:
        seq (str): DNA/RNA/AA sequence to display
        wrap (int, optional): set displayed sequence line length

    Returns:
        zipped tuple: of paired (wrapped seq text, seq index) values per line
    """
    seq_lines = [seq[x_i : x_i + wrap] for x_i in range(0, len(seq), wrap)]
    seq_indeces = [
        (
            "".join(
                [
                    f"000{str(x_i)}"[-4:] + ":...." * 4 + "|"
                    for x_i in range(
                        len(ljoin(seq_lines[: n - 1])), len(ljoin(seq_lines[:n])), 25
                    )
                ]
            )
        )[: len(seq_lines[n - 1])]
        for n in range(1, len(seq_lines) + 1)
    ]
    return zip(seqlines, seq_indeces)
