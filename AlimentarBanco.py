# jdbc:postgresql://aws-0-sa-east-1.pooler.supabase.com:5432/postgres?user=postgres.bwvqneansuqchkccmhxq&password=Feisenha123##
from datetime import timedelta
from datetime import datetime, date
from math import floor
import random
import re
from sqlalchemy import create_engine, text, inspect as sql_inspect
import pandas as pd
from faker import Faker
import json
import time
import sys
import sqlalchemy
import inspect

config_dados = [
    {
        'function':'generate_data_Funcionario',
        'table':'funcionario',
        'n': 100,
    },
    {
        'function':'generate_data_Hospital',
        'table':'hospital',
        'n': 10,
    },
    {
        'function':'generate_data_Area_De_Atuacao',
        'table':'area_de_atuacao',
        'n': 100,
    },
    {
        'function':'generate_data_Area_Atuacao_Hospital',
        'table':'area_atuacao_hospital',
        'n': 150,
    },
    {
        'function':'generate_data_Hospital_Funcionario',
        'table':'hospital_funcionario',
        'n': 100,
    },
    {
        'function':'generate_data_Paciente',
        'table':'paciente',
        'n': 100,
    },
    
    {
        'function':'generate_data_Especializacao',
        'table':'especializacao',
        'n': 50,
    },

    {
        'function':'generate_data_Area_Atuacao_Especializacao',
        'table':'area_atuacao_especializacao',
        'n': 150,
    },
    {
        'function':'generate_data_Especializacao_Funcionario',
        'table':'especializacao_funcionario',
        'n': 5,
    },
    {
        'function':'generate_data_Agendamento',
        'table':'agendamento',
        'n': 100,
    },
]

fake = Faker('pt_BR')
def generate_data_Funcionario(n:int):
    """
    📄 Tabela: funcionario
    🧱 Coluna: id - Tipo: INTEGER
    🧱 Coluna: nome - Tipo: VARCHAR(100)
    🧱 Coluna: idade - Tipo: INTEGER
    🧱 Coluna: salario - Tipo: DOUBLE PRECISION
    🧱 Coluna: data_nascimento - Tipo: DATE
    🔑 Chave Primária: ['id']
"""
    data = []
    for _ in range(n):
        data.append({
            'nome': fake.name(),
            'idade': fake.random_int(min=18, max=80),
            'salario': fake.random_number(digits=5),
            'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=80),
        })
    return data

def generate_data_Hospital(n:int, engine: sqlalchemy.engine.Engine):
    """
    📄 Tabela: hospital
    🧱 Coluna: id - Tipo: INTEGER
    🧱 Coluna: nome - Tipo: VARCHAR(100)
    🧱 Coluna: endereco - Tipo: VARCHAR(100)
    🧱 Coluna: quantidade_quartos - Tipo: INTEGER
    🧱 Coluna: leitos - Tipo: INTEGER
    🧱 Coluna: avaliacao - Tipo: INTEGER
    🧱 Coluna: cnpj - Tipo: VARCHAR(20)
    🧱 Coluna: id_responsavel - Tipo: INTEGER
    🔑 Chave Primária: ['id']
    🔗 FK: ['id_responsavel'] → funcionario.['id']
    """
    data = []
    try:
        # Passar engine diretamente para pandas
        ids_responsaveis_df = pd.read_sql_query("SELECT id FROM funcionario", engine)
        if ids_responsaveis_df.empty:
            print("AVISO: Tabela 'funcionario' está vazia. Não é possível gerar dados para 'hospital'.")
            return []
        ids_responsaveis = ids_responsaveis_df['id'].tolist()
    except Exception as e:
        print(f"Erro ao buscar IDs de funcionario para hospital: {e}")
        return []

    for _ in range(n):
        data.append({
            'nome': fake.company(),
            'endereco': fake.address(),
            'quantidade_quartos': fake.random_int(min=10, max=100),
            'leitos': fake.random_int(min=10, max=100),
            'avaliacao': fake.random_int(min=1, max=5),
            'cnpj': fake.cnpj(), # Usar fake.cnpj() para formato correto
            'id_responsavel': random.choice(ids_responsaveis),
        })
    return data

def generate_data_Area_De_Atuacao(n:int):
    """
    📄 Tabela: area_de_atuacao
    🧱 Coluna: id - Tipo: INTEGER
    🧱 Coluna: nome - Tipo: VARCHAR(100)
    🧱 Coluna: codigo_area - Tipo: VARCHAR(20)
    🔑 Chave Primária: ['id']
    """
    data = []
    nomes_areas = [
        "Cardiologia",
        "Pediatria", 
        "Ortopedia",
        "Ginecologia e Obstetrícia",
        "Psiquiatria",
        "Dermatologia",
        "Endocrinologia",
        "Neurologia",
        "Urologia",
        "Hematologia",
        "Imunologia",
        "Gastroenterologia",
        "Oftalmologia",
        "Otorrinolaringologia",
        "Pneumologia",
        "Reumatologia",
        "Oncologia",
        "Nefrologia",
        "Geriatria",
        "Infectologia",
        "Anestesiologia",
        "Cirurgia Geral",
        "Cirurgia Plástica",
        "Cirurgia Cardíaca",
        "Cirurgia Vascular",
        "Medicina Nuclear",
        "Radiologia",
        "Patologia",
        "Medicina do Trabalho",
        "Medicina Intensiva",
        "Medicina de Família",
        "Medicina Esportiva",
        "Nutrologia",
        "Homeopatia",
        "Acupuntura",
        "Fisiatria",
        "Genética Médica",
        "Mastologia",
        "Proctologia",
        "Medicina Legal"
    ]
    for nome in nomes_areas:
        data.append({
            'nome': nome,
            'codigo_area': fake.random_number(digits=2),
        })
    return data

def generate_data_Area_Atuacao_Hospital(n:int, engine: sqlalchemy.engine.Engine):
    """
    📄 Tabela: area_atuacao_hospital
    🧱 Coluna: id_hospital - Tipo: INTEGER
    🧱 Coluna: id_area_atuacao - Tipo: INTEGER
    🔑 Chave Primária: ['id_hospital', 'id_area_atuacao']
    🔗 FK: ['id_area_atuacao'] → area_de_atuacao.['id']
    🔗 FK: ['id_hospital'] → hospital.['id']
    Garante participação mínima de hospital e area_de_atuacao.
    """
    data = []
    combinacoes_geradas = set()
    try:
        # Passar engine diretamente para pandas
        ids_hospitais_df = pd.read_sql_query("SELECT id FROM hospital", engine)
        ids_areas_df = pd.read_sql_query("SELECT id FROM area_de_atuacao", engine)

        if ids_hospitais_df.empty or ids_areas_df.empty:
            print("AVISO: Tabelas 'hospital' ou 'area_de_atuacao' estão vazias. Não é possível gerar dados para 'area_atuacao_hospital'.")
            return []
        ids_hospitais = ids_hospitais_df['id'].tolist()
        ids_areas = ids_areas_df['id'].tolist()
    except Exception as e:
        print(f"Erro ao buscar IDs para area_atuacao_hospital: {e}")
        return []

    # Garantir participação de cada hospital
    for h_id in ids_hospitais:
        if not ids_areas: continue # Segurança caso area esteja vazia
        a_id = random.choice(ids_areas)
        combinacoes_geradas.add((h_id, a_id))

    # Garantir participação de cada area de atuacao
    for a_id in ids_areas:
        if not ids_hospitais: continue # Segurança
        h_id = random.choice(ids_hospitais)
        combinacoes_geradas.add((h_id, a_id))

    # Adicionar mais combinações aleatórias até n (ou máximo possível)
    max_combinacoes = len(ids_hospitais) * len(ids_areas)
    target_count = min(n, max_combinacoes)

    while len(combinacoes_geradas) < target_count:
        h_id = random.choice(ids_hospitais)
        a_id = random.choice(ids_areas)
        combinacoes_geradas.add((h_id, a_id))

    # Converter set de tuplas para lista de dicionários
    data = [{'id_hospital': h, 'id_area_atuacao': a} for h, a in combinacoes_geradas]
    random.shuffle(data) # Embaralhar para não ter padrão óbvio

    return data

def generate_data_Hospital_Funcionario(n:int, engine: sqlalchemy.engine.Engine):
    """
    📄 Tabela: hospital_funcionario
    🧱 Coluna: id_hospital - Tipo: INTEGER
    🧱 Coluna: id_funcionario - Tipo: INTEGER
    🔑 Chave Primária: ['id_hospital', 'id_funcionario']
    🔗 FK: ['id_funcionario'] → funcionario.['id']
    🔗 FK: ['id_hospital'] → hospital.['id']
    Garante participação mínima de hospital e funcionario.
    """
    data = []

    try:
        # Passar engine diretamente para pandas
        ids_hospitais_df = pd.read_sql_query("SELECT id FROM hospital", engine)
        ids_funcionarios_df = pd.read_sql_query("SELECT id FROM funcionario", engine)

        if ids_hospitais_df.empty or ids_funcionarios_df.empty:
             print("AVISO: Tabelas 'hospital' ou 'funcionario' estão vazias. Não é possível gerar dados para 'hospital_funcionario'.")
             return []
        ids_hospitais = ids_hospitais_df['id'].tolist()
        ids_funcionarios = ids_funcionarios_df['id'].tolist()
    except Exception as e:
        print(f"Erro ao buscar IDs para hospital_funcionario: {e}")
        return []

    # Garantir participação de cada hospital
    for h_id in ids_hospitais:
        quantidade_funcionarios = random.randint(1, n)
        for _ in range(quantidade_funcionarios):
            f_id = random.choice(ids_funcionarios)
            data.append({'id_hospital': h_id, 'id_funcionario': f_id})


    return data

def generate_data_Especializacao(n:int):
    """
    📄 Tabela: especializacao
    🧱 Coluna: id - Tipo: INTEGER
    🧱 Coluna: nome - Tipo: VARCHAR(100)
    🧱 Coluna: descricao - Tipo: VARCHAR(100)
    🧱 Coluna: codigo_especializacao - Tipo: VARCHAR(100)
    🔑 Chave Primária: ['id']
"""
    data = []
    nomes_especializacoes = [
        "Cardiologia",
        "Pediatria", 
        "Ortopedia",
        "Ginecologia e Obstetrícia",
        "Psiquiatria",
        "Dermatologia",
        "Endocrinologia",
        "Neurologia",
        "Urologia",
        "Hematologia",
        "Imunologia",
        "Oftalmologia",
        "Otorrinolaringologia",
        "Pneumologia",
        "Reumatologia",
        "Nefrologia",
        "Gastroenterologia",
        "Oncologia",
        "Anestesiologia",
        "Cirurgia Geral",
        "Cirurgia Plástica",
        "Cirurgia Cardíaca",
        "Cirurgia Vascular",
        "Cirurgia Pediátrica",
        "Medicina Intensiva",
        "Medicina do Trabalho",
        "Medicina Nuclear",
        "Radiologia",
        "Patologia",
        "Geriatria",
        "Infectologia",
        "Medicina de Família",
        "Medicina Esportiva",
        "Nutrologia",
        "Homeopatia",
        "Acupuntura",
        "Alergologia",
        "Angiologia",
        "Coloproctologia",
        "Mastologia"
    ]
    for nome in nomes_especializacoes:
        data.append({
            'nome': nome,
            'descricao': fake.sentence(),
            'codigo_especializacao': fake.random_number(digits=3),
        })
    return data
def generate_data_Area_Atuacao_Especializacao(n:int, engine: sqlalchemy.engine.Engine):
    """
    📄 Tabela: area_atuacao_especializacao
    🧱 Coluna: id_area_atuacao - Tipo: INTEGER
    🧱 Coluna: id_especializacao - Tipo: INTEGER
    🔑 Chave Primária: ['id_area_atuacao', 'id_especializacao']
    🔗 FK: ['id_area_atuacao'] → area_de_atuacao.['id']
    🔗 FK: ['id_especializacao'] → especializacao.['id']
    Garante participação mínima de area_de_atuacao e especializacao.
    """
    data = []
    combinacoes_geradas = set()
    try:
        # Passar engine diretamente para pandas
        ids_areas_df = pd.read_sql_query("SELECT id FROM area_de_atuacao", engine)
        ids_especializacoes_df = pd.read_sql_query("SELECT id FROM especializacao", engine)

        if ids_areas_df.empty or ids_especializacoes_df.empty:
             print("AVISO: Tabelas 'area_de_atuacao' ou 'especializacao' estão vazias. Não é possível gerar dados para 'area_atuacao_especializacao'.")
             return []
        ids_areas = ids_areas_df['id'].tolist()
        ids_especializacoes = ids_especializacoes_df['id'].tolist()
    except Exception as e:
        print(f"Erro ao buscar IDs para area_atuacao_especializacao: {e}")
        return []

    # Garantir participação de cada area
    for a_id in ids_areas:
        if not ids_especializacoes: continue
        e_id = random.choice(ids_especializacoes)
        combinacoes_geradas.add((a_id, e_id))

    # Garantir participação de cada especializacao
    for e_id in ids_especializacoes:
        if not ids_areas: continue
        a_id = random.choice(ids_areas)
        combinacoes_geradas.add((a_id, e_id))

    # Adicionar mais combinações aleatórias até n
    max_combinacoes = len(ids_areas) * len(ids_especializacoes)
    target_count = min(n, max_combinacoes)

    while len(combinacoes_geradas) < target_count:
        a_id = random.choice(ids_areas)
        e_id = random.choice(ids_especializacoes)
        combinacoes_geradas.add((a_id, e_id))

    data = [{'id_area_atuacao': a, 'id_especializacao': e} for a, e in combinacoes_geradas]
    random.shuffle(data)

    return data

def generate_data_Especializacao_Funcionario(n:int, engine: sqlalchemy.engine.Engine):
    """
    📄 Tabela: especializacao_funcionario
    🧱 Coluna: id_funcionario - Tipo: INTEGER
    🧱 Coluna: id_especializacao - Tipo: INTEGER
    🔑 Chave Primária: ['id_funcionario', 'id_especializacao']
    🔗 FK: ['id_funcionario'] → funcionario.['id']
    🔗 FK: ['id_especializacao'] → especializacao.['id']
    Garante participação mínima de funcionario e especializacao.
    """
    data = []
    try:
        # Passar engine diretamente para pandas
        ids_funcionarios_df = pd.read_sql_query("SELECT id FROM funcionario", engine)
        ids_especializacoes_df = pd.read_sql_query("SELECT id FROM especializacao", engine)

        if ids_funcionarios_df.empty or ids_especializacoes_df.empty:
            print("AVISO: Tabelas 'funcionario' ou 'especializacao' estão vazias. Não é possível gerar dados para 'especializacao_funcionario'.")
            return []
        ids_funcionarios = ids_funcionarios_df['id'].tolist()
        ids_especializacoes = ids_especializacoes_df['id'].tolist()
    except Exception as e:
        print(f"Erro ao buscar IDs para especializacao_funcionario: {e}")
        return []

    # Garantir participação de cada funcionario
    for f_id in ids_funcionarios:
        quantidade_especializacoes = random.randint(1, n)
        for _ in range(quantidade_especializacoes):
            e_id = random.choice(ids_especializacoes)
            data.append({'id_funcionario': f_id, 'id_especializacao': e_id})


    return data

def generate_data_Paciente(n:int):
    """
    📄 Tabela: paciente
    🧱 Coluna: id - Tipo: INTEGER
    🧱 Coluna: nome - Tipo: VARCHAR(100)
    🧱 Coluna: idade - Tipo: INTEGER
    🧱 Coluna: data_nascimento - Tipo: DATE
    🧱 Coluna: cpf - Tipo: VARCHAR(20)
    🧱 Coluna: sexo - Tipo: VARCHAR(1)
    🔑 Chave Primária: ['id']
    """
    data = []
    for _ in range(n):
        data.append({
            'nome': fake.name(),
            'idade': fake.random_int(min=1,  max=100),
            'data_nascimento': fake.date_of_birth(minimum_age=1, maximum_age=100),
            'cpf': fake.random_number(digits=11),   
            'sexo': fake.random_element(elements=('M', 'F')),
        })
    return data


def generate_data_Agendamento(n:int, engine: sqlalchemy.engine.Engine):
    """
    📄 Tabela: agendamento
    🧱 Coluna: id_hospital - Tipo: INTEGER
    🧱 Coluna: id_paciente - Tipo: INTEGER
    🧱 Coluna: id_funcionario - Tipo: INTEGER
    🧱 Coluna: id_area_atuacao - Tipo: INTEGER
    🧱 Coluna: data_consulta - Tipo: DATE
    🧱 Coluna: agendamento_realizado - Tipo: BOOLEAN
    🔑 Chave Primária: ['id_hospital', 'id_funcionario', 'id_paciente', 'id_area_atuacao', 'data_consulta']
    🔗 FK: ['id_area_atuacao'] → area_de_atuacao.['id']
    🔗 FK: ['id_funcionario'] → funcionario.['id']
    🔗 FK: ['id_hospital'] → hospital.['id']
    🔗 FK: ['id_paciente'] → paciente.['id']
    
    """
    data = []
    combinacoes_geradas = set()
    try:
        # Passar engine diretamente para pandas
        ids_hospitais_df = pd.read_sql_query("SELECT id FROM hospital", engine)
        ids_pacientes_df = pd.read_sql_query("SELECT id FROM paciente", engine)
        ids_funcionarios_df = pd.read_sql_query("SELECT id FROM funcionario", engine)
        ids_areas_df = pd.read_sql_query("SELECT id FROM area_de_atuacao", engine)

        if ids_hospitais_df.empty or ids_pacientes_df.empty or ids_funcionarios_df.empty or ids_areas_df.empty:
            print("AVISO: Uma ou mais tabelas FK (hospital, paciente, funcionario, area_de_atuacao) estão vazias. Não é possível gerar dados para 'agendamento'.")
            return []

        ids_hospitais = ids_hospitais_df['id'].tolist()
        ids_pacientes = ids_pacientes_df['id'].tolist()
        ids_funcionarios = ids_funcionarios_df['id'].tolist()
        ids_areas = ids_areas_df['id'].tolist()

    except Exception as e:
        print(f"Erro ao buscar IDs para agendamento: {e}")
        return []

    # Garantir participação de cada paciente
    for p_id in ids_pacientes:
        for a in range(fake.random_int(min=n//3,  max=n)):
            h_id = random.choice(ids_hospitais)
            f_id = random.choice(ids_funcionarios)
            a_id = random.choice(ids_areas)
            data_consulta = fake.date_between(start_date='-1y', end_date='+1y')
            data.append({'id_hospital': h_id, 'id_paciente': p_id, 'id_funcionario': f_id, 'id_area_atuacao': a_id, 'data_consulta': data_consulta, 'agendamento_realizado': fake.boolean()})
    

    # Garantir participação de cada area_de_atuacao
    

    return data

def criar_conexao()->sqlalchemy.engine.Engine:

    # Fetch variables
    USER = 'postgres.bwvqneansuqchkccmhxq'
    PASSWORD = 'Feisenha123##'
    HOST ='aws-0-sa-east-1.pooler.supabase.com'
    PORT =5432
    DBNAME = 'postgres'

    # Construct the SQLAlchemy connection string
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    engine = create_engine(DATABASE_URL)
    return engine



def criar_banco(engine:sqlalchemy.engine.Engine):
    """
    Cria o banco de dados
    """
    with open("CreateTable.sql", "r") as arquivo:
        sql = arquivo.read()
    with engine.connect() as conexao:
        conexao.execute(text(sql))
        conexao.commit()
    return True



def pegar_schema(engine:sqlalchemy.engine.Engine):
    """
    Pega o schema do banco de dados utilizando o SQLAlchemy inspector
    """
    schema = ""
    inspector = sql_inspect(engine)
    tabelas = inspector.get_table_names(schema='public')

    for tabela in tabelas:
        schema+= f"\n📄 Tabela: {tabela}\n"
        colunas = inspector.get_columns(tabela, schema='public')
        for col in colunas:
            schema+=f"  🧱 Coluna: {col['name']} - Tipo: {col['type']}\n"
        pk = inspector.get_pk_constraint(tabela, schema='public')
        schema +=f"  🔑 Chave Primária: {pk.get('constrained_columns', [])}\n"
        fks = inspector.get_foreign_keys(tabela, schema='public')
        for fk in fks:
            schema +=f"  🔗 FK: {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}\n"

    return schema

def truncar_todo_banco(engine:sqlalchemy.engine.Engine):
    """
    Trunca todas as tabelas do banco de dados
    """
    inspector = sql_inspect(engine)
    tabelas = inspector.get_table_names(schema='public')
    for tabela in tabelas:
        with engine.connect() as conexao:
            conexao.execute(text(f"TRUNCATE TABLE {tabela} RESTART IDENTITY CASCADE"))
            conexao.commit()
        print(f"Tabela {tabela} truncada com sucesso")
    return True





def pegar_informacoes_schema(engine: sqlalchemy.engine.Engine, schema: str = 'public') -> dict:
    """
    Pega informações detalhadas do schema (tabelas, colunas, PKs, FKs).
    """
    inspector = sql_inspect(engine)
    schema_info = {
        'tabelas': {},
        'foreign_keys': []
    }

    try:
        tabelas = inspector.get_table_names(schema=schema)
        for tabela in tabelas:
            colunas = inspector.get_columns(tabela, schema=schema)
            pk_constraint = inspector.get_pk_constraint(tabela, schema=schema)
            primary_keys = pk_constraint['constrained_columns'] if pk_constraint else []

            schema_info['tabelas'][tabela] = {
                'colunas': colunas,
                'primary_keys': primary_keys
            }

            fks = inspector.get_foreign_keys(tabela, schema=schema)
            for fk in fks:
                constrained_columns = fk['constrained_columns'] if isinstance(fk['constrained_columns'], list) else [fk['constrained_columns']]
                referred_columns = fk['referred_columns'] if isinstance(fk['referred_columns'], list) else [fk['referred_columns']]

                if len(constrained_columns) != len(referred_columns):
                     print(f"Aviso: Número de colunas inconsistente na FK da tabela '{tabela}': {fk['name']}")
                     continue
                fk_info = {
                    'referencing_table': tabela,
                    'referencing_columns': constrained_columns,
                    'referred_table': fk['referred_table'],
                    'referred_columns': referred_columns,
                    'name': fk['name']
                }
                schema_info['foreign_keys'].append(fk_info)

    except Exception as e:
        print(f"Erro ao inspecionar o schema '{schema}': {e}")
        return schema_info

    return schema_info


def gerar_querys_validacao(schema_info: dict, schema: str = 'public') -> list[tuple[str, str]]:
    """
    Gera queries SQL para validar nulidade, integridade referencial e participação em N:M.
    Retorna uma lista de tuplas (descricao_da_query, query_sql).
    """
    querys_validacao = []

    # 1. Validar colunas NOT NULL
    for tabela, info_tabela in schema_info.get('tabelas', {}).items():
        for coluna_info in info_tabela.get('colunas', []):
            if not coluna_info['nullable']:
                nome_coluna = coluna_info['name']
                descricao = f"Verifica NULL na coluna {schema}.{tabela}.{nome_coluna} (NOT NULL)"
                query = f'SELECT COUNT(1) FROM "{schema}"."{tabela}" WHERE "{nome_coluna}" IS NULL;'
                querys_validacao.append((descricao, query))


    for fk in schema_info.get('foreign_keys', []):
        tabela_origem = fk['referencing_table']
        colunas_origem = fk['referencing_columns']
        tabela_destino = fk['referred_table']
        colunas_destino = fk['referred_columns']
        fk_name = fk['name']

        # Monta as condições do JOIN e do WHERE
        join_conditions = " AND ".join([f't1."{orig}" = t2."{dest}"' for orig, dest in zip(colunas_origem, colunas_destino)])
        where_null_check = " OR ".join([f't2."{dest}" IS NULL' for dest in colunas_destino]) # Se qualquer parte da PK referenciada for nula, o join falha
        # Verifica apenas FKs que não são nulas na origem
        where_origem_not_null = " AND ".join([f't1."{orig}" IS NOT NULL' for orig in colunas_origem])


        descricao = f"Verifica registros órfãos na tabela '{tabela_origem}' pela FK '{fk_name}' para '{tabela_destino}'"
        query = f"""
        SELECT COUNT(1)
        FROM "{schema}"."{tabela_origem}" t1
        LEFT JOIN "{schema}"."{tabela_destino}" t2 ON {join_conditions}
        WHERE ({where_null_check}) AND ({where_origem_not_null});
        """
        querys_validacao.append((descricao, " ".join(query.split())))

    relacoes_nm = [
        ('area_de_atuacao', 'id', 'area_atuacao_hospital', 'id_area_atuacao'),
        ('hospital', 'id', 'area_atuacao_hospital', 'id_hospital'),
        ('especializacao', 'id', 'area_atuacao_especializacao', 'id_especializacao'),
        ('area_de_atuacao', 'id', 'area_atuacao_especializacao', 'id_area_atuacao'),
        ('hospital', 'id', 'hospital_funcionario', 'id_hospital'),
        ('funcionario', 'id', 'hospital_funcionario', 'id_funcionario'),
        ('paciente', 'id', 'agendamento', 'id_paciente'),
        ('funcionario', 'id', 'agendamento', 'id_funcionario'),
        ('area_de_atuacao', 'id', 'agendamento', 'id_area_atuacao'),
    ]

    print("\n--- Iniciando validações de participação N:M ---")
    for tabela_principal, pk_principal, tabela_associacao, fk_associacao in relacoes_nm:
        # Verifica se as tabelas existem no schema antes de gerar a query
        if tabela_principal in schema_info.get('tabelas', {}) and tabela_associacao in schema_info.get('tabelas', {}):
            descricao = f"Verifica se todo(a) '{tabela_principal}' possui pelo menos um registro em '{tabela_associacao}'"
            query = f"""
            SELECT COUNT(t1."{pk_principal}")
            FROM "{schema}"."{tabela_principal}" t1
            LEFT JOIN "{schema}"."{tabela_associacao}" t2 ON t1."{pk_principal}" = t2."{fk_associacao}"
            WHERE t2."{fk_associacao}" IS NULL;
            """
            querys_validacao.append((descricao, " ".join(query.split())))
        else:
            print(f"  AVISO: Pulando validação N:M para '{tabela_principal}' <-> '{tabela_associacao}' pois uma ou ambas as tabelas não foram encontradas no schema.")
    print("--- Fim validações N:M ---")

    return querys_validacao

def executar_validacoes(engine: sqlalchemy.engine.Engine, querys: list[tuple[str, str]]) -> bool:
    """
    Executa as queries de validação e reporta falhas.
    Retorna True se todas as validações passaram, False caso contrário.
    """
    todas_passaram = True
    with engine.connect() as connection:
        for descricao, query in querys:
            try:
                print(f"Executando validação: {descricao}")
                result = connection.execute(text(query))
                count = result.scalar_one_or_none()

                if count is None:
                     print(f"  AVISO: A query não retornou um count. Query: {query}")
                elif count > 0:
                    print(f"  FALHA: A validação encontrou {count} linha(s) inválida(s).")
                    print(f"  Query: {query}")
                    todas_passaram = False
                else:
                    print("  SUCESSO: Nenhuma linha inválida encontrada.")
                    pass

            except Exception as e:
                print(f"  ERRO ao executar a query de validação: {e}")
                print(f"  Query: {query}")
                todas_passaram = False 
            print("-" * 20) 

    return todas_passaram




if __name__ == "__main__":
    
    schema_banco = 'public'
    
    conexao = criar_conexao()
    print("Criando banco de dados...",end="\n\n\n")
    if criar_banco(conexao):
        print("Banco de dados criado com sucesso")
    else:
        print("Erro ao criar banco de dados")

    print("Pegando o schema do markdown bonitinho...",end="\n\n\n")
    schema = pegar_schema(conexao)
    print(schema)
    with open('Schema.md', 'w', encoding='utf-8') as arquivo:
        arquivo.write(schema)
    print("Schema salvo em Schema.md")
    print("-" * 20,end="\n\n\n")
    print("Truncando tabelas...",end="\n\n\n")
    if truncar_todo_banco(conexao):
        print("Tabelas truncadas com sucesso")
    print("Iniciando a geração dos dados...",end="\n\n\n")
    for config in config_dados:
        print(f"Iniciando a geração dos dados para a tabela: {config['table']}")
        func = globals()[config['function']]
        # Verificar se a função precisa do engine usando o inspect padrão
        sig = inspect.signature(func)
        if 'engine' in sig.parameters:
            data = func(config['n'], conexao) # Passa a conexão (engine)
        else:
            data = func(config['n']) # Chama sem a conexão

        if not data: # Pular se a geração de dados falhou (ex: tabelas FK vazias)
            print(f"Nenhum dado gerado para {config['table']}, pulando inserção.")
            print("-" * 20)
            continue

        df = pd.DataFrame(data)
        if config['table'] == 'area_atuacao_hospital':
            df = df.drop_duplicates(subset=['id_area_atuacao', 'id_hospital'])
        elif config['table'] == 'area_atuacao_especializacao':
            df = df.drop_duplicates(subset=['id_area_atuacao', 'id_especializacao'])
        elif config['table'] == 'hospital_funcionario':
            df = df.drop_duplicates(subset=['id_hospital', 'id_funcionario'])
        elif config['table'] == 'agendamento':
            df = df.drop_duplicates(subset=['id_hospital', 'id_funcionario', 'id_paciente', 'id_area_atuacao', 'data_consulta'])
        elif config['table'] == 'especializacao_funcionario':
            df = df.drop_duplicates(subset=['id_funcionario', 'id_especializacao'])
        try:
            df.to_sql(config['table'], conexao, if_exists='append', index=False, schema='public')
            print(f"Dados gerados para a tabela: {config['table']}")
            print("-" * 20)
        except Exception as e:
            print(f"Erro ao gerar dados para a tabela: {config['table']}")
            print(f"Erro: {e}")
            print(f"Dados: {df}")
    

    print("Iniciando a validação dos dados...",end="\n\n\n")
    if conexao:
        print(f"\nInspecionando o schema '{schema_banco}'...")
        schema_info = pegar_informacoes_schema(conexao, schema=schema_banco)
        
        if not schema_info.get('tabelas'):
             print("Nenhuma tabela encontrada no schema ou erro ao buscar informações.")
        else:
            print("Informações do schema:")
            for tabela, info_tabela in schema_info.get('tabelas', {}).items():
                print(f"Tabela: {tabela}")
            for coluna in info_tabela.get('colunas', []):
                print(f"Coluna: {coluna['name']} - Tipo: {coluna['type']}")
            
            print("-" * 20)
            for fk in schema_info.get('foreign_keys', []):
                print(f"FK: {fk['name']} - Tabela de origem: {fk['referencing_table']} - Tabela de destino: {fk['referred_table']} - Colunas de origem: {fk['referencing_columns']} - Colunas de destino: {fk['referred_columns']}")



        if schema_info.get('tabelas'):
            print("\nGerando queries de validação...")
            print("Esperando 10 segundos...")
            time.sleep(10)
            querys_validacao = gerar_querys_validacao(schema_info, schema=schema_banco)

            if not querys_validacao:
                print("Nenhuma query de validação foi gerada.")
            else:
                print(f"\nIniciando {len(querys_validacao)} validações...")
                resultado_final = executar_validacoes(conexao, querys_validacao)

                print("\n--- Resultado Final da Validação ---")
                if resultado_final:
                    print("✅ Todas as validações foram executadas com sucesso e passaram!")
                else:
                    print("❌ Algumas validações falharam ou encontraram erros.")
        conexao.dispose()
    else:
        print("Não foi possível conectar ao banco. Saindo.")
        sys.exit(1) 














