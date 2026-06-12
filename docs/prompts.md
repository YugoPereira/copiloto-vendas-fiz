# Engenharia de Prompts e Sistema RAG

## Visão Geral

O Agente Fiz B2B foi desenvolvido utilizando técnicas de Engenharia de Prompt e Retrieval-Augmented Generation (RAG), permitindo que as respostas sejam mais consistentes, contextualizadas e alinhadas ao posicionamento da marca.

Em vez de depender exclusivamente do conhecimento do modelo de linguagem, o sistema utiliza fontes de conhecimento estruturadas para enriquecer o processo de decisão da IA.

---

# Arquitetura da Inteligência

A geração das respostas ocorre em três etapas:

1. Recebimento da mensagem do cliente;
2. Busca de contexto no catálogo de produtos;
3. Envio das informações para o Google Gemini juntamente com a persona comercial.

Essa abordagem reduz alucinações e melhora a precisão das recomendações.

---

# Prompt Principal

Arquivo:

```text
prompts/prompt-principal.md
```

Responsável por definir:

* personalidade do agente;
* tom de voz;
* estilo de comunicação;
* comportamento durante a negociação;
* postura comercial da marca.

O objetivo é garantir uma experiência consistente em todos os atendimentos.

---

# Prompt Classificador

Arquivo:

```text
prompts/prompt-classificador.md
```

Após o encerramento da conversa, o histórico completo é enviado para um segundo prompt especializado em extração de informações.

Esse prompt converte dados não estruturados em JSON, permitindo alimentar automaticamente o pipeline de dados.

Exemplos de informações extraídas:

* nome do cliente;
* produto de interesse;
* quantidade;
* dia de entrega;
* objeção principal;
* status da negociação;
* resumo do atendimento.

---

# Base de Conhecimento

## Catálogo de Produtos

Arquivo:

```text
knowledge/produtos-fiz.json
```

Contém informações estruturadas sobre os produtos da marca.

Exemplos:

* sabores;
* embalagens;
* diferenciais;
* características técnicas.

---

## Matriz de Objeções

Arquivo:

```text
knowledge/matriz-objecoes.md
```

Contém respostas orientadas para lidar com objeções comerciais comuns.

Exemplos:

* "Não tenho espaço na geladeira";
* "A marca é pouco conhecida";
* "Meus clientes não pedem esse produto";
* "Já trabalho com outras marcas".

---

# Funcionamento do RAG

Quando o cliente menciona um produto, o sistema realiza uma busca no catálogo.

Fluxo:

```text
Cliente
    │
    ▼
Mensagem recebida
    │
    ▼
Busca no catálogo de produtos
    │
    ▼
Contexto recuperado
    │
    ▼
Google Gemini
    │
    ▼
Resposta contextualizada
```

Essa estratégia permite que o agente trabalhe utilizando informações atualizadas e específicas do negócio.

---

# Benefícios da Abordagem

## Redução de Alucinações

As respostas são fundamentadas em uma base de conhecimento própria.

---

## Maior Consistência

Todos os atendimentos seguem a mesma identidade de comunicação.

---

## Facilidade de Atualização

Novos produtos ou novas objeções podem ser adicionados sem alterar o código do sistema.

---

## Separação de Responsabilidades

A inteligência do negócio permanece desacoplada da lógica da aplicação.

---

# Extração Estruturada de Dados

Após o encerramento da negociação, o histórico da conversa é processado por um prompt especializado.

Fluxo:

```text
Histórico da Conversa
          │
          ▼
Prompt Classificador
          │
          ▼
Google Gemini
          │
          ▼
JSON Estruturado
          │
          ▼
Pipeline ETL
          │
          ▼
SQLite
```

Essa abordagem permite transformar conversas em informações estruturadas para análise posterior.

---

# Tecnologias Utilizadas

* Google Gemini 2.5 Flash;
* Engenharia de Prompt;
* Retrieval-Augmented Generation (RAG);
* JSON estruturado;
* Pipeline ETL;
* SQLite.

---

# Objetivo da Estratégia

O objetivo do Agente Fiz B2B não é apenas responder perguntas, mas transformar conhecimento comercial em um ativo reutilizável.

Ao combinar Engenharia de Prompt com RAG, o sistema consegue oferecer respostas mais precisas, manter a identidade da marca e gerar dados estruturados capazes de apoiar análises e decisões futuras.
