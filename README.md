# Otimizador de Horários Escolares com Algoritmo Genético

## Visão Geral

Este projeto implementa um **algoritmo genético** para geração e otimização de cronogramas escolares (school scheduling), considerando:
- Preferências de professores;
- Capacidade e tipo de salas (normais e laboratórios);
- Conflitos de turma e professor;
- Carga horária por disciplina;
- Distribuição equilibrada ao longo do dia.

A interface é construída com **Streamlit**, oferecendo visualização em tempo real da evolução, métricas, gráficos e cronograma final.

## Funcionalidades Principais

- Geração heurística inicial de cromossomos (soluções) com base em preferências e tipos de sala.
- Cálculo de fitness sofisticado com:
  - Penalizações por conflitos (professor/ turma);
  - Bônus por cobertura correta da carga horária;
  - Ajuste de capacidade de sala;
  - Atendimento às preferências de horário dos professores;
  - Verificação de tipo de sala adequado (laboratório vs normal);
  - Balanceamento da ocupação ao longo dos horários.
- Operadores genéticos:
  - Seleção por torneio;
  - Crossover uniforme com reparo de conflitos;
  - Mutação (remoção/adicionamento aleatório de aulas);
  - Elitismo configurável.
- Análise detalhada do melhor indivíduo (fitness, cobertura, conflitos, preferências, distribuição).
- Visualizações interativas com Plotly e dashboard de métricas via Streamlit.

## Requisitos

- Python 3.10+ (testado em ambientes similares)
- Bibliotecas:
  - streamlit
  - pandas
  - numpy
  - plotly

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/franklinarauj/algoritmo-genetico.git
   cd algoritmo-genetico
   ```

2. Instale dependências (exemplo usando pip):
   ```bash
   pip install -r requirements.txt
   ```
   Ou, se preferir instalar manualmente:
   ```bash
   pip install streamlit pandas numpy plotly
   ```

3. Execute a aplicação:
   ```bash
   python -m streamlit run ag_school_scheduler.py
   ```

## Estrutura do Projeto

```
algoritmo-genetico/
├── ag_school_scheduler.py   # Aplicação principal
├── README.md                # Documentação do projeto
├── LICENSE                  # Licença do projeto
├── requirements.txt         # Dependências
├── CHANGELOG.md             # Histórico de versões
```

## Estrutura de Dados

- **Salas**: definidas com nome, capacidade e tipo (`normal` ou `laboratório`).
- **Professores**: possuem nome, disciplinas que lecionam e preferências de horários.
- **Turmas**: associadas a um número de alunos e conjunto de disciplinas.
- **Disciplinas**: com nome, carga horária semanal, tipo de sala necessário e lista de professores possíveis.

## Configurações do Algoritmo

Na sidebar é possível ajustar:

- `Tamanho da População`: número de cromossomos por geração.
- `Máximo de Gerações`: quantas gerações serão evoluídas.
- `Taxa de Mutação`: probabilidade de mutações por geração.
- `Taxa de Cruzamento`: chance de aplicar crossover entre pais.
- `Elitismo`: fração da população preservada diretamente na próxima geração.

## Fluxo do Algoritmo

1. Geração inicial da população usando heurísticas (`gerar_cromossomo_inteligente`).
2. Avaliação do fitness de cada indivíduo com `calcular_fitness_otimizado`.
3. Repetição de:
   - Seleção por torneio;
   - Crossover (com reparo de conflitos);
   - Mutação;
   - Reavaliação e atualização do melhor indivíduo;
   - Registro do histórico de fitness.
4. Exibição em tempo real dos progressos e métricas.
5. Ao término, mostra análise detalhada e cronograma otimizado.

## Como Usar

1. Abra a interface com Streamlit.
2. Ajuste os parâmetros na barra lateral.
3. Clique em **"Executar Otimização"**.
4. Acompanhe:
   - Evolução do fitness;
   - Cobertura de carga horária;
   - Conflitos e preferências atendidas.
5. Filtre e inspecione o cronograma final por dia, horário ou turma.
6. Explore as abas de análise (ocupação, mapa de calor, por disciplina, por professor, estatísticas gerais).

## Personalização

Você pode adaptar:

- Conjuntos de turmas, disciplinas, professores e salas para outra escola ou período.
- Função de fitness para incluir novas restrições (ex.: limites de aulas por dia por professor).
- Operadores genéticos (por exemplo, outro tipo de crossover ou mutação mais inteligente).
- Adicionar restrições de bloqueio (ex.: horário em que certa disciplina não pode ocorrer).

## Boas Práticas e Dicas de Performance

- **Elitismo moderado** ajuda a preservar progresso sem estagnar.
- Ajuste `taxa_mutacao` para evitar convergência precoce (taxas muito baixas) ou ruído excessivo (taxas muito altas).
- A inicialização inteligente reduz o tempo até soluções plausíveis.
- Para instâncias grandes, reduza visualizações em tempo real ou amostre gerações para evitar sobrecarga na UI.

## Possíveis Melhorias Futuras

- Suporte a múltiplos períodos (manhã/tarde/noite).
- Restrições de sequência (por exemplo, não colocar certas disciplinas em sequência).
- Exportar cronograma final para Excel/PDF.
- Interface administrativa para editar dados (professores, turmas) dinamicamente.
- Paralelização da avaliação de fitness.

## Licença
Este projeto é licenciado sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## Feito por Franklin Araújo
- [LinkedIn](https://linkedin.com/in/franklinarauj/)