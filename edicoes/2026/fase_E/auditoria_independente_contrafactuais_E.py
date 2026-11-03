# Auditoria independente de contrafactuais da Fase E - cálculo alternativo
import pandas as pd, numpy as np, json, math
from pathlib import Path
b=Path("Fase_B/saida_B");e=Path("Fase_E")
a=pd.read_csv(b/"pontuacoes.csv")
d=a.query("documento=='A15'").sort_values("pid").reset_index(drop=True)
cf=pd.read_csv(e/"contrafactuais_publicados.csv")
base=pd.read_csv(e/"retroteste_nao_identificavel.json") if False else json.loads((e/"retroteste_nao_identificavel.json").read_text())
bonus=json.loads((e/"efeito_bonus_observado.json").read_text())
assert len(d)==305 and len(cf)==30 and cf.cenario.nunique()==5
assert base["validacao_externa"] is False and base["divergencias_componentes"]==0
cases={
 "final_publicada":d.total_publicado,
 "sem_bonus_objetivo_e_curricular":d.nota_prova+d.nota_curriculo,
 "somente_objetiva_sem_bonus":d.nota_prova,
 "somente_etapa1_com_bonus":d.nota_prova+d.bonus_prova,
 "sem_curriculo_mantendo_bonus_objetivo":d.nota_prova+d.bonus_prova
}
t=0
for rec in cf.itertuples():
    values=cases[rec.cenario].values
    k=int(rec.k)
    # second method sorts full array rather than using partition
    th=np.sort(values)[-k]
    high=int((values>th+1e-8).sum())
    equal=int(np.isclose(values,th,atol=1e-8).sum())
    selected=k-high
    assert abs(th-rec.nota_fronteira)<1e-10
    assert high==rec.acima_estrito and equal==rec.empatados_fronteira
    assert selected==rec.vagas_dentro_empate
    assert math.comb(equal,selected)==rec.combinacoes_possiveis
    assert high+equal==rec.total_ate_empate
    t+=5
bnum=d.bonus_prova+d.bonus_curriculo
assert int((bnum>0).sum())==bonus["n_com_bonus_positivo"]==5
assert abs(float(bnum.sum())-bonus["soma_dos_bonus_pontos"])<1e-8
assert abs(float(bnum.mean())-bonus["media_bonus_nos_305"])<1e-8
assert not (e/"classificacao_oficial_reconstruida.csv").exists()
assert not (e/"probabilidade_real_aprovacao.csv").exists()
res={"status":"APROVADO_DENTRO_DOS_305_PUBLICADOS","registros_checados":30,
     "validacoes_independentes":t+6,
     "preserva_empates":True,"N_presentes":"DESCONHECIDO",
     "classificacao_real":"NAO_RECONSTRUIDA",
     "bonificacoes_positivas":5,
     "aprovacao_Fase_E":"PENDENTE_AVALIACAO_INTEGRADA_COM_MONTE_CARLO",
     "nota":"A13 e A15 espelhos, nao teste preditivo externo"}
(e/"auditoria_independente_contrafactuais_E.json").write_text(json.dumps(res,indent=2,ensure_ascii=False)+"\n")
print(res)