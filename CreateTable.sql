;DROP TABLE IF EXISTS public.Funcionario CASCADE
;DROP TABLE IF EXISTS public.Hospital CASCADE
;DROP TABLE IF EXISTS public.Paciente CASCADE
;DROP TABLE IF EXISTS public.Area_De_Atuacao CASCADE
;DROP TABLE IF EXISTS public.Especializacao CASCADE
;DROP TABLE IF EXISTS public.Area_Atuacao_Hospital CASCADE
;DROP TABLE IF EXISTS public.Hospital_Funcionario CASCADE
;DROP TABLE IF EXISTS public.Agendamento CASCADE
;DROP TABLE IF EXISTS public.Area_Atuacao_Especializacao CASCADE
;DROP TABLE IF EXISTS public.Especializacao_Funcionario CASCADE

;CREATE TABLE public.Funcionario(
	 id SERIAL NOT NULL PRIMARY KEY
	,nome VARCHAR(100) NOT NULL
	,idade INT NOT NULL
    ,salario float NOT NULL
    ,data_nascimento DATE NOT NULL
)

;CREATE TABLE public.Hospital(
	 id SERIAL NOT NULL PRIMARY KEY
	,nome VARCHAR(100) NOT NULL
	,endereco VARCHAR(100) NOT NULL
    ,quantidade_quartos INT NOT NULL
    ,leitos INT NOT NULL
    ,avaliacao INT NOT NULL
    ,cnpj VARCHAR(20) NOT NULL
    ,id_responsavel INT NOT NULL
)

;CREATE TABLE public.Paciente(
	 id SERIAL NOT NULL PRIMARY KEY
	,nome VARCHAR(100) NOT NULL
	,idade INT NOT NULL
    ,data_nascimento DATE NOT NULL
    ,cpf varchar(20)  NOT NULL
    ,sexo varchar(1) NOT NULL
)

;CREATE TABLE public.Area_De_Atuacao(
	 id SERIAL NOT NULL PRIMARY KEY
	,nome VARCHAR(100) NOT NULL
	,codigo_area varchar(20) NOT NULL
)

;CREATE TABLE public.Especializacao(
	 id SERIAL NOT NULL PRIMARY KEY
	,nome VARCHAR(100) NOT NULL
	,descricao VARCHAR(100) NOT NULL
    ,codigo_especializacao VARCHAR(100) NOT NULL
)

;CREATE TABLE public.Area_Atuacao_Hospital(
	 id_hospital INT NOT NULL
	,id_area_atuacao INT NOT NULL
    ,PRIMARY KEY (id_hospital, id_area_atuacao)
)

;CREATE TABLE public.Hospital_Funcionario(
	 id_hospital INT NOT NULL
	,id_funcionario INT NOT NULL
    ,PRIMARY KEY (id_hospital, id_funcionario)
)

;CREATE TABLE public.Agendamento(
	 id_hospital INT NOT NULL
    ,id_paciente INT NOT NULL
	,id_funcionario INT NOT NULL
    ,id_area_atuacao INT NOT NULL
    ,data_consulta DATE NOT NULL
    ,agendamento_realizado bool NOT NULL
    ,PRIMARY KEY (id_hospital, id_funcionario, id_paciente, id_area_atuacao, data_consulta)
)

;CREATE TABLE public.Area_Atuacao_Especializacao(
	 id_area_atuacao INT NOT NULL
    ,id_especializacao INT NOT NULL
    ,PRIMARY KEY (id_area_atuacao, id_especializacao)
)

;CREATE TABLE public.Especializacao_Funcionario(
	 id_funcionario INT NOT NULL
    ,id_especializacao INT NOT NULL
    ,PRIMARY KEY (id_funcionario, id_especializacao)
)


;ALTER TABLE public.Hospital
  	ADD CONSTRAINT fk_id_responsavel FOREIGN KEY(id_responsavel) REFERENCES Funcionario(id)

;ALTER TABLE public.Area_Atuacao_Hospital
	 ADD CONSTRAINT fkid_hospital FOREIGN KEY(id_hospital) REFERENCES Hospital(id)
	,ADD CONSTRAINT fk_id_area_atuacao FOREIGN KEY(id_area_atuacao) REFERENCES Area_De_Atuacao(id)

;ALTER TABLE public.Hospital_Funcionario
	 ADD CONSTRAINT fk_id_hospital FOREIGN KEY(id_hospital) REFERENCES Hospital(id)
	,ADD CONSTRAINT fk_id_funcionario FOREIGN KEY(id_funcionario) REFERENCES Funcionario(id)

;ALTER TABLE public.Area_Atuacao_Especializacao
	 ADD CONSTRAINT fk_id_area_atuacao FOREIGN KEY(id_area_atuacao) REFERENCES Area_De_Atuacao(id)
	,ADD CONSTRAINT fk_id_especializacao FOREIGN KEY(id_especializacao) REFERENCES Especializacao(id)

;ALTER TABLE public.Especializacao_Funcionario
	 ADD CONSTRAINT fk_id_funcionario FOREIGN KEY(id_funcionario) REFERENCES Funcionario(id)
	,ADD CONSTRAINT fk_id_especializacao FOREIGN KEY(id_especializacao) REFERENCES Especializacao(id)

;ALTER TABLE public.Agendamento
	 ADD CONSTRAINT fk_id_funcionario FOREIGN KEY(id_funcionario) REFERENCES Funcionario(id)
	,ADD CONSTRAINT fk_id_paciente FOREIGN KEY(id_paciente) REFERENCES Paciente(id)
	,ADD CONSTRAINT fk_id_hospital FOREIGN KEY(id_hospital) REFERENCES Hospital(id)
	,ADD CONSTRAINT fk_id_area_atuacao FOREIGN KEY(id_area_atuacao) REFERENCES Area_De_Atuacao(id)