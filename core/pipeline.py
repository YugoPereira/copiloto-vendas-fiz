import os
import sqlite3
import csv
import uuid
from datetime import datetime, UTC
from core.config import DIR_DATABASE, DIR_DATASETS

class PipelineDados:
    @staticmethod
    def inicializar_banco():
        os.makedirs(DIR_DATABASE, exist_ok=True)
        conn = sqlite3.connect(f"{DIR_DATABASE}/vendas.db")
        cursor = conn.cursor()

        # Tabela 1: Dimensão Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                telefone TEXT PRIMARY KEY,
                nome TEXT,
                cidade TEXT
            )
        ''')

        # Tabela 2: Fato Negociações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS negociacoes (
                id_negociacao TEXT PRIMARY KEY,
                telefone TEXT,
                produto_interesse TEXT,
                quantidade TEXT,
                dia_entrega TEXT,
                status_negociacao TEXT,
                objecao_principal TEXT,
                resumo TEXT,
                timestamp_inicio TEXT,
                timestamp_fim TEXT
            )
        ''')

        # Tabela 3: Fato Mensagens
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensagens (
                id_mensagem TEXT PRIMARY KEY,
                id_negociacao TEXT,
                telefone TEXT,
                autor TEXT,
                mensagem TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def salvar_mensagem_bd(id_negociacao, telefone, autor, mensagem):
        """Salva a mensagem individual para métricas de BI"""
        PipelineDados.inicializar_banco()
        
        # Usando context manager para garantir fechamento da conexão
        with sqlite3.connect(f"{DIR_DATABASE}/vendas.db") as conn:
            cursor = conn.cursor()
            id_msg = str(uuid.uuid4())[:8]
            timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO mensagens (id_mensagem, id_negociacao, telefone, autor, mensagem, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (id_msg, id_negociacao, telefone, autor, mensagem, timestamp))
            conn.commit()

    @staticmethod
    def salvar_negociacao(negociacao_obj):
        """Salva a consolidação da venda e exporta backup CSV"""
        PipelineDados.inicializar_banco()
        dados = negociacao_obj.to_dict()
        timestamp_fim = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

        # Conexão segura com banco de dados
        with sqlite3.connect(f"{DIR_DATABASE}/vendas.db") as conn:
            cursor = conn.cursor()

            cidade_atual = dados.get('cidade', '').strip() or "Não Informada"

            # Atualiza cliente
            cursor.execute('''
                INSERT OR REPLACE INTO clientes (telefone, nome, cidade)
                VALUES (?, ?, ?)
            ''', (dados['telefone_cliente'], dados['nome_cliente'], cidade_atual))

            # Atualiza negociação
            cursor.execute('''
                INSERT OR REPLACE INTO negociacoes
                (id_negociacao, telefone, produto_interesse, quantidade, dia_entrega, status_negociacao, objecao_principal, resumo, timestamp_inicio, timestamp_fim)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dados['id_negociacao'], dados['telefone_cliente'], dados['produto_interesse'],
                dados['quantidade'], dados['dia_entrega'], dados['status_negociacao'],
                dados['objecao_principal'], dados['resumo'], dados['timestamp_inicio'], timestamp_fim
            ))
            conn.commit()
        
        # Backup em CSV (Mantido para segurança)
        os.makedirs(DIR_DATASETS, exist_ok=True)
        arquivo_csv = f"{DIR_DATASETS}/base_negociacoes.csv"
        existe_csv = os.path.isfile(arquivo_csv)
        with open(arquivo_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=dados.keys(), delimiter=';')
            if not existe_csv: writer.writeheader()
            writer.writerow(dados)