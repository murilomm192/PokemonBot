import pandas as pd
import sqlite3

con = sqlite3.connect("pokemon_cache.sqlite")

cur = con.cursor()

print(cur)

df = pd.read_sql_query("SELECT * FROM sqlite_master WHERE type='table';", con)
