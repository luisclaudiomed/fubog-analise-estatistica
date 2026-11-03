from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd, numpy as np, json, itertools, hashlib, sqlite3, math, platform
BASE=Path("Fase_B/saida_B"); OUT=Path("Fase_C");OUT.mkdir(exist_ok=True)
D=lambda x: Decimal(str(x))
scores=pd.read_csv(BASE/"pontuacoes.csv")
keys=pd.read_csv(BASE/"gabaritos.csv")
people=pd.read_csv(BASE/"candidatos.csv")
calls=pd.read_csv(BASE/"convocacoes.csv")
checks=[]
def test(name,condition,note=""):
    checks.append({"teste":name,"resultado":"PASS" if bool(condition) else "FAIL","nota":note})
    if not condition: raise AssertionError(f"{name}: {note}")
def pts(p, bonus=False):
    if p is None:return None
    q=D(p)
    if q<0 or q>90:raise ValueError("prova fora da escala")
    if bonus and q>=D(45):
        q=min(D(90),q+D("0.10")*q)
    return q
def curr(c,bonus=False):
    if c is None:return None
    q=D(c)
    if q<0 or q>10:raise ValueError("curriculo fora da escala")
    if bonus and q>0:q=min(D(10),q+D(".10")*q)
    return q
def eligible(raw,curricular):
    if raw is None or curricular is None:return None
    return D(raw)>=D(45) and D(curricular)>D(0)
def total(proof,cur,bonus_proof=0,bonus_cur=0):
    if proof is None or cur is None:return None
    arr=[proof,cur,bonus_proof,bonus_cur]
    if any(x is None for x in arr):return None
    return sum(map(D,arr))
test("C_BASE_305_PESSOAS",len(people)==305 and people.pid.is_unique)
test("C_610_DOCUMENTOS",len(scores)==610 and set(scores.documento)=={"A13","A15"})
test("C_GRAO",not scores[["pid","documento"]].duplicated().any())
test("C_GABARITOS_800",len(keys)==800 and keys.groupby(["documento","tipo"]).size().eq(100).all())
test("C_INTERVALO_PROVA",scores.nota_prova.between(0,90).all())
test("C_ESCALA_GRADE_OBSERVADA",np.max(abs(scores.nota_prova.to_numpy()/0.9-np.rint(scores.nota_prova.to_numpy()/0.9)))<1e-8)
test("C_CURRICULO_LIMITES",scores.nota_curriculo.between(0,10).all())
test("C_MINIMA_NA_AMOSTRA_PUBLICADA",scores.nota_prova.ge(45).all())
test("C_BONUS_ETAPA_1_CAP",((scores.nota_prova+scores.bonus_prova)<=90.0000001).all())
test("C_BONUS_ETAPA_2_CAP",((scores.nota_curriculo+scores.bonus_curriculo)<=10.0000001).all())
test("C_BONUS_CURRICULO_NAO_ZERO",((scores.bonus_curriculo==0)|(scores.nota_curriculo>0)).all())
test("C_SOMA_610",all(total(r.nota_prova,r.nota_curriculo,r.bonus_prova,r.bonus_curriculo)==D(r.total_publicado) for r in scores.itertuples()))
piv=scores.pivot(index="pid",columns="documento",values=["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo","total_publicado"])
test("C_DUAS_PUBLICACOES_CONCORDAM",all(np.max(abs(piv[(col,"A13")]-piv[(col,"A15")]))<1e-8 for col in ["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo","total_publicado"]))
test("C_PISO_45_PREBONUS",pts("44.10",True)==D("44.10") and pts("45",True)==D("49.5"))
test("C_TETO_BONUS_OBJ",pts("90",True)==D("90"))
test("C_TETO_BONUS_CUR",curr("9.75",True)==D("10"))
test("C_CURRICULO_ZERO_ELIMINA",eligible("72","0") is False and eligible("72","0.1") is True)
test("C_NULL_PROPAGA",total(None,5) is None and eligible(None,4) is None)
test("C_EXTREMOS",total(90,10)==100 and curr(0,True)==0)
def annulled_score(answers,final_keys,annulled,weight):
    # regra 7.29: crédito universal somente ao tipo de prova correspondente; nunca muda gabarito oficial
    return sum(D(weight) for q,ans in answers.items() if q in annulled or ans==final_keys.get(q))
test("C_ANULADA_CREDITO_UNIVERSAL",annulled_score({1:"A",2:"B"},{1:"C",2:"A"},{2},"0.9")==D("0.9"))
test("C_DESEMPATE_TOPO_DESCONHECIDO", sorted([{"final":80,"prova":70},{"final":80,"prova":72}],key=lambda a:(-a["final"],-a["prova"]))[0]["prova"]==72)
test("C_SOMENTE_HIPOTESES_IDENTIFICAVEIS",len(calls)==308 and calls.pid.isna().sum()>0)
# Implementacao independente em inteiros centesimais para confirmar toda a base.
def as_cent(x):
    return int((D(x)*100).quantize(D("1"),rounding=ROUND_HALF_UP))
bad=[]
for r in scores.itertuples():
    c=as_cent(r.nota_prova)+as_cent(r.bonus_prova)+as_cent(r.nota_curriculo)+as_cent(r.bonus_curriculo)
    if c!=as_cent(r.total_publicado):bad.append(r.pid)
test("C_MOTOR_INDEPENDENTE_610",len(bad)==0)
con=sqlite3.connect(BASE/"fubog_ingresso_2026_B.sqlite")
test("C_SQLITE_INTEGRO",con.execute("pragma integrity_check").fetchone()[0]=="ok")
test("C_SQLITE_610",con.execute("select count(*) from pontuacoes").fetchone()[0]==610);con.close()
# Sem respostas individuais e sem notas de todos os candidatos de outras instituicoes: NAO reconstruir posicoes oficiais.
out={
 "edicao":"FUBOG_INGRESSO_2026","regime":"PSU-GO, prova unificada; sem z-score",
 "etapa1_max":90,"etapa2_max":10,"total_max":100,"n_questoes_gabarito_por_tipo":100,
 "nota_minima_prova":45,"curriculo_zero_elimina":True,
 "bonus_MFC_percentual":10,"bonus_etapas_separadas_com_teto":True,
 "selecionados_por_vaga_ate":15,
 "cotas_versoes":{"edital_original":{"AC":4,"PcD":1,"pretos":1},"errata_jan":{"pretos_pardos":1},"retificacao_11fev":{"AC":6,"PcD":1,"pretos_pardos":1}},
 "empates":{"nota_final":True,"maior_primeira_etapa":True,"idade_60_ou_mais":True,"maior_idade":True},
 "nao_identificavel":["arredondamento literal","prova definitiva tipo/itens anulados","respostas individuais","idade para desempates","notas dos candidatos de outros programas","documentos e pontuacoes curriculares individuais"],
 "riscos":["retificacao judicial na modalidade de reserva","relatorio de notas nao classificatorio","preferencias mudam a convocacao","141 eventos sem PID vinculavel"],
 "B_n_pessoas":305,"B_n_linhas_conferidas":len(scores),"B_chamadas_com_id_nao_seguro":int(calls.pid.isna().sum()),
 "verificacoes":len(checks),"falhas":sum(c["resultado"]=="FAIL" for c in checks)
}
(OUT/"normas_fubog_2026_C.json").write_text(json.dumps(out,indent=2,ensure_ascii=False))
pd.DataFrame(checks).to_csv(OUT/"testes_motor_C.csv",index=False)
pd.DataFrame({"pid":scores.pid,"documento":scores.documento,
"nota_final_publicada":scores.total_publicado,
"nota_reconstruida":scores[["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo"]].sum(axis=1),
"residuo":scores[["nota_prova","bonus_prova","nota_curriculo","bonus_curriculo"]].sum(axis=1)-scores.total_publicado}).to_csv(OUT/"reconciliacao_final_C.csv",index=False,float_format="%.12g")
print(json.dumps({"status":"PASSOU_COM_RESSALVAS",**{k:out[k] for k in ["B_n_pessoas","B_n_linhas_conferidas","B_chamadas_com_id_nao_seguro","verificacoes","falhas"]}},ensure_ascii=False))
