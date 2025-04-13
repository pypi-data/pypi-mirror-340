from typing import List

from bluer_options.terminal import show_usage, xtra
from bluer_ai.help.generic import help_functions as generic_help_functions
from bluer_sandbox.help.notebooks import help_functions as help_notebooks

from bluer_sandbox import ALIAS


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "notebooks": help_notebooks,
    }
)
