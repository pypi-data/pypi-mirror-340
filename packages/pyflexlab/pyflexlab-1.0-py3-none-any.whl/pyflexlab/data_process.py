#!/usr/bin/env python
"""This module is responsible for processing and plotting the data"""

from typing import Literal
import pandas as pd

from .file_organizer import FileOrganizer, print_help_if_needed


class DataProcess(FileOrganizer):
    """This class is responsible for processing the data"""

    def __init__(self, proj_name: str) -> None:
        """
        Initialize the FileOrganizer and load the settings for matplotlib saved in another file

        Args:
        - proj_name: the name of the project
        """
        super().__init__(proj_name)
        self.dfs = {}

    @print_help_if_needed
    def load_dfs(
        self,
        measure_mods: tuple[str],
        *var_tuple: float | str,
        tmpfolder: str = "",
        measure_nickname: str = "",
        cached: bool = False,
        header: Literal[None, "infer"] = "infer",
        skiprows: int = None,
    ) -> pd.DataFrame:
        """
        Load a dataframe from a file, save the dataframe as a member variable and also return it

        Args:
        - measure_mods: the measurement modules
        - *var_tuple: the arguments for the modules
        - **kwargs: the arguments for the pd.read_csv function
        - cached: whether to save the df into self.dfs["cache"] instead of self.dfs (overwritten by the next load_dfs call, only with temperary usage)
        """
        file_path = self.get_filepath(
            measure_mods,
            *var_tuple,
            tmpfolder=tmpfolder,
            parent_folder=measure_nickname,
        )
        mainname_str, _ = FileOrganizer.name_fstr_gen(*measure_mods)
        if not cached:
            self.dfs[mainname_str] = pd.read_csv(
                file_path,
                sep=",",
                skiprows=skiprows,
                header=header,
                float_precision="round_trip",
            )
            return self.dfs[mainname_str].copy()
        else:
            self.dfs["cache"] = pd.read_csv(
                file_path,
                sep=",",
                skiprows=skiprows,
                header=header,
                float_precision="round_trip",
            )
            return self.dfs["cache"].copy()

    def rename_columns(self, measurename_main: str, rename_dict: dict) -> None:
        """
        Rename the columns of the dataframe

        Args:
        - rename_dict: the renaming rules, e.g. {"old_name": "new_name"}
        """
        self.dfs[measurename_main].rename(columns=rename_dict, inplace=True)
        if "cache" in self.dfs:
            self.dfs["cache"].rename(columns=rename_dict, inplace=True)

    @property
    def fig_path(self, measure_nickname: str) -> str:
        """
        Get the path to the figure

        Args:
        - measure_nickname: the nickname of the measure
        """
        fig_dir = self.proj_path / "figs" / measure_nickname
        return fig_dir

def calc_relative_mr(df: pd.DataFrame, tolerance: float = 5E-3) -> tuple[pd.DataFrame, float]:
    """
    Calculate the relative value of MR

    Args:
    - df: the dataframe
    - tolerance: the tolerance of the reference value

    Returns:
    - df: the dataframe with the relative value of MR
    - r_ref: the reference value of MR
    """
    df = df.copy()
    ref_df = df[abs(df["B"] - 0) <= tolerance].copy()
    r_ref = ref_df["V_source"].mean() / ref_df["I"].mean()
    df["r_mr"] = df["V_source"] / df["I"] / r_ref
    return df, r_ref
