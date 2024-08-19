CREATE DATABASE mstar
COLLATE Latin1_General_100_CI_AS_SC_UTF8;


CREATE TABLE users(
	id INT PRIMARY KEY IDENTITY(1,1),
	uuid UNIQUEIDENTIFIER DEFAULT NEWID(),
    email nvarchar(50),
    primeiro_nome nvarchar(20),
    ultimo_nome nvarchar(20),
    password nvarchar(100),
	is_admin BIT,
	is_active BIT
);

CREATE TABLE unidade(
	id INT PRIMARY KEY IDENTITY(1,1),
	nome nvarchar(50),
	cidade nvarchar(50),
	uf varchar(2),
	endereco nvarchar(50)
);

CREATE TABLE tipo_mercadoria(
 	id INT PRIMARY KEY IDENTITY(1,1),
 	nome nvarchar(50),
 	descricao nvarchar(100)
);

CREATE TABLE cliente(
	id INT PRIMARY KEY IDENTITY(1,1),
	primeiro_nome varchar(20),
	ultimo_nome varchar(20),
	cpf CHAR(11),
	telefone CHAR(11),
	email nvarchar(50),
	cep CHAR(8),
	cidade NVARCHAR(50),
	uf VARCHAR(2),
	endereco nvarchar(50)
	
);

CREATE TABLE mercadoria (
 	id INT PRIMARY KEY IDENTITY(1,1),
	nome nvarchar(50),
	fabricante nvarchar(50),
	numero_registro int,
	descricao nvarchar(100),
	tipo int
	
	FOREIGN KEY (tipo) REFERENCES tipo_mercadoria(id)
);

CREATE TABLE entrada_mercadoria(
	id INT PRIMARY KEY IDENTITY(1,1),
	data DATETIME DEFAULT GETDATE(),
	unidade int,
	quantidade int,
	mercadoria int,
	usuario int,
	
	FOREIGN KEY (unidade) REFERENCES unidade(id),
	FOREIGN KEY (mercadoria) REFERENCES mercadoria(id),
	FOREIGN KEY (usuario) REFERENCES users(id),
	
);

CREATE TABLE saida_mercadoria(
	id INT PRIMARY KEY IDENTITY(1,1),
	data DATETIME,
	quantidade int,
	unidade_saida int,
	unidade_destino int,
	entrega BIT,
	mercadoria int,
	usuario int,
	
	FOREIGN KEY (unidade_saida) REFERENCES unidade(id),
	FOREIGN KEY (unidade_destino) REFERENCES unidade(id),
	FOREIGN KEY (mercadoria) REFERENCES mercadoria(id),
	FOREIGN KEY (usuario) REFERENCES users(id),
	
);

CREATE TABLE estoque_mercadoria(
	id INT PRIMARY KEY IDENTITY(1,1),
	mercadoria int,
	quantidade int
	
	FOREIGN KEY (mercadoria) REFERENCES mercadoria(id),
)
