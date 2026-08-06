"""
Run all queries in sql/analysis_queries.sql against data/churn.db
and print the results for each one.
"""

import sqlite3

conn = sqlite3.connect("../data/churn.db")
cur = conn.cursor()

with open("../sql/analysis_queries.sql", encoding="utf-8") as f:
    content = f.read()

# Split the file into blocks separated by blank lines -- each block is
# one comment line (the query's title) followed by its SQL.
blocks = [b.strip() for b in content.split("\n\n") if b.strip()]

for block in blocks:
    lines = block.split("\n")
    title = lines[0].replace("-- ", "").strip()
    query = "\n".join(l for l in lines if not l.strip().startswith("--")).strip()

    if not query:
        continue

    print(f"--- {title} ---")
    cur.execute(query)
    col_names = [d[0] for d in cur.description]
    print(" | ".join(col_names))
    for row in cur.fetchall():
        print(" | ".join(str(v) for v in row))
    print()

conn.close()