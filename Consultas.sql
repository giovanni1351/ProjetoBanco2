-- 1) Listar detalhes dos agendamentos, incluindo nomes de funcionário, hospital, paciente e área de atuação.
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



-- 2) Listar funcionários com mais de uma especialização.
SELECT
    f.nome AS Nome_Funcionario,
    COUNT(ef.id_especializacao) AS Quantidade_Especializacoes
FROM public.funcionario f
JOIN public.especializacao_funcionario ef ON f.id = ef.id_funcionario
GROUP BY f.nome
HAVING COUNT(ef.id_especializacao) > 1;


-- 3) Listar todos os funcionários que trabalham em um hospital específico (ex: Hospital com id = 1).
SELECT
    f.nome AS Nome_Funcionario,
    f.idade,
    h.nome AS Nome_Hospital
FROM public.funcionario f
JOIN public.hospital_funcionario hf ON f.id = hf.id_funcionario
JOIN public.hospital h ON hf.id_hospital = h.id
WHERE h.id = 1; -- Substitua 1 pelo ID do hospital desejado


-- 4) Calcular a idade média dos pacientes por sexo.
SELECT
    p.sexo,
    AVG(p.idade) AS Idade_Media
FROM public.paciente p
GROUP BY p.sexo;


-- 5) Calcular o salário médio dos funcionários por especialização.
SELECT
    e.nome AS Nome_Especializacao,
    ROUND(AVG(f.salario)::numeric, 2) AS Salario_Medio
FROM public.funcionario f
JOIN public.especializacao_funcionario ef ON f.id = ef.id_funcionario
JOIN public.especializacao e ON ef.id_especializacao = e.id
GROUP BY e.nome
ORDER BY Salario_Medio DESC;


-- 6) Encontrar a área de atuação com o maior número de agendamentos registrados.
SELECT
    aa.nome AS Area_Atuacao_Mais_Movimentada,
    COUNT(a.id_paciente) AS Total_Agendamentos
FROM public.agendamento a
JOIN public.area_de_atuacao aa ON a.id_area_atuacao = aa.id
GROUP BY aa.nome
ORDER BY Total_Agendamentos DESC
LIMIT 1;


-- 7) Contar o número de especializações distintas oferecidas em cada hospital (com base nos funcionários).
SELECT
    h.nome AS Nome_Hospital,
    COUNT(DISTINCT ef.id_especializacao) AS Numero_Especializacoes_Distintas
FROM public.hospital h
JOIN public.hospital_funcionario hf ON h.id = hf.id_hospital
JOIN public.especializacao_funcionario ef ON hf.id_funcionario = ef.id_funcionario
GROUP BY h.nome
ORDER BY Numero_Especializacoes_Distintas DESC;

-- 8) Quantidade de consultas de pacientes que possuem mais de 90 anos.
SELECT 
    p.nome
     ,COUNT(DISTINCT a.data_consulta) AS QUANTIDADES_DE_CONSULTAS
FROM agendamento a
    INNER JOIN public.paciente p on a.id_paciente = p.id
WHERE p.idade > 90
GROUP BY p.nome;

-- 9) Pacientes que foram atendidos mais do que 5 vez pelo mesmo medico
WITH CTE AS (
    SELECT *,row_number() over (PARTITION BY id_paciente,id_funcionario ORDER BY data_consulta DESC) RN FROM agendamento
)
SELECT * FROM CTE WHERE RN >4


-- 10) Calcular a quantidade média de funcionários por hospital.
SELECT AVG(funcionarios_por_hospital) AS Media_Funcionarios_Por_Hospital
FROM (
    SELECT h.id, COUNT(hf.id_funcionario) AS funcionarios_por_hospital
    FROM public.hospital h
    LEFT JOIN public.hospital_funcionario hf ON h.id = hf.id_hospital
    GROUP BY h.id
) AS contagem_funcionarios;



