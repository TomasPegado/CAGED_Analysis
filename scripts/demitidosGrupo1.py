import numpy as np
import pandas as pd
import CAGED.scripts.data_load as data_load
import openpyxl
from scipy.stats import t
from statsmodels.stats import weightstats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


grupo1 = pd.read_excel("/home/tomas/Pacifica/CAGED/Dados/grupo1.xlsx")

grupo1.head()
grupo1.groupby('sexo').describe()['salário']

# Grupo dos demitidos
grupo1_demitidos = grupo1[grupo1['saldomovimentação'] == -1]
grupo1_demitidos = grupo1_demitidos.dropna()

## Média Salarial por sexo
grupo1_demitidos.groupby('sexo').describe()['salário']

## Médial Salarial por raca
grupo1_demitidos.groupby('raça').describe()['salário']