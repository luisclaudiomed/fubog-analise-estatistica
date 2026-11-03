# FUBOG — ingresso 2026 | Relatório técnico da Fase D

**Objeto:** seleção unificada PSU-GO 2026 (prova em 23/11/2025), instituição FUBOG. **O estudo descreve apenas os candidatos publicados.** O relatório de notas não possui caráter classificatório. Não foi executada a Fase E.

## População e fontes

- A13 e A15 são duas publicações das **mesmas 305 pessoas**, não 610 participantes. A auditoria anterior da Fase B corrigiu quatro campos de indexação e confirmou a igualdade numérica das versões.
- A relação candidato/vaga identifica **354 inscrições**, não comparecimentos. O número real de presentes é **desconhecido**.
- A aplicação compartilhada do PSU-GO possui quatro tipos; há 800 posições de gabaritos preliminares/retificados, mas não respostas individuais nem gabarito definitivo consolidado.
- São 400 posições estruturais no catálogo (100×4), com enunciado, dificuldade empírica e discriminação **ausentes**. Não foram estimadas artificialmente.

## Descritivas dos publicados (n=305)

| Medida | Valor |
|---|---:|
| Média de prova objetiva bruta (0–90) | 58.677 |
| DP descritivo da objetiva (ddof=0) | 6.854 |
| Média da nota final (0–100) | 65.461 |
| Mediana final | 65.45 |
| P95 final apenas dos publicados | 79.26 |
| Spearman objetiva vs. final | 0.9600 |

Foram contabilizados **46360 pares**. Com a objetiva sem bonificação, **1625 pares empatavam na primeira etapa** e **3171 dos 44674 pares comparáveis inverteram sua ordem** entre objetiva e total final (7.10%). Trata-se de descrição da pontuação, não de classificação oficial da AREMG nem de efeito causal do currículo.

**Bonificação publicada:** 5 pessoas com bônus positivo na prova e 5 no currículo. O efeito causal individual da elegibilidade não foi identificado.

## Modelos hipotéticos e limites de identificabilidade

Beta-binomial, máxima entropia discreta e mistura foram calibradas **somente** à média e ao DP dos 305 publicados. Para o limiar bruto 75,6, as massas teóricas são:

- beta binomial published moments: 0.455%
- max entropy published moments: 0.808%
- mixture published moments: 0.799%

O limite por programação linear baseado apenas nesses dois momentos e suporte 0–90 permite, no mesmo limiar, um intervalo teórico de **0% a 14.07%**. Isso explicita a ausência de identificação pela média/DP isoladas, **não** quantifica probabilidade de aprovação, presença nem pontuação de toda a população.

O teste interno de sensibilidade usou 214 pessoas de treino e 91 de teste; a fração observada ≥75,6 no teste foi 0.0%, enquanto o modelo hipotético ajustado no treino atribuía 1.13%. Isso não constitui calibração histórica externa.

## Riscos e restrições científicos

1. N de presentes desconhecido e seleção informativa dos divulgados; não transferir quantis ao conjunto completo.
2. Sem respostas individuais por item, enunciados oficiais integrais ou gabarito definitivo consolidado: sem dificuldade/discriminação empírica, IRT ou DIF.
3. A13 e A15 não representam replicação independente; são publicações do mesmo grupo.
4. As preferências e 141 eventos sem vinculo seguro impedem reconstrução fiel da classificação/convocações.
5. Sem cadeias posteriores, não há MCMC/R-hat/ESS/PPC aplicáveis. Três famílias teóricas não demonstram validade externa.

## Auditoria e decisão

**26/26 testes do motor** e **43/43 verificações independentes** passaram. Os 21 requisitos foram individualmente avaliados: cumprido: 10; cumprido_com_ressalva: 6; limitado: 4; nao_aplicavel: 1.

**Portão D→E aprovado com ressalvas científicas**, condicionado a manter as limitações como limites reais e nunca tratar simulações como probabilidades pessoais. Nenhuma atividade da Fase E foi iniciada.

Fontes e código: `Fase_B/saida_B/*` e `Fase_D/*` no projeto Deepnote; documentação científica pública, sem microdados pessoais, no GitHub.
