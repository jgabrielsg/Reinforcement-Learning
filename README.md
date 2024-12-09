# Projeto de Reinforcement Learning
## João Gabriel, Gustavo Bianchi e Leonardo

O objetivo desse código é treinar dois agentes LLM para cooperarem na solução de problemas de análise de dados e criarem códigos.
O ambiente de treinamento é um ambiente customizado, onde os agentes devem aprender a cooperar para maximizar a recompensa.

Para resolver esse problema, usamos dois tipos de agentes principais: um agente que escreve o código inicial e um agente que 
revisa e sugere melhorias. O agente revisor deve ser capaz de identificar erros e sugerir melhorias no código. O agente que 
escreve o código deve ser capaz de corrigir os erros e melhorar o código.

Problema passado para a LLM:

```
We have a Sales.csv with 4 columns: Date, with the date (format 2024-09-25) of the sale;
Price, how much money (format 20.99USD) the client paid for the sale;
Store, in which store was made that sale, the IDs go from 1 to 5
State, the state the sale was made. We work in 2 states, Paraná and Acre
There's some data missing, with null values and outliers. Find the outliers (like a sale costing more than 
100000USD) and the missing data and get rid of them. After that, your job is to create 2 visualizations: 
- Sales per state
- Sales per month of the year.
```

# Agentes

## Agente Codificador

O agente codificador é responsável por escrever o código para a análise, retornando o código pedido pelo prompt de entrada.

Ação | Descrição
-----|----------
Processamento dos dados | Limpar, transformar e preparar os dados para análise.
Analisar os dados | Realizar análises estatísticas, ou contruir modelos de aprendizado de máquina.
Visualizar os resultados | Gerar gráficos e visualizações dos dados.

## Agente Revisor

O agente revisor é responsável por revisar o código escrito pelo agente codificador e sugerir melhorias, recebendo o código do codificador e retornando um
feedback

Ação | Descrição
-----|----------
Análise Estática | Analisar o código com [Ruff](https://docs.astral.sh/ruff/)
Executar código | Executar o código atual para verificar se ele está correto, identificando bugs.
Propor Refatoração | Propor refatorações para melhorar a qualidade do código, através de um score para várias habilidades do código

## Novo Agente

Além dos dois agentes básicos (codificador e revisor), criou-se um novo agente: o Agente de Monitoramento e Feedback.

## Agente de monitoramento e feedback

O agente de monitoramento e feedback é responsável por acompanhar a execução das tarefas realizadas pelos outros agentes (codificador e revisor), 
garantindo que os recursos computacionais sejam utilizados de maneira eficiente. Ele identifica gargalos de desempenho e fornece 
feedback contínuo para melhorar a qualidade e a eficiência do processo.

### Espaço de Ações

O espaço de ações do agente de monitoramento é composto por operações relacionadas ao desempenho do sistema. Cada ação representa uma etapa 
do monitoramento ou da análise de eficiência.

Ação | Descrição
-----|----------
Monitorar Tempo de Execução | Acompanhar o tempo gasto na execução de código, identificando gargalos ou ineficiências.
Monitorar Uso de Recursos | Avaliar o uso de memória e CPU durante a execução, sugerindo melhorias para otimização.
Fornecer Feedback de Eficiência | Enviar feedback contínuo para o Codificador e o Revisor sobre o desempenho do código e possíveis melhorias.
