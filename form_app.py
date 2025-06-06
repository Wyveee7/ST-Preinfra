import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Conexão com o banco de dados MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host="database-1.cxkk6gmy4fma.us-east-2.rds.amazonaws.com",  # Exemplo: "127.0.0.1" ou o IP do banco na nuvem
        user="admin",  # Exemplo: "root"
        password="preinfraadmin",  # Sua senha
        database="stpreinfradb"  # Nome do banco de dados
    )
    return conn

# Função para salvar os dados no MySQL
def save_data_to_mysql(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserir dados na tabela 'observacoes'
    query = """
        INSERT INTO observacoes (datahora, email, observador, avaliacao, setor, posicoes, epis, limpeza)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()

# Título e dados do formulário
st.set_page_config(page_title="Formulário de Observação", layout="centered")
st.title("📝 Formulário de Observação de Segurança")

email = st.text_input("E-mail")
observador = st.selectbox("Observador", ["Bruno", "Jonan", "Fabiane"])
avaliacao = st.selectbox("Avaliação", ["1", "2", "3", "4"])
setor = st.selectbox("Setor", [
    "Fôrmas", "Armação", "Desforma", "Corte Solda", "Concretagem", 
    "Movimentação", "Estocagem", "Controle de Qualidade", "Manutenção", 
    "Administrativo", "Limpeza", "Outros"
])

# === A. POSIÇÃO DAS PESSOAS ===
st.header("A. Posição das Pessoas")
posicoes = {
    "Postura correta na atividade": 0,
    "Manutenção de distância segura de equipamentos": 0,
    "Trabalho em altura com segurança": 0,
    "Afastamento de áreas de risco": 0,
    "Utilização correta de ferramentas": 0,
}
for item in posicoes:
    posicoes[item] = st.selectbox(item, [0.0, 0.1, 0.2, 0.3], key=item)

# === B. EPIs ===
st.header("B. EPIs")
epis = {
    "Capacete": 0,
    "Óculos de proteção": 0,
    "Luvas": 0,
    "Protetor auricular": 0,
    "Botina": 0,
    "Colete": 0,
}
for item in epis:
    epis[item] = st.selectbox(item, [0.0, 0.75], key=item)

# === C. ARRUMAÇÃO E LIMPEZA ===
st.header("C. Arrumação e Limpeza")
limpeza = {
    "Local de trabalho limpo": 0,
    "Organização de ferramentas": 0,
    "Sinalização adequada": 0,
    "Descarte correto de resíduos": 0,
}
for item in limpeza:
    limpeza[item] = st.selectbox(item, [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], key=item)

# === BOTÃO DE SALVAR ===
if st.button("Salvar Dados"):
    dados = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        email,
        observador,
        avaliacao,
        setor,
        str(posicoes),
        str(epis),
        str(limpeza)
    )

    # Salvar no banco MySQL
    save_data_to_mysql(dados)
    st.success("✅ Dados salvos com sucesso!")

# === RELATÓRIOS ===
st.sidebar.header("Relatórios")
if st.sidebar.button("Gerar Relatório"):
    conn = get_db_connection()
    query = "SELECT * FROM observacoes"
    df = pd.read_sql(query, conn)
    conn.close()

    st.write("Relatório de Observações de Segurança")
    st.dataframe(df)
