import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import os

logo_site = "selo_fundo_azul.png"

st.set_page_config(initial_sidebar_state="collapsed",
                   page_title="Termo de Boas Práticas", 
                   layout="wide", 
                   page_icon=logo_site)

st.title("Termo de Boas Práticas")
st.write("Por favor, leia o termo abaixo e confirme sua leitura ao terminar.")

termo_pc = "termo_computadores.pdf"

if os.path.exists(termo_pc):
    with open(termo_pc, "rb") as f:
        pdf_bytes = f.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="650" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.warning("PDF não existe")

st.markdown("---")

#FORMULARIO

st.subheader("Confirmação de Leitura")

nome = st.text_input("Digite seu nome completo: ")
email = st.text_input("Digite seu e-mail corporativo: ")
confirmacao = st.checkbox("Eu li e estou ciente do termo de responsabilidade.")

if st.button("Salvar Confirmação"):
    if nome.strip() == "":
        st.error("Por favor, digite seu nome.")
    if email.strip() == "":
        st.error("Por favor, digite seu e-mail.")
    elif not confirmacao:
        st.error("Por favor, clique na caixa de confirmação.")

#CSV

    else: 
        registro = "registro.csv"
        data = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        novo_registro = pd.DataFrame([{"Nome": nome, "E-mail": email, "Data/Hora":data}])

        if os.path.exists(registro):
            df_existente = pd.read_csv(registro, sep=';')
            if nome in df_existente["Nome"].values:
                st.warning("Esse nome já existe na lista de assinaturas.")
                if email in df_existente["E-mail"].values:
                    st.warning("Esse e-mail já existe na lista de assinaturas.")
            else:
                df_existente = pd.concat([df_existente, novo_registro], ignore_index=True)
                df_existente.to_csv(registro, index=False, sep=';')
                st.success(f"Obrigado, {nome}! Sua assinatura foi confirmada.")
        else:
            novo_registro.to_csv(registro, index=False, sep=';')
            st.success(f"Obrigado, {nome}! Sua assinatura foi confirmada.")

#PAINEL ADM

st.sidebar.title("Administrador")
senha = st.sidebar.text_input("Digite a senha: ", type="password")

if senha == "Far@#mix26":
    st.sidebar.subheader("Assinaturas Concluídas: ")
    if os.path.exists("registro.csv"):
        df_leituras = pd.read_csv("registro.csv", sep=';')
        st.sidebar.dataframe(df_leituras)
    else:
        st.sidebar.info("Nenhum registro.")