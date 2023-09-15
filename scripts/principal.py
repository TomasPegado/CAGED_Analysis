import numpy as np
import pandas as pd
import CAGED.scripts.data_load as data_load
import openpyxl
from scipy.stats import t
from statsmodels.stats import weightstats




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
grupo1 = pd.read_excel("/home/tomas/Pacifica/CAGED/Dados/grupo1.xlsx")

grupo1.head()
grupo1.groupby('sexo').describe()['salário']

grupo1_contratados = grupo1[grupo1['saldomovimentação'] == 1]
grupo1_contratados.groupby('sexo').describe()['salário']

# Grupo dos contratados

grupo1_contratados = grupo1_contratados.dropna()

## Testar se homens ganham mais que mulheres
"""
    H0: Uma pessoa ser do sexo masculino não afeta o valor do seu salário na contratação
    Ha: Uma pessoa ser do sexo masculino afeta positivamente seu salário na contratação
    """
amostra_contratados = grupo1_contratados.groupby('sexo').sample(n=10000) # Amostra com 10000 cada
amostra_contratados.groupby('sexo').describe()['salário']


### Assumindo Ho verdadeira
media_populacional=0

### Evidencias amostrais
media_amostral = 5084.403013 - 3854.108434
dpM = 20738.744125
dpF = 25815.835545
desvio_padrao_amostral = dpM - dpF
n = 10000
graus_liberdade=(n-1)*2
alfa = 0.05
grau_confiança = 1-alfa

t_obs=(media_amostral-media_populacional)/(np.sqrt((dpM/n)+(dpF/n)))
t_critico=t.ppf(1-(alfa), graus_liberdade)

print(f't_obs: {t_obs} e t_critico: {t_critico}')
if t_obs>t_critico:
    print('t_obs > t_critico : Rejeita H0')
else:
    print('Não rejeita H0')

#### Valor P:

valor_p=(1-t.cdf(t_obs,graus_liberdade))

print(f'alfa: {alfa}', f'x',  f'valor-p: {valor_p}' )
if valor_p < alfa:
    print(f'valor-p < alfa => Rejeito Ho')
else:
    print(f'valor-p > alfa => Não rejeito Ho')

#### Effect Size:

r=round(np.sqrt((t_obs**2)/(t_obs**2+(graus_liberdade))), 3)
r_square=round(r**2, 3)
r,r_square

print(f'r: {r}')  
print(f'r_square: {r_square}')
