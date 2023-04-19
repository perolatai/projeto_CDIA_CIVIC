import pandas as pd
import psycopg2

df_Evidences = pd.read_csv(
    'projeto_CIVIC/01-Apr-2022-ClinicalEvidenceSummaries.csv')
df_Evidences = df_Evidences.drop(['gene_civic_url', 'evidence_civic_url', 'asco_abstract_id', 'nct_ids',
                                  'variant_summary', 'variant', 'start', 'stop', 'representative_transcript',
                                  'reference_bases', 'reference_build', 'ensembl_version', 'variant_bases', 'gene',
                                  'last_review_date', 'variant_civic_url', 'gene_id',
                                  'chromosome2', 'start2', 'stop2', 'representative_transcript2'], axis=1)
col = df_Evidences.pop('evidence_id')
df_Evidences.insert(0, 'evidence_id', col)

df_Variant = pd.read_csv('projeto_CIVIC/01-Apr-2022-VariantSummaries.csv')
df_Variant = df_Variant.drop(['Unnamed: 32', 'Unnamed: 31', 'Unnamed: 29',
                              'Unnamed: 30', 'assertion_civic_urls', 'variant_civic_url',
                              'last_review_date', 'chromosome2', 'start2', 'stop2', 'representative_transcript2',
                              'variant_groups', 'gene', 'entrez_id', 'assertion_ids', 'is_flagged', 'chromosome'], axis=1)
col = df_Variant.pop('variant_id')
df_Variant.insert(0, 'variant_id', col)

df_Gene = pd.read_csv('projeto_CIVIC/01-Apr-2022-GeneSummaries.csv')
df_Gene = df_Gene.drop(
    ['gene_civic_url', 'gene_id', 'last_review_date', 'is_flagged'], axis=1)
df_Gene.rename(columns={'name': 'gene'}, inplace=True)
col = df_Gene.pop('entrez_id')
df_Gene.insert(0, 'entrez_id', col)


conn = psycopg2.connect(
    database=database,
    host=host,
    user=user,
    password=password,
    port=port)

mycursor = conn.cursor()


def insert_dataframe_into_mysql(df, table_name, connection):
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(df.columns))
    columns = ', '.join(df.columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    for _, row in df.iterrows():
        row = pd.concat([pd.Series([0]), row])
        row = row.iloc[1:]
        values = tuple(row.fillna('None'))
        cursor.execute(sql, values)
    connection.commit()


insert_dataframe_into_mysql(df_Gene, 'genes', conn)
insert_dataframe_into_mysql(df_Variant, 'variantes', conn)
insert_dataframe_into_mysql(df_Evidences, 'evidencias', conn)
