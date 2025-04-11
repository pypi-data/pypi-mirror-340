# --- Embedded Documentation Data ---
# --- Pandas: Core Functionality ---
PANDAS_CORE_DOCS = [
    # === Creation ===
    {
        'name': 'DataFrame',
        'prefix': 'pd.',
        'sig': '(data=None, index=None, columns=None, ...)',
        'desc': 'Creates a DataFrame (a 2D table). `data` can be a dictionary, list of lists, numpy array, etc. `index` provides row labels, `columns` provides column labels.',
        'example': 'data = {"col1": [1, 2], "col2": [3, 4]}\ndf = pd.DataFrame(data=data)'
    },
    {
        'name': 'Series',
        'prefix': 'pd.',
        'sig': '(data=None, index=None, name=None, ...)',
        'desc': 'Creates a Series (a 1D labeled array, like a single column). `data` can be a list, numpy array, dictionary. `index` provides labels.',
        'example': 's = pd.Series([10, 20, 30], index=["a", "b", "c"], name="MySeries")'
    },
    # === Reading/Writing Data ===
    {
        'name': 'read_csv',
        'prefix': 'pd.',
        'sig': '(filepath_or_buffer, sep=",", header="infer", index_col=None, usecols=None, ...)',
        'desc': 'Reads a comma-separated values (CSV) file into a DataFrame. `filepath_or_buffer` is the path. `sep` is the delimiter. `header` identifies column names row. `index_col` sets a column as index. `usecols` selects specific columns to read.',
        'example': 'df = pd.read_csv("my_data.csv")\ndf_cols = pd.read_csv("data.csv", usecols=["Name", "Score"])'
    },
    {
        'name': 'to_csv',
        'prefix': 'df.',
        'sig': '(path_or_buf, sep=",", index=True, header=True, mode="w", ...)',
        'desc': 'Writes the DataFrame to a CSV file. `path_or_buf` is the output filename/path. `index=False` prevents writing the index. `header=False` prevents writing column names. `mode="a"` appends instead of overwriting.',
        'example': 'df.to_csv("output.csv", index=False)'
    },
    {
        'name': 'read_excel',
        'prefix': 'pd.',
        'sig': '(io, sheet_name=0, header=0, index_col=None, ...)',
        'desc': 'Reads an Excel file (.xls, .xlsx) into a DataFrame. `io` is the file path. `sheet_name` specifies the sheet to read (name or index). Requires `openpyxl` or `xlrd` installed.',
        'example': '# Needs openpyxl: pip install openpyxl\ndf = pd.read_excel("spreadsheet.xlsx", sheet_name="Sheet1")'
    },
    {
        'name': 'to_excel',
        'prefix': 'df.',
        'sig': '(excel_writer, sheet_name="Sheet1", index=True, ...)',
        'desc': 'Writes the DataFrame to an Excel file. `excel_writer` is the path. `sheet_name` sets the sheet name. Requires `openpyxl` installed.',
        'example': '# Needs openpyxl: pip install openpyxl\ndf.to_excel("output.xlsx", sheet_name="Results", index=False)'
    },
    # === Inspection ===
    {
        'name': 'head',
        'prefix': 'df_or_series.',
        'sig': '(n=5)',
        'desc': 'Returns the first `n` rows of a DataFrame or Series.',
        'example': 'first_rows = df.head()'
    },
    {
        'name': 'tail',
        'prefix': 'df_or_series.',
        'sig': '(n=5)',
        'desc': 'Returns the last `n` rows of a DataFrame or Series.',
        'example': 'last_rows = df.tail(3)'
    },
     {
        'name': 'info',
        'prefix': 'df.',
        'sig': '(verbose=True, show_counts=True, ...)',
        'desc': 'Prints a concise summary of a DataFrame: index dtype, column dtypes, non-null counts, memory usage.',
        'example': 'df.info()'
    },
     {
        'name': 'describe',
        'prefix': 'df_or_series.',
        'sig': '(percentiles=None, include=None, exclude=None)',
        'desc': 'Generates descriptive statistics (count, mean, std, min, max, percentiles) for numeric columns by default. Use `include="all"` for all columns, `include=["object"]` for strings, etc.',
        'example': 'numeric_stats = df.describe()\nall_stats = df.describe(include="all")'
    },
     {
        'name': 'shape',
        'prefix': 'df_or_series.',
        'sig': '(attribute)',
        'desc': 'Returns a tuple representing the dimensionality (rows, columns for DF; length, for Series) of the object.',
        'example': 'rows, cols = df.shape\nlength = series.shape[0]'
    },
     {
        'name': 'columns',
        'prefix': 'df.',
        'sig': '(attribute)',
        'desc': 'Returns the column labels (Index object) of the DataFrame.',
        'example': 'column_names = df.columns'
    },
     {
        'name': 'index',
        'prefix': 'df_or_series.',
        'sig': '(attribute)',
        'desc': 'Returns the row labels (index object) of the DataFrame or Series.',
        'example': 'row_index = df.index'
    },
    {
        'name': 'dtypes',
        'prefix': 'df_or_series.',
        'sig': '(attribute)',
        'desc': 'Returns the data types of the columns (for DF) or the Series.',
        'example': 'types = df.dtypes'
    },
    {
        'name': 'isnull',
        'prefix': 'df_or_series.',
        'sig': '()',
        'desc': 'Returns a boolean same-sized object indicating if values are missing (NaN, None, NaT). Often used with `.sum()` to count missing values per column/series.',
        'example': 'missing_mask = df.isnull()\nmissing_counts = df.isnull().sum()'
    },
    {
        'name': 'notnull',
        'prefix': 'df_or_series.',
        'sig': '()',
        'desc': 'Returns a boolean same-sized object indicating if values are *not* missing. Opposite of `isnull`.',
        'example': 'non_missing_mask = df.notnull()'
    },
    {
        'name': 'nunique',
        'prefix': 'df_or_series.',
        'sig': '(axis=0, dropna=True)',
        'desc': 'Counts the number of distinct elements. For DF, counts per column (`axis=0`) or row (`axis=1`). For Series, counts in the Series.',
        'example': 'unique_per_col = df.nunique()\nunique_in_series = df["Category"].nunique()'
    },
    {
        'name': 'duplicated',
        'prefix': 'df_or_series.',
        'sig': '(subset=None, keep="first")',
        'desc': 'Returns a boolean Series indicating which rows (DF) or values (Series) are duplicates. `keep="first"` marks subsequent duplicates as True. `keep="last"` marks previous ones. `keep=False` marks all duplicates.',
        'example': 'is_duplicate_row = df.duplicated()\nall_duplicates = df[df.duplicated(keep=False)]'
    },
    # === Selection / Indexing ===
     {
        'name': '[]',
        'prefix': 'df',
        'sig': '["col_name"] or [list_of_cols] or [boolean_mask]',
        'desc': 'Selects columns by name(s) or rows using a boolean Series/array (boolean indexing). Single column returns Series, multiple cols or boolean mask returns DataFrame.',
        'example': 'ages = df["Age"] # Select column\nsubset = df[["Name", "Score"]] # Select multiple columns\nhigh_scores = df[df["Score"] > 90] # Boolean indexing'
    },
     {
        'name': 'loc[]',
        'prefix': 'df_or_series.',
        'sig': '[row_label(s), column_label(s)]',
        'desc': 'Selects using *labels*. Can use single labels, lists, label slices, or boolean arrays/Series matching the index/columns.',
        'example': 'val = df.loc["idx_A", "Col_X"]\nsubset = df.loc[df["Group"] == "B", ["Col_Y", "Col_Z"]] # Boolean rows, label cols'
    },
     {
        'name': 'iloc[]',
        'prefix': 'df_or_series.',
        'sig': '[row_position(s), column_position(s)]',
        'desc': 'Selects using integer *positions*. Can use single integers, lists, integer slices, or boolean arrays matching dimensions.',
        'example': 'val = df.iloc[0, 1]\nsubset = df.iloc[0:5, [0, 2]] # First 5 rows, columns 0 and 2'
    },
     {
        'name': 'query',
        'prefix': 'df.',
        'sig': '(expr, inplace=False, **kwargs)',
        'desc': 'Queries the columns of a DataFrame with a boolean expression string `expr`. Often more readable than complex boolean indexing.',
        'example': 'result = df.query("Age > 30 and City == \"London\"")'
    },
    # === Data Manipulation ===
    {
        'name': 'copy',
        'prefix': 'df_or_series.',
        'sig': '(deep=True)',
        'desc': 'Creates a copy of the object. Important to avoid modifying the original data unintentionally when working with slices.',
        'example': 'df_copy = df.copy()'
    },
    {
        'name': 'rename',
        'prefix': 'df_or_series.',
        'sig': '(mapper=None, index=None, columns=None, inplace=False, ...)',
        'desc': 'Renames index labels or column names using a dictionary or function passed to `index` or `columns` args (or `mapper` for Series index).',
        'example': 'df_renamed = df.rename(columns={"old_name": "new_name", "val": "Value"})'
    },
    {
        'name': 'drop',
        'prefix': 'df.',
        'sig': '(labels=None, axis=0, index=None, columns=None, inplace=False, ...)',
        'desc': 'Drops specified labels (rows or columns). Use `labels` and `axis` (0 for rows, 1 for columns), or use `index` (for row labels) or `columns` (for column labels).',
        'example': 'df_dropped_cols = df.drop(columns=["ColA", "ColB"])\ndf_dropped_rows = df.drop(index=["idx1", "idx2"])'
    },
    {
        'name': 'astype',
        'prefix': 'df_or_series.',
        'sig': '(dtype, ...)',
        'desc': 'Casts the object (or specific columns of a DF) to a specified `dtype` (e.g., "int", "float", "str", "category", "datetime64[ns]").',
        'example': 'df["Count"] = df["Count"].astype(int)\ndf = df.astype({"Age": float, "Category": "category"})'
    },
     {
        'name': 'sort_values',
        'prefix': 'df_or_series.',
        'sig': '(by, axis=0, ascending=True, inplace=False, ...)',
        'desc': 'Sorts by values. For DF, specify column(s) with `by`. For Series, sorts the Series values. `ascending=False` for descending.',
        'example': 'df_sorted = df.sort_values(by=["Group", "Value"], ascending=[True, False])'
    },
     {
        'name': 'sort_index',
        'prefix': 'df_or_series.',
        'sig': '(axis=0, ascending=True, inplace=False, ...)',
        'desc': 'Sorts by the index labels.',
        'example': 'df_sorted = df.sort_index(ascending=False)'
    },
     {
        'name': 'dropna',
        'prefix': 'df_or_series.',
        'sig': '(axis=0, how="any", subset=None, inplace=False, ...)',
        'desc': 'Removes missing values (NaN). `axis=0` drops rows, `axis=1` drops columns. `subset` specifies labels to check.',
        'example': 'df_clean = df.dropna(subset=["EssentialColumn"])]'
    },
     {
        'name': 'fillna',
        'prefix': 'df_or_series.',
        'sig': '(value, method=None, inplace=False, ...)',
        'desc': 'Fills missing values (NaN) using `value` or a `method` like "ffill" (forward fill) or "bfill" (backward fill).',
        'example': 'df_filled = df.fillna(0)\nseries_ffilled = series.fillna(method="ffill")'
    },
    {
        'name': 'apply',
        'prefix': 'df_or_series_groupby.',
        'sig': '(func, axis=0, ...)',
        'desc': 'Applies a function `func` along an axis (0 for columns, 1 for rows for DF) or to each group after `groupby`. The function receives a Series (or DataFrame row) or a group DataFrame.',
        'example': 'df["ColA_norm"] = df["ColA"].apply(lambda x: (x - x.mean()) / x.std())\ndf.apply(np.sum, axis=0) # Sum columns\ndf.groupby("Group").apply(my_custom_func)'
    },
    {
        'name': 'map',
        'prefix': 'series.',
        'sig': '(arg, na_action=None)',
        'desc': 'Maps values of a Series according to an input mapping (dictionary, function, or Series). Used for element-wise transformation.',
        'example': 'series_mapped = series.map({"A": 1, "B": 2})\nseries_calc = series.map(lambda x: x * 10)'
    },
    {
        'name': 'set_index',
        'prefix': 'df.',
        'sig': '(keys, drop=True, append=False, inplace=False, ...)',
        'desc': 'Sets the DataFrame index (row labels) using one or more existing columns specified by `keys`. `drop=True` removes the column(s) used as the new index.',
        'example': 'df_indexed = df.set_index("ID")'
    },
    {
        'name': 'reset_index',
        'prefix': 'df_or_series.',
        'sig': '(level=None, drop=False, inplace=False, ...)',
        'desc': 'Resets the index, making the old index into a regular column(s). `drop=True` discards the old index instead of adding it as a column.',
        'example': 'df_reset = df.reset_index()\ndf_dropped_index = df.reset_index(drop=True)'
    },
    # === Grouping & Aggregation ===
     {
        'name': 'groupby',
        'prefix': 'df.',
        'sig': '(by, axis=0, level=None, as_index=True, sort=True, ...)',
        'desc': 'Groups rows based on values in column(s) specified by `by`. Returns a GroupBy object, typically followed by an aggregation.',
        'example': 'grouped = df.groupby("Category")'
    },
    {
        'name': 'agg',
        'prefix': 'df_or_series_groupby.',
        'sig': '(func, ...)',
        'desc': 'Applies one or more aggregation functions. Can be a single function name ("sum"), list of names (["sum", "mean"]), or a dictionary mapping columns to functions ({ "Value":"sum", "Count":"mean" }).',
        'example': 'agg_results = grouped.agg(["mean", "std"])\nagg_dict = grouped.agg(Max_Value=("Value", "max"), Avg_Count=("Count", "mean"))'
    },
    {
        'name': 'aggregate',
        'prefix': 'df_or_series_groupby.',
        'sig': '(func, ...)',
        'desc': 'Alias for `.agg()`.',
        'example': 'agg_results = grouped.aggregate(["mean", "std"])'
    },
     {
        'name': 'mean',
        'prefix': 'df_or_series_groupby.',
        'sig': '(numeric_only=True, ...)',
        'desc': 'Computes mean of groups (GroupBy) or along axis (DF/Series).',
        'example': 'mean_per_group = df.groupby("Category").mean()'
    },
     {
        'name': 'sum',
        'prefix': 'df_or_series_groupby.',
        'sig': '(numeric_only=True, ...)',
        'desc': 'Computes sum of groups (GroupBy) or along axis (DF/Series).',
        'example': 'sum_per_group = df.groupby("Category")["Value"].sum()'
    },
     {
        'name': 'count',
        'prefix': 'df_or_series_groupby.',
        'sig': '()',
        'desc': 'Computes count of non-NA values per group (GroupBy) or along axis (DF/Series).',
        'example': 'count_per_group = df.groupby("Category").count()'
    },
     {
        'name': 'size',
        'prefix': 'groupby.',
        'sig': '()',
        'desc': 'Computes group sizes (including NA values). Returns a Series.',
        'example': 'size_per_group = df.groupby("Category").size()'
    },
     {
        'name': 'min',
        'prefix': 'df_or_series_groupby.',
        'sig': '(numeric_only=True, ...)',
        'desc': 'Computes minimum value per group or along axis.',
        'example': 'min_per_group = df.groupby("Category")["Value"].min()'
    },
     {
        'name': 'max',
        'prefix': 'df_or_series_groupby.',
        'sig': '(numeric_only=True, ...)',
        'desc': 'Computes maximum value per group or along axis.',
        'example': 'max_per_group = df.groupby("Category")["Value"].max()'
    },
     {
        'name': 'median',
        'prefix': 'df_or_series_groupby.',
        'sig': '(numeric_only=True, ...)',
        'desc': 'Computes median value per group or along axis.',
        'example': 'median_per_group = df.groupby("Category")["Value"].median()'
    },
     {
        'name': 'std',
        'prefix': 'df_or_series_groupby.',
        'sig': '(numeric_only=True, ...)',
        'desc': 'Computes standard deviation per group or along axis.',
        'example': 'std_per_group = df.groupby("Category")["Value"].std()'
    },
     {
        'name': 'var',
        'prefix': 'df_or_series_groupby.',
        'sig': '(numeric_only=True, ...)',
        'desc': 'Computes variance per group or along axis.',
        'example': 'var_per_group = df.groupby("Category")["Value"].var()'
    },
     {
        'name': 'value_counts',
        'prefix': 'series.',
        'sig': '(normalize=False, sort=True, ascending=False, ...)',
        'desc': 'Returns counts of unique values in a Series. `normalize=True` gives proportions.',
        'example': 'counts = df["Type"].value_counts()\nproportions = df["Type"].value_counts(normalize=True)'
    },
    # === Combining / Reshaping ===
    {
        'name': 'merge',
        'prefix': 'pd.',
        'sig': '(left, right, how="inner", on=None, left_on=None, right_on=None, left_index=False, right_index=False, ...)',
        'desc': 'Combines two DataFrames based on common columns (`on`, `left_on`/`right_on`) or indices (`left_index`/`right_index`). `how` = "left", "right", "outer", "inner".',
        'example': 'merged_df = pd.merge(df_left, df_right, on="common_id", how="inner")'
    },
    {
        'name': 'concat',
        'prefix': 'pd.',
        'sig': '(objs, axis=0, join="outer", ignore_index=False, ...)',
        'desc': 'Concatenates (stacks) multiple Pandas objects (Series/DataFrames) along an axis. `axis=0` stacks vertically (rows), `axis=1` stacks horizontally (columns). `join="inner"` keeps only shared labels on the *other* axis. `ignore_index=True` creates a new default index.',
        'example': 'combined_df = pd.concat([df1, df2, df3], ignore_index=True)'
    },
    {
        'name': 'pivot_table',
        'prefix': 'df.',
        'sig': '(values=None, index=None, columns=None, aggfunc="mean", ...)',
        'desc': 'Creates a spreadsheet-style pivot table. Aggregates `values` based on groups specified by `index` (rows) and `columns` (columns). `aggfunc` specifies the aggregation function(s).',
        'example': 'pivot = df.pivot_table(values="Sales", index="Region", columns="Product", aggfunc="sum")'
    },
    {
        'name': 'melt',
        'prefix': 'df.',
        'sig': '(id_vars=None, value_vars=None, var_name=None, value_name="value")',
        'desc': 'Unpivots a DataFrame from wide format to long format. `id_vars` are columns to keep as identifiers. `value_vars` are columns to unpivot (defaults to all others).',
        'example': 'long_df = df.melt(id_vars=["Name"], value_vars=["Test1", "Test2"], var_name="Test", value_name="Score")'
    },
    # === String Operations (.str) ===
    {
        'name': 'contains',
        'prefix': 'series.str.',
        'sig': '(pat, case=True, na=None, ...)',
        'desc': 'Tests if a pattern `pat` (string or regex) is contained within each string of the Series. Returns boolean Series.',
        'example': 'contains_error = df["Log"].str.contains("ERROR", case=False)'
    },
    {
        'name': 'startswith',
        'prefix': 'series.str.',
        'sig': '(pat, na=None)',
        'desc': 'Tests if each string starts with `pat`. Returns boolean Series.',
        'example': 'starts_with_a = df["Name"].str.startswith("A")'
    },
    {
        'name': 'endswith',
        'prefix': 'series.str.',
        'sig': '(pat, na=None)',
        'desc': 'Tests if each string ends with `pat`. Returns boolean Series.',
        'example': 'is_png = df["Filename"].str.endswith(".png")'
    },
    {
        'name': 'replace',
        'prefix': 'series.str.',
        'sig': '(pat, repl, n=-1, case=None, regex=True, ...)',
        'desc': 'Replaces occurrences of `pat` (string or regex) with `repl` in each string of the Series.',
        'example': 'cleaned_text = df["Text"].str.replace("[^\w\s]", "", regex=True) # Remove punctuation'
    },
    {
        'name': 'lower',
        'prefix': 'series.str.',
        'sig': '()',
        'desc': 'Converts strings in the Series to lowercase.',
        'example': 'lower_case_names = df["Name"].str.lower()'
    },
    {
        'name': 'upper',
        'prefix': 'series.str.',
        'sig': '()',
        'desc': 'Converts strings in the Series to uppercase.',
        'example': 'upper_case_codes = df["Code"].str.upper()'
    },
    {
        'name': 'split',
        'prefix': 'series.str.',
        'sig': '(pat=None, n=-1, expand=False, ...)',
        'desc': 'Splits strings around a delimiter `pat`. `expand=True` returns a DataFrame with split parts in separate columns.',
        'example': 'split_names = df["FullName"].str.split(" ", expand=True)'
    },
    # === Datetime Operations (.dt) / Functions ===
    {
        'name': 'to_datetime',
        'prefix': 'pd.',
        'sig': '(arg, format=None, errors="raise", ...)',
        'desc': 'Converts argument `arg` (Series, list, etc.) to datetime objects. `format` specifies the expected date format string (e.g., "%Y-%m-%d"). `errors="coerce"` turns unparseable dates into NaT (Not a Time).',
        'example': 'df["Date"] = pd.to_datetime(df["DateString"], format="%m/%d/%Y")\ndf["Timestamp"] = pd.to_datetime(df["Epoch"], unit="s")'
    },
    {
        'name': 'year',
        'prefix': 'series.dt.',
        'sig': '(attribute)',
        'desc': 'Extracts the year from a Series of datetime objects.',
        'example': 'years = df["Date"].dt.year'
    },
    {
        'name': 'month',
        'prefix': 'series.dt.',
        'sig': '(attribute)',
        'desc': 'Extracts the month (1-12) from a Series of datetime objects.',
        'example': 'months = df["Date"].dt.month'
    },
    {
        'name': 'day',
        'prefix': 'series.dt.',
        'sig': '(attribute)',
        'desc': 'Extracts the day of the month (1-31) from a Series of datetime objects.',
        'example': 'days = df["Date"].dt.day'
    },
    {
        'name': 'hour',
        'prefix': 'series.dt.',
        'sig': '(attribute)',
        'desc': 'Extracts the hour (0-23) from a Series of datetime objects.',
        'example': 'hours = df["Timestamp"].dt.hour'
    },
    {
        'name': 'dayofweek',
        'prefix': 'series.dt.',
        'sig': '(attribute)',
        'desc': 'Extracts the day of the week (Monday=0, Sunday=6) from a Series of datetime objects.',
        'example': 'weekdays = df["Date"].dt.dayofweek'
    },
    {
        'name': 'date',
        'prefix': 'series.dt.',
        'sig': '(attribute)',
        'desc': 'Extracts the date part (no time) from a Series of datetime objects.',
        'example': 'just_dates = df["Timestamp"].dt.date'
    },
]

# --- Pandas: Plotting Methods (`df.plot.*`) ---
PANDAS_PLOT_DOCS = [
     {
        'name': 'line',
        'prefix': 'df.plot.',
        'sig': '(x=None, y=None, **kwargs)',
        'desc': 'Plot Series or DataFrame columns as lines. Uses the index by default for x-axis. `x` and `y` can specify column names.',
        'example': '# Assuming df is a DataFrame\ndf.plot.line(y="Value")\ndf.plot.line(x="Time", y="Temperature")'
    },
     {
        'name': 'bar',
        'prefix': 'df.plot.',
        'sig': '(x=None, y=None, **kwargs)',
        'desc': 'Create a vertical bar plot. Uses index for x-axis if `x` is None. `y` specifies column(s) for bar heights.',
        'example': 'df.plot.bar(y="Count")\ndf.plot.bar(x="Category", y="Amount")'
    },
     {
        'name': 'barh',
        'prefix': 'df.plot.',
        'sig': '(x=None, y=None, **kwargs)',
        'desc': 'Create a horizontal bar plot.',
        'example': 'df.plot.barh(y="Length")'
    },
     {
        'name': 'hist',
        'prefix': 'df.plot.',
        'sig': '(y=None, bins=10, **kwargs)',
        'desc': 'Draw one histogram per DataFrame column (or for a Series). `bins` controls number of bins.',
        'example': '# Plot histogram for each numeric column in df\ndf.plot.hist(alpha=0.5) \n# Plot histogram for a specific series\ndf["Age"].plot.hist(bins=20)'
    },
     {
        'name': 'box',
        'prefix': 'df.plot.',
        'sig': '(y=None, by=None, **kwargs)',
        'desc': 'Make a box-and-whisker plot for each column or grouped by another column (`by`). Shows median, quartiles, and outliers.',
        'example': 'df.plot.box(y=["ColA", "ColB"])\n# Boxplot of "Value" grouped by "Category"\ndf.plot.box(column="Value", by="Category")'
    },
     {
        'name': 'kde',
        'prefix': 'df.plot.',
        'sig': '(y=None, bw_method=None, **kwargs)',
        'desc': 'Generate Kernel Density Estimate plot (smoothed histogram) for Series or DataFrame columns.',
        'example': 'df["Score"].plot.kde()'
    },
     {
        'name': 'density',
        'prefix': 'df.plot.',
        'sig': '(bw_method=None, **kwargs)',
        'desc': 'Alias for `.kde()`',
        'example': 'df["Score"].plot.density()'
    },
     {
        'name': 'area',
        'prefix': 'df.plot.',
        'sig': '(y=None, stacked=True, **kwargs)',
        'desc': 'Create an area plot. `stacked=True` (default) stacks areas, `stacked=False` overlaps them.',
        'example': 'df.plot.area(y=["A", "B", "C"])'
    },
     {
        'name': 'pie',
        'prefix': 'df.plot.',
        'sig': '(y=None, **kwargs)',
        'desc': 'Generate a pie plot for a Series or a single DataFrame column specified by `y`.',
        'example': 'df["Counts"].plot.pie(autopct="%1.1f%%")'
    },
     {
        'name': 'scatter',
        'prefix': 'df.plot.',
        'sig': '(x, y, s=None, c=None, **kwargs)',
        'desc': 'Create a scatter plot using columns `x` and `y`. `s` can specify size based on another column, `c` can specify color based on another column.',
        'example': 'df.plot.scatter(x="Height", y="Weight", c="Age", colormap="viridis")'
    },
     {
        'name': 'hexbin',
        'prefix': 'df.plot.',
        'sig': '(x, y, C=None, gridsize=100, **kwargs)',
        'desc': 'Create a hexbin plot (2D histogram) using columns `x` and `y`. Good for visualizing density of points in a scatter plot. `gridsize` controls hexagon size.',
        'example': 'df.plot.hexbin(x="Longitude", y="Latitude", gridsize=20)'
    },
]

# --- Matplotlib: Pyplot Functions ---
MPL_PYPLOT_DOCS = [
    # Note: These are largely the same as before, kept for completeness
    {
        'name': 'figure',
        'prefix': 'plt.',
        'sig': '(num=None, figsize=None, ...)',
        'desc': 'Creates a new figure window for plotting. `figsize=(width, height)` sets the size in inches.',
        'example': 'fig = plt.figure(figsize=(8, 6)) # Creates an 8x6 inch figure'
    },
    {
        'name': 'subplots',
        'prefix': 'plt.',
        'sig': '(nrows=1, ncols=1, **kwargs)',
        'desc': 'Creates a figure and a set of subplots (Axes). Returns the figure and an array of Axes objects. This is the recommended way to create plots.',
        'example': 'fig, ax = plt.subplots() # Creates a figure with a single subplot (Axes)\nfig, axes = plt.subplots(2, 1) # Creates a figure with 2 rows, 1 column of subplots'
    },
    {
        'name': 'plot',
        'prefix': 'plt.',
        'sig': '(x, y, format_string="...", **kwargs)',
        'desc': 'Plots y versus x as lines and/or markers on the *current* Axes. The `format_string` combines color, marker, and line style (e.g., "ro-" for red circles connected by solid line). `kwargs` are extra options like `label="data1"`, `linewidth=2`.',
        'example': 'plt.plot([1, 2, 3], [4, 1, 5], "go--", label="Sample") # Green circles, dashed line'
    },
    {
        'name': 'scatter',
        'prefix': 'plt.',
        'sig': '(x, y, s=None, c=None, marker="o", **kwargs)',
        'desc': 'Creates a scatter plot of y versus x on the *current* Axes. `s` controls marker size, `c` controls marker color (can be a single color or sequence), `marker` sets the shape (e.g., "o", "s", "^").',
        'example': 'plt.scatter([1, 2, 3], [4, 1, 5], s=50, c="red", marker="^") # Red triangles, size 50'
    },
    {
        'name': 'bar',
        'prefix': 'plt.',
        'sig': '(x, height, width=0.8, bottom=None, **kwargs)',
        'desc': 'Creates a bar chart on the *current* Axes. `x` gives the positions of the bars, `height` gives their heights. `width` controls bar width.',
        'example': 'plt.bar(["A", "B", "C"], [10, 15, 7], color="skyblue")'
    },
    {
        'name': 'hist',
        'prefix': 'plt.',
        'sig': '(x, bins=None, range=None, density=False, **kwargs)',
        'desc': 'Computes and draws a histogram of data `x` on the *current* Axes. `bins` controls the number or edges of bins. `density=True` normalizes the histogram.',
        'example': 'data = [1, 2, 2, 3, 3, 3, 4, 4, 5]\nplt.hist(data, bins=3, color="lightgreen", edgecolor="black")'
    },
    {
        'name': 'pie',
        'prefix': 'plt.',
        'sig': '(x, labels=None, autopct=None, **kwargs)',
        'desc': 'Creates a pie chart representing data `x` on the *current* Axes. `labels` provides text labels for slices. `autopct` formats the numerical value displayed on slices (e.g., "%1.1f%%").',
        'example': 'plt.pie([15, 30, 45, 10], labels=["Frogs", "Hogs", "Dogs", "Logs"], autopct="%1.1f%%")'
    },
    {
        'name': 'xlabel',
        'prefix': 'plt.',
        'sig': '(xlabel, **kwargs)',
        'desc': 'Sets the label for the x-axis of the *current* Axes.',
        'example': 'plt.xlabel("Time (seconds)")'
    },
    {
        'name': 'ylabel',
        'prefix': 'plt.',
        'sig': '(ylabel, **kwargs)',
        'desc': 'Sets the label for the y-axis of the *current* Axes.',
        'example': 'plt.ylabel("Temperature (°C)")'
    },
    {
        'name': 'title',
        'prefix': 'plt.',
        'sig': '(label, **kwargs)',
        'desc': 'Sets the title for the *current* Axes.',
        'example': 'plt.title("Experiment Results")'
    },
    {
        'name': 'legend',
        'prefix': 'plt.',
        'sig': '(**kwargs)',
        'desc': 'Places a legend on the *current* Axes. Uses labels provided in plotting commands (e.g., `label="data1"` in `plt.plot`).',
        'example': 'plt.plot([1], [1], label="Line A")\nplt.legend()'
    },
    {
        'name': 'grid',
        'prefix': 'plt.',
        'sig': '(visible=None, which="major", axis="both", **kwargs)',
        'desc': 'Turns the plot grid lines on or off for the *current* Axes.',
        'example': 'plt.grid(True, linestyle=":", color="gray") # Turn on dotted gray grid'
    },
    {
        'name': 'show',
        'prefix': 'plt.',
        'sig': '()',
        'desc': 'Displays all open figure windows and blocks until they are closed. Usually called once at the end of a script when using `pyplot` directly.',
        'example': 'plt.plot([1,2],[3,4])\nplt.show() # Shows the plot'
    },
    {
        'name': 'savefig',
        'prefix': 'plt.',
        'sig': '(fname, **kwargs)',
        'desc': 'Saves the *current* figure to a file (e.g., PNG, JPG, PDF). `fname` is the filename/path.',
        'example': 'plt.savefig("my_plot.png", dpi=300) # Saves as PNG with 300 DPI'
    },
    # Add more pyplot functions here if needed...
    {
        'name': 'xlim',
        'prefix': 'plt.',
        'sig': '(left=None, right=None)',
        'desc': 'Gets or sets the x-axis limits of the *current* Axes.',
        'example': 'plt.xlim(0, 10) # Set x-axis from 0 to 10'
    },
    {
        'name': 'ylim',
        'prefix': 'plt.',
        'sig': '(bottom=None, top=None)',
        'desc': 'Gets or sets the y-axis limits of the *current* Axes.',
        'example': 'plt.ylim(-1, 1)'
    },
        {
        'name': 'xticks',
        'prefix': 'plt.',
        'sig': '(ticks=None, labels=None, **kwargs)',
        'desc': 'Gets or sets the x-axis tick locations and labels of the *current* Axes.',
        'example': 'plt.xticks([0, 5, 10], ["Start", "Middle", "End"])'
    },
    {
        'name': 'yticks',
        'prefix': 'plt.',
        'sig': '(ticks=None, labels=None, **kwargs)',
        'desc': 'Gets or sets the y-axis tick locations and labels of the *current* Axes.',
        'example': 'plt.yticks([0, 0.5, 1.0])'
    },
    {
        'name': 'text',
        'prefix': 'plt.',
        'sig': '(x, y, s, **kwargs)',
        'desc': 'Adds text `s` at location `(x, y)` in data coordinates on the *current* Axes.',
        'example': 'plt.text(2, 5, "Important Point", fontsize=12)'
    },
    {
        'name': 'annotate',
        'prefix': 'plt.',
        'sig': '(text, xy, xytext=None, arrowprops=None, **kwargs)',
        'desc': 'Adds an annotation (text + optional arrow) to the *current* Axes. `text` is the annotation text. `xy` is the point to annotate. `xytext` is the position for the text. `arrowprops` styles the arrow.',
        'example': 'plt.annotate("Peak", xy=(3, 5), xytext=(4, 6), arrowprops=dict(facecolor=\'black\', shrink=0.05))'
    },
    {
        'name': 'axhline',
        'prefix': 'plt.',
        'sig': '(y=0, xmin=0, xmax=1, **kwargs)',
        'desc': 'Adds a horizontal line across the *current* Axes at y-coordinate `y`.',
        'example': 'plt.axhline(0, color=\'grey\', lw=0.5)'
    },
    {
        'name': 'axvline',
        'prefix': 'plt.',
        'sig': '(x=0, ymin=0, ymax=1, **kwargs)',
        'desc': 'Adds a vertical line across the *current* Axes at x-coordinate `x`.',
        'example': 'plt.axvline(5, color=\'red\', linestyle=\'--\')'
    },
    {
        'name': 'fill_between',
        'prefix': 'plt.',
        'sig': '(x, y1, y2=0, where=None, **kwargs)',
        'desc': 'Fills the area between two horizontal curves `y1` and `y2` (defaults to 0) defined by `x` coordinates on the *current* Axes.',
        'example': 'plt.fill_between(x_values, y_lower, y_upper, color=\'lightblue\', alpha=0.5)'
    },
    {
        'name': 'style.use',
        'prefix': 'plt.',
        'sig': '(style)',
        'desc': 'Applies a pre-defined Matplotlib style sheet (e.g., "ggplot", "seaborn-v0_8-darkgrid"). Affects subsequent plots.',
        'example': 'plt.style.use("ggplot")'
    },
    {
        'name': 'cla',
        'prefix': 'plt.',
        'sig': '()',
        'desc': 'Clears the *current* Axes.',
        'example': 'plt.cla() # Clears the current plot axes'
    },
    {
        'name': 'clf',
        'prefix': 'plt.',
        'sig': '()',
        'desc': 'Clears the *current* Figure.',
        'example': 'plt.clf() # Clears the entire current figure'
    },
    {
        'name': 'close',
        'prefix': 'plt.',
        'sig': '(fig=None)',
        'desc': 'Closes a figure window. If `fig` is None, closes the *current* figure. `plt.close("all")` closes all figures.',
        'example': 'plt.close() # Closes the current figure\nplt.close(fig_object) # Closes a specific figure'
    },

]

# --- Matplotlib: Axes Object Methods ---
# Note: Many of these overlap with pyplot, but are called on an `ax` object.
# We only list the most common object-oriented equivalents/additions here.
MPL_AXES_DOCS = [
     {
        'name': 'plot',
        'prefix': 'ax.',
        'sig': '(x, y, format_string="...", **kwargs)',
        'desc': 'Plots y versus x as lines/markers on *this specific Axes* (`ax`). Use instead of `plt.plot` when you have an Axes object (e.g., from `plt.subplots`). Options are the same as `plt.plot`.',
        'example': 'fig, ax = plt.subplots()\nax.plot([0, 1], [1, 0], "r--") # Plot on the specific Axes `ax`'
    },
     {
        'name': 'scatter',
        'prefix': 'ax.',
        'sig': '(x, y, s=None, c=None, marker="o", **kwargs)',
        'desc': 'Creates a scatter plot on *this specific Axes*. Options are the same as `plt.scatter`.',
        'example': 'fig, ax = plt.subplots()\nax.scatter([1, 2, 3], [4, 1, 5], c="blue")'
    },
     {
        'name': 'bar',
        'prefix': 'ax.',
        'sig': '(x, height, width=0.8, bottom=None, **kwargs)',
        'desc': 'Creates a bar chart on *this specific Axes*. Options are the same as `plt.bar`.',
        'example': 'fig, ax = plt.subplots()\nax.bar(["X", "Y"], [5, 8])'
    },
     {
        'name': 'hist',
        'prefix': 'ax.',
        'sig': '(x, bins=None, range=None, density=False, **kwargs)',
        'desc': 'Computes and draws a histogram on *this specific Axes*. Options are the same as `plt.hist`.',
        'example': 'fig, ax = plt.subplots()\ndata = [1, 1, 2, 3, 3, 3]\nax.hist(data, bins=3)'
    },
     {
        'name': 'pie',
        'prefix': 'ax.',
        'sig': '(x, labels=None, autopct=None, **kwargs)',
        'desc': 'Creates a pie chart on *this specific Axes*. Options are the same as `plt.pie`.',
        'example': 'fig, ax = plt.subplots()\nax.pie([10, 20], labels=["A", "B"])'
    },
     {
        'name': 'set_xlabel',
        'prefix': 'ax.',
        'sig': '(xlabel, **kwargs)',
        'desc': 'Sets the label for the x-axis of *this specific Axes*. Preferred over `plt.xlabel` when using the object-oriented approach.',
        'example': 'fig, ax = plt.subplots()\nax.set_xlabel("X Value")'
    },
     {
        'name': 'set_ylabel',
        'prefix': 'ax.',
        'sig': '(ylabel, **kwargs)',
        'desc': 'Sets the label for the y-axis of *this specific Axes*. Preferred over `plt.ylabel`.',
        'example': 'fig, ax = plt.subplots()\nax.set_ylabel("Y Value")'
    },
     {
        'name': 'set_title',
        'prefix': 'ax.',
        'sig': '(label, **kwargs)',
        'desc': 'Sets the title for *this specific Axes*. Preferred over `plt.title`.',
        'example': 'fig, ax = plt.subplots()\nax.set_title("Plot Title")'
    },
     {
        'name': 'legend',
        'prefix': 'ax.',
        'sig': '(**kwargs)',
        'desc': 'Places a legend on *this specific Axes*. Preferred over `plt.legend`.',
        'example': 'fig, ax = plt.subplots()\nax.plot([1], [1], label="Data")\nax.legend()'
    },
     {
        'name': 'grid',
        'prefix': 'ax.',
        'sig': '(visible=None, which="major", axis="both", **kwargs)',
        'desc': 'Turns the grid lines on or off for *this specific Axes*. Preferred over `plt.grid`.',
        'example': 'fig, ax = plt.subplots()\nax.grid(True)'
    },
     {
        'name': 'set_xlim',
        'prefix': 'ax.',
        'sig': '(left=None, right=None)',
        'desc': 'Sets the x-axis limits for *this specific Axes*. Preferred over `plt.xlim`.',
        'example': 'ax.set_xlim(0, 50)'
    },
    {
        'name': 'set_ylim',
        'prefix': 'ax.',
        'sig': '(bottom=None, top=None)',
        'desc': 'Sets the y-axis limits for *this specific Axes*. Preferred over `plt.ylim`.',
        'example': 'ax.set_ylim(10, 20)'
    },
    {
        'name': 'set_xticks',
        'prefix': 'ax.',
        'sig': '(ticks, labels=None, **kwargs)',
        'desc': 'Sets the x-axis tick locations and optionally labels for *this specific Axes*. Preferred over `plt.xticks`.',
        'example': 'ax.set_xticks([0, 1, 2], labels=["Low", "Med", "High"])'
    },
    {
        'name': 'set_yticks',
        'prefix': 'ax.',
        'sig': '(ticks, labels=None, **kwargs)',
        'desc': 'Sets the y-axis tick locations and optionally labels for *this specific Axes*. Preferred over `plt.yticks`.',
        'example': 'ax.set_yticks([100, 200, 300])'
    },
    {
        'name': 'text',
        'prefix': 'ax.',
        'sig': '(x, y, s, **kwargs)',
        'desc': 'Adds text `s` at location `(x, y)` in data coordinates on *this specific Axes*. Preferred over `plt.text`.',
        'example': 'ax.text(0.5, 0.5, "Center Text")'
    },
    {
        'name': 'annotate',
        'prefix': 'ax.',
        'sig': '(text, xy, xytext=None, arrowprops=None, **kwargs)',
        'desc': 'Adds an annotation to *this specific Axes*. Preferred over `plt.annotate`.',
        'example': 'ax.annotate("Note", xy=(1, 1), xytext=(1.5, 1.5), arrowprops=dict(arrowstyle="->"))'
    },
    {
        'name': 'axhline',
        'prefix': 'ax.',
        'sig': '(y=0, xmin=0, xmax=1, **kwargs)',
        'desc': 'Adds a horizontal line across *this specific Axes*. Preferred over `plt.axhline`.',
        'example': 'ax.axhline(10, color=\'k\', linestyle=\':\')'
    },
    {
        'name': 'axvline',
        'prefix': 'ax.',
        'sig': '(x=0, ymin=0, ymax=1, **kwargs)',
        'desc': 'Adds a vertical line across *this specific Axes*. Preferred over `plt.axvline`.',
        'example': 'ax.axvline(0.5, color=\'g\')'
    },
     {
        'name': 'fill_between',
        'prefix': 'ax.',
        'sig': '(x, y1, y2=0, where=None, **kwargs)',
        'desc': 'Fills the area between two horizontal curves on *this specific Axes*. Preferred over `plt.fill_between`.',
        'example': 'ax.fill_between(x_vals, y1_vals, y2_vals, alpha=0.3)'
    },
    {
        'name': 'clear',
        'prefix': 'ax.',
        'sig': '()',
        'desc': 'Clears *this specific Axes* (removes plotted elements, resets limits, etc.). Preferred over `plt.cla`.',
        'example': 'ax.clear()'
    },
] 