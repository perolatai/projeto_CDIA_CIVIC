CREATE TABLE genes
(
    entrez_id INTEGER PRIMARY KEY,
    gene VARCHAR(255),
    description TEXT
);

CREATE TABLE variantes
(
    variant_id INTEGER PRIMARY KEY,
    variant VARCHAR(255),
    summary TEXT,
    start VARCHAR(255),
    stop VARCHAR(255),
    reference_bases VARCHAR(255),
    variant_bases VARCHAR(255),
    representative_transcript VARCHAR(255),
    ensembl_version VARCHAR(255),
    reference_build VARCHAR(255),
    variant_types VARCHAR(255),
    hgvs_expressions VARCHAR(255),
    civic_variant_evidence_score FLOAT,
    allele_registry_id VARCHAR(255),
    clinvar_ids VARCHAR(255),
    variant_aliases VARCHAR(255)
);

CREATE TABLE evidencias
(
    evidence_id INTEGER PRIMARY KEY,
    entrez_id INTEGER,
    disease VARCHAR(255),
    doid VARCHAR(255),
    phenotypes VARCHAR(255),
    drugs VARCHAR(255),
    drug_interaction_type VARCHAR(255),
    evidence_type VARCHAR(255),
    evidence_direction VARCHAR(255),
    evidence_level VARCHAR(255),
    clinical_significance VARCHAR(255),
    evidence_statement TEXT,
    citation_id VARCHAR(255),
    source_type VARCHAR(255),
    citation VARCHAR(255),
    rating VARCHAR(255),
    evidence_status VARCHAR(255),
    variant_id INTEGER,
    chromosome VARCHAR(255),
    variant_origin VARCHAR(255),
    is_flagged BOOLEAN,
    FOREIGN KEY (entrez_id) REFERENCES genes(entrez_id),
    FOREIGN KEY (variant_id) REFERENCES variantes(variant_id)
);
