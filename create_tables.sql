CREATE TABLE patients (
    PID TEXT PRIMARY KEY NOT NULL,
    cancerStatus TEXT NOT NULL
    );

CREATE TABLE genes (
    geneName TEXT PRIMARY KEY NOT NULL,
    chromosome TEXT NOT NULL
    );

CREATE TABLE mutations (
    MID INTEGER PRIMARY KEY,
    geneName TEXT NOT NULL,
    startCoord INT, 
    endCoord INT,
    effect TEXT,
    type TEXT,
    FOREIGN KEY (geneName) REFERENCES genes(geneName)
    );

CREATE TABLE codons (
    MID INT NOT NULL,
    codon TEXT NOT NULL,
    PRIMARY KEY (MID, codon),
    FOREIGN KEY (MID) REFERENCES mutations(MID)
    );

CREATE TABLE patient_mutations (
    PID TEXT NOT NULL,
    MID INT NOT NULL,
    PRIMARY KEY (PID, MID),
    FOREIGN KEY (PID) REFERENCES patients(PID),
    FOREIGN KEY (MID) REFERENCES mutations(MID)
    );
