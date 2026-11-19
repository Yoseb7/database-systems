import sqlite3
import pandas as pd

df = pd.read_csv("mutationu.csv")

connection = sqlite3.connect("database.db")
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()


try:
    mutation_ids = {}

    for mutation_name in df.columns[1:]:
        parts = mutation_name.split("_")

        gene_name = parts[0]
        location = parts[2]
        effect = parts[3]
        mut_type = parts[4]
        codons = parts[5:]

        chromosome, coordinates = location.split(":")
        start_coord, end_coord = coordinates.split("-")

        start_coord = int(start_coord)
        end_coord = int(end_coord)

        cursor.execute("""INSERT OR IGNORE INTO genes (geneName, chromosome) VALUES (?, ?)""", (gene_name, chromosome))

        cursor.execute("""INSERT INTO mutations (geneName, startCoord, endCoord, effect, type) VALUES (?, ?, ?, ?, ?)""", (gene_name, start_coord, end_coord, effect, mut_type))

        mid = cursor.lastrowid
        mutation_ids[mutation_name] = mid

        for codon in codons:
            cursor.execute("""INSERT OR IGNORE INTO codons (MID, codon) VALUES (?, ?)""", (mid, codon))

    for _, row in df.iterrows():
        patient_id = str(row.iloc[0]).strip()

        if patient_id.startswith("NC"):
            cancer_status = "NC"
        else:
            cancer_status = "C"
        
        cursor.execute("""INSERT OR IGNORE INTO patients (PID, cancerStatus) VALUES (?, ?)""", (patient_id, cancer_status)) 

        for mutation_name in df.columns[1:]:
            if row[mutation_name] == 1:
                mid = mutation_ids[mutation_name]
                cursor.execute("""INSERT OR IGNORE INTO patient_mutations (PID, MID) VALUES (?, ?)""", (patient_id, mid))

    connection.commit()
    print("Data loaded successfully.")

finally:
    connection.close()
