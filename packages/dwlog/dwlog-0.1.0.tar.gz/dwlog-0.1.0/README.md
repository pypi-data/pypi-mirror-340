# dslogger
Logging functionalities for data wrangling in Python.

Similar to [tidylog](https://github.com/elbersb/tidylog) but for Python.

Currently it supports pandas only, but PRs for Modin/polars/whatever are welcome!

PRs to add pandas functions are also welcome!

Remember to:

1. `import dslogger.pandas` _after_ `import pandas as pd`
2. Initialize the logger `logging.basicConfig(level=logging.INFO)` 

## Example

```
>python
Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
>>> import numpy as np
>>> import logging
>>> import dslogger.pandas
>>> logging.basicConfig(level=logging.INFO)
>>> df = pd.DataFrame({"a":[1,1,2,np.nan,3,np.nan],"b":[5,5,6,7,np.nan,np.nan]})
>>> df
     a    b
0  1.0  5.0
1  1.0  5.0
2  2.0  6.0
3  NaN  7.0
4  3.0  NaN
5  NaN  NaN
>>> df.drop_duplicates()
INFO:dslogger:Dropped 1/6 (16.67%) duplicated rows, remains 5/6 (83.33%) rows
     a    b
0  1.0  5.0
2  2.0  6.0
3  NaN  7.0
4  3.0  NaN
5  NaN  NaN
>>> df.dropna()
INFO:dslogger:Dropped 3/6 (50.0%) rows
     a    b
0  1.0  5.0
1  1.0  5.0
2  2.0  6.0
>>> df.dropna(subset=['a'])
INFO:dslogger:Dropped 2/6 (33.33%) rows
     a    b
0  1.0  5.0
1  1.0  5.0
2  2.0  6.0
4  3.0  NaN
>>> df.to_excel("test.xlsx", index=False, sheet_name="Sheet1")
>>> df2 = pd.read_excel("test.xlsx", sheet_name="Sheet1")
INFO:dslogger:Read Excel file 'test.xlsx' with shape (5 x 2)
>>> from pathlib import Path
>>> Path("test.xlsx").unlink(missing_ok=True)
```


