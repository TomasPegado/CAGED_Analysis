import numpy as np
import pandas as pd
import CAGED.scripts.data_load as data_load
import openpyxl
from scipy.stats import t
from statsmodels.stats import weightstats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


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

#5) Intervalo de confiança para a diferença entre as médias assumindo variâncias diferentes
    #Estatística do Teste T - presumindo variancias diferentes

t_obs, pvalue, gl = weightstats.ttest_ind(amostra_contratados[ amostra_contratados['sexo']=='M']['salário'] , amostra_contratados[ amostra_contratados['sexo']=='F' ]['salário'], alternative="two-sided", usevar="unequal")

n_M=len(amostra_contratados[amostra_contratados['sexo']=='M'])
mean_M=amostra_contratados[amostra_contratados['sexo']=='M']['salário'].mean()
std_M=amostra_contratados[amostra_contratados['sexo']=='M']['salário'].std()
var_M=std_M**2

n_F=len(amostra_contratados[amostra_contratados['sexo']=='F'])
mean_F=amostra_contratados[amostra_contratados['sexo']=='F']['salário'].mean()
std_F=amostra_contratados[amostra_contratados['sexo']=='F']['salário'].std()
var_F=std_F**2


t_interval = t.interval( grau_confiança , gl , loc= mean_M-mean_F, scale= np.sqrt(var_M/n_M + var_F/n_F) )

print(f'Intervalo 95%: {t_interval}') 

#### Effect Size:

r=round(np.sqrt((t_obs**2)/(t_obs**2+(graus_liberdade))), 3)
r_square=round(r**2, 3)
r,r_square

print(f'r: {r}')  
print(f'r_square: {r_square}')


#### Linear Regression

amostra_contratados['sexo_dummy'] = amostra_contratados['sexo'].map({'M':0, 'F': 1})
amostra_contratados.groupby('sexo_dummy').describe()['salário']

y = amostra_contratados['salário']
x1 = amostra_contratados['sexo_dummy']
x1 = sm.add_constant(x1)

model = sm.OLS(y, x1).fit()

# Imprimindo o resultado
print(model.summary())
 
