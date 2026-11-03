# FUBOG ingresso 2026 — Fase E; contrafactuais limitados aos 305 publicados.
from pathlib import Path
import numpy as np, pandas as pd, json, math
from decimal import Decimal
b=Path("Fase_B/saida_B");o=Path("Fase_E");o.mkdir(exist_ok=True)
d=pd.read_csv(b/"pontuacoes.csv")
a=d[d.documento=="A15"].sort_values("pid").reset_index(drop=True)
v=d[d.documento=="A13"].sort_values("pid").reset_index(drop=True)
assert len(a)==len(v)==305 and a.pid.is_unique and (a.pid.to_numpy()==v.pid.to_numpy()).all()
cs=["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo","total_publicado"]
assert np.allclose(a[cs],v[cs],atol=1e-9,rtol=0)
assert np.allclose(a[cs[:4]].sum(axis=1),a.total_publicado,atol=1e-9,rtol=0)
r=[]
scenarios={
 "final_publicada":a.total_publicado.to_numpy(float),
 "sem_bonus_objetivo_e_curricular":(a.nota_prova+a.nota_curriculo).to_numpy(float),
 "somente_objetiva_sem_bonus":a.nota_prova.to_numpy(float),
 "somente_etapa1_com_bonus":(a.nota_prova+a.bonus_prova).to_numpy(float),
 "sem_curriculo_mantendo_bonus_objetivo":(a.nota_prova+a.bonus_prova).to_numpy(float),
}
for nm,scores in scenarios.items():
    for k in (4,6,8,60,90,120):
        border=float(np.partition(scores,-k)[-k])
        mandatory=np.flatnonzero(scores>border+1e-8)
        tied=np.flatnonzero(abs(scores-border)<=1e-8)
        must_take=k-len(mandatory)
        assert 1<=must_take<=len(tied), (nm,k)
        comb=math.comb(len(tied),must_take)
        r.append({"cenario":nm,"k":k,"n_publicados":305,"nota_fronteira":border,
                  "acima_estrito":len(mandatory),"empatados_fronteira":len(tied),
                  "vagas_dentro_empate":must_take,"combinacoes_possiveis":comb,
                  "total_ate_empate":len(mandatory)+len(tied),
                  "tipo":"ORDENACAO_CONTRAFACTUAL_DE_PUBLICADOS_SEM_DESEMPATE_OFICIAL"})
pd.DataFrame(r).to_csv(o/"contrafactuais_publicados.csv",index=False,float_format="%.12g")
# A13 e A15 descrevem a mesma coorte e as mesmas notas; não são teste temporal independente.
retro={"marco_t0":"A13","marco_t1":"A15","mesmas_305_pessoas":True,
       "mesmas_610_observacoes_documentais":True,
       "divergencias_componentes":0,"validacao_externa":False,
       "estado":"replay tautologico, nenhum teste preditivo interanual"}
(o/"retroteste_nao_identificavel.json").write_text(json.dumps(retro,ensure_ascii=False,indent=2)+"\n")
# Descrição de impacto do bônus sem imputar ausência. Diferença aritmética direta nos 305.
pub=a.total_publicado.to_numpy(float)
sem=(a.nota_prova+a.nota_curriculo).to_numpy(float)
pb=(a.bonus_prova+a.bonus_curriculo).to_numpy(float)
assert np.max(np.abs(pub-sem-pb))<1e-8
bonus={"pessoas_publicadas":305,"n_com_bonus_positivo":int((pb>0).sum()),
       "soma_dos_bonus_pontos":float(pb.sum()),
       "media_bonus_nos_305":float(pb.mean()),
       "fracao_bonus_positiva":float((pb>0).mean()),
       "modificacao_mecanica":True,"efeito_causal_de_aprovacao":None}
(o/"efeito_bonus_observado.json").write_text(json.dumps(bonus,ensure_ascii=False,indent=2)+"\n")
# Independent method: every chosen k must meet threshold cardinality inequalities.
df=pd.read_csv(o/"contrafactuais_publicados.csv")
for row in df.itertuples():
    s=scenarios[row.cenario]
    assert np.sum(s>row.nota_fronteira+1e-8)==row.acima_estrito
    assert np.sum(abs(s-row.nota_fronteira)<=1e-8)==row.empatados_fronteira
    assert row.acima_estrito+row.vagas_dentro_empate==row.k
    assert math.comb(row.empatados_fronteira,row.vagas_dentro_empate)==row.combinacoes_possiveis
assert df.groupby("cenario").size().eq(6).all() and len(df)==30
checks={"status":"PASS","observados_distintos":305,
        "contrafactuais":30,"controles_inequacoes":30*4,
        "A13_A15_componentes_iguais":True,
        "bonus":bonus,"exemplo_top6":df.query("k==6").to_dict("records"),
        "retroteste":retro,
        "limite":"nenhum cenário equivale à classificação real nem ao número de matriculados"}
(o/"auditoria_contrafactuais.json").write_text(json.dumps(checks,ensure_ascii=False,indent=2,default=str)+"\n")
print(json.dumps({"status":"PASS","contrafactuais":30,"testes_desigualdade":120,
                   "bonus_n":bonus["n_com_bonus_positivo"],
                   "top6":df.query("k==6")[["cenario","nota_fronteira","empatados_fronteira","combinacoes_possiveis"]].to_dict("records")},
                  ensure_ascii=False))