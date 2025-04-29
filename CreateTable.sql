;DROP TABLE IF EXISTS public.Funcionario
;DROP TABLE IF EXISTS public.Hospital
;DROP TABLE IF EXISTS public.Paciente
;DROP TABLE IF EXISTS public.AreaDeAtuacao
;DROP TABLE IF EXISTS public.Especializacao
;DROP TABLE IF EXISTS public.AreaAtuacaoHospital
;DROP TABLE IF EXISTS public.Hospital_Funcionario
;DROP TABLE IF EXISTS public.Agendamento
;DROP TABLE IF EXISTS public.Area_Atuacao_Especializacao
;DROP TABLE IF EXISTS public.Especializacao_Funcionario

;create table public.Funcionario(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	idade int not null,
    salario float not null,
    data_nascimento date not null
)

;create table public.Hospital(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	endereco VARCHAR(100) not null,
    quantidade_quartos int not null,
    leitos int not null,
    avaliacao int not null,
    cnpj int not null,
    id_responsavel int not null
)

;create table public.Paciente(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	idade int not null,
    data_nascimento date not null,
    cpf varchar(15)  not null,
    sexo varchar(1) not null
)

;create table public.AreaDeAtuacao(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	codigo_area varchar(15) not null
)

;create table public.Especializacao(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	descricao VARCHAR(100) not null,
    codigo_especializacao VARCHAR(100) not null
)

;create table public.AreaAtuacaoHospital(
	id_hospital int not null,
	id_area_atuacao int not null,
    PRIMARY KEY (id_hospital, id_area_atuacao)
)

;create table public.Hospital_Funcionario(
	id_hospital int not null,
	id_funcionario int not null,
    PRIMARY KEY (id_hospital, id_funcionario)
)

;create table public.Agendamento(
	id_hospital int not null,
    id_paciente int not null,
	id_funcionario int not null,
    id_area_atuacao int not null,
    data_consulta date not null,
    agendamento_realizado bool not null,
    PRIMARY KEY (id_hospital, id_funcionario, id_paciente, id_area_atuacao, data_consulta)
)

;create table public.Area_Atuacao_Especializacao(
	id_area_atuacao int not null,
    id_especializacao int not null,
    PRIMARY KEY (id_area_atuacao, id_especializacao)
)

;create table public.Especializacao_Funcionario(
	id_funcionario int not null,
    id_especializacao int not null,
    PRIMARY KEY (id_funcionario, id_especializacao)
)