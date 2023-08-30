import pandas as pd
import re

def split_coords(x: str) -> list:
    return re.findall(r"(\d+)", x)

def convert_dms_to_dd(row: list[int]) -> float:
    return row[0] + row[1]/60 + row[2]/3600

def transform_coord(df: pd.DataFrame, 
                    col: str,
                    ):
    df[[f"d_{col}", f"m_{col}", f"s_{col}"]] = df[col].apply(split_coords).to_list()
    df[[f"d_{col}", f"m_{col}", f"s_{col}"]] = df[[f"d_{col}", f"m_{col}", f"s_{col}"]].astype(int)
    df[f"dd_{col}"] = df[[f"d_{col}", f"m_{col}", f"s_{col}"]].apply(convert_dms_to_dd, axis=1)
    df.drop(columns=[f"d_{col}", f"m_{col}", f"s_{col}"], inplace=True)

def calc_coordinates(df: pd.DataFrame):
    df[["lat", "lon"]] = df["geo_coords"].str.split(' ', expand=True)

    transform_coord(df, "lat")
    transform_coord(df, "lon")

    df.drop(columns=["lat", "lon", "geo_coords"], inplace=True)

if __name__ == "__main__":
    df = pd.read_excel("data\\PRNG_MIEJSCOWOSCI_XLSX.xlsx",
                       usecols=["identyfikator PRNG", 
                                "nazwa główna", 
                                "status nazwy", 
                                "nazwa miejscowości nadrzędnej", 
                                "współrzędne geograficzne", 
                                "województwo", 
                                "powiat", 
                                "gmina"]
    )

    # Rename columns
    df.rename(columns = {'identyfikator PRNG':'id',
                     'nazwa główna': 'name',
                     'status nazwy': 'status',
                     "nazwa miejscowości nadrzędnej": "higher_rank_object_name",
                     "współrzędne geograficzne": "geo_coords",
                     "województwo": "voivodeship",
                     "powiat": "district",
                     "gmina": "commune"
                     }, 
                inplace = True)
    
    df["name"] = df["name"].str.lower()
    
    calc_coordinates(df)
    df.to_csv("data\\prepared_data.csv", index=False)
