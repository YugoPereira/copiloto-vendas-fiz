# Integração com Power BI

## Visão Geral

O Agente Fiz B2B foi projetado com uma arquitetura **BI-Ready**, permitindo que as informações geradas durante as negociações sejam consumidas por ferramentas de Business Intelligence.

O banco de dados SQLite (`vendas.db`) atua como a camada de persistência da solução, possibilitando análises comerciais e operacionais em tempo real.

---

# Fonte de Dados

Banco de dados:

```text
database/vendas.db
```

Tecnologia:

* SQLite

Ferramenta de visualização:

* Microsoft Power BI

---

# Conectando ao Power BI

No Power BI Desktop:

1. Clique em **Obter Dados**;
2. Selecione **SQLite Database**;
3. Escolha o arquivo:

```text
database/vendas.db
```

4. Importe as tabelas:

* clientes;
* negociacoes;
* mensagens.

---

# Modelo Relacional

O banco foi modelado para facilitar a construção de um modelo estrela (*Star Schema*).

## Relacionamentos

```text
clientes[telefone]
        │
        ▼
negociacoes[telefone]

negociacoes[id_negociacao]
        │
        ▼
mensagens[id_negociacao]
```

---

# Tabelas

## Dimensão Clientes

Tabela responsável pelo cadastro único dos pontos de venda.

Principais campos:

* telefone;
* nome;
* cidade.

---

## Fato Negociações

Tabela responsável pela consolidação das vendas.

Principais campos:

* id_negociacao;
* produto_interesse;
* quantidade;
* dia_entrega;
* status_negociacao;
* objecao_principal;
* timestamp_inicio;
* timestamp_fim.

---

## Fato Mensagens

Tabela responsável pelo histórico completo das interações.

Principais campos:

* id_mensagem;
* id_negociacao;
* autor;
* mensagem;
* timestamp.

---

# Indicadores de Negócio

A estrutura atual permite construir indicadores como:

## Conversão de Vendas

Quantidade de negociações fechadas.

Exemplo:

* Pedidos Fechados;
* Pedidos Cancelados;
* Taxa de Conversão.

---

## Produtos Mais Vendidos

Análise da demanda por SKU.

Exemplos:

* FIZ Limão;
* FIZ Guaraná;
* FIZ Zero Açúcar.

---

## Principais Objeções

Mapeamento das barreiras comerciais.

Exemplos:

* Falta de espaço na geladeira;
* Marca pouco conhecida;
* Baixa saída.

---

## Tempo Médio de Atendimento

Diferença entre:

* timestamp_inicio;
* timestamp_fim.

Permite identificar:

* negociações rápidas;
* negociações mais complexas;
* eficiência operacional.

---

## Quantidade Média de Interações

Número de mensagens trocadas até o fechamento da venda.

Essa métrica ajuda a avaliar:

* esforço comercial;
* qualidade do atendimento;
* eficiência da negociação.

---

# Exemplos de Dashboards

## Dashboard Comercial

Indicadores:

* Total de negociações;
* Vendas fechadas;
* Taxa de conversão;
* Produtos mais vendidos.

---

## Dashboard Operacional

Indicadores:

* Tempo médio de atendimento;
* Quantidade média de mensagens por negociação;
* Evolução diária das interações.

---

## Dashboard de Trade Marketing

Indicadores:

* Principais objeções;
* Preferências dos clientes;
* Aceitação dos produtos;
* Penetração da marca por cidade.

---

# Exemplo de Medidas DAX

## Total de Negociações

```DAX
Total Negociações =
COUNT(negociacoes[id_negociacao])
```

---

## Pedidos Fechados

```DAX
Pedidos Fechados =
CALCULATE(
    COUNT(negociacoes[id_negociacao]),
    negociacoes[status_negociacao] = "Pedido Fechado"
)
```

---

## Taxa de Conversão

```DAX
Taxa Conversão =
DIVIDE(
    [Pedidos Fechados],
    [Total Negociações]
)
```

---

# Objetivo da Arquitetura

Mais do que automatizar conversas, o Agente Fiz B2B busca transformar dados desestruturados em inteligência comercial.

Ao registrar negociações e interações em um banco relacional, a solução permite que áreas comerciais e de Trade Marketing tenham acesso a informações capazes de apoiar decisões estratégicas baseadas em dados.
