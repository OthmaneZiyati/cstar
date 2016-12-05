import pandas as pd
fileUser = '/home/antony/git/cstar/data/2015-12-02_userbase.csv'
df = pd.read_csv(fileUser)
df.columns = [c.lower() for c in df.columns] #postgres doesn't like capitals or spaces

from sqlalchemy import create_engine
engine = create_engine('postgresql://username:password@localhost:5432/dbname')

df.to_sql("my_table_name", engine)
