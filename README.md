# Agente Fiz B2B & Sales Intelligence Pipeline 🥤📊

[🔗 Acessar Repositório do Projeto](https://github.com/YugoPereira/copiloto-vendas-fiz)

---

## 🎯 Contexto e Objetivos

Este projeto foi idealizado e desenvolvido como parte prática do bootcamp de **Inteligência Artificial aplicada a Vendas**, promovido pela **DIO em parceria com a Heineken**.

O objetivo central foi criar um **Copiloto de Vendas B2B Autônomo** para a marca **Fiz (Grupo Heineken)**, buscando resolver uma dor recorrente da distribuição logística: a dificuldade de penetração no mercado fragmentado de padarias por meio da força de vendas tradicional.

Segundo o mapeamento do canal, o Brasil possui aproximadamente **72 mil padarias**, sendo cerca de **21% concentradas na Grande São Paulo**. Apesar do alto potencial de consumo de refrigerantes *single serve* (consumo individual), a marca apresenta um *market share* de apenas **0,9%** nesse segmento.

### Principais desafios identificados

* Baixa cobertura física da equipe comercial;
* Prioridade dos vendedores em canais de maior volume de bebidas alcoólicas;
* Pouco tempo disponível dos proprietários para reuniões presenciais;
* Necessidade de um processo de reposição mais ágil.

### Solução proposta

Um **Agente B2B autônomo via WhatsApp**, capaz de:

* Gerar pedidos de reposição rapidamente;
* Utilizar uma persona alinhada ao tom de voz da marca;
* Apresentar o portfólio de forma leve e objetiva;
* Registrar dados para análises futuras.

---

## 🤖 Tecnologias Utilizadas

### Modelagem Analítica

* SQL;
* Estruturação de banco de dados relacional;
* Data Analytics;
* Integração com Power BI.

### Workflow Automation (No-Code / Low-Code)

* OpenClaw;
* n8n;
* Make;
* Integrações via API do WhatsApp.

### Desenvolvimento e Validação

* Python;
* Scripts auxiliares para testes locais;
* Validação de requisições para LLMs.

### Engenharia de Prompts

* Construção de persona;
* Sistema RAG (*Retrieval-Augmented Generation*);
* Roteiros para tratamento de objeções de vendas.

---

## 🧐 Processo de Criação

O ecossistema foi concebido para ir além de um chatbot tradicional, atuando em duas frentes estratégicas.

### 📱 Opção 1: Implantação em Produção via WhatsApp

Destinada à equipe comercial, permitindo rápida adoção sem necessidade de programação.

1. Acesse sua plataforma de automação preferida (OpenClaw, n8n ou Make);
2. Importe o arquivo:

```text
/automacao_whatsapp/fluxo_agente_fiz.json
```

3. Insira a chave da API (Google Gemini ou OpenAI);
4. Conecte o WhatsApp corporativo por meio do QR Code.

---

### 💻 Opção 2: Teste Local via Terminal

Voltada para desenvolvedores e analistas interessados em validar a lógica do agente.

#### 1. Clonar o repositório

```bash
git clone https://github.com/YugoPereira/copiloto-vendas-fiz.git
cd copiloto-vendas-fiz
```

#### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

#### 3. Configurar as credenciais

Renomeie:

```text
.env.example
```

para

```text
.env
```

e adicione sua chave de API.

#### 4. Executar o agente

```bash
python app_local.py
```

---

## 🚀 Resultados

Toda interação realizada pelo agente no WhatsApp gera um **webhook**, responsável por alimentar o banco de dados relacional.

O arquivo:

```text
/data_architecture/schema_vendas.sql
```

foi modelado para integração com o **Power BI**, permitindo:

### 📈 Monitoramento de desempenho

* Comparação da taxa de conversão do Agente B2B com a performance da força de vendas tradicional.

### 🗣️ Mapeamento de objeções

* Geração de nuvem de palavras;
* Identificação das principais barreiras do varejo.

Exemplos:

* "Falta espaço na geladeira";
* "Marca desconhecida".

### 🥤 Análise de sortimento

Avaliação dos produtos com maior índice de:

* Aceitação;
* Rejeição;
* Penetração da linha **Zero Açúcar** em comparação à linha **Regular**.

---

## 💭 Reflexão

A implementação de agentes autônomos integrados a pipelines de dados representa uma mudança significativa na operação de canais B2B fragmentados.

Mais do que reduzir o **Custo de Aquisição de Clientes (CAC)** e ampliar a capilaridade sem aumentar o *headcount*, essa arquitetura transforma dados desestruturados — como conversas no WhatsApp — em **Business Intelligence acionável**, permitindo respostas mais rápidas e decisões orientadas por dados para as áreas de Trade Marketing.

---

## 👨‍💻 Autor

**Yugo Pereira**

Feito com propósito, estratégia e paixão por tecnologia e dados 💙