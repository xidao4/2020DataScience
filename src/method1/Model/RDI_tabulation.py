import json
import prettytable as pt
import os
from matplotlib import pyplot as plt
import numpy as np
from pandas import *

# 获得RDI数值和RDI各项参数的列表
f = open("../PDI/d_difficulty_dict_with_metrics_2.json", encoding="utf8")
res = f.read()
data = json.loads(res)
data = list(dict.values(data))

tb = pt.PrettyTable()
tb.field_names = ["RDI", "avg_cc_score", "avg_cc_level", "avg_LLOC", "avg_unique_operator_Nums",
                  "avg_unique_operand_Nums", "avg_operator_Nums", "avg_operand_Nums"]
for rec in data:
    lis = [rec["RDI"], rec["avg_cc_score"], rec["avg_cc_level"], rec["avg_LLOC"], rec["avg_unique_operator_Nums"],
           rec["avg_unique_operand_Nums"], rec["avg_operator_Nums"], rec["avg_operand_Nums"]]
    tb.add_row(lis)

print(tb)