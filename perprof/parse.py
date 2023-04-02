"""
Functions to parse the files.

The files must be in the following format::

    ---
    <Metadata 01>: <Value 01>
    <Metadata 02>: <Value 02>
    ---
    <Problem Name 01> <Exit Flag 01> <Cost 01>
    <Problem Name 02> <Exit Flag 02> <Cost 02>
    <Problem Name 03> <Exit Flag 03> <Cost 03>
    ...
"""

import gettext
import os.path

# pylint: disable=import-outside-toplevel

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
THIS_TRANSLATION = gettext.translation("perprof", os.path.join(THIS_DIR, "locale"))
_ = THIS_TRANSLATION.gettext


def _error_message(filename, line_number, details):
    """
    Format the error message.

    Args:
        filename (str): name of the file with the error
        line_number (int): number of the line with the error
        details (str): details about the error

    Returns:
        error (str): the error message
    """
    return _("ERROR when reading line #{} of {}:\n    {}").format(
        line_number, filename, details
    )


def _str_sanitize(str2sanitize):
    """
    Sanitize the problem name for LaTeX.

    Args:
        str2sanitize (str): string to be sanitize
    Returns:
        output (std): sanitized string
    """
    return str2sanitize.replace("_", "-")


def _parse_yaml(options, yaml_header):
    """
    Parse the yaml header.

    Args:
        options (dict): the local options for the parser
        yaml_header (str): The YAML header
    """
    import yaml

    metadata = yaml.load(yaml_header, Loader=yaml.FullLoader)
    for opt in metadata:
        if opt not in options:
            raise ValueError("'" + opt + "'" + _(" is not a valid option for YAML."))
        options[opt] = metadata[opt]


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def parse_file(filename, parser_options):
    """
    Parse one file.

    Args:
        filename (str): name of the file to be parser
        parser_options (dict):
            dictionary with the following keys:

            - subset (list): list with the name of the problems to use
            - success (list): list with strings to mark sucess
            - mintime (float): minimum time running the solver
            - maxtime (float): maximum time running the solver
        bool free_format: if False request that fail be mark with ``d``

    Returns:
        data (dict): performance profile data
        algname (str): name of the solver
    """
    options = parser_options.copy()
    options["algname"] = _str_sanitize(filename)
    colopts = ["name", "exit", "time", "fval", "primal", "dual"]
    col = {}
    for colopt in colopts:
        # Columns starts at 1 but indexing at 0
        options["col_" + colopt] = colopts.index(colopt) + 1
        col[colopt] = colopts.index(colopt)
    data = {}
    with open(filename, encoding="utf-8") as file_:
        line_number = 0
        in_yaml = False
        yaml_header = ""
        for line in file_:
            line_number += 1
            ldata = line.split()
            if len(ldata) == 0:
                continue  # Empty line
            # This is for backward compatibility
            if ldata[0] == "#Name" and len(ldata) >= 2:
                options["algname"] = _str_sanitize(ldata[1])
            # Handle YAML
            elif ldata[0] == "---":
                if in_yaml:
                    _parse_yaml(options, yaml_header)
                    for colopt in colopts:
                        # Columns starts at 1 but indexing at 0
                        col[colopt] = options["col_" + colopt] - 1
                    in_yaml = False
                else:
                    in_yaml = True
            elif in_yaml:
                yaml_header += line
            # Parse data
            elif len(ldata) < 2:
                raise ValueError(
                    _error_message(
                        filename,
                        line_number,
                        _("This line must have at least 2 elements."),
                    )
                )
            else:
                ldata[col["name"]] = _str_sanitize(ldata[col["name"]])
                pname = ldata[col["name"]]
                if options["subset"] and pname not in options["subset"]:
                    continue
                if pname in data:
                    raise ValueError(
                        _error_message(
                            filename,
                            line_number,
                            _("Duplicated problem: ") + pname + ".",
                        )
                    )
                try:
                    time = float(ldata[col["time"]])
                except Exception as exc:
                    raise ValueError(
                        _error_message(
                            filename,
                            line_number,
                            _("Problem has no time/cost: ") + pname + ".",
                        )
                    ) from exc
                if time < options["mintime"]:
                    time = options["mintime"]
                if time >= options["maxtime"]:
                    continue
                if parser_options["compare"] == "optimalvalues":
                    try:
                        if parser_options["unc"]:
                            primal = 0.0
                        else:
                            primal = float(ldata[col["primal"]])
                        dual = float(ldata[col["dual"]])
                    except Exception as exc:
                        raise ValueError(
                            _error_message(
                                filename,
                                line_number,
                                _("Column for primal or dual is out of bounds"),
                            )
                        ) from exc
                    if max(primal, dual) > parser_options["infeas_tol"]:
                        continue
                    data[pname] = {"time": time, "fval": float("inf")}
                    try:
                        data[pname]["fval"] = float(ldata[col["fval"]])
                    except Exception as exc:
                        raise ValueError(
                            _error_message(
                                filename,
                                line_number,
                                _("Column for fval is out of bounds"),
                            )
                        ) from exc
                elif parser_options["compare"] == "exitflag":
                    if time == 0:
                        raise ValueError(
                            _error_message(
                                filename, line_number, _("Time spending can't be zero.")
                            )
                        )
                    if ldata[col["exit"]] in options["success"]:
                        if len(ldata) < 3:
                            raise ValueError(
                                _error_message(
                                    filename,
                                    line_number,
                                    _("This line must have at least 3 elements."),
                                )
                            )
                        data[pname] = {"time": time, "fval": float("inf")}
                    elif options["free_format"] or ldata[col["exit"]] == "d":
                        data[pname] = {"time": float("inf"), "fval": float("inf")}
                    else:
                        raise ValueError(
                            _error_message(
                                filename,
                                line_number,
                                _(
                                    "The second element in this lime must be {} or d."
                                ).format(", ".join(options["success"])),
                            )
                        )
                else:
                    raise KeyError(
                        _(
                            "The parser option 'compare' should be "
                            "'exitflag' or 'optimalvalues'"
                        )
                    )

    if not data:
        raise ValueError(
            _("ERROR: List of problems (intersected with subset, if any) is empty")
        )
    return data, options["algname"]
