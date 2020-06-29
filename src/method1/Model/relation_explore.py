import matplotlib.pyplot as plt
#import seaborn as sns
#import pandas as pd
import json

f=open("../PDI/s_difficulty_dict_with_metrics.json",encoding="utf8")
res=f.read()
diff_dict=json.loads(res)

#matplotlib
cc_score=[]
cc_lvl=[]
LLOC=[]
u_rator=[]
u_rand=[]
rator=[]
rand=[]
RDI=[]
for v in diff_dict.values():
    cc_score.append(v["avg_cc_score"])
    cc_lvl.append(v["avg_cc_level"])
    LLOC.append(v["avg_LLOC"])
    u_rator.append(v["avg_unique_operator_Nums"])
    u_rand.append(v["avg_unique_operand_Nums"])
    rator.append(v["avg_operator_Nums"])
    rand.append(v["avg_operand_Nums"])
    RDI.append(v["RDI"])
# plt.scatter(cc_score,RDI)
# plt.show()
# plt.scatter(cc_lvl,RDI)
# plt.show()
# plt.scatter(LLOC,RDI)
# plt.show()
plt.scatter(u_rator,RDI)
plt.show()
plt.scatter(u_rand,RDI)
plt.show()
plt.scatter(rator,RDI)
plt.show()
plt.scatter(rand,RDI)
plt.show()

# #Seaborn
# df=pd.DataFrame({'x':,'y':})
# sns.jointplot(x="x",y="y",data=df,kind='scatter')