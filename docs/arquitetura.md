# Arquitetura do Sistema

## Visão Geral

O Agente Fyz B2B foi desenvolvido seguindo uma arquitetura modular, com foco em simplicidade operacional, escalabilidade e geração de inteligência de negócios.

A solução separa a lógica de interação com o cliente da camada de processamento e persistência de dados, permitindo que conversas comerciais sejam transformadas em informações estruturadas para análise posterior.

A arquitetura foi concebida para suportar dois cenários:

* Testes locais via terminal Python;
* Implantação futura via WhatsApp, sem exigir conhecimento técnico do representante comercial.

---

# Fluxo Geral da Solução

1. **Input:** o cliente interage pelo terminal (ou futuramente via WhatsApp).

2. **Orquestração:** o Agente Fyz utiliza o Google Gemini para interpretar a intenção do usuário e conduzir a conversa seguindo a persona da marca.

3. **RAG (Retrieval-Augmented Generation):** antes de responder, o agente consulta o catálogo de produtos, garantindo maior precisão técnica.

4. **Pipeline de Dados (ETL):** as informações da negociação são transformadas em dados estruturados.

5. **Persistência:** os registros são armazenados em um banco de dados SQLite.

6. **Business Intelligence:** os dados ficam prontos para consumo por ferramentas analíticas como Power BI.

---

# Componentes Técnicos

## 1. Camada de Agente (Core)

### `agente.py`

Orquestrador principal do sistema.

Responsável por:

* controlar o fluxo da conversa;
* enviar mensagens ao modelo de IA;
* coordenar o processo de extração das informações da negociação;
* acionar o pipeline de persistência.

### `llm.py`

Cliente responsável pela comunicação com o Google Gemini.

Implementa mecanismos de:

* retry;
* tratamento de exceções;
* resiliência em caso de falhas temporárias.

### `produtos.py`

Camada de RAG responsável pela consulta ao catálogo de produtos.

Seu objetivo é fornecer contexto técnico adicional para a IA durante o processo de venda.

---

## 2. Camada de Persistência (Data)

### `pipeline.py`

Implementa o padrão ETL (Extract, Transform, Load).

Responsável por:

* estruturar os dados da negociação;
* persistir informações no SQLite;
* manter arquivos CSV como backup;
* preparar os dados para consumo por ferramentas de BI.

### `models.py`

Define as estruturas de dados da aplicação através de Dataclasses.

Essa abordagem garante:

* consistência;
* tipagem;
* facilidade de manutenção.

---

## 3. Camada de Conhecimento (Knowledge)

### `prompt-principal.md`

Define a persona e o comportamento do Agente Fyz.

### `prompt-classificador.md`

Responsável pela extração estruturada dos dados em formato JSON.

### `matriz-objecoes.md`

Base de conhecimento para tratamento das principais objeções comerciais.

### produtos-fyz.json

Catálogo estruturado dos produtos da marca Fyz.

---

# Arquitetura de Dados

O sistema foi projetado para transformar interações comerciais em dados estruturados, permitindo análises posteriores em ferramentas de Business Intelligence.

## Dimensão Clientes

Tabela responsável pelo cadastro único dos pontos de venda.

Principais atributos:

* telefone;
* nome;
* cidade.

---

## Fato Negociações

Tabela responsável pela consolidação das vendas realizadas.

Principais atributos:

* id_negociacao;
* produto_interesse;
* quantidade;
* dia_entrega;
* status_negociacao;
* timestamp_inicio;
* timestamp_fim.

---

## Fato Mensagens

Tabela responsável pelo armazenamento granular das interações realizadas durante o atendimento.

Principais atributos:

* id_mensagem;
* autor;
* mensagem;
* timestamp.

---

Essa estrutura foi modelada para facilitar a criação de modelos estrela (*Star Schema*) e análises em ferramentas de BI.

---

# Modelagem do Banco de Dados (SQLite)

A solução utiliza um banco de dados relacional SQLite, composto por três tabelas principais:

### clientes (Dimensão)

Cadastro único dos pontos de venda.

### negociacoes (Fato)

Consolidação das transações comerciais.

### mensagens (Fato)

Histórico completo das interações realizadas durante a negociação.

Essa modelagem permite análises de:

* produtos mais vendidos;
* taxa de conversão;
* tempo médio de atendimento;
* objeções mais frequentes;
* quantidade de interações por venda.

---

# Integração com Power BI

O banco SQLite foi modelado para integração direta com ferramentas de Business Intelligence.

## Relacionamentos

```text
clientes[telefone]
        ↓
negociacoes[telefone]

negociacoes[id_negociacao]
        ↓
mensagens[id_negociacao]
```

## Indicadores Possíveis

* Taxa de conversão das negociações;
* Produtos mais vendidos;
* Principais objeções comerciais;
* Tempo médio de atendimento;
* Quantidade média de interações por venda;
* Evolução diária das negociações;
* Penetração da marca por cidade ou região.

---

# Fluxo da Arquitetura

```text
Cliente
   │
   ▼
WhatsApp / Terminal
   │
   ▼
Agente de IA (Google Gemini)
   │
   ▼
RAG (Catálogo de Produtos)
   │
   ▼
Pipeline ETL
   │
   ▼
SQLite
 ┌──────────────┬──────────────┬──────────────┐
 │ clientes     │ negociacoes  │ mensagens    │
 └──────────────┴──────────────┴──────────────┘
                │
                ▼
            Power BI
                │
                ▼
      Inteligência Comercial
```

---

# Princípios Arquiteturais

A arquitetura foi construída priorizando:

* simplicidade operacional;
* modularidade;
* separação de responsabilidades;
* persistência dos dados;
* preparação para Business Intelligence;
* futura integração com WhatsApp e APIs externas.

O objetivo principal é transformar conversas comerciais em ativos de dados, permitindo que áreas comerciais e de Trade Marketing tomem decisões baseadas em evidências e não apenas em percepções.
