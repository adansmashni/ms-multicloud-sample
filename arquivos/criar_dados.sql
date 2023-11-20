CREATE TABLE providers (
    id SERIAL PRIMARY KEY,
    nome_provedor VARCHAR(100) NOT NULL,
    companhia VARCHAR(100) NOT NULL
);

INSERT INTO providers (nome_provedor, companhia)
VALUES
    ('AWS', 'Amazon'),
    ('Azure', 'Microsoft'),
    ('GCP', 'Google');