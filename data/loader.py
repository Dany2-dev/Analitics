import pandas as pd

def load_data(file):
    sheets = pd.read_excel(file, sheet_name=None)
    dfs = []

    for sheet_name, df in sheets.items():
        df = df.copy()
        df.columns = df.columns.str.lower().str.strip()

        name = sheet_name.lower()
        if "1" in name:
            periodo = "1T"
        elif "2" in name:
            periodo = "2T"
        elif "extra" in name or "et" in name:
            periodo = "ET"
        else:
            periodo = sheet_name

        df["periodo"] = periodo
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
