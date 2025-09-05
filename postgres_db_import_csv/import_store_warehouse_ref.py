import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# --- CONFIGURATION ---
CSV_PATH = r'C:\Users\raghavan.mohan\Downloads\store_warehouse_ref-npe0409.csv'  # <-- Update path as needed
DB_PARAMS = {
    'host': 'your_host',
    'port': 5432,
    'dbname': 'your_db',
    'user': 'your_user',
    'password': 'your_password'
}
TABLE_NAME = 'store_warehouse_ref'
UNIQUE_COL = 'store_internal_id'
COLUMNS = [
    'store_internal_id', 'warehouse_ship_no',
    'warehouse_franchise', 'warehouse_account_no'
]

# --- 1. READ CSV ---
df = pd.read_csv(CSV_PATH)

# --- 2. VALIDATE COLUMNS ---
missing = set(COLUMNS) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns in CSV: {missing}")

# --- 3. DROP ROWS WITH NULL PRIMARY KEY ---
df = df.dropna(subset=[UNIQUE_COL])

# --- 4. CONNECT TO DATABASE ---
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# --- 5. FETCH EXISTING PRIMARY KEYS ---
cur.execute(f"SELECT {UNIQUE_COL} FROM {TABLE_NAME};")
existing_keys = set(str(row[0]) for row in cur.fetchall())  # ensure string type

# --- 6. FILTER STRICTLY NEW ROWS ---
df[UNIQUE_COL] = df[UNIQUE_COL].astype(str)  # ensure all keys are string
new_rows_df = df[~df[UNIQUE_COL].isin(existing_keys)].copy()

# --- 7. INSERT & PRINT ONLY TRULY INSERTED ROWS ---
if not new_rows_df.empty:
    records = new_rows_df[COLUMNS].values.tolist()
    insert_sql = f'''
        INSERT INTO {TABLE_NAME} (
            store_internal_id, warehouse_ship_no,
            warehouse_franchise, warehouse_account_no
        ) VALUES %s
        ON CONFLICT ({UNIQUE_COL}) DO NOTHING;
    '''
    execute_values(cur, insert_sql, records)
    conn.commit()
    print(f"Inserted {len(records)} new rows:")
    for idx, row in new_rows_df.iterrows():
        print(dict(row[COLUMNS]))
else:
    print("No new rows were inserted.")

cur.close()
conn.close()