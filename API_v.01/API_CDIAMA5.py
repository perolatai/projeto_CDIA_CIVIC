from flask import Flask, make_response, jsonify, request
import psycopg2

# Credenciais da base de dados
conn = psycopg2.connect(
    database=database,
    host=host,
    user=user,
    password=password,
    port=port)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Cursor
cursor = conn.cursor()

# GET para a tabela GENES inteira;


@app.route('/genes', methods=['GET'])
def get_genes():
    cursor.execute('SELECT * FROM genes')
    lista_genes = cursor.fetchall()

    # Adicionando os rótulos das colunas;
    genes = list()
    for gene in lista_genes:
        genes.append(
            {
                'id': gene[0],
                'gene': gene[1],
                'descrição': gene[2]
            }
        )

    return make_response(
        jsonify(
            message='Genes:',
            data=genes
        )
    )

# GET para a tabela EVIDENCIAS inteira;


@app.route('/evidencias', methods=['GET'])
def get_evidencias():
    cursor.execute('SELECT * FROM evidencias')
    lista_evidencias = cursor.fetchall()

    # Adicionando os rótulos das colunas;
    evidencias = list()
    for evidencia in lista_evidencias:
        evidencias.append(
            {
                'evidence_id': evidencia[0],
                'entrez_id': evidencia[1],
                'disease': evidencia[2],
                'doid': evidencia[3],
                'phenotypes': evidencia[4],
                'drugs': evidencia[5],
                'drug_interaction_type': evidencia[6],
                'evidence_type': evidencia[7],
                'evidence_direction': evidencia[8],
                'evidence_level': evidencia[9],
                'clinical_significance': evidencia[10],
                'evidence_statement': evidencia[11],
                'citation_id': evidencia[12],
                'source_type': evidencia[13],
                'citation': evidencia[14],
                'rating': evidencia[15],
                'evidence_status': evidencia[16],
                'variant_id': evidencia[17],
                'chromosome': evidencia[18],
                'variant_origin': evidencia[19],
                'is_flagged': evidencia[20]
            }
        )

    return make_response(
        jsonify(
            message='Evidencias',
            data=evidencias
        )
    )

# GET para a tabela VARIANTES inteira;


@app.route('/variantes', methods=['GET'])
def get_variantes():
    cursor.execute('SELECT * FROM variantes')
    lista_variantes = cursor.fetchall()

    # Adicionando os rótulos das colunas;
    variantes = list()
    for variante in lista_variantes:
        variantes.append(
            {
                'variant_id': variante[0],
                'variant': variante[1],
                'summary': variante[2],
                'start': variante[3],
                'stop': variante[4],
                'reference_bases': variante[5],
                'variant_bases': variante[6],
                'representative_transcript': variante[7],
                'ensembl_version': variante[8],
                'reference_build': variante[9],
                'variant_types': variante[10],
                'hgvs_expressions': variante[11],
                'civic_variant_evidence_score': variante[12],
                'allele_registry_id': variante[13],
                'clinvar_ids': variante[14],
                'variant_aliases': variante[15]
            }
        )

    return make_response(
        jsonify(
            message='Variantes:',
            data=variantes
        )
    )


if __name__ == "__main__":
    app.run()
