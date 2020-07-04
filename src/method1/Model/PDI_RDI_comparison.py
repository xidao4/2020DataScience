import json
import prettytable as pt
import os
from matplotlib import pyplot as plt
import numpy as np
from pandas import *

f = open("../PDI/s_difficulty_dict_with_metrics.json", encoding="utf8")
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