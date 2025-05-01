-- Listar detalhes dos agendamentos, incluindo nomes de funcionário, hospital, paciente e área de atuação.
SELECT
    a.data_consulta as Data_Consulta,
    f.nome AS Nome_Funcionario,
    h.nome AS Nome_Hospital,
    p.nome AS Nome_Paciente,
    aa.nome AS Nome_Area_Atuacao,
    aa.codigo_area AS Codigo_Area_Atuacao
FROM public.agendamento AS a
LEFT JOIN public.funcionario f ON f.id = a.id_funcionario
LEFT JOIN public.hospital h ON a.id_hospital = h.id
LEFT JOIN public.paciente p ON a.id_paciente = p.id
LEFT JOIN public.area_de_atuacao aa ON a.id_area_atuacao = aa.id;

-- Contar o número de agendamentos por área de atuação em uma data específica (ex: '2024-01-15').
SELECT
    aa.nome AS Area_Atuacao,
    COUNT(a.id_paciente) AS Numero_Agendamentos
FROM public.agendamento a
JOIN public.area_de_atuacao aa ON a.id_area_atuacao = aa.id
WHERE a.data_consulta = '2024-01-15' -- Substitua pela data desejada
GROUP BY aa.nome;

-- Listar agendamentos que ainda não foram realizados.
SELECT
    a.data_consulta as Data_Consulta,
    p.nome AS Nome_Paciente,
    f.nome AS Nome_Funcionario,
    h.nome AS Nome_Hospital,
    aa.nome AS Area_Atuacao
FROM public.agendamento a
JOIN public.paciente p ON a.id_paciente = p.id
JOIN public.funcionario f ON a.id_funcionario = f.id
JOIN public.hospital h ON a.id_hospital = h.id
JOIN public.area_de_atuacao aa ON a.id_area_atuacao = aa.id
WHERE a.agendamento_realizado = FALSE;


-- Listar todos os funcionários e suas especializações.
SELECT
    f.nome AS Nome_Funcionario,
    f.idade,
    f.salario,
    e.nome AS Nome_Especializacao,
    e.descricao AS Descricao_Especializacao
FROM public.funcionario f
INNER JOIN public.especializacao_funcionario ef ON f.id = ef.id_funcionario
INNER JOIN public.especializacao e ON ef.id_especializacao = e.id;

-- Listar funcionários que possuem exatamente 2 especializações.
SELECT
    f.nome,
    COUNT(e.id) AS Numero_Especializacoes
FROM public.especializacao_funcionario ef
LEFT JOIN public.especializacao e ON e.id = ef.id_especializacao
LEFT JOIN public.funcionario f ON f.id = ef.id_funcionario
GROUP BY f.nome
HAVING COUNT(e.id) = 2;

-- Listar funcionários com mais de uma especialização.
SELECT
    f.nome AS Nome_Funcionario,
    COUNT(ef.id_especializacao) AS Quantidade_Especializacoes
FROM public.funcionario f
JOIN public.especializacao_funcionario ef ON f.id = ef.id_funcionario
GROUP BY f.nome
HAVING COUNT(ef.id_especializacao) > 1;

-- Listar funcionários e os hospitais onde trabalham.
SELECT
    f.nome AS Nome_Funcionario,
    h.nome AS Nome_Hospital
FROM public.funcionario f
JOIN public.hospital_funcionario hf ON f.id = hf.id_funcionario
JOIN public.hospital h ON hf.id_hospital = h.id
ORDER BY h.nome, f.nome;

-- Listar todos os funcionários que trabalham em um hospital específico (ex: Hospital com id = 1).
SELECT
    f.nome AS Nome_Funcionario,
    f.idade,
    h.nome AS Nome_Hospital
FROM public.funcionario f
JOIN public.hospital_funcionario hf ON f.id = hf.id_funcionario
JOIN public.hospital h ON hf.id_hospital = h.id
WHERE h.id = 1; -- Substitua 1 pelo ID do hospital desejado


-- Listar áreas de atuação, nome e endereço dos hospitais associados.
SELECT
    ada.nome AS Area_Atuacao,
    h.nome AS Nome_Hospital,
    h.endereco AS Endereco_Hospital
FROM public.area_atuacao_hospital AS aah
LEFT JOIN public.area_de_atuacao ada ON aah.id_area_atuacao = ada.id
LEFT JOIN public.hospital h ON aah.id_hospital = h.id;

-- Listar todos os hospitais e seus respectivos funcionários responsáveis.
SELECT
    h.nome AS Nome_Hospital,
    h.endereco AS Endereco_Hospital,
    f.nome AS Nome_Responsavel
FROM public.hospital h
LEFT JOIN public.funcionario f ON h.id_responsavel = f.id;

-- Listar hospitais e a quantidade de áreas de atuação que eles cobrem, ordenado pela quantidade.
SELECT
    h.nome AS Nome_Hospital,
    COUNT(aah.id_area_atuacao) AS Quantidade_Areas_Atuacao
FROM public.hospital h
LEFT JOIN public.area_atuacao_hospital aah ON h.id = aah.id_hospital
GROUP BY h.nome
ORDER BY Quantidade_Areas_Atuacao DESC;

-- Listar hospitais com avaliação maior que um valor específico (ex: 4) e quantidade de leitos.
SELECT
    h.nome AS Nome_Hospital,
    h.avaliacao,
    h.leitos
FROM public.hospital h
WHERE h.avaliacao > 4 -- Substitua 4 pelo valor de avaliação desejado
ORDER BY h.avaliacao DESC;



-- Listar todas as especializações pertencentes a uma área de atuação específica (ex: Area de Atuação com id = 1).
SELECT
    e.nome AS Nome_Especializacao,
    e.descricao,
    aa.nome AS Area_Atuacao
FROM public.especializacao e
JOIN public.area_atuacao_especializacao aae ON e.id = aae.id_especializacao
JOIN public.area_de_atuacao aa ON aae.id_area_atuacao = aa.id
WHERE aa.id = 1; -- Substitua 1 pelo ID da área de atuação desejada


-- Listar todos os pacientes do sexo feminino com mais de 30 anos.
SELECT
    p.nome AS Nome_Paciente,
    p.idade,
    p.data_nascimento,
    p.cpf
FROM public.paciente p
WHERE p.sexo = 'F' AND p.idade > 30;

-- Calcular a idade média dos pacientes por sexo.
SELECT
    p.sexo,
    AVG(p.idade) AS Idade_Media
FROM public.paciente p
GROUP BY p.sexo;

