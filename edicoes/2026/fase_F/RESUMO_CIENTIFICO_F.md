# FUBOG 2026 — Fase F: validação científica independente

**Edição:** ingresso 2026, prova PSU-GO em 23/11/2025. **Portão F→G:** aprovado com ressalvas científicas. Fase G **não iniciada**.

## Portão precedente
O pacote E foi reavaliado antes da F: ZIP íntegro, **31/31 entradas do manifesto por SHA-256**, ata E→F assinada metodologicamente com ressalvas, e 25 requisitos E com evidências. A ausência de validação externa (E21) permaneceu **limitada** — não foi tratada como concluída.

## Auditoria F realizada
- **366/366 testes independentes locais aprovados**, incluindo metadados e hashes do ZIP, regras de escala, momentos das distribuições, erro Monte Carlo, intervalos e cenários.
- O gerador E foi executado integralmente outra vez em diretório temporário. **7/7 CSVs reproduzidos byte a byte**, SHA-256 idêntico.
- A solução analítica de empates foi calculada de novo por multinomial sem reutilizar o helper do gerador. Cenário sintético N=180 / k=60: beta-binomial **88,566859%**, máxima entropia **88,388576%**, mistura **88,370027%**.
- Em 1.000.000 de simulações beta-binomiais, a ampliação por empates foi **88,5512%**. É probabilidade **condicional de cenário artificial**, não chance real de aprovação.
- Auditoria independente no Deepnote (run `33eeaa79-4c0e-4324-9a91-b865b46c344a`): 305 pessoas, 610 linhas A13/A15, 610 somas Decimal sem resíduo, igualdade entre as versões, 30 contrafactuais e 150 controles independentes de fronteira. Vínculo de **141 eventos de chamada** não foi imputado.
- Verificação independente de momentos no Deepnote (run `dbfd4a2e-7585-4ce4-a258-85c0b646e63f`): média objetiva **58,67704918** e DP descritivo **6,85423391** dos 305 publicados.
- **25 requisitos F**: 8 cumpridos, 11 cumpridos com ressalvas, 5 limitados e 1 não aplicável.

## Limites que impedem alegações mais fortes
1. O número de presentes é desconhecido; 354 inscrições não equivalem a 305 resultados publicados nem ao número de presentes.
2. A13 e A15 são publicações das mesmas 305 pessoas; não há validação temporal externa.
3. Sem matriz pessoa×item, não há dificuldade empírica/discriminação, IRT ou DIF.
4. O gabarito preliminar retificado de 24/11 tem 400 posições verificadas, mas o comunicado posterior não autentica os números exatos de anulações/gabarito definitivo integral.
5. Não se reconstrói classificação/matrícula real a partir de nota, preferência e chamadas incompletas.
6. A fonte histórica remota não foi arquivada em PDF binário original; SHA-256 dos pacotes só prova sua integridade interna.
7. Não há posterior Bayesiana; não reivindicar diagnósticos MCMC/Rhat/ESS/PPC inexistentes.

**Conclusão:** **APPROVED_WITH_CAVEATS** / aprovado com ressalvas **no escopo de consistência documental interna e matemática condicional**. Não atesta validade preditiva nem probabilidade de aprovação. **A próxima fase autorizada é G (relatório final)**. Não iniciar outro ano antes de concluir e auditar G.

**Pacote científico canônico:** `FUBOG_2026_Fase_F_pacote_auditavel.zip`, SHA-256 `d9eb475cc55842e4a2496c622e3d00b3e9756264b5045d500ae9bd249a707677`. Pacote original preservado no chat, incluindo scripts, manifesto e os 7 CSVs reproduzíveis; a publicação no GitHub contém apenas documentação e código não identificável.
