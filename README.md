# Novo Agente

Além dos dois agentes básicos (codificador e revisor), criou-se um novo agente: o Agente de Monitoramento e Feedback.

## Agente de monitoramento e feedback

O agente de monitoramento e feedback é responsável por acompanhar a execução das tarefas realizadas pelos outros agentes (codificador e revisor), garantindo que os recursos computacionais sejam utilizados de maneira eficiente. Ele identifica gargalos de desempenho e fornece feedback contínuo para melhorar a qualidade e a eficiência do processo.

### Espaço de Ações

O espaço de ações do agente de monitoramento é composto por operações relacionadas ao desempenho do sistema. Cada ação representa uma etapa do monitoramento ou da análise de eficiência.

Ação | Descrição
-----|----------
Monitorar Tempo de Execução | Acompanhar o tempo gasto na execução de código, identificando gargalos ou ineficiências.
Monitorar Uso de Recursos | Avaliar o uso de memória e CPU durante a execução, sugerindo melhorias para otimização.
Fornecer Feedback de Eficiência | Enviar feedback contínuo para o Codificador e o Revisor sobre o desempenho do código e possíveis melhorias.
