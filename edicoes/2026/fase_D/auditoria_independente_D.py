"""Auditoria independente da Fase D de 2026. Não importa execute_D.py."""
from pathlib import Path
from itertools import combinations
import numpy as np,pandas as pd,math,json,hashlib
from scipy import stats,optimize
P=Path("Fase_B/saida_B");D=Path("Fase_D")
F=pd.read_csv(P/"pontuacoes.csv");A=F[F.documento=="A15"].sort_values("pid").reset_index(drop=True)
B=F[F.documento=="A13"].sort_values("pid").reset_index(drop=True)
R=json.loads((D/"resumo_D.json").read_text())
T=[]
def chk(label,ok,detail=""):
    T.append(dict(teste=label,passou=bool(ok),detalhe=detail))
    if not ok:raise AssertionError(f"{label}: {detail}")
chk("fase_D_status",R["fase"]=="D" and R["edicao"]=="FUBOG_INGRESSO_2026")
chk("duas_fontes_mesmas_pessoas",len(A)==len(B)==305 and A.pid.equals(B.pid))
for field in ["nota_prova","nota_curriculo","bonus_prova","bonus_curriculo","total_publicado"]:
    chk("A13_A15_"+field,np.allclose(A[field].to_numpy(float),B[field].to_numpy(float),atol=1e-10,rtol=0))
chk("totais_independentes",np.max(abs(A.nota_prova+A.bonus_prova+A.nota_curriculo+A.bonus_curriculo-A.total_publicado))<1e-10)
chk("media_primaria",abs(float(A.nota_prova.mean())-R["media_prova_publicados"])<1e-11)
chk("desvio_primario",abs(float(A.nota_prova.std(ddof=0))-R["dp_prova_publicados"])<1e-11)
chk("media_final",abs(float(A.total_publicado.mean())-R["media_final_publicados"])<1e-11)
chk("p95_final",abs(float(A.total_publicado.quantile(.95))-R["P95_final_publicados"])<1e-10)
S=pd.read_csv(D/"estatisticas_publicados.csv")
s=S[(S.populacao=="FUBOG_publicados_A15")&(S.campo=="total_publicado")].iloc[0]
chk("estatisticas_publicados",int(s.n)==305 and abs(s.media-A.total_publicado.mean())<1e-10)
pairs=pd.read_csv(D/"pares_inversoes.csv")
x=A.nota_prova.to_numpy(float);y=A.total_publicado.to_numpy(float)
nv=ni=nt=ny=0
for i in range(len(x)):
 for j in range(i+1,len(x)):
    dx=x[i]-x[j];dy=y[i]-y[j]
    if abs(dx)<1e-9:nt+=1
    if abs(dy)<1e-9:ny+=1
    if abs(dx)>1e-9 and abs(dy)>1e-9:
        nv+=1
        ni+=int(dx*dy<0)
row=pairs[pairs.cenario=="objetiva_sem_bonus"].iloc[0]
chk("pares_305",int(row.pares_total)==len(x)*(len(x)-1)//2==46360)
chk("pares_comparaveis",int(row.pares_comparaveis)==nv)
chk("inversoes_indep",int(row.invertidos)==ni)
chk("empates_indep",int(row.empates_primeira)==nt and int(row.empates_final)==ny)
cor=pd.read_csv(D/"correlacoes.csv")
rho=stats.spearmanr(x,y).statistic
cr=cor[(cor.pares=="prova_vs_final")].iloc[0]
chk("spearman",abs(rho-cr.spearman)<1e-10)
br=pd.read_csv(D/"bonificacoes_observadas.csv")
for z in br.itertuples():
    chk("bonus_"+z.etapa,int((A[z.etapa]>0).sum())==z.pessoas_com_bonus and abs(A[z.etapa].sum()-z.soma_pontos_bonus)<1e-10)
Q=pd.read_csv(D/"catalogo_questoes_limites.csv")
chk("sem_dificuldade_fingida",len(Q)==400 and Q.dificuldade_empirica.isna().all() and Q.discriminacao_empirica.isna().all())
chk("sem_respostas_individuais",pd.read_csv(P/"respostas_individuais.csv").empty)
MOD=pd.read_csv(D/"modelos_hipoteticos_massa.csv")
m=R["media_prova_publicados"];sd=R["dp_prova_publicados"]
for name,g in MOD.groupby("familia"):
    g=g.sort_values("nota_bruta");xx=g.nota_bruta.to_numpy(float);p=g.massa.to_numpy(float)
    chk("massa_"+name,abs(sum(p)-1)<1e-8 and min(p)>=-1e-12)
    chk("momento_"+name,abs(np.dot(xx,p)-m)<1e-6 and abs(math.sqrt(np.dot((xx-m)**2,p))-sd)<1e-6)
    chk("nao_populacao_real_"+name,not ("presentes_reais" in R and isinstance(R["presentes_reais"],int)))
bounds=pd.read_csv(D/"limites_LP_momentos.csv")
grid=np.arange(101,dtype=float)*.9
mat=np.stack([np.ones(101),grid,grid*grid])
rhs=[1,m,m*m+sd*sd]
for b in bounds.itertuples():
    w=(grid>=b.limiar_bruto_ge-1e-9).astype(float)
    lo=optimize.linprog(w,A_eq=mat,b_eq=rhs,bounds=(0,None),method="highs")
    hi=optimize.linprog(-w,A_eq=mat,b_eq=rhs,bounds=(0,None),method="highs")
    chk("LP_"+str(b.limiar_bruto_ge),lo.success and hi.success and
        abs(b.limite_inferior-lo.fun)<1e-7 and abs(b.limite_superior+hi.fun)<1e-7)
chk("sem_classe_final_inventada",not (D/"classificacao_real.csv").exists())
chk("sem_posterior_MCMC",not (D/"posterior.csv").exists())
chk("sem_fase_E",R["nenhuma_fase_E_executada"] and not (Path("Fase_E")).exists())
chk("figuras_quatro",len(list(D.glob("fig_D*.png")))==4 and all(q.stat().st_size>5000 for q in D.glob("fig_D*.png")))
chk("motor_testes_todos",pd.read_csv(D/"testes_motor_D.csv").aprovado.all())
chk("sem_presenca_falsa",R["presentes_reais"]=="DESCONHECIDO" and R["inscricoes_publicadas"]==354)
chk("holdout_sem_alegar_validade_externa","nao calibracao externa" in R["internal_holdout"]["validade"])
pd.DataFrame(T).to_csv(D/"testes_independentes_D.csv",index=False)
result={"status":"APROVADO_COM_RESSALVAS_CIENTIFICAS","n_independentes":len(T),
        "aprovados":sum(a["passou"] for a in T),
        "n_publicados":len(A),"n_linhas":len(F),"correlacao_objetiva_final":rho,
        "inversoes":ni,"empates_objetiva":nt,
        "identificabilidade":"N de presentes e matrizes pessoa×item indisponíveis"}
(D/"auditoria_independente_D.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False))
