# Projeto 2 de banco de dados

# Alunos
 - Giovanni Chahin Morassi 22123025-3
 - Tiago Fagundes 22123017-0
 - Herinque Finatti 22123030-3

# Tema Escolhido: Sistema de Convenio

```mermaid
erDiagram

    Paciente || -- |{ Agendamento : tem 
    Hospital || -- |{ Agendamento : tem 
    Area_De_Atuação || -- |{ Agendamento : tem 
    Funcionários || -- |{ Agendamento : tem 
    Area_De_Atuação || -- |{ Area_Atuacao_Hospital : tem
    Hospital || -- |{ Area_Atuacao_Hospital : tem
    Especializações || -- |{ Especializacoes_Funcionario : tem
    Funcionários || -- |{ Especializacoes_Funcionario : tem
    Hospital || -- |{ hospital_funcionario : tem
    Funcionários || -- |{ hospital_funcionario : tem

    



    Paciente {
        int id pk
        string nome 
        int idade
        date data_nascimento
        
    }

    Agendamento {
        int id_funcionario pk
        int id_funcionario fk
        int id_paciente pk
        int id_paciente fk
        int id_hospital pk
        int id_hospital fk
        int id_area_atuacao pk
        int id_area_atuacao fk
        datetime data_consulta  
        bool agendamento_realizado  

    }

    Funcionários {
        int id pk
        string nome
    }

    Area_De_Atuação {
        int id pk

    }

    Especializações {
        int id pk
        string Descricao
    }

    Hospital {
        int id pk

    }

    Area_Atuacao_Hospital {
        int id_hospital pk
        int id_hospital fk
        int id_Area_Atuacao pk
        int id_Area_Atuacao fk
    }

    Especializacoes_Funcionario {
        int id_funcionario pk
        int id_funcionario fk
        int id_Especializacao pk
        int id_Especializacao fk
    }
    hospital_funcionario {
        int id_funcionario pk
        int id_funcionario fk
        int id_hospital pk
        int id_hospital fk
    }


```


