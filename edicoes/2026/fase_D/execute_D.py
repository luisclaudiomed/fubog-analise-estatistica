"""FUBOG ingresso 2026 — Fase D; descrição de PUBLICADOS, não de presentes.
Entradas: A13 e A15 de Fase B (duas versões de 305 pessoas); nenhuma imputação.
"""
from pathlib import Path
from itertools import combinations
import numpy as np, pandas as pd, json, math, platform
from scipy import stats, optimize, special
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE=Path("Fase_B/saida_B")
OUT=Path("Fase_D");OUT.mkdir(parents=True,exist_ok=True)
OBS=BASE/"pontuacoes.csv"
T=[]
def verify(name, condition):
    T.append(dict(teste=name,aprovado=bool(condition)))
    if not condition:raise AssertionError(name)
def save(df,name):
    pd.DataFrame(df).to_csv(OUT/name,index=False,float_format="%.12g")
def js(obj,name):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str)+"\n")
def cv(v):return float(v) if pd.notna(v) else None

a=pd.read_csv(OBS)
persons=pd.read_csv(BASE/"candidatos.csv")
keys=pd.read_csv(BASE/"gabaritos.csv")
questions=pd.read_csv(BASE/"questoes.csv")
inscriptions=pd.read_csv(BASE/"estatisticas_inscricoes.csv")
answers=pd.read_csv(BASE/"respostas_individuais.csv")
external=pd.read_csv(BASE/"estatisticas_externas.csv")
calls=pd.read_csv(BASE/"convocacoes.csv")
changes=pd.read_csv(BASE/"alteracoes_gabarito.csv")
verify("D_grao_610_305",len(a)==610 and persons.pid.nunique()==305 and a[["pid","documento"]].duplicated().sum()==0)
obs=a[a.documento=="A15"].copy().sort_values("pid").reset_index(drop=True)
prev=a[a.documento=="A13"].copy().sort_values("pid").reset_index(drop=True)
verify("D_305_sem_duplicacao",len(obs)==305 and obs.pid.is_unique)
verify("D_duas_fontes_identicas_nota",np.allclose(obs[["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo","total_publicado"]],
prev[["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo","total_publicado"]],rtol=0,atol=1e-8))
verify("D_soma_etapas",np.allclose(obs[["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo"]].sum(axis=1),obs.total_publicado,rtol=0,atol=1e-8))
verify("D_questoes_gabaritos",len(questions)==400 and len(keys)==800)
verify("D_respostas_vazias",answers.empty and questions.enunciado.isna().all())
verify("D_ha_354_inscricoes_nao_presentes",int(inscriptions.iloc[0].total_inscricoes)==354 and pd.isna(inscriptions.iloc[0].total_presentes))
verify("D_sem_ranking_oficial",pd.read_csv(BASE/"classificacoes.csv").posicao.isna().all())
verify("D_nao_imputar_chamada",calls.pid.isna().sum()==141)

fields=["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo","total_publicado"]
groups={"FUBOG_publicados_A15":obs}
for p,v in obs.groupby("preferencia",dropna=False):
    if pd.notna(p):groups["preferencia_"+str(p)]=v
des=[]
for group,df in groups.items():
 for col in fields:
    x=df[col].dropna().to_numpy(float)
    if not len(x):continue
    q=lambda z:float(np.quantile(x,z,method="linear"))
    des.append(dict(populacao=group,campo=col,n=len(x),media=float(np.mean(x)),mediana=q(.5),
                    desvio_amostral=float(np.std(x,ddof=1)) if len(x)>1 else np.nan,
                    desvio_populacao_descritivo=float(np.std(x,ddof=0)),
                    q25=q(.25),q75=q(.75),IQR=q(.75)-q(.25),
                    MAD=float(np.median(np.abs(x-np.median(x)))),
                    P90=q(.9),P95=q(.95),P97=q(.97),P98=q(.98),P99=q(.99),
                    minimo=float(x.min()),maximo=float(x.max()),unidade="pontos; SOMENTE publicados"))
save(des,"estatisticas_publicados.csv")
verify("D_descritivas_global",len([r for r in des if r["populacao"]=="FUBOG_publicados_A15"])==5)

# Empates, correlações e inversões são descritivos, NÃO causais
first=obs.nota_prova.to_numpy(float)+obs.bonus_prova.to_numpy(float)
final=obs.total_publicado.to_numpy(float)
obj_only=obs.nota_prova.to_numpy(float)
bonus=(obs.bonus_prova.to_numpy(float)+obs.bonus_curriculo.to_numpy(float))
curr=obs.nota_curriculo.to_numpy(float)+obs.bonus_curriculo.to_numpy(float)
pairs=[]
for label,xx in [("objetiva_sem_bonus",obj_only),("primeira_com_bonus",first)]:
 d=xx[:,None]-xx[None,:];e=final[:,None]-final[None,:];tri=np.triu(np.ones(d.shape,dtype=bool),1)
 tie_first=tri & (abs(d)<1e-9)
 tie_final=tri & (abs(e)<1e-9)
 comp=tri & (~tie_first) & (~tie_final)
 reversed_pairs=int((comp & (d*e<0)).sum())
 concordant=int((comp & (d*e>0)).sum())
 total_pairs=len(xx)*(len(xx)-1)//2
 assert reversed_pairs+concordant+int(tie_first.sum())+int((tie_final&~tie_first).sum())==total_pairs
 pairs.append(dict(cenario=label,pessoas=len(xx),pares_total=total_pairs,empates_primeira=int(tie_first.sum()),
    empates_final=int(tie_final.sum()),empates_ambas=int((tie_first&tie_final).sum()),
    pares_comparaveis=int(comp.sum()),concordantes=concordant,invertidos=reversed_pairs,
    taxa_inversao_condicional=reversed_pairs/int(comp.sum()) if comp.sum() else np.nan))
save(pairs,"pares_inversoes.csv")
tie=[]
for field in ["nota_prova","total_publicado"]:
 counts=obs[field].value_counts()
 for val,n in counts[counts>1].sort_index(ascending=False).items():
    tie.append(dict(campo=field,nota=float(val),pessoas_empatadas=int(n),pares_empatados=int(n*(n-1)/2)))
save(tie,"grupos_empates.csv")
corr=[]
for xname,x in [("prova",obj_only),("primeira_com_bonus",first),("curriculo_com_bonus",curr),("bonus_total",bonus)]:
 for yname,y in [("curriculo",curr),("final",final)]:
    with np.errstate(invalid="ignore"):
        if np.unique(x).size<2 or np.unique(y).size<2:continue
        rho=stats.spearmanr(x,y).statistic
        tau=stats.kendalltau(x,y).statistic
        rr=np.corrcoef(x,y)[0,1]
    corr.append(dict(pares=xname+"_vs_"+yname,n=len(x),spearman=float(rho),
                     kendall_tau_b=float(tau),pearson=float(rr),
                     tipo="estatistica_descritiva;amostra_publicada_e_selecionada"))
save(corr,"correlacoes.csv")
verify("D_inversoes_305",all(r["pares_total"]==46360 for r in pairs))

# Bônus observáveis; eficácia causal e elegibilidade individual não identificadas
bonus_rows=[]
for field in ["bonus_prova","bonus_curriculo"]:
 x=obs[field].to_numpy(float)
 bonus_rows.append(dict(etapa=field,pessoas_com_bonus=int(np.count_nonzero(x>0)),
         soma_pontos_bonus=float(np.sum(x)),media_bonus_dentre_bonificados=float(np.mean(x[x>0])) if (x>0).any() else 0,
         maxima_observada=float(np.max(x)),n_total=len(x)))
save(bonus_rows,"bonificacoes_observadas.csv")
verify("D_sem_bonus_ficticio",all(r["n_total"]==305 for r in bonus_rows))

# Catálogo: 4 provas × 100 posições, SEM enunciados ou dificuldade empírica
catalog=questions.copy()
catalog["dificuldade_empirica"]=np.nan
catalog["discriminacao_empirica"]=np.nan
catalog["status_tematizacao"]="IMPOSSIVEL_SEM_CADERNO_OFICIAL"
catalog.to_csv(OUT/"catalogo_questoes_limites.csv",index=False)
gabs=keys.groupby(["documento","tipo"],dropna=False).size().rename("n").reset_index()
verify("D_gabaritos_4x2x100",len(gabs)==8 and (gabs.n==100).all())
verify("D_gabarito_32_diferencas",len(changes)==32)

# Identificabilidade: duas versões do mesmo grupo NÃO duplicam informação populacional
mu=float(obj_only.mean());sd=float(obj_only.std(ddof=0))
grid=np.arange(101,dtype=float)*.9
pmfs={};diag=[]
p0=mu/90
ratio=(sd/.9)**2/(100*p0*(1-p0))
if ratio>1+1e-9 and ratio<100-1e-9:
 conc=(100-ratio)/(ratio-1)
 alpha=p0*conc;beta=(1-p0)*conc
 pmfs["beta_binomial_published_moments"]=stats.betabinom.pmf(np.arange(101),100,alpha,beta)
else:
 diag.append(dict(familia="beta_binomial_published_moments",estado="inviavel_momentos",
                    motivo=f"dispersao de publicados={ratio:.4f}; binomial exige fator de variancia > 1"))
def max_ent(tmu,tsd):
 z=(grid-tmu)/tsd
 def probs(theta):
    q=theta[0]*z+theta[1]*z*z
    return np.exp(q-special.logsumexp(q))
 def moments(theta):
    p=probs(theta)
    return np.array([float(p@z),float(p@(z*z)-1)])
 sol=optimize.least_squares(moments,[0,-.5],xtol=1e-12,gtol=1e-12,ftol=1e-12,max_nfev=1000)
 if np.max(np.abs(moments(sol.x)))>1e-7:raise ArithmeticError("Maxent moments not reproducible")
 return probs(sol.x)
pmfs["max_entropy_published_moments"]=max_ent(mu,sd)
delta=min(2.,sd*.45)
sd_internal=math.sqrt(sd*sd-delta*delta)
pmfs["mixture_published_moments"]=.5*max_ent(mu-delta,sd_internal)+.5*max_ent(mu+delta,sd_internal)
for name,p in pmfs.items():
 verify("D_modelo_massas_"+name,abs(p.sum()-1)<1e-8 and abs(p@grid-mu)<1e-6
           and abs(math.sqrt(p@((grid-mu)**2))-sd)<1e-6)
 diag.append(dict(familia=name,estado="ajuste_a_dois_momentos_DOS_PUBLICADOS",
                    media=mu,desvio=sd,p_ge_75p6=float(p[grid>=75.6-1e-8].sum()),
                    nota="NAO descreve distribuicao de todos os presentes"))
save(diag,"diagnostico_modelos.csv")
save([dict(familia=name,nota_bruta=float(score),massa=float(p[i]))
     for name,p in pmfs.items() for i,score in enumerate(grid)],"modelos_hipoteticos_massa.csv")

# Programação linear: limites sob os momentos dos publicados apenas, suporte artificial [0,90].
limits=[]
mat=np.vstack([np.ones(len(grid)),grid,grid**2])
rhs=np.array([1.,mu,mu**2+sd**2])
for threshold in [63.,67.5,72.,75.6,81.]:
 selector=(grid>=threshold-1e-9).astype(float)
 low=optimize.linprog(selector,A_eq=mat,b_eq=rhs,bounds=(0,None),method="highs")
 high=optimize.linprog(-selector,A_eq=mat,b_eq=rhs,bounds=(0,None),method="highs")
 verify("D_LP_soluvel_"+str(threshold),low.success and high.success)
 limits.append(dict(limiar_bruto_ge=threshold,limite_inferior=float(low.fun),limite_superior=float(-high.fun),
            momento="media+DP descritivos PUBLICADOS, tratados como exatos",populacao_real_geral="NAO_IDENTIFICAVEL"))
save(limits,"limites_LP_momentos.csv")

# Validação interna holdout SEM interpretar como calibração externa
rng=np.random.default_rng(2026);idx=rng.permutation(len(obj_only))
train=idx[:round(.7*len(idx))];test=idx[round(.7*len(idx)):]
hmu=float(obj_only[train].mean());hsd=float(obj_only[train].std(ddof=0))
hp=max_ent(hmu,hsd)
observed_tail=float((obj_only[test]>=75.6-1e-8).mean())
pred_tail=float(hp[grid>=75.6-1e-8].sum())
internal=dict(treino_n=len(train),teste_n=len(test),corte_bruto=75.6,
              proporcao_observada_teste=observed_tail,proporcao_hipotetica_treino=pred_tail,
              erro_absoluto=abs(observed_tail-pred_tail),
              validade="somente dentro dos 305 publicados; nao calibracao externa")
js(internal,"holdout_publicados.json")
verify("D_holdout_sem_vazamento",set(train).isdisjoint(set(test)) and len(train)+len(test)==305)

fig,ax=plt.subplots(figsize=(9,5));ax.hist(obj_only,bins=np.arange(-.45,90.91,.9),edgecolor="white")
ax.set(title="FUBOG 2026 — prova objetiva dos 305 publicados",xlabel="Pontos na prova (0–90)",ylabel="Número de pessoas publicadas")
ax.grid(axis="y",alpha=.2);fig.tight_layout();fig.savefig(OUT/"fig_D1_objetiva_publicados.png",dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5));ax.scatter(obj_only,obs.nota_curriculo.to_numpy(float),s=14,alpha=.65)
ax.set(title="FUBOG 2026 — objetiva versus currículo (publicados)",xlabel="Prova objetiva (pontos)",ylabel="Currículo (pontos)")
ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/"fig_D2_prova_curriculo.png",dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5))
ax.hist(obj_only,bins=np.arange(-.45,90.91,.9),density=True,alpha=.25,label="Publicados (histograma)")
for name,p in pmfs.items():ax.plot(grid,p/.9,label=name.replace("_"," "),linewidth=1.5)
ax.set(title="Hipóteses por dois momentos — NÃO representam presentes",xlabel="Nota bruta",ylabel="Densidade");ax.legend(fontsize=8);fig.tight_layout()
fig.savefig(OUT/"fig_D3_modelos_hipoteticos.png",dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5))
a1=obs.groupby("preferencia").agg(n=("pid","size"),media=("total_publicado","mean")).reset_index()
ax.bar(a1.preferencia.astype(str),a1.media)
ax.set(title="Média final por ordem de preferência — só publicados",xlabel="Preferência registrada",ylabel="Média nota final (pontos)")
ax.grid(axis="y",alpha=.2);fig.tight_layout();fig.savefig(OUT/"fig_D4_preferencias.png",dpi=150);plt.close(fig)

verify("D_figuras_quatro",len(list(OUT.glob("fig_D*.png")))==4)
verify("D_nenhum_rank_ou_presenca_inferidos",not (OUT/"classificacao_real.csv").exists())
verify("D_nao_confunde_versoes",len(obs)==305 and len(prev)==305)
save(T,"testes_motor_D.csv")
report=dict(edicao="FUBOG_INGRESSO_2026",fase="D",
    observados_unicos=len(obs),linhas_fontes=len(a),inscricoes_publicadas=354,presentes_reais="DESCONHECIDO",
    media_prova_publicados=mu,dp_prova_publicados=sd,mediana_final_publicados=float(np.median(final)),
    media_final_publicados=float(np.mean(final)),P95_final_publicados=float(np.quantile(final,.95)),
    inversoes_ordenacao=pairs,correlacoes=corr,
    bonus=bonus_rows,models=diag,lp_bounds=limits,internal_holdout=internal,
    testes=len(T),passaram=sum(x["aprovado"] for x in T),
    sistema={"python":platform.python_version(),"numpy":np.__version__,"scipy":__import__("scipy").__version__},
    riscos=["ausencia de respostas pessoa×questao","cadernos oficiais indisponiveis","gabarito definitivo nao consolidado",
        "305 publicados != 354 inscritos != presentes","141 eventos sem vinculo seguro",
        "notas finais nao constituem ranking oficial","parametros modelos condicionais apenas aos publicados"],
    nenhuma_fase_E_executada=True)
js(report,"resumo_D.json")
print(json.dumps({"status":"CALCULADO_AGUARDANDO_AUDITORIA","observados":len(obs),"tests":len(T),
 "media_objetiva":round(mu,4),"desvio_objetiva":round(sd,4),"media_final":round(report["media_final_publicados"],4),
 "correlacao_objetiva_final":round(float(stats.spearmanr(obj_only,final).statistic),4),
 "modelos":list(pmfs)},ensure_ascii=False))
