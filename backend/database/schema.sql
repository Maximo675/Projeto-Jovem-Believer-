-- ============================================
-- SCHEMA DO BANCO DE DADOS - INFANT.ID
-- PostgreSQL
-- ============================================
-- Este arquivo contém o schema completo para
-- criar as tabelas do banco de dados.

-- Executar conectado ao banco alvo (ex: infant_id_platform).
-- Para criar o banco antes: CREATE DATABASE infant_id_platform;

-- ============================================
-- Função de trigger: atualiza data_atualizacao
-- automaticamente em qualquer UPDATE
-- ============================================
CREATE OR REPLACE FUNCTION update_data_atualizacao()
RETURNS TRIGGER AS $$
BEGIN
    NEW.data_atualizacao = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Tabela: Hospitais
-- ============================================
CREATE TABLE IF NOT EXISTS hospitals (
    id               SERIAL PRIMARY KEY,
    nome             VARCHAR(255)  NOT NULL UNIQUE,
    estado           VARCHAR(2)    NOT NULL,
    cidade           VARCHAR(120)  NOT NULL,
    endereco         VARCHAR(255)  NOT NULL,
    telefone         VARCHAR(20)   NOT NULL,
    email            VARCHAR(120)  NOT NULL UNIQUE,
    cnpj             VARCHAR(18),
    ativo            BOOLEAN       DEFAULT TRUE,
    data_criacao     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_hospitals_estado ON hospitals (estado);
CREATE INDEX IF NOT EXISTS idx_hospitals_email  ON hospitals (email);

CREATE OR REPLACE TRIGGER trg_hospitals_update
    BEFORE UPDATE ON hospitals
    FOR EACH ROW EXECUTE FUNCTION update_data_atualizacao();

-- ============================================
-- Tabela: Usuários
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id               SERIAL PRIMARY KEY,
    email            VARCHAR(120) NOT NULL UNIQUE,
    nome             VARCHAR(120) NOT NULL,
    senha_hash       VARCHAR(255) NOT NULL,
    hospital_id      INT,
    funcao           VARCHAR(50)  DEFAULT 'usuario',
    ativo            BOOLEAN      DEFAULT TRUE,
    data_criacao     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_users_email           ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_hospital        ON users (hospital_id);
CREATE INDEX IF NOT EXISTS idx_users_hospital_funcao ON users (hospital_id, funcao);

CREATE OR REPLACE TRIGGER trg_users_update
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_data_atualizacao();

-- ============================================
-- Tabela: Cursos
-- ============================================
CREATE TABLE IF NOT EXISTS courses (
    id               SERIAL PRIMARY KEY,
    titulo           VARCHAR(255) NOT NULL,
    descricao        TEXT         NOT NULL,
    nivel            VARCHAR(20)  DEFAULT 'basico',
    tempo_estimado   INT,
    autor            VARCHAR(120) NOT NULL,
    imagem_url       VARCHAR(255),
    ativo            BOOLEAN      DEFAULT TRUE,
    data_criacao     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_courses_ativo ON courses (ativo);
CREATE INDEX IF NOT EXISTS idx_courses_nivel ON courses (nivel);

CREATE OR REPLACE TRIGGER trg_courses_update
    BEFORE UPDATE ON courses
    FOR EACH ROW EXECUTE FUNCTION update_data_atualizacao();

-- ============================================
-- Tabela: Aulas
-- ============================================
CREATE TABLE IF NOT EXISTS lessons (
    id                     SERIAL PRIMARY KEY,
    curso_id               INT         NOT NULL,
    titulo                 VARCHAR(255) NOT NULL,
    descricao              TEXT         NOT NULL,
    conteudo               TEXT         NOT NULL,  -- LONGTEXT → TEXT no PostgreSQL
    ordem                  INT          NOT NULL,
    duracao                INT,
    video_url              VARCHAR(255),
    material_complementar  TEXT,
    ativo                  BOOLEAN      DEFAULT TRUE,
    data_criacao           TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao       TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (curso_id) REFERENCES courses(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_lessons_curso      ON lessons (curso_id);
CREATE INDEX IF NOT EXISTS idx_lessons_ordem      ON lessons (ordem);
CREATE INDEX IF NOT EXISTS idx_lessons_curso_ativo ON lessons (curso_id, ativo);

CREATE OR REPLACE TRIGGER trg_lessons_update
    BEFORE UPDATE ON lessons
    FOR EACH ROW EXECUTE FUNCTION update_data_atualizacao();

-- ============================================
-- Tabela: Progresso
-- ============================================
CREATE TABLE IF NOT EXISTS progress (
    id               SERIAL PRIMARY KEY,
    usuario_id       INT       NOT NULL,
    curso_id         INT       NOT NULL,
    aula_id          INT,
    percentual       INT       DEFAULT 0,
    concluido        BOOLEAN   DEFAULT FALSE,
    data_inicio      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_conclusao   TIMESTAMP,
    tempo_gasto      INT       DEFAULT 0,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES users(id)   ON DELETE CASCADE,
    FOREIGN KEY (curso_id)   REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (aula_id)    REFERENCES lessons(id) ON DELETE SET NULL,
    UNIQUE (usuario_id, curso_id)
);

CREATE INDEX IF NOT EXISTS idx_progress_usuario          ON progress (usuario_id);
CREATE INDEX IF NOT EXISTS idx_progress_curso            ON progress (curso_id);
CREATE INDEX IF NOT EXISTS idx_progress_concluido        ON progress (concluido);
CREATE INDEX IF NOT EXISTS idx_progress_usuario_concluido ON progress (usuario_id, concluido);

CREATE OR REPLACE TRIGGER trg_progress_update
    BEFORE UPDATE ON progress
    FOR EACH ROW EXECUTE FUNCTION update_data_atualizacao();

-- ============================================
-- Tabela: Conversas com IA
-- ============================================
CREATE TABLE IF NOT EXISTS ia_conversations (
    id            SERIAL PRIMARY KEY,
    usuario_id    INT         NOT NULL,
    curso_id      INT,
    pergunta      TEXT        NOT NULL,
    resposta      TEXT        NOT NULL,
    modelo_ia     VARCHAR(50) DEFAULT 'gpt-3.5-turbo',
    tokens_usados INT         DEFAULT 0,
    avaliacao     INT,
    data_criacao  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES users(id)   ON DELETE CASCADE,
    FOREIGN KEY (curso_id)   REFERENCES courses(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_ia_conv_usuario ON ia_conversations (usuario_id);
CREATE INDEX IF NOT EXISTS idx_ia_conv_data    ON ia_conversations (data_criacao);

-- ============================================
-- Tabela: Certificados
-- ============================================
CREATE TABLE IF NOT EXISTS certificates (
    id                   SERIAL PRIMARY KEY,
    usuario_id           INT         NOT NULL,
    curso_id             INT         NOT NULL,
    numero_certificado   VARCHAR(50) NOT NULL UNIQUE,
    data_emissao         TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    validade             INT,
    arquivo_url          VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES users(id)   ON DELETE CASCADE,
    FOREIGN KEY (curso_id)   REFERENCES courses(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_certificates_usuario ON certificates (usuario_id);
CREATE INDEX IF NOT EXISTS idx_certificates_curso   ON certificates (curso_id);
CREATE INDEX IF NOT EXISTS idx_certificates_numero  ON certificates (numero_certificado);

-- Fim do schema
