# Auditoria de continuidade — 2026-11-03 — ingresso 2026

## Portão D → E
Ata D→E lida. Aprovação **com ressalvas**, restrita a descrição e hipóteses dos 305 candidatos publicados. Os registros informam 26/26 testes internos, 43/43 verificações independentes; requisitos D01–D21: 10 cumpridos, 6 com ressalvas, 4 limitados e 1 não aplicável. Isso autoriza iniciar E, mas não extrapolar para todos os presentes.

## Execução já existente da Fase E
Foram inspecionados os artefatos existentes: 30 cenários/limiares contrafactuais (5 cenários × 6 valores de k), 120 verificações de desigualdades, 156 verificações independentes reportadas e reprodução SHA-256 de 4 arquivos reportada. O escopo é **305 notas publicadas**, não a classificação oficial. As publicações A13 e A15 representam as mesmas pessoas; a comparação não é validação externa. O relatório independente assinala explicitamente: `aprovacao_Fase_E = PENDENTE_AVALIACAO_INTEGRADA_COM_MONTE_CARLO`.

## Decisão
**Fase E: PARCIAL, NÃO APROVADA PARA PORTÃO E→F.** Os testes relatados foram inspecionados como artefatos; não foram reexecutados nesta auditoria. Falta localizar e confrontar o plano original A–G, implementar/auditar o componente Monte Carlo da fase E conforme plano e comprovar critérios de aceite. Não produzir probabilidade real de aprovação sem população de presentes, classificação/convocações vinculadas e validação externa. Não iniciar F nem outra edição.

## Limites de proveniência
O relatório de reprodução de hashes alerta que o binário histórico oficial não foi autenticado. Não confundir integridade interna com autenticidade da fonte. Não publicar dados individuais no GitHub público.
