-- Estrutura de banco de dados para alimentar o Dashboard de Trade Marketing no Power BI

-- Tabela de Cadastro das Padarias Prospectadas
CREATE TABLE lead_padaria (
    id_padaria INT PRIMARY KEY AUTO_INCREMENT,
    nome_fantasia VARCHAR(100),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    data_primeiro_contato DATE
);

-- Tabela de Logs do Agente de Inteligência Artificial
CREATE TABLE interacoes_ia (
    id_interacao INT PRIMARY KEY AUTO_INCREMENT,
    id_padaria INT,
    data_interacao DATETIME,
    objecao_identificada VARCHAR(100), -- Ex: 'Falta de Espaço', 'Prefere a Líder'
    sabor_oferecido VARCHAR(50),
    status_venda VARCHAR(20), -- 'Convertido', 'Em Negociação', 'Perdido'
    FOREIGN KEY (id_padaria) REFERENCES lead_padaria(id_padaria)
);