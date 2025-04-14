#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2024-present Raffaele Mancuso <raffaele.mancuso4@unibo.it>
# SPDX-License-Identifier: MIT

import pandas
import logging

# -- PANDAS DATAFRAME --- #

def mvcols(self, start_cols=list(), end_cols=list()):
    # Make sure start_cols and end_cols are lists
    if isinstance(start_cols, str):
        start_cols = [start_cols]
    if isinstance(end_cols, str):
        start_cols = [end_cols]
    # Make sure columns exist in the dataframe
    for col in start_cols + end_cols:
        if col not in self.columns:
            raise ValueError(f"Column '{col}' not found in dataframe")
    # Get columns for which we preserve the order
    cols = [x for x in self.columns if ((x not in start_cols) and (x not in end_cols))]
    # New column ordering
    cols = start_cols + cols + end_cols
    # Return
    return self[cols]
pandas.DataFrame.mvcols = mvcols

def df_dropna_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        nrow0 = self.shape[0]
        out_df = self.dropna_original(*args, **kwargs)
        if not kwargs.get("inplace", False):
            nrow1 = out_df.shape[0]
        else:
            nrow1 = self.shape[0]
        logging.getLogger("dwlog").info(f"Dropped {perc(nrow0-nrow1,nrow0)} rows")
    finally:
        pandas_monkey()
    return out_df

def df_sort_values(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        out_df = self.sort_values_original(*args, **kwargs)
        logging.getLogger("dwlog").info(f"Sorted on {args[0]}")
    finally:
        pandas_monkey()
    return out_df

def df_drop_duplicates_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        nrow0 = self.shape[0]
        out_df = self.drop_duplicates_original(*args, **kwargs)
        if not kwargs.get("inplace", False):
            nrow1 = out_df.shape[0]
        else:
            nrow1 = self.shape[0]
        logging.getLogger("dwlog").info(f"Dropped {perc(nrow0-nrow1,nrow0)} duplicated rows, "
                                            f"remains {perc(nrow1,nrow0)} rows")
    finally:
        pandas_monkey()
    return out_df

def df_nunique_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        nun = self.nunique_original(*args, **kwargs)
        logging.getLogger("dwlog").info(f"There are {nun:,d} unique rows")
    finally:
        pandas_monkey()
    return nun

def df_groupby_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        nun = self.groupby_original(*args, **kwargs)
        if isinstance(args[0], str):
            groups = args[0]
        elif isinstance(args[0], list):
            groups = ", ".join(args[0])
        else:
            groups = "ERROR"
        logging.getLogger("dwlog").info(f"Grouped by {groups}")
    finally:
        pandas_monkey()
    return nun

def df_query_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        nrow0 = self.shape[0]
        out_df = self.query_original(*args, **kwargs)
        if not kwargs.get("inplace", False):
            nrow1 = out_df.shape[0]
        else:
            nrow1 = self.shape[0]
        logging.getLogger("dwlog").info(f"Dropped {nrow0-nrow1}/{nrow0} rows")
    finally:
        pandas_monkey()
    return out_df

def df_head_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        nrow0 = self.shape[0]
        out_df = self.head_original(*args, **kwargs)
        if not kwargs.get("inplace", False):
            nrow1 = out_df.shape[0]
        else:
            nrow1 = self.shape[0]
        n = kwargs.get("n", args[0])
        logging.getLogger("dwlog").info(f"Get first {n} rows, "
                                            f"selected {nrow0-nrow1}/{nrow0} rows")
    finally:
        pandas_monkey()
    return out_df

def df_tail_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    try:
        nrow0 = self.shape[0]
        out_df = self.tail_original(*args, **kwargs)
        if not kwargs.get("inplace", False):
            nrow1 = out_df.shape[0]
        else:
            nrow1 = self.shape[0]
        n = kwargs.get("n", args[0])
        logging.getLogger("dwlog").info(f"Get last {n} rows, "
                                            f"selected {nrow0-nrow1}/{nrow0} rows")
    finally:
        pandas_monkey()
    return out_df
    
def df_rename_monkey(self, *args, **kwargs):
    def proc_pair(x,y):
        col_pairs = list(zip(x, y))
        col_pairs = list(filter(lambda x: x[0]!=x[1], col_pairs))
        col_pairs = [str(x[0])+" -> "+str(x[1]) for x in col_pairs]
        col_pairs = ", ".join(col_pairs)
        return col_pairs
    # Main
    pandas_unmonkey()
    try:
        # Get starting columns and indexes
        start_cols = self.columns
        start_ixs = self.index
        # Rename
        out_df = self.rename_original(*args, **kwargs)
        if "inplace" in kwargs and kwargs["inplace"]:
            out_df = self
        # Get final columns and indexes
        fin_cols = out_df.columns
        fin_ixs = out_df.index
        # Make pairs
        col_pairs = proc_pair(start_cols, fin_cols)
        ix_pairs = proc_pair(start_ixs, fin_ixs)
        # Log
        if col_pairs and ix_pairs:
            msg = f"Renamed columns: {col_pairs}; Renamed indexes: {ix_pairs}"
        elif col_pairs:
            msg = f"Renamed columns: {col_pairs}"
        elif ix_pairs:
            msg = f"Renamed indexes: {ix_pairs}"
        else:
            msg = "No renaming"
        logging.info(msg)
    finally:
        pandas_monkey()
    return out_df

def df_getitem_monkey(self, key):
    out_df = self.getitem_original(key)
    if isinstance(out_df, pandas.Series):
        logging.getLogger("dwlog").info("Selected a single column, returned as a Series")
        return out_df
    start_cols = self.columns
    fin_cols = out_df.columns
    start_ixs = self.index
    fin_ixs = out_df.index
    logging.getLogger("dwlog").info(f"Selected {perc(len(fin_ixs),len(start_ixs))} rows "
                                         f"and {perc(len(fin_cols),len(start_cols))} columns")
    return out_df

def df_merge_monkey(self, *args, **kwargs):
    args = (self,) + args
    return merge_monkey(*args, **kwargs)

# -- PANDAS DATAFRAMEGROUPBY --- #

def dfgb_head_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    out_df = self.head_original(*args, **kwargs)
    nrow1 = out_df.shape[0]
    n = kwargs.get("n", args[0])
    logging.getLogger("dwlog").info(f"Get first {n:,d} rows of each group, "
                                         f"for a total of {nrow1:,d} rows")
    pandas_monkey()
    return out_df

def dfgb_tail_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    out_df = self.tail_original(*args, **kwargs)
    nrow1 = out_df.shape[0]
    n = kwargs.get("n", args[0])
    logging.getLogger("dwlog").info(f"Get last {n:,d} rows of each group, "
                                         f"for a total of {nrow1:,d} rows")
    pandas_monkey()
    return out_df

# -- PANDAS SERIES --- #

def sr_drop_duplicates_monkey(self, *args, **kwargs):
    pandas_unmonkey()
    nrow0 = self.shape[0]
    out_df = self.drop_duplicates_original(*args, **kwargs)
    if not kwargs.get("inplace", False):
        nrow1 = out_df.shape[0]
    else:
        nrow1 = self.shape[0]
    logging.getLogger("dwlog").info(f"Dropped {perc(nrow0-nrow1,nrow0)} rows, "
                                         f"remains {perc(nrow1,nrow0)} rows")
    pandas_monkey()
    return out_df

# -- PANDAS NAMESPACE --- #

def concat_monkey(dfs, *args, **kwargs):
    out_df = pandas.concat_original(dfs, *args, **kwargs)
    ls = [f"({df.shape[0]:,d} x {df.shape[1]:,d})" for df in dfs]
    ls = " + ".join(ls)
    logging.getLogger("dwlog").info(f"Concatenating {ls} -> ({out_df.shape[0]:,d} x {out_df.shape[1]:,d})")
    return out_df

def merge_monkey(*args, **kwargs):
    pandas_unmonkey()
    to_delete = False
    if "indicator" in kwargs and kwargs["indicator"] is False:
        raise ValueError("The 'indicator' argument must be set to True")
    elif "indicator" not in kwargs:
        kwargs["indicator"] = True
        to_delete = True
    out_df = pandas.merge_original(*args, **kwargs)
    stats_df = pandas.DataFrame({"n":out_df["_merge"].value_counts(), "p":out_df["_merge"].value_counts()/out_df["_merge"].shape[0]})
    stats_df["n"] = stats_df["n"].apply(lambda x: "{:,}".format(x)) 
    stats_df["p"] = stats_df["p"].apply(lambda x: "{:.2%}".format(x))
    stats_df.index.name = None
    logging.getLogger("dwlog").info(f"\n{stats_df}\n")
    if to_delete:
        out_df.drop(columns=["_merge"], inplace=True)
    pandas_monkey()
    return out_df

def read_excel_monkey(*args, **kwargs):
    out_df = pandas.read_excel_original(*args, **kwargs)
    file = args[0]
    logging.getLogger("dwlog").info(f"Read Excel file '{file}' with shape ({out_df.shape[0]:,d} x {out_df.shape[1]:,d})")
    return out_df

def read_csv_monkey(*args, **kwargs):
    out_df = pandas.read_csv_original(*args, **kwargs)
    file = args[0]
    logging.getLogger("dwlog").info(f"Read CSV file '{file}' with shape ({out_df.shape[0]:,d} x {out_df.shape[1]:,d})")
    return out_df

def read_sql_query_monkey(*args, **kwargs):
    out_df = pandas.read_sql_query_original(*args, **kwargs)
    logging.getLogger("dwlog").info(f"Read SQL query with shape ({out_df.shape[0]:,d} x {out_df.shape[1]:,d})")
    return out_df


# --- INITIALIZERS --- #

def perc(a,b):
    p = round((a/b)*100, 2)
    return f"{a:,d}/{b:,d} ({p}%)"

def pandas_monkey_init():
    pandas.DataFrame.rename_original = pandas.DataFrame.rename
    pandas.DataFrame.rename_monkey = df_rename_monkey
    pandas.DataFrame.getitem_original = pandas.DataFrame.__getitem__
    pandas.DataFrame.getitem_monkey = df_getitem_monkey
    pandas.DataFrame.merge_original = pandas.DataFrame.merge
    pandas.DataFrame.merge_monkey = df_merge_monkey
    pandas.Series.drop_duplicates_original = pandas.Series.drop_duplicates
    pandas.Series.drop_duplicates_monkey = sr_drop_duplicates_monkey
    pandas.concat_original = pandas.concat
    pandas.concat_monkey = concat_monkey
    pandas.merge_original = pandas.merge
    pandas.merge_monkey = merge_monkey
    pandas.read_excel_original = pandas.read_excel
    pandas.read_excel_monkey = read_excel_monkey
    pandas.read_csv_original = pandas.read_csv
    pandas.read_csv_monkey = read_csv_monkey
    pandas.read_sql_query_original = pandas.read_sql_query
    pandas.read_sql_query_monkey = read_sql_query_monkey
    pandas.DataFrame.groupby_original = pandas.DataFrame.groupby
    pandas.DataFrame.groupby_monkey = df_groupby_monkey
    pandas.DataFrame.query_original = pandas.DataFrame.query
    pandas.DataFrame.query_monkey = df_query_monkey
    pandas.DataFrame.nunique_original = pandas.DataFrame.nunique
    pandas.DataFrame.nunique_monkey = df_nunique_monkey
    pandas.DataFrame.drop_duplicates_original = pandas.DataFrame.drop_duplicates
    pandas.DataFrame.drop_duplicates_monkey = df_drop_duplicates_monkey
    pandas.DataFrame.sort_values_original = pandas.DataFrame.sort_values
    pandas.DataFrame.sort_values_monkey = df_sort_values
    pandas.DataFrame.dropna_original = pandas.DataFrame.dropna
    pandas.DataFrame.dropna_monkey = df_dropna_monkey
    pandas.DataFrame.head_original = pandas.DataFrame.head
    pandas.DataFrame.head_monkey = df_head_monkey
    pandas.DataFrame.tail_original = pandas.DataFrame.tail
    pandas.DataFrame.tail_monkey = df_tail_monkey
    pandas.api.typing.DataFrameGroupBy.head_original = pandas.api.typing.DataFrameGroupBy.head
    pandas.api.typing.DataFrameGroupBy.head_monkey = dfgb_head_monkey
    pandas.api.typing.DataFrameGroupBy.tail_original = pandas.api.typing.DataFrameGroupBy.tail
    pandas.api.typing.DataFrameGroupBy.tail_monkey = dfgb_tail_monkey

def pandas_monkey():
    pandas.DataFrame.drop_duplicates = pandas.DataFrame.drop_duplicates_monkey
    pandas.DataFrame.dropna = pandas.DataFrame.dropna_monkey
    pandas.DataFrame.query = pandas.DataFrame.query_monkey
    pandas.DataFrame.rename = pandas.DataFrame.rename_monkey
    pandas.DataFrame.__getitem__ = pandas.DataFrame.getitem_monkey
    pandas.concat = pandas.concat_monkey
    pandas.merge = pandas.merge_monkey
    pandas.read_excel = pandas.read_excel_monkey
    pandas.read_csv = pandas.read_csv_monkey
    pandas.read_sql_query = pandas.read_sql_query_monkey
    pandas.DataFrame.nunique = pandas.DataFrame.nunique_monkey
    pandas.Series.drop_duplicates = pandas.Series.drop_duplicates_monkey
    pandas.DataFrame.groupby = pandas.DataFrame.groupby_monkey
    pandas.DataFrame.merge = pandas.DataFrame.merge_monkey
    pandas.DataFrame.sort_values = pandas.DataFrame.sort_values_monkey
    pandas.DataFrame.head = pandas.DataFrame.head_monkey
    pandas.DataFrame.tail = pandas.DataFrame.tail_monkey
    pandas.api.typing.DataFrameGroupBy.head = pandas.api.typing.DataFrameGroupBy.head_monkey
    pandas.api.typing.DataFrameGroupBy.tail = pandas.api.typing.DataFrameGroupBy.tail_monkey

def pandas_unmonkey():
    pandas.DataFrame.drop_duplicates = pandas.DataFrame.drop_duplicates_original
    pandas.DataFrame.dropna = pandas.DataFrame.dropna_original
    pandas.DataFrame.query = pandas.DataFrame.query_original
    pandas.DataFrame.rename = pandas.DataFrame.rename_original
    pandas.DataFrame.__getitem__ = pandas.DataFrame.getitem_original
    pandas.concat = pandas.concat_original
    pandas.merge = pandas.merge_original
    pandas.read_excel = pandas.read_excel_original
    pandas.read_csv = pandas.read_csv_original
    pandas.read_sql_query = pandas.read_sql_query_original
    pandas.DataFrame.nunique = pandas.DataFrame.nunique_original
    pandas.Series.drop_duplicates = pandas.Series.drop_duplicates_original
    pandas.DataFrame.groupby = pandas.DataFrame.groupby_original
    pandas.DataFrame.merge = pandas.DataFrame.merge_original
    pandas.DataFrame.sort_values = pandas.DataFrame.sort_values_original
    pandas.DataFrame.head = pandas.DataFrame.head_original
    pandas.DataFrame.tail = pandas.DataFrame.tail_original
    pandas.api.typing.DataFrameGroupBy.head = pandas.api.typing.DataFrameGroupBy.head_original
    pandas.api.typing.DataFrameGroupBy.tail = pandas.api.typing.DataFrameGroupBy.tail_original

try:
    pandas.monekypatched
except AttributeError:
    pandas_monkey_init()
    pandas_monkey()
    pandas.monekypatched = True