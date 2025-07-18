DROP DATABASE IF EXISTS personagens_bd;

CREATE DATABASE personagens_bd;
USE personagens_bd;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
    ALTER TABLE usuarios ADD COLUMN email VARCHAR(255) UNIQUE;
    ALTER TABLE usuarios ADD COLUMN confirmation_token VARCHAR(255);
    ALTER TABLE usuarios ADD COLUMN confirmed BOOLEAN DEFAULT FALSE;
);

CREATE TABLE personagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    nome VARCHAR(255),
    idade INT,
    classe VARCHAR(255),
    raca VARCHAR(255),
    sexo VARCHAR(255),
    vigor INT,
    mente INT,
    fortitude INT,
    forca INT,
    destreza INT,
    inteligencia INT,
    fe INT,
    arcano INT,
    build_escolhida VARCHAR(255),
    equipamento TEXT,
    roupas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);