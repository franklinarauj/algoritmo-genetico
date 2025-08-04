import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from copy import deepcopy
import json
import time

# Configuração da página
st.set_page_config(
    page_title="Otimizador de Horários - Algoritmo Genético",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dados otimizados para melhor fitness e ocupação (08:00-18:00)
salas = {
    # Salas normais
    1: {"nome": "Sala 101", "capacidade": 40, "tipo": "normal"},
    2: {"nome": "Sala 201", "capacidade": 35, "tipo": "normal"},
    3: {"nome": "Sala 301", "capacidade": 40, "tipo": "normal"},
    4: {"nome": "Sala 401", "capacidade": 45, "tipo": "normal"},
    5: {"nome": "Sala 501", "capacidade": 40, "tipo": "normal"},
    6: {"nome": "Sala 601", "capacidade": 35, "tipo": "normal"},
    7: {"nome": "Sala 701", "capacidade": 40, "tipo": "normal"},
    8: {"nome": "Sala 801", "capacidade": 45, "tipo": "normal"},
    9: {"nome": "Sala 901", "capacidade": 35, "tipo": "normal"},
    10: {"nome": "Sala 1001", "capacidade": 40, "tipo": "normal"},
    11: {"nome": "Sala 1101", "capacidade": 35, "tipo": "normal"},
    12: {"nome": "Sala 1201", "capacidade": 40, "tipo": "normal"},
    # Laboratórios
    13: {"nome": "Lab Física I", "capacidade": 30, "tipo": "laboratório"},
    14: {"nome": "Lab Física II", "capacidade": 35, "tipo": "laboratório"},
    15: {"nome": "Lab Química I", "capacidade": 30, "tipo": "laboratório"},
    16: {"nome": "Lab Química II", "capacidade": 35, "tipo": "laboratório"},
    17: {"nome": "Lab Biologia I", "capacidade": 30, "tipo": "laboratório"},
    18: {"nome": "Lab Biologia II", "capacidade": 35, "tipo": "laboratório"},
    19: {"nome": "Lab Informática", "capacidade": 35, "tipo": "laboratório"},
    20: {"nome": "Lab Robótica", "capacidade": 35, "tipo": "laboratório"},
}

# Professores com preferências ajustadas para os novos horários
professores = {
    # Matemática 1 e 2
    "PROF_JOSE_MAT": {"nome": "José Silva", "preferencias": ["SEG_08H", "TER_09H", "QUA_14H", "QUI_16H"], "disciplinas": ["MAT101", "MAT102"]},
    "PROF_MARIA_MAT": {"nome": "Maria Santos", "preferencias": ["TER_08H", "QUA_10H", "QUI_13H", "SEX_15H"], "disciplinas": ["MAT101", "MAT102"]},
    "PROF_CARLOS_MAT": {"nome": "Carlos Pereira", "preferencias": ["SEG_13H", "QUA_08H", "SEX_10H"], "disciplinas": ["MAT101", "MAT102"]},
    
    # Física 1 e 2
    "PROF_ANTONIO_FIS": {"nome": "Antonio Lima", "preferencias": ["TER_09H", "QUI_08H", "SEX_14H"], "disciplinas": ["FIS201", "FIS202"]},
    "PROF_LUCAS_FIS": {"nome": "Lucas Costa", "preferencias": ["SEG_11H", "QUA_08H", "QUI_15H"], "disciplinas": ["FIS201", "FIS202"]},
    
    # Química 1 e 2
    "PROF_ANA_QUI": {"nome": "Ana Oliveira", "preferencias": ["SEG_09H", "TER_11H", "QUA_13H", "SEX_14H"], "disciplinas": ["QUI301", "QUI302"]},
    "PROF_PEDRO_QUI": {"nome": "Pedro Rodrigues", "preferencias": ["TER_08H", "QUA_10H", "SEX_16H"], "disciplinas": ["QUI301", "QUI302"]},
    
    # Literatura
    "PROF_CARLA_LIT": {"nome": "Carla Fernandes", "preferencias": ["SEG_10H", "TER_14H", "QUA_16H"], "disciplinas": ["LIT401", "LIT402"]},
    "PROF_PAULO_LIT": {"nome": "Paulo Oliveira", "preferencias": ["TER_12H", "QUA_15H", "QUI_09H"], "disciplinas": ["LIT401", "LIT402"]},

    # Lingua Portuguesa
    "PROF_CAMILA_POR": {"nome": "Camila Mendes", "preferencias": ["TER_13H", "QUA_15H", "QUI_09H"], "disciplinas": ["POR403", "POR404"]},
    "PROF_MARCOS_POR": {"nome": "Marcos Souza", "preferencias": ["TER_13H", "QUA_15H", "QUI_09H"], "disciplinas": ["POR403", "POR404"]},
    "PROF_JULIA_POR": {"nome": "Julia Santos", "preferencias": ["TER_08H", "QUI_13H", "SEX_15H"], "disciplinas": ["POR403", "POR404"]},
    
    # História
    "PROF_LUCIA_HIS": {"nome": "Lúcia Almeida", "preferencias": ["SEG_13H", "TER_15H", "QUA_09H"], "disciplinas": ["HIS501", "HIS502"]},
    "PROF_RICARDO_HIS": {"nome": "Ricardo Barbosa", "preferencias": ["TER_16H", "QUI_10H"], "disciplinas": ["HIS501", "HIS502"]},

    # Geografia
    "PROF_SANDRA_GEO": {"nome": "Sandra Castro", "preferencias": ["TER_11H", "QUA_17H"], "disciplinas": ["GEO601", "GEO602"]},
    "PROF_FERNANDO_GEO": {"nome": "Fernando Gomes", "preferencias": ["TER_17H", "QUA_08H", "QUI_11H"], "disciplinas": ["GEO601", "GEO602"]},

    # Economia
    "PROF_LEONARDO_ECO": {"nome": "Leonardo Silva", "preferencias": ["SEG_12H", "TER_14H", "QUA_10H"], "disciplinas": ["ECO701"]},
    "PROF_REGINA_ECO": {"nome": "Regina Costa", "preferencias": ["TER_16H", "QUI_14H"], "disciplinas": ["ECO701"]},

    # Ciências Sociais
    "PROF_SARA_CSS": {"nome": "Sara Martins", "preferencias": ["SEG_10H", "TER_12H", "QUA_14H"], "disciplinas": ["CSS801"]},
    "PROF_FREDERICO_CSS": {"nome": "Frederico Almeida", "preferencias": ["SEG_09H", "TER_11H", "QUA_13H"], "disciplinas": ["CSS801"]},

    # Biologia 1 e 2
    "PROF_BEATRIZ_BIO": {"nome": "Beatriz Ramos", "preferencias": ["SEG_14H", "TER_08H", "QUI_13H"], "disciplinas": ["BIO901", "BIO902"]},
    "PROF_GABRIEL_BIO": {"nome": "Gabriel Pinto", "preferencias": ["TER_14H", "QUA_11H", "SEX_08H"], "disciplinas": ["BIO901", "BIO902"]},
    
    # Inglês e Espanhol
    "PROF_CAMILA_ING": {"nome": "Camila Dias", "preferencias": ["SEG_15H", "QUA_14H", "SEX_10H"], "disciplinas": ["ING011"]},
    "PROF_RAFAEL_ESP": {"nome": "Rafael Monteiro", "preferencias": ["TER_10H", "QUI_08H", "SEX_12H"], "disciplinas": ["ESP012"]},

    # Educação Física
    "PROF_JULIO_EDF": {"nome": "Júlio Santos", "preferencias": ["SEG_16H", "QUA_13H", "SEX_09H"], "disciplinas": ["EDF023"]},
    "PROF_PATRICIA_EDF": {"nome": "Patrícia Lima", "preferencias": ["TER_11H", "QUI_15H", "SEX_11H"], "disciplinas": ["EDF023"]},

    # Filosofia
    "PROF_VANIA_FIL": {"nome": "Vânia Costa", "preferencias": ["SEG_12H", "TER_14H", "QUA_10H"], "disciplinas": ["FIL034"]},
    "PROF_ANDRE_FIL": {"nome": "André Silva", "preferencias": ["TER_16H", "QUI_12H"], "disciplinas": ["FIL034"]},

    # Sociologia
    "PROF_JOMAR_SOC": {"nome": "Jomar Pereira", "preferencias": ["SEG_10H", "TER_12H", "QUA_14H"], "disciplinas": ["SOC035"]},
    "PROF_PRISCILA_SOC": {"nome": "Priscila Rocha", "preferencias": ["SEG_09H", "TER_11H", "QUA_13H"], "disciplinas": ["SOC035"]},
    
    # Arte
    "PROF_RENATA_ART": {"nome": "Renata Moura", "preferencias": ["SEG_11H", "QUA_15H", "SEX_13H"], "disciplinas": ["ART046"]},
    "PROF_ANDREA_ART": {"nome": "André Neves", "preferencias": ["TER_09H", "QUI_17H", "SEX_17H"], "disciplinas": ["ART046"]},
    
    # Tecnologia
    "PROF_ROBERTA_TEC": {"nome": "Roberta Silva", "preferencias": ["SEG_17H", "TER_13H", "QUI_10H"], "disciplinas": ["TEC256"]},
    "PROF_DIEGO_TEC": {"nome": "Diego Cardoso", "preferencias": ["TER_15H", "QUA_17H", "SEX_14H"], "disciplinas": ["TEC256"]},

    # Robótica
    "PROF_ARTHUR_ROB": {"nome": "Arthur Gomes", "preferencias": ["SEG_08H", "TER_10H", "QUI_12H"], "disciplinas": ["ROB512"]},
    "PROF_LEVI_ROB": {"nome": "Levi Martins", "preferencias": ["TER_14H", "QUA_16H", "SEX_15H"], "disciplinas": ["ROB512"]}
}

# Turmas com distribuição mais realista de alunos (máximo 35 por turma), divisão por série e disciplinas
turmas = {
    # Ensino Fundamental II - 6º ano
    "6A": {"alunos": 32, "disciplinas": ["MAT101", "LIT401", "POR403", "HIS501", "GEO601", "ING011", "EDF023"]},
    "6B": {"alunos": 30, "disciplinas": ["MAT101", "LIT401", "POR403", "HIS501", "GEO601", "ING011", "EDF023"]},
    "6C": {"alunos": 31, "disciplinas": ["MAT101", "LIT401", "POR403", "HIS501", "GEO601", "ING011", "EDF023"]},
    
    # Ensino Fundamental II - 7º ano
    "7A": {"alunos": 33, "disciplinas": ["MAT101", "LIT401", "POR403", "HIS501", "GEO601", "ING011", "EDF023", "FIS201", "ART046"]},
    "7B": {"alunos": 32, "disciplinas": ["MAT101", "LIT401", "POR403", "HIS501", "GEO601", "ING011", "EDF023", "FIS201", "ART046"]},
    "7C": {"alunos": 30, "disciplinas": ["MAT101", "LIT401", "POR403", "HIS501", "GEO601", "ING011", "EDF023", "FIS201", "ART046"]},
    
    # Ensino Fundamental II - 8º ano
    "8A": {"alunos": 34, "disciplinas": ["MAT102", "LIT402", "POR404", "HIS502", "GEO602", "ING011", "EDF023", "FIS201", "QUI301", "BIO901"]},
    "8B": {"alunos": 32, "disciplinas": ["MAT102", "LIT402", "POR404", "HIS502", "GEO602", "ING011", "EDF023", "FIS201", "QUI301", "BIO901"]},
    "8C": {"alunos": 31, "disciplinas": ["MAT102", "LIT402", "POR404", "HIS502", "GEO602", "ING011", "EDF023", "FIS201", "QUI301", "BIO901"]},
    
    # Ensino Fundamental II - 9º ano
    "9A": {"alunos": 35, "disciplinas": ["MAT102", "LIT402", "POR404", "HIS502", "GEO602", "ING011", "ESP012", "FIS202", "QUI302", "BIO901", "FIL034"]},
    "9B": {"alunos": 33, "disciplinas": ["MAT102", "LIT402", "POR404", "HIS502", "GEO602", "ING011", "ESP012", "FIS202", "QUI302", "BIO901", "FIL034"]},
    "9C": {"alunos": 32, "disciplinas": ["MAT102", "LIT402", "POR404", "HIS502", "GEO602", "ING011", "ESP012", "FIS202", "QUI302", "BIO901", "FIL034"]},
    
    # Ensino Médio - 1º ano
    "1EM-A": {"alunos": 35, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ING011", "ESP012", "FIL034", "SOC035", "TEC256"]},
    "1EM-B": {"alunos": 34, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ING011", "ESP012", "FIL034", "SOC035", "TEC256"]},
    "1EM-C": {"alunos": 33, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ING011", "ESP012", "FIL034", "SOC035", "TEC256"]},
    
    # Ensino Médio - 2º ano
    "2EM-A": {"alunos": 33, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ING011", "ESP012", "FIL034", "SOC035", "ART046", "ROB512"]},
    "2EM-B": {"alunos": 32, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ING011", "ESP012", "FIL034", "SOC035", "ART046", "ROB512"]},
    
    # Ensino Médio - 3º ano
    "3EM-A": {"alunos": 30, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ECO701", "CSS801", "ING011", "FIL034", "SOC035", "ROB512"]},
    "3EM-B": {"alunos": 28, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ECO701", "CSS801", "ING011", "FIL034", "SOC035", "ROB512"]},
    "3EM-C": {"alunos": 29, "disciplinas": ["MAT102", "LIT402", "POR404", "FIS202", "QUI302", "BIO902", "HIS502", "GEO602", "ECO701", "CSS801", "ING011", "FIL034", "SOC035", "ROB512"]},
}

# Disciplinas com cargas horárias realistas (aulas por semana)
disciplinas = {
    # Matemática
    "MAT101": {"nome": "Matemática I", "carga": 6, "sala_tipo": "normal", "professores": ["PROF_JOSE_MAT", "PROF_MARIA_MAT", "PROF_CARLOS_MAT"]},
    "MAT102": {"nome": "Matemática II", "carga": 6, "sala_tipo": "normal", "professores": ["PROF_JOSE_MAT", "PROF_MARIA_MAT", "PROF_CARLOS_MAT"]},

    # Física
    "FIS201": {"nome": "Física I", "carga": 5, "sala_tipo": "laboratório", "professores": ["PROF_ANTONIO_FIS", "PROF_LUCAS_FIS"]},
    "FIS202": {"nome": "Física II", "carga": 5, "sala_tipo": "laboratório", "professores": ["PROF_ANTONIO_FIS", "PROF_LUCAS_FIS"]},

    # Química
    "QUI301": {"nome": "Química I", "carga": 4, "sala_tipo": "laboratório", "professores": ["PROF_ANA_QUI", "PROF_PEDRO_QUI"]},
    "QUI302": {"nome": "Química II", "carga": 4, "sala_tipo": "laboratório", "professores": ["PROF_ANA_QUI", "PROF_PEDRO_QUI"]},

    # Literatura
    "LIT401": {"nome": "Literatura I", "carga": 3, "sala_tipo": "normal", "professores": ["PROF_CARLA_LIT", "PROF_PAULO_LIT"]},
    "LIT402": {"nome": "Literatura II", "carga": 4, "sala_tipo": "normal", "professores": ["PROF_CARLA_LIT", "PROF_PAULO_LIT"]},

    # Língua Portuguesa
    "POR403": {"nome": "Língua Portuguesa I", "carga": 4, "sala_tipo": "normal", "professores": ["PROF_CAMILA_POR", "PROF_MARCOS_POR", "PROF_JULIA_POR"]},
    "POR404": {"nome": "Língua Portuguesa II", "carga": 4, "sala_tipo": "normal", "professores": ["PROF_CAMILA_POR", "PROF_MARCOS_POR", "PROF_JULIA_POR"]},

    # História
    "HIS501": {"nome": "História I", "carga": 3, "sala_tipo": "normal", "professores": ["PROF_LUCIA_HIS", "PROF_RICARDO_HIS"]},
    "HIS502": {"nome": "História II", "carga": 4, "sala_tipo": "normal", "professores": ["PROF_LUCIA_HIS", "PROF_RICARDO_HIS"]},

    # Geografia
    "GEO601": {"nome": "Geografia I", "carga": 3, "sala_tipo": "normal", "professores": ["PROF_SANDRA_GEO", "PROF_FERNANDO_GEO"]},
    "GEO602": {"nome": "Geografia II", "carga": 4, "sala_tipo": "normal", "professores": ["PROF_SANDRA_GEO", "PROF_FERNANDO_GEO"]},

    # Economia
    "ECO701": {"nome": "Economia Básica", "carga": 2, "sala_tipo": "normal", "professores": ["PROF_LEONARDO_ECO", "PROF_REGINA_ECO"]},

    # Ciências Sociais
    "CSS801": {"nome": "Ciências Sociais", "carga": 2, "sala_tipo": "normal", "professores": ["PROF_SARA_CSS", "PROF_FREDERICO_CSS"]},

    # Biologia
    "BIO901": {"nome": "Biologia I", "carga": 4, "sala_tipo": "laboratório", "professores": ["PROF_BEATRIZ_BIO", "PROF_GABRIEL_BIO"]},
    "BIO902": {"nome": "Biologia II", "carga": 4, "sala_tipo": "laboratório", "professores": ["PROF_BEATRIZ_BIO", "PROF_GABRIEL_BIO"]},

    # Inglês e Espanhol
    "ING011": {"nome": "Inglês", "carga": 2, "sala_tipo": "normal", "professores": ["PROF_CAMILA_ING"]},
    "ESP012": {"nome": "Espanhol", "carga": 2, "sala_tipo": "normal", "professores": ["PROF_RAFAEL_ESP"]},

    # Educação Física
    "EDF023": {"nome": "Educação Física", "carga": 3, "sala_tipo": "normal", "professores": ["PROF_JULIO_EDF", "PROF_PATRICIA_EDF"]},

    # Filosofia e Sociologia
    "FIL034": {"nome": "Filosofia", "carga": 2, "sala_tipo": "normal", "professores": ["PROF_VANIA_FIL", "PROF_ANDRE_FIL"]},
    "SOC035": {"nome": "Sociologia", "carga": 2, "sala_tipo": "normal", "professores": ["PROF_JOMAR_SOC", "PROF_PRISCILA_SOC"]},

    # Artes
    "ART046": {"nome": "Artes", "carga": 2, "sala_tipo": "normal", "professores": ["PROF_RENATA_ART", "PROF_ANDREA_ART"]},

    # Tecnologia e Robótica
    "TEC256": {"nome": "Tecnologia Básica", "carga": 3, "sala_tipo": "laboratório", "professores": ["PROF_ROBERTA_TEC", "PROF_DIEGO_TEC"]},
    "ROB512": {"nome": "Robótica", "carga": 3, "sala_tipo": "laboratório", "professores": ["PROF_ARTHUR_ROB", "PROF_LEVI_ROB"]},
}

# Configurações do sistema
DIAS = ["SEG", "TER", "QUA", "QUI", "SEX"]
HORARIOS = ["08:00", "08:50", "09:40", "10:30", "11:20", "13:00", "13:50", "14:40", "15:30", "16:20", "17:10"]
SALAS_IDS = list(range(1, 21))  # 20 salas

# Horário de almoço (não alocar aulas)
HORARIO_ALMOCO = "12:10"

# Funções auxiliares
def criar_cronograma_base():
    """Cria lista base de aulas que precisam ser alocadas"""
    aulas = []
    for turma_id, turma_info in turmas.items():
        for disciplina_id in turma_info['disciplinas']:
            carga_horaria = disciplinas[disciplina_id]['carga']
            
            professores_disponiveis = disciplinas[disciplina_id].get('professores', [])
            
            if not professores_disponiveis:
                professores_disponiveis = [
                    prof_id for prof_id, prof_info in professores.items()
                    if disciplina_id in prof_info['disciplinas']
                ]
            
            for _ in range(carga_horaria):
                aulas.append({
                    'turma': turma_id,
                    'disciplina': disciplina_id,
                    'professores_possiveis': professores_disponiveis
                })
    
    return aulas

def criar_cromossomo_vazio():
    """Cria um cromossomo vazio (todas as posições sem aulas)"""
    cromossomo = {}
    for dia in DIAS:
        for horario in HORARIOS:
            for sala_id in SALAS_IDS:
                cromossomo[(dia, horario, sala_id)] = None
    return cromossomo

def validar_cromossomo(slots):
    """Valida um cromossomo e retorna lista de erros"""
    erros = []
    for dia in DIAS:
        for horario in HORARIOS:
            professores_horario = {}
            turmas_horario = {}
            
            for sala_id in SALAS_IDS:
                slot_key = (dia, horario, sala_id)
                if slot_key in slots and slots[slot_key] is not None:
                    aula = slots[slot_key]
                    prof = aula['professor']
                    turma = aula['turma']
                    
                    if prof in professores_horario:
                        erros.append(f"Professor {prof} em conflito no {dia} às {horario}")
                    else:
                        professores_horario[prof] = sala_id
                    
                    if turma in turmas_horario:
                        erros.append(f"Turma {turma} em conflito no {dia} às {horario}")
                    else:
                        turmas_horario[turma] = sala_id
    
    return erros

def calcular_fitness_otimizado(slots):
    """Calcula o fitness de um cromossomo (valores mais realistas)"""
    fitness = 1000  # base inicial positiva

    # Penalizar conflitos (mais severo)
    erros = validar_cromossomo(slots)
    fitness -= len(erros) * 200  # aumentado de 100

    # Verificar cobertura de carga horária
    aulas_alocadas = {}
    for slot_key, aula in slots.items():
        if aula is not None:
            key = (aula['turma'], aula['disciplina'])
            aulas_alocadas[key] = aulas_alocadas.get(key, 0) + 1

    for turma_id, turma_info in turmas.items():
        for disciplina_id in turma_info['disciplinas']:
            carga_necessaria = disciplinas[disciplina_id]['carga']
            carga_alocada = aulas_alocadas.get((turma_id, disciplina_id), 0)

            # bônus proporcional à cobertura correta
            if carga_alocada == carga_necessaria:
                fitness += 50  # bônus completo
            elif carga_alocada < carga_necessaria:
                fitness += (carga_alocada / carga_necessaria) * 30
                fitness -= (carga_necessaria - carga_alocada) * 15
            else:
                fitness -= (carga_alocada - carga_necessaria) * 25

    # Avaliar qualidade das alocações
    for slot_key, aula in slots.items():
        if aula is not None:
            dia, horario, sala_id = slot_key
            turma_id = aula['turma']
            prof_id = aula['professor']
            disc_id = aula['disciplina']

            # Verificar capacidade
            capacidade_sala = salas[sala_id]['capacidade']
            alunos_turma = turmas[turma_id]['alunos']

            if alunos_turma <= capacidade_sala:
                # Bônus proporcional ao ajuste de capacidade
                margem = (capacidade_sala - alunos_turma) / capacidade_sala
                if margem < 0.3:  # ajuste perfeito
                    fitness += 8
                elif margem < 0.5:  # bom ajuste
                    fitness += 5
                else:  # sala muito grande
                    fitness += 2
            else:
                # Penalidade proporcional ao excesso
                excesso = (alunos_turma - capacidade_sala) / alunos_turma
                fitness -= 50 * (1 + excesso)

            # Verificar tipo de sala
            tipo_necessario = disciplinas[disc_id]['sala_tipo']
            tipo_sala = salas[sala_id]['tipo']

            if tipo_necessario == 'laboratório' and tipo_sala != 'laboratório':
                fitness -= 40
            elif tipo_necessario == tipo_sala:
                fitness += 15

            # Verificar preferências do professor (corrigido)
            hora_sem_minutos = horario.split(':')[0]
            # Remover o zero à esquerda se houver
            if hora_sem_minutos.startswith('0'):
                hora_sem_minutos = hora_sem_minutos[1:]
            
            pref_horario = f"{dia}_{hora_sem_minutos}H"
            
            # Verificar todas as variações possíveis
            preferencias_prof = professores[prof_id]['preferencias']
            preferencia_atendida = False
            
            for pref in preferencias_prof:
                if pref == pref_horario:
                    preferencia_atendida = True
                    break
                # Também verificar com zero à esquerda
                if pref == f"{dia}_0{hora_sem_minutos}H" and len(hora_sem_minutos) == 1:
                    preferencia_atendida = True
                    break
            
            if preferencia_atendida:
                fitness += 40  # aumentado de 30

            # Verificar se professor leciona a disciplina
            if disc_id not in professores[prof_id]['disciplinas']:
                fitness -= 100

    # Bônus por distribuição equilibrada ao longo do dia
    aulas_por_horario = {}
    for slot_key, aula in slots.items():
        if aula is not None:
            _, horario, _ = slot_key
            aulas_por_horario[horario] = aulas_por_horario.get(horario, 0) + 1
    
    # Penalizar horários muito vazios ou muito cheios
    for horario in HORARIOS:
        qtd = aulas_por_horario.get(horario, 0)
        ideal = len(SALAS_IDS) * len(DIAS) * 0.6  # 60% de ocupação ideal
        
        if qtd > 0:
            desvio = abs(qtd - ideal) / ideal
            if desvio < 0.2:
                fitness += 5
            elif desvio > 0.5:
                fitness -= 10

    return max(0, fitness)

def teria_conflito_otimizado(cromossomo, slot_key, turma_id, prof_id):
    """Verifica se haveria conflito ao adicionar uma aula"""
    dia, horario, _ = slot_key
    
    for sala_id in SALAS_IDS:
        check_slot = (dia, horario, sala_id)
        if check_slot in cromossomo and cromossomo[check_slot] is not None:
            aula_existente = cromossomo[check_slot]
            if (aula_existente['professor'] == prof_id or 
                aula_existente['turma'] == turma_id):
                return True
    
    return False

def gerar_cromossomo_inteligente():
    """Gera um cromossomo inicial usando heurísticas"""
    cromossomo = criar_cromossomo_vazio()
    aulas_para_alocar = criar_cronograma_base()
    
    random.shuffle(aulas_para_alocar)
    
    for aula_info in aulas_para_alocar:
        turma_id = aula_info['turma']
        disciplina_id = aula_info['disciplina']
        professores_possiveis = aula_info['professores_possiveis']
        
        if not professores_possiveis:
            continue
            
        professor_id = random.choice(professores_possiveis)
        
        alunos_turma = turmas[turma_id]['alunos']
        tipo_sala_necessario = disciplinas[disciplina_id]['sala_tipo']
        
        # Encontrar salas adequadas
        salas_adequadas = []
        for sala_id, sala_info in salas.items():
            if (sala_info['capacidade'] >= alunos_turma and
                (tipo_sala_necessario != 'laboratório' or sala_info['tipo'] == 'laboratório')):
                salas_adequadas.append(sala_id)
        
        if not salas_adequadas:
            salas_adequadas = list(salas.keys())
        
        alocado = False
        
        # Tentar alocar em horários preferenciais
        slots_preferenciais = []
        for pref in professores[professor_id]['preferencias']:
            try:
                dia, horario_pref = pref.split('_')
                # Remover o 'H' e adicionar ':00'
                hora = horario_pref.replace('H', '')
                # Adicionar zero à esquerda se necessário
                if len(hora) == 1:
                    hora = '0' + hora
                elif len(hora) == 2 and not hora.startswith('0'):
                    if int(hora) < 10:
                        hora = '0' + hora
                
                horario = hora + ':00'
                
                if horario in HORARIOS:
                    for sala_id in salas_adequadas:
                        slots_preferenciais.append((dia, horario, sala_id))
            except:
                continue
        
        random.shuffle(slots_preferenciais)
        
        for slot_key in slots_preferenciais:
            if slot_key in cromossomo and cromossomo[slot_key] is None:
                if not teria_conflito_otimizado(cromossomo, slot_key, turma_id, professor_id):
                    cromossomo[slot_key] = {
                        'turma': turma_id,
                        'professor': professor_id,
                        'disciplina': disciplina_id
                    }
                    alocado = True
                    break
        
        # Se não conseguiu alocar em preferencial, tentar aleatório
        if not alocado:
            tentativas = 0
            max_tentativas = 100
            
            while tentativas < max_tentativas and not alocado:
                dia = random.choice(DIAS)
                horario = random.choice(HORARIOS)
                sala_id = random.choice(salas_adequadas)
                slot_key = (dia, horario, sala_id)
                
                if slot_key in cromossomo and cromossomo[slot_key] is None:
                    if not teria_conflito_otimizado(cromossomo, slot_key, turma_id, professor_id):
                        cromossomo[slot_key] = {
                            'turma': turma_id,
                            'professor': professor_id,
                            'disciplina': disciplina_id
                        }
                        alocado = True
                
                tentativas += 1
    
    return cromossomo

def analisar_cromossomo_detalhado(cromossomo):
    """Análise detalhada de um cromossomo"""
    erros = validar_cromossomo(cromossomo)
    fitness = calcular_fitness_otimizado(cromossomo)

    slots_ocupados = sum(1 for slot in cromossomo.values() if slot is not None)
    total_slots = len(cromossomo)

    # Contar aulas por turma/disciplina
    aulas_por_turma = {}
    for aula in cromossomo.values():
        if aula is not None:
            key = (aula['turma'], aula['disciplina'])
            aulas_por_turma[key] = aulas_por_turma.get(key, 0) + 1

    # Calcular cobertura
    cobertura_total = 0
    aulas_necessarias_total = 0

    for turma_id, turma_info in turmas.items():
        for disciplina_id in turma_info['disciplinas']:
            carga_necessaria = disciplinas[disciplina_id]['carga']
            carga_atual = aulas_por_turma.get((turma_id, disciplina_id), 0)

            cobertura_total += min(carga_atual, carga_necessaria)
            aulas_necessarias_total += carga_necessaria

    cobertura_percentual = (cobertura_total / aulas_necessarias_total) * 100 if aulas_necessarias_total > 0 else 0

    # Análise de problemas
    problemas_capacidade = 0
    problemas_tipo_sala = 0
    preferencias_atendidas = 0

    for slot_key, aula in cromossomo.items():
        if aula is not None:
            dia, horario, sala_id = slot_key
            turma_id = aula['turma']
            prof_id = aula['professor']
            disc_id = aula['disciplina']

            if turmas[turma_id]['alunos'] > salas[sala_id]['capacidade']:
                problemas_capacidade += 1

            if (disciplinas[disc_id]['sala_tipo'] == 'laboratório' and 
                salas[sala_id]['tipo'] != 'laboratório'):
                problemas_tipo_sala += 1

            hora_sem_minutos = horario.split(':')[0]
            pref_horario = f"{dia}_{hora_sem_minutos}H"
            if pref_horario in professores[prof_id]['preferencias']:
                preferencias_atendidas += 1

    return {
        'fitness': fitness,
        'conflitos': len(erros),
        'ocupacao': slots_ocupados / total_slots,
        'cobertura': cobertura_percentual,
        'problemas_capacidade': problemas_capacidade,
        'problemas_tipo_sala': problemas_tipo_sala,
        'preferencias_atendidas': preferencias_atendidas,
        'slots_ocupados': slots_ocupados,
        'total_slots': total_slots,
        'aulas_por_turma': aulas_por_turma
    }

def calcular_estatisticas_base():
    """Calcula estatísticas básicas do sistema"""
    total_aulas = 0
    for turma_info in turmas.values():
        for disciplina_id in turma_info['disciplinas']:
            total_aulas += disciplinas[disciplina_id]['carga']
    
    # Ajustado para considerar todos os slots disponíveis
    slots_disponiveis = len(DIAS) * len(HORARIOS) * len(SALAS_IDS)
    taxa_ocupacao_ideal = (total_aulas / slots_disponiveis) * 100
    
    return {
        'total_aulas': total_aulas,
        'slots_disponiveis': slots_disponiveis,
        'taxa_ocupacao': taxa_ocupacao_ideal
    }

# Classe para o Algoritmo Genético
class AlgoritmoGenetico:
    def __init__(self, tamanho_populacao, taxa_mutacao, taxa_cruzamento, elitismo):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_cruzamento = taxa_cruzamento
        self.elitismo = elitismo
        self.populacao = []
        self.melhor_individuo = None
        self.melhor_fitness = -float('inf')
        self.historico_fitness = []
        self.geracao_atual = 0
        
    def criar_populacao_inicial(self):
        """Cria a população inicial de cromossomos"""
        self.populacao = []
        for i in range(self.tamanho_populacao):
            cromossomo = gerar_cromossomo_inteligente()
            fitness = calcular_fitness_otimizado(cromossomo)
            self.populacao.append({
                'cromossomo': cromossomo,
                'fitness': fitness
            })
            
            # Atualizar melhor indivíduo
            if fitness > self.melhor_fitness:
                self.melhor_fitness = fitness
                self.melhor_individuo = deepcopy(cromossomo)
        
        # Ordenar população por fitness
        self.populacao.sort(key=lambda x: x['fitness'], reverse=True)
        
    def selecao_torneio(self, tamanho_torneio=3):
        """Seleção por torneio"""
        torneio = random.sample(self.populacao, tamanho_torneio)
        return max(torneio, key=lambda x: x['fitness'])
    
    def crossover(self, pai1, pai2):
        """Operador de cruzamento uniforme"""
        filho = criar_cromossomo_vazio()
        
        for slot_key in filho.keys():
            # 50% de chance de herdar de cada pai
            if random.random() < 0.5:
                filho[slot_key] = deepcopy(pai1['cromossomo'][slot_key])
            else:
                filho[slot_key] = deepcopy(pai2['cromossomo'][slot_key])
        
        # Reparar conflitos após crossover
        self.reparar_conflitos(filho)
        
        return filho
    
    def mutacao(self, cromossomo):
        """Operador de mutação"""
        cromossomo_mutado = deepcopy(cromossomo)
        
        # Número de genes a mutar
        num_mutacoes = max(1, int(len(cromossomo) * self.taxa_mutacao))
        
        for _ in range(num_mutacoes):
            # Escolher slot aleatório
            slot_key = random.choice(list(cromossomo_mutado.keys()))
            
            # 50% de chance de remover ou adicionar aula
            if random.random() < 0.5 and cromossomo_mutado[slot_key] is not None:
                # Remover aula
                cromossomo_mutado[slot_key] = None
            else:
                # Tentar adicionar nova aula
                aulas_base = criar_cronograma_base()
                if aulas_base:
                    aula_aleatoria = random.choice(aulas_base)
                    if aula_aleatoria['professores_possiveis']:
                        professor = random.choice(aula_aleatoria['professores_possiveis'])
                        
                        # Verificar se não há conflito
                        if not teria_conflito_otimizado(cromossomo_mutado, slot_key, 
                                                       aula_aleatoria['turma'], professor):
                            cromossomo_mutado[slot_key] = {
                                'turma': aula_aleatoria['turma'],
                                'professor': professor,
                                'disciplina': aula_aleatoria['disciplina']
                            }
        
        return cromossomo_mutado
    
    def reparar_conflitos(self, cromossomo):
        """Repara conflitos básicos no cromossomo"""
        # Detectar e remover conflitos de professor e turma
        for dia in DIAS:
            for horario in HORARIOS:
                professores_horario = {}
                turmas_horario = {}
                
                for sala_id in SALAS_IDS:
                    slot_key = (dia, horario, sala_id)
                    if slot_key in cromossomo and cromossomo[slot_key] is not None:
                        aula = cromossomo[slot_key]
                        prof = aula['professor']
                        turma = aula['turma']
                        
                        # Verificar conflito de professor
                        if prof in professores_horario:
                            # Remover aula conflitante
                            cromossomo[slot_key] = None
                        else:
                            professores_horario[prof] = sala_id
                        
                        # Verificar conflito de turma
                        if turma in turmas_horario:
                            # Remover aula conflitante
                            cromossomo[slot_key] = None
                        else:
                            turmas_horario[turma] = sala_id
    
    def evoluir_geracao(self):
        """Evolui uma geração"""
        nova_populacao = []
        
        # Elitismo - manter os melhores indivíduos
        num_elite = int(self.tamanho_populacao * self.elitismo)
        for i in range(num_elite):
            nova_populacao.append(deepcopy(self.populacao[i]))
        
        # Gerar resto da população
        while len(nova_populacao) < self.tamanho_populacao:
            # Seleção
            pai1 = self.selecao_torneio()
            pai2 = self.selecao_torneio()
            
            # Crossover
            if random.random() < self.taxa_cruzamento:
                filho = self.crossover(pai1, pai2)
            else:
                filho = deepcopy(pai1['cromossomo'])
            
            # Mutação
            if random.random() < self.taxa_mutacao:
                filho = self.mutacao(filho)
            
            # Calcular fitness
            fitness = calcular_fitness_otimizado(filho)
            
            nova_populacao.append({
                'cromossomo': filho,
                'fitness': fitness
            })
            
            # Atualizar melhor indivíduo
            if fitness > self.melhor_fitness:
                self.melhor_fitness = fitness
                self.melhor_individuo = deepcopy(filho)
        
        # Atualizar população
        self.populacao = nova_populacao
        self.populacao.sort(key=lambda x: x['fitness'], reverse=True)
        
        # Registrar histórico
        self.historico_fitness.append(self.melhor_fitness)
        self.geracao_atual += 1
        
        # Retornar estatísticas da geração
        fitness_medio = sum(ind['fitness'] for ind in self.populacao) / len(self.populacao)
        fitness_min = min(ind['fitness'] for ind in self.populacao)
        fitness_max = max(ind['fitness'] for ind in self.populacao)
        
        return {
            'geracao': self.geracao_atual,
            'melhor_fitness': self.melhor_fitness,
            'fitness_medio': fitness_medio,
            'fitness_min': fitness_min,
            'fitness_max': fitness_max
        }

# Header
st.title("🎓 Otimizador de Horários Escolares")
st.markdown("### Algoritmo Genético - Período Integral (08:00-18:00) - Aulas de 50 minutos")
st.markdown("---")

# Sidebar para configurações
st.sidebar.header("⚙️ Configurações do Algoritmo")

tamanho_populacao = st.sidebar.slider("Tamanho da População", 50, 300, 100, 10)
max_geracoes = st.sidebar.slider("Máximo de Gerações", 50, 500, 200, 10)
taxa_mutacao = st.sidebar.slider("Taxa de Mutação", 0.01, 0.5, 0.1, 0.01)
taxa_cruzamento = st.sidebar.slider("Taxa de Cruzamento", 0.5, 1.0, 0.8, 0.05)
elitismo = st.sidebar.slider("Taxa de Elitismo", 0.05, 0.4, 0.2, 0.05)

st.sidebar.markdown("---")

# Informações do problema
estatisticas = calcular_estatisticas_base()

with st.expander("📊 Informações do Sistema Expandido", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Turmas", len(turmas))
    with col2:
        st.metric("Professores", len(professores))
    with col3:
        st.metric("Salas", len(salas))
    with col4:
        st.metric("Aulas Necessárias", estatisticas['total_aulas'])
    
    # Informações adicionais
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Slots Disponíveis", estatisticas['slots_disponiveis'])
    with col6:
        st.metric("Aulas/Dia", len(HORARIOS))
    with col7:
        st.metric("Laboratórios", len([s for s in salas.values() if s['tipo'] == 'laboratório']))
    with col8:
        st.metric("Taxa Ocupação Ideal", f"{estatisticas['taxa_ocupacao']:.1f}%")
    
    st.info("💡 **Observação:** Intervalo de almoço das 12:10 às 13:00 (sem aulas neste período)")

# Estado da aplicação
if 'ag_running' not in st.session_state:
    st.session_state.ag_running = False
if 'ag_instance' not in st.session_state:
    st.session_state.ag_instance = None
if 'resultados' not in st.session_state:
    st.session_state.resultados = None

# Botões de controle
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Executar Otimização", type="primary", disabled=st.session_state.ag_running):
        st.session_state.ag_running = True
        st.session_state.ag_instance = AlgoritmoGenetico(
            tamanho_populacao=tamanho_populacao,
            taxa_mutacao=taxa_mutacao,
            taxa_cruzamento=taxa_cruzamento,
            elitismo=elitismo
        )

with col2:
    if st.button("⏸️ Pausar", disabled=not st.session_state.ag_running):
        st.session_state.ag_running = False

with col3:
    if st.button("🔄 Resetar"):
        st.session_state.ag_running = False
        st.session_state.ag_instance = None
        st.session_state.resultados = None
        st.rerun()

# Executar algoritmo genético
if st.session_state.ag_running and st.session_state.ag_instance is not None:
    ag = st.session_state.ag_instance
    
    # Progress bar e status
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Placeholder para métricas em tempo real
    metrics_placeholder = st.empty()
    chart_placeholder = st.empty()
    
    # Inicializar população se necessário
    if ag.geracao_atual == 0:
        status_text.text("Inicializando população...")
        ag.criar_populacao_inicial()
        analise_inicial = analisar_cromossomo_detalhado(ag.melhor_individuo)
    
    # Container para histórico de fitness
    historico_stats = {
        'Geração': [],
        'Melhor Fitness': [],
        'Fitness Médio': [],
        'Fitness Mínimo': []
    }
    
    # Executar gerações
    while ag.geracao_atual < max_geracoes and st.session_state.ag_running:
        # Evoluir geração
        stats = ag.evoluir_geracao()
        
        # Atualizar progress bar
        progress = int((ag.geracao_atual / max_geracoes) * 100)
        progress_bar.progress(progress)
        status_text.text(f"Geração {ag.geracao_atual}/{max_geracoes} - Fitness: {stats['melhor_fitness']:.1f}")
        
        # Atualizar histórico
        historico_stats['Geração'].append(stats['geracao'])
        historico_stats['Melhor Fitness'].append(stats['melhor_fitness'])
        historico_stats['Fitness Médio'].append(stats['fitness_medio'])
        historico_stats['Fitness Mínimo'].append(stats['fitness_min'])
        
        # Atualizar métricas em tempo real
        with metrics_placeholder.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Melhor Fitness", f"{stats['melhor_fitness']:.1f}")
            with col2:
                st.metric("Fitness Médio", f"{stats['fitness_medio']:.1f}")
            with col3:
                st.metric("Geração", f"{ag.geracao_atual}")
            with col4:
                delta = stats['melhor_fitness'] - stats['fitness_medio']
                st.metric("Diversidade", f"{delta:.1f}")
        
        # Atualizar gráfico
        if len(historico_stats['Geração']) > 1:
            df_historico = pd.DataFrame(historico_stats)
            fig = px.line(df_historico, 
                        x='Geração', 
                        y=['Melhor Fitness', 'Fitness Médio', 'Fitness Mínimo'],
                        title="Evolução do Fitness ao Longo das Gerações")
            fig.update_layout(height=400, yaxis_title="Fitness")
            chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        # Pequena pausa para visualização
        time.sleep(0.01)
    
    # Finalizar execução
    if ag.geracao_atual >= max_geracoes:
        progress_bar.progress(100)
        status_text.text("✅ Otimização concluída!")
        st.session_state.ag_running = False
        
        # Salvar resultados
        st.session_state.resultados = {
            'melhor_cromossomo': ag.melhor_individuo,
            'melhor_fitness': ag.melhor_fitness,
            'historico': ag.historico_fitness,
            'analise_final': analisar_cromossomo_detalhado(ag.melhor_individuo)
        }

# Exibir resultados se disponíveis
if st.session_state.resultados is not None:
    resultados = st.session_state.resultados
    analise_final = resultados['analise_final']
    melhor_cromossomo = resultados['melhor_cromossomo']
    
    st.success("🎉 Otimização concluída com sucesso!")
    
    # Resultados
    st.markdown("## 📈 Resultados da Otimização")
    
    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Fitness Final", f"{analise_final['fitness']:.1f}")
    
    with col2:
        st.metric("Conflitos", analise_final['conflitos'])
    
    with col3:
        st.metric("Cobertura", f"{analise_final['cobertura']:.1f}%")
    
    with col4:
        st.metric("Preferências", analise_final['preferencias_atendidas'])
    
    with col5:
        st.metric("Ocupação", f"{analise_final['ocupacao']*100:.1f}%")
    
    # Gráfico de evolução final
    st.markdown("### 📊 Evolução do Fitness")
    
    df_fitness = pd.DataFrame({
        'Geração': range(len(resultados['historico'])),
        'Fitness': resultados['historico']
    })
    
    fig = px.line(df_fitness, x='Geração', y='Fitness', 
                    title="Evolução do Melhor Fitness ao Longo das Gerações")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de análise detalhada
    st.markdown("### 📋 Análise Detalhada")
    
    analise_data = {
        'Métrica': ['Fitness', 'Conflitos', 'Ocupação (%)', 'Cobertura (%)', 
                    'Prob. Capacidade', 'Prob. Tipo Sala', 'Preferências OK',
                    'Slots Ocupados', 'Total Slots'],
        'Valor': [
            f"{analise_final['fitness']:.1f}",
            str(analise_final['conflitos']),
            f"{analise_final['ocupacao']*100:.1f}",
            f"{analise_final['cobertura']:.1f}",
            str(analise_final['problemas_capacidade']),
            str(analise_final['problemas_tipo_sala']),
            str(analise_final['preferencias_atendidas']),
            str(analise_final['slots_ocupados']),
            str(analise_final['total_slots'])
        ]
    }
    
    df_analise = pd.DataFrame(analise_data)
    st.dataframe(df_analise, use_container_width=True)
    
    # Cronograma visual
    st.markdown("### 📅 Cronograma Otimizado")
    
    # Criar dataframe para o cronograma
    cronograma_data = []
    for slot_key, aula in melhor_cromossomo.items():
        if aula is not None:
            dia, horario, sala_id = slot_key
                       
            # Verificar problemas
            hora_sem_minutos = horario.split(':')[0]
            # Remover o zero à esquerda se houver
            if hora_sem_minutos.startswith('0'):
                hora_sem_minutos = hora_sem_minutos[1:]

            pref_horario = f"{dia}_{hora_sem_minutos}H"

            # Verificar todas as variações possíveis
            tem_preferencia = False
            for pref in professores[aula['professor']]['preferencias']:
                if pref == pref_horario or (pref == f"{dia}_0{hora_sem_minutos}H" and len(hora_sem_minutos) == 1):
                    tem_preferencia = True
                    break

            problema_cap = turmas[aula['turma']]['alunos'] > salas[sala_id]['capacidade']
            problema_sala = (disciplinas[aula['disciplina']]['sala_tipo'] == 'laboratório' 
                            and salas[sala_id]['tipo'] != 'laboratório')
            
            cronograma_data.append({
                'Dia': dia,
                'Horário': horario,
                'Sala': salas[sala_id]['nome'],
                'Turma': aula['turma'],
                'Disciplina': disciplinas[aula['disciplina']]['nome'],
                'Professor': professores[aula['professor']]['nome'],
                'Preferência': "✓" if tem_preferencia else "",
                'Problemas': "⚠️" if (problema_cap or problema_sala) else "Nenhum"
            })
    
    if cronograma_data:
        df_cronograma = pd.DataFrame(cronograma_data)
        
        # Filtros para o cronograma
        col1, col2, col3 = st.columns(3)
        with col1:
            dias_selecionados = st.multiselect("Filtrar por dia:", DIAS, default=DIAS)
        with col2:
            def format_horario(h):
                inicio = h
                h_split = h.split(':')
                minutos_inicio = int(h_split[0]) * 60 + int(h_split[1])
                minutos_fim = minutos_inicio + 50
                hora_fim = minutos_fim // 60
                min_fim = minutos_fim % 60
                return f"{inicio} - {hora_fim:02d}:{min_fim:02d}"
            
            horarios_selecionados = st.multiselect(
                "Filtrar por horário:", 
                HORARIOS, 
                default=HORARIOS[:5],  # Mostrar só manhã por padrão
                format_func=format_horario
            )
        with col3:
            turmas_unicas = sorted(set(item['Turma'] for item in cronograma_data))
            turmas_selecionadas = st.multiselect("Filtrar por turma:", turmas_unicas, 
                                                default=turmas_unicas[:5])
        
        # Aplicar filtros
        df_filtrado = df_cronograma[
            (df_cronograma['Dia'].isin(dias_selecionados)) &
            (df_cronograma['Horário'].isin(horarios_selecionados)) &
            (df_cronograma['Turma'].isin(turmas_selecionadas))
        ]
        
        st.dataframe(df_filtrado, use_container_width=True, height=400)
        
        # Tabs para diferentes visualizações        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Ocupação", "🔥 Mapa de Calor", 
                                        "📚 Por Disciplina", "👨‍🏫 Por Professor", 
                                        "📊 Análise do Sistema"])
        
        with tab1:
            # Gráfico de ocupação por horário
            ocupacao_por_horario = df_cronograma.groupby('Horário').size().reset_index(name='Aulas')
            ocupacao_por_horario['Capacidade'] = len(SALAS_IDS) * len(DIAS)
            ocupacao_por_horario['Ocupação (%)'] = (ocupacao_por_horario['Aulas'] / 
                                                    ocupacao_por_horario['Capacidade']) * 100
            
            fig_ocupacao = px.bar(
                ocupacao_por_horario, 
                x='Horário', 
                y='Ocupação (%)',
                title="Taxa de Ocupação por Horário",
                text='Ocupação (%)'
            )
            fig_ocupacao.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_ocupacao.update_layout(height=400, yaxis_range=[0, 100])
            st.plotly_chart(fig_ocupacao, use_container_width=True)
        
        with tab2:
            # Mapa de calor do cronograma
            heatmap_data = []
            dias_ordenados = DIAS.copy()  # Manter a ordem original
            
            for dia in dias_ordenados:
                row_data = []
                for horario in HORARIOS:
                    aulas_neste_slot = len([
                        aula for slot_key, aula in melhor_cromossomo.items()
                        if aula is not None and slot_key[0] == dia and slot_key[1] == horario
                    ])
                    row_data.append(aulas_neste_slot)
                heatmap_data.append(row_data)
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=heatmap_data,
                x=HORARIOS,
                y=dias_ordenados,  # Usar a lista ordenada
                colorscale='Blues',
                text=heatmap_data,
                texttemplate="%{text}",
                textfont={"size": 12},
                hovertemplate='Dia: %{y}<br>Horário: %{x}<br>Aulas: %{z}<extra></extra>'
            ))
            
            fig_heatmap.update_layout(
                title="Ocupação por Dia e Horário",
                xaxis_title="Horário",
                yaxis_title="Dia da Semana",
                height=400,
                yaxis=dict(autorange='reversed')  # Isso garante que SEG apareça no topo
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with tab3:
            # Análise por disciplina
            disciplinas_stats = []
            for disc_id, disc_info in disciplinas.items():
                aulas_alocadas = sum(1 for aula in melhor_cromossomo.values() 
                                    if aula is not None and aula['disciplina'] == disc_id)
                
                turmas_disciplina = [t for t, info in turmas.items() 
                                    if disc_id in info['disciplinas']]
                
                carga_total_necessaria = len(turmas_disciplina) * disc_info['carga']
                
                disciplinas_stats.append({
                    'Disciplina': disc_info['nome'],
                    'Tipo Sala': disc_info['sala_tipo'],
                    'Carga/Turma': disc_info['carga'],
                    'Turmas': len(turmas_disciplina),
                    'Total Necessário': carga_total_necessaria,
                    'Alocadas': aulas_alocadas,
                    'Cobertura (%)': (aulas_alocadas / carga_total_necessaria * 100) 
                                    if carga_total_necessaria > 0 else 0
                })
            
            df_disciplinas = pd.DataFrame(disciplinas_stats)
            df_disciplinas = df_disciplinas.sort_values('Cobertura (%)', ascending=False)
            
            # Gráfico de cobertura
            fig_cobertura = px.bar(
                df_disciplinas.sort_values('Cobertura (%)', ascending=True),
                x='Cobertura (%)',
                y='Disciplina',
                orientation='h',
                title="Cobertura da Carga Horária por Disciplina",
                color='Cobertura (%)',
                color_continuous_scale='RdYlGn',
                range_color=[0, 100]
            )
            fig_cobertura.update_layout(height=600)
            st.plotly_chart(fig_cobertura, use_container_width=True)
            
            # Tabela detalhada
            st.dataframe(df_disciplinas, use_container_width=True)
        
        with tab4:
            # Análise por professor
            prof_stats = []
            for prof_id, prof_info in professores.items():
                aulas_prof = [aula for aula in melhor_cromossomo.values() 
                            if aula is not None and aula['professor'] == prof_id]
                
                prefs_atendidas = 0
                for slot_key, aula in melhor_cromossomo.items():
                    if aula is not None and aula['professor'] == prof_id:
                        dia, horario, _ = slot_key
                        hora_sem_minutos = horario.split(':')[0]
                        # Remover o zero à esquerda se houver
                        if hora_sem_minutos.startswith('0'):
                            hora_sem_minutos = hora_sem_minutos[1:]
                        
                        pref_horario = f"{dia}_{hora_sem_minutos}H"
                        
                        # Verificar todas as variações possíveis
                        for pref in prof_info['preferencias']:
                            if pref == pref_horario or (pref == f"{dia}_0{hora_sem_minutos}H" and len(hora_sem_minutos) == 1):
                                prefs_atendidas += 1
                                break
                
                prof_stats.append({
                    'Professor': prof_info['nome'],
                    'Total Aulas': len(aulas_prof),
                    'Preferências Atendidas': prefs_atendidas,
                    'Taxa Preferência (%)': (prefs_atendidas / len(aulas_prof) * 100) 
                                            if len(aulas_prof) > 0 else 0
                })
            
            with tab5:
                st.markdown("#### 📊 Análise Detalhada do Sistema de Horários")
                
                # Calcular estatísticas por série
                stats_por_serie = {}
                total_aulas_sistema = 0
                
                for turma_id, turma_info in turmas.items():
                    # Identificar a série
                    if turma_id.startswith('6'):
                        serie = '6º ano'
                    elif turma_id.startswith('7'):
                        serie = '7º ano'
                    elif turma_id.startswith('8'):
                        serie = '8º ano'
                    elif turma_id.startswith('9'):
                        serie = '9º ano'
                    elif turma_id.startswith('1EM'):
                        serie = '1º EM'
                    elif turma_id.startswith('2EM'):
                        serie = '2º EM'
                    elif turma_id.startswith('3EM'):
                        serie = '3º EM'
                    
                    if serie not in stats_por_serie:
                        stats_por_serie[serie] = {
                            'turmas': 0,
                            'total_alunos': 0,
                            'disciplinas': len(turma_info['disciplinas']),
                            'carga_estimada': 0
                        }
                    
                    stats_por_serie[serie]['turmas'] += 1
                    stats_por_serie[serie]['total_alunos'] += turma_info['alunos']
                    
                    # Calcular carga horária estimada
                    for disc_id in turma_info['disciplinas']:
                        carga = disciplinas[disc_id]['carga']
                        stats_por_serie[serie]['carga_estimada'] += carga
                        total_aulas_sistema += carga
                
                # Criar DataFrame para visualização
                df_series = pd.DataFrame([
                    {
                        'Série': serie,
                        'Nº Turmas': info['turmas'],
                        'Total Alunos': info['total_alunos'],
                        'Média Alunos/Turma': round(info['total_alunos'] / info['turmas'], 1),
                        'Nº Disciplinas': info['disciplinas'],
                        'Carga Total (aulas/semana)': info['carga_estimada']
                    }
                    for serie, info in stats_por_serie.items()
                ])
                
                # Ordenar por série
                ordem = ['6º ano', '7º ano', '8º ano', '9º ano', '1º EM', '2º EM', '3º EM']
                df_series['ordem'] = df_series['Série'].map({s: i for i, s in enumerate(ordem)})
                df_series = df_series.sort_values('ordem').drop('ordem', axis=1)
                
                # Exibir tabela
                st.dataframe(df_series, use_container_width=True)
                
                # Métricas gerais
                col1, col2, col3, col4 = st.columns(4)
                
                slots_totais = len(DIAS) * len(HORARIOS) * len(SALAS_IDS)
                taxa_ocupacao_teorica = (total_aulas_sistema / slots_totais) * 100
                
                with col1:
                    st.metric("Total de Aulas/Semana", total_aulas_sistema)
                with col2:
                    st.metric("Slots Disponíveis", slots_totais)
                with col3:
                    st.metric("Taxa Ocupação Teórica", f"{taxa_ocupacao_teorica:.1f}%")
                with col4:
                    st.metric("Margem para Otimização", f"{100 - taxa_ocupacao_teorica:.1f}%")
                
                # Gráficos de análise
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de progressão de disciplinas
                    fig_prog = px.line(
                        df_series, 
                        x='Série', 
                        y='Nº Disciplinas',
                        title='Progressão de Disciplinas por Série',
                        markers=True
                    )
                    fig_prog.update_layout(height=400)
                    st.plotly_chart(fig_prog, use_container_width=True)
                
                with col2:
                    # Gráfico de carga horária
                    fig_carga = px.bar(
                        df_series,
                        x='Série',
                        y='Carga Total (aulas/semana)',
                        title='Carga Horária Total por Série',
                        text='Carga Total (aulas/semana)'
                    )
                    fig_carga.update_traces(texttemplate='%{text}', textposition='outside')
                    fig_carga.update_layout(height=400)
                    st.plotly_chart(fig_carga, use_container_width=True)
                
                # Análise de distribuição de recursos
                st.markdown("#### 🏫 Distribuição de Recursos")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Análise de salas
                    salas_normais = len([s for s in salas.values() if s['tipo'] == 'normal'])
                    salas_lab = len([s for s in salas.values() if s['tipo'] == 'laboratório'])
                    
                    fig_salas = px.pie(
                        values=[salas_normais, salas_lab],
                        names=['Salas Normais', 'Laboratórios'],
                        title='Distribuição de Tipos de Sala'
                    )
                    fig_salas.update_layout(height=300)
                    st.plotly_chart(fig_salas, use_container_width=True)
                
                with col2:
                    # Análise de disciplinas por tipo
                    disc_normais = len([d for d in disciplinas.values() if d['sala_tipo'] == 'normal'])
                    disc_lab = len([d for d in disciplinas.values() if d['sala_tipo'] == 'laboratório'])
                    
                    fig_disc_tipo = px.pie(
                        values=[disc_normais, disc_lab],
                        names=['Disciplinas em Sala Normal', 'Disciplinas em Laboratório'],
                        title='Disciplinas por Tipo de Sala Necessária'
                    )
                    fig_disc_tipo.update_layout(height=300)
                    st.plotly_chart(fig_disc_tipo, use_container_width=True)
                
                # Insights
                st.markdown("#### 💡 Insights do Sistema")
                
                # Calcular alguns insights
                media_alunos = sum(t['alunos'] for t in turmas.values()) / len(turmas)
                capacidade_media_salas = sum(s['capacidade'] for s in salas.values()) / len(salas)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"""
                    **Características do Sistema:**
                    - Média de {media_alunos:.1f} alunos por turma
                    - Capacidade média das salas: {capacidade_media_salas:.1f} alunos
                    - {len([p for p in professores.values() if len(p['disciplinas']) > 1])} professores lecionam múltiplas disciplinas
                    - Sistema opera com {len(HORARIOS)} horários de 50min por dia
                    """)
                
                with col2:
                    st.success(f"""
                    **Pontos Fortes:**
                    - Taxa de ocupação teórica ideal (~{taxa_ocupacao_teorica:.0f}%)
                    - Progressão gradual de disciplinas (7→14)
                    - {salas_lab} laboratórios para {disc_lab} disciplinas especializadas
                    - Flexibilidade para otimização e preferências
                    """)

            df_prof = pd.DataFrame(prof_stats)
            df_prof = df_prof.sort_values('Taxa Preferência (%)', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_prof_aulas = px.bar(
                    df_prof.sort_values('Total Aulas', ascending=True).tail(15),
                    x='Total Aulas',
                    y='Professor',
                    orientation='h',
                    title="Top 15 Professores - Carga Horária"
                )
                fig_prof_aulas.update_layout(height=500)
                st.plotly_chart(fig_prof_aulas, use_container_width=True)
            
            with col2:
                fig_prof_pref = px.bar(
                    df_prof[df_prof['Total Aulas'] > 0].sort_values('Taxa Preferência (%)', 
                                                                    ascending=True).tail(15),
                    x='Taxa Preferência (%)',
                    y='Professor',
                    orientation='h',
                    title="Top 15 Professores - Taxa de Preferências Atendidas",
                    color='Taxa Preferência (%)',
                    color_continuous_scale='RdYlGn',
                    range_color=[0, 100]
                )
                fig_prof_pref.update_layout(height=500)
                st.plotly_chart(fig_prof_pref, use_container_width=True)
    
    # Análise de qualidade
    st.markdown("### 🎯 Análise de Qualidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Pontos Positivos")
        if analise_final['conflitos'] == 0:
            st.success("✓ Nenhum conflito de horário")
        if analise_final['cobertura'] >= 90:
            st.success("✓ Excelente cobertura das cargas horárias")
        if analise_final['preferencias_atendidas'] >= 50:
            st.success("✓ Excelente atendimento às preferências")
        elif analise_final['preferencias_atendidas'] >= 20:
            st.success("✓ Bom atendimento às preferências dos professores")
        if analise_final['problemas_capacidade'] == 0:
            st.success("✓ Nenhum problema de capacidade das salas")
        if analise_final['problemas_tipo_sala'] == 0:
            st.success("✓ Tipos de sala adequados para todas as disciplinas")
        if analise_final['ocupacao'] > 0.7:
            st.success("✓ Excelente taxa de ocupação das salas")
    
    with col2:
        st.markdown("#### ⚠️ Pontos de Atenção")
        if analise_final['conflitos'] > 0:
            st.error(f"✗ {analise_final['conflitos']} conflitos encontrados")
        if analise_final['cobertura'] < 90:
            st.warning(f"⚠ Cobertura das cargas horárias: {analise_final['cobertura']:.1f}%")
        if analise_final['preferencias_atendidas'] < 20:
            st.warning(f"⚠ Poucas preferências atendidas: {analise_final['preferencias_atendidas']}")
        if analise_final['problemas_capacidade'] > 0:
            st.warning(f"⚠ {analise_final['problemas_capacidade']} problemas de capacidade")
        if analise_final['problemas_tipo_sala'] > 0:
            st.warning(f"⚠ {analise_final['problemas_tipo_sala']} problemas de tipo de sala")
        if analise_final['ocupacao'] < 0.5:
            st.warning(f"⚠ Baixa taxa de ocupação: {analise_final['ocupacao']*100:.1f}%")
    
    # Exportar resultados
    st.markdown("### 💾 Exportar Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.download_button(
            label="📊 Baixar Cronograma (CSV)",
            data=df_cronograma.to_csv(index=False, encoding='utf-8-sig'),
            file_name=f"cronograma_otimizado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        ):
            st.success("Cronograma exportado!")
    
    with col2:
        if st.download_button(
            label="📈 Baixar Análise (CSV)",
            data=df_disciplinas.to_csv(index=False, encoding='utf-8-sig'),
            file_name=f"analise_disciplinas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        ):
            st.success("Análise exportada!")
    
    with col3:
        # Exportar JSON completo
        export_data = {
            'configuracoes': {
                'tamanho_populacao': tamanho_populacao,
                'max_geracoes': max_geracoes,
                'taxa_mutacao': taxa_mutacao,
                'taxa_cruzamento': taxa_cruzamento,
                'elitismo': elitismo
            },
            'resultados': {
                'fitness_final': analise_final['fitness'],
                'conflitos': analise_final['conflitos'],
                'cobertura': analise_final['cobertura'],
                'ocupacao': analise_final['ocupacao'],
                'preferencias_atendidas': analise_final['preferencias_atendidas']
            },
            'cronograma': cronograma_data
        }
        
        if st.download_button(
            label="📦 Baixar Dados Completos (JSON)",
            data=json.dumps(export_data, indent=2, ensure_ascii=False),
            file_name=f"otimizacao_completa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        ):
            st.success("Dados completos exportados!")

# Sidebar com informações dos dados
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Dados do Sistema")

with st.sidebar.expander("👥 Professores"):
    for prof_id, prof_info in list(professores.items())[:5]:
        st.write(f"**{prof_info['nome']}**")
        st.write(f"Disciplinas: {', '.join(prof_info['disciplinas'])}")
        st.write("---")
    if len(professores) > 5:
        st.write(f"... e mais {len(professores) - 5} professores")

with st.sidebar.expander("🏫 Salas"):
    for sala_id, sala_info in list(salas.items())[:5]:
        st.write(f"**{sala_info['nome']}**")
        st.write(f"Capacidade: {sala_info['capacidade']} alunos")
        st.write(f"Tipo: {sala_info['tipo']}")
        st.write("---")
    if len(salas) > 5:
        st.write(f"... e mais {len(salas) - 5} salas")

with st.sidebar.expander("👨‍🎓 Turmas"):
    for turma_id, turma_info in list(turmas.items())[:5]:
        disciplinas_nomes = [disciplinas[d]['nome'] for d in turma_info['disciplinas']]
        st.write(f"**{turma_id}**")
        st.write(f"Alunos: {turma_info['alunos']}")
        st.write(f"Disciplinas: {len(disciplinas_nomes)}")
        st.write("---")
    if len(turmas) > 5:
        st.write(f"... e mais {len(turmas) - 5} turmas")

# Informações sobre o algoritmo
with st.sidebar.expander("🧬 Sobre o Algoritmo Genético"):
    st.markdown("""
    **Componentes do AG:**
    - **População**: Conjunto de soluções candidatas
    - **Fitness**: Função que avalia a qualidade da solução
    - **Seleção**: Torneio entre indivíduos
    - **Crossover**: Recombinação uniforme
    - **Mutação**: Alteração aleatória de genes
    - **Elitismo**: Preservação dos melhores
    
    **Penalidades no Fitness:**
    - Conflitos: -200 pontos
    - Falta de aulas: -15 pontos/aula
    - Excesso de aulas: -25 pontos/aula
    - Capacidade excedida: -50 pontos (proporcional)
    - Tipo sala errado: -40 pontos
    
    **Bônus no Fitness:**
    - Aula alocada corretamente: +50 pontos
    - Preferência atendida: +40 pontos
    - Capacidade adequada: +2 a +8 pontos
    - Tipo sala correto: +15 pontos
    - Distribuição equilibrada: +5 pontos
    
    **Horários:**
    - Aulas de 50 minutos
    - Intervalo de almoço: 12:10-13:00
    - 11 horários por dia (5h30min manhã + 4h10min tarde)
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p><strong>🎓 Sistema de Otimização de Horários Escolares</strong></p>
        <p>Algoritmo Genético • Python + Streamlit</p>
        <p>Período Integral (08:00-18:00) • Aulas de 50 minutos</p>
        <p>20 Salas • 20 Turmas • 38 Professores • 26 Disciplinas</p>
    </div>
    """, 
    unsafe_allow_html=True
)