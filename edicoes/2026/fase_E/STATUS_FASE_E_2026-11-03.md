# FUBOG ingresso 2026 — Fase E consolidada (03/11/2026)

**Decisão do portão E→F: APROVADO COM RESSALVAS CIENTÍFICAS, apenas para simulação condicional.** A Fase F ainda não foi executada.

## Evidências da Fase E
- **25/25 requisitos avaliados**: 12 cumpridos, 10 cumpridos com ressalvas, 2 não aplicáveis e 1 limitado (E21). Não há pendências formais após a ata.
- Simulador sintético: lotes 1.000/10.000/100.000 em cada uma de três famílias e 1.000.000 para beta-binomial; 54 cenários fatoriais, 36 de vagas/multiplicadores e 4 modelos curriculares.
- Conferência de probabilidade por multinomial independente: **12/12 testes** reexecutados e aprovados. Auditoria integrada local: **246/246 verificações** aprovadas. A reprodução anterior de **7 arquivos CSV** foi reconferida por SHA-256.
- No Deepnote: **30 contrafactuais** sobre 305 pessoas publicadas (não 610 pessoas), **156 verificações independentes** e reprodução SHA-256 de **4/4 arquivos**.
- Cinco cenários de pontuação para k=4/6/8/60/90/120, preservando empates sem criar desempates fictícios.

## Resultados sob hipótese artificial
Cenário beta-binomial, N sintético=180, k=60, sem bônus: **88,5512%** de ampliação por empate em 1 milhão de coortes; cálculo exato **88,566859%**. O erro MC e seus intervalos quantificam somente ruído computacional, **não chance de ingresso**.

## Limites que continuam em vigor
- **E21 LIMITADO:** não houve validação preditiva temporal independente. A13 e A15 têm os mesmos 305 nomes e notas coincidentes; não são dois anos distintos.
- **E03 e E18 NÃO APLICÁVEIS:** esta edição não usa z-score e um índice Sobol global não foi reivindicado sem distribuição conjunta fundamentada.
- **E24 com ressalva:** os dados individuais observacionais permanecem no Deepnote; o simulador e sua reexecução estão no ZIP local. Auditoria integrada de evidências de dois ambientes, não reprodução de toda a análise num só processo.
- Gabarito oficial: **400/400 respostas PRELIMINARES RETIFICADAS** confirmadas. Existe comunicado pós-recursos de gabarito definitivo, mas as alterações específicas/anulações não foram confirmadas pelo PDF consultado. Não foram imputadas.
- N presentes, matriz pessoa×questão, classificação oficial e matrículas efetivas continuam desconhecidos.

**Próxima etapa autorizada:** somente a Fase F, para validação científica independente de A–E. Não iniciar outra edição antes da conclusão auditada de F e G.

**Pacote canônico da fase:** `FUBOG_2026_Fase_E_consolidada_auditavel.zip`, com manifesto de 31 arquivos e SHA-256 do ZIP `f7f670b991a4a7171689b552a2a61a43828f98f26ab9be30b4105496e8cd4ef8`. O ZIP permanece como arquivo da conversa, não foi importado integralmente no GitHub público.
