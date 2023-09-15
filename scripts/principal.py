import numpy as np
import pandas as pd
import CAGED.scripts.data_load as data_load
import openpyxl




dados = data_load.loadCleanDadosCaged()
print(dados.head())


# Grupo de ensino superior completo
"""grupo1 = dados[dados["cod_instrucao"] > 8]
grupo1 = grupo1[grupo1['salário'] != ',00']
grupo1 = grupo1.dropna(subset=['salário'])
for i in range(len(grupo1)):
    grupo1.iloc[i,6] = grupo1.iloc[i,6].replace(",", ".")
    print(i)

grupo1.to_excel("/home/tomas/Pacifica/CAGED/Dados/grupo1.xlsx", index=False)

"""
