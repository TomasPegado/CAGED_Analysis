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
grupo1.groupby('raça').describe()['salário']

# Grupo dos contratados
grupo1_contratados = grupo1[grupo1['saldomovimentação'] == 1]
grupo1_contratados = grupo1_contratados.dropna()

## Média Salarial por sexo
grupo1_contratados.groupby('sexo').describe()['salário']

## Médial Salarial por raca
grupo1_contratados.groupby('raça').describe()['salário']

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
media_amostral = 5148.613408 - 3520.964574
dpM = 18606.713372
dpF = 9112.501700
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

r=round(np.sqrt((t_obs**2)/(t_obs**2+(gl))), 3)
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

## Testar se Brancos com ensino superior ganham mais que outras raças
"""
    H0: Uma pessoa ser da raça branca não afeta o valor do seu salário na contratação
    Ha: Uma pessoa ser da raça branca afeta positivamente seu salário na contratação
    """

amostra_contratatBrancos = grupo1_contratados.replace({'raça': {'Amarela': 'Outra', 'Indígena': 'Outra', 'Parda': 'Outra', 'Preta': 'Outra'}}, inplace=False)
 
amostra_contratatBrancos = amostra_contratatBrancos[amostra_contratatBrancos['raça'] != 'Não Informado']
amostra_contratatBrancos = amostra_contratatBrancos.groupby('raça').sample(n=10000)

amostra_contratatBrancos.groupby('raça').describe()['salário']
### Assumindo Ho verdadeira
media_populacional=0

### Evidencias amostrais
media_amostral = 4873.884372 - 3660.388454
dpB = 25706.513090
dpO = 7729.766801
desvio_padrao_amostral = dpB - dpO
n = 10000
graus_liberdade=(n-1)*2
alfa = 0.05
grau_confiança = 1-alfa

t_obs=(media_amostral-media_populacional)/(np.sqrt((dpB/n)+(dpO/n)))
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

#### Intervalor de Confiança

t_obs, pvalue, gl = weightstats.ttest_ind(amostra_contratatBrancos[ amostra_contratatBrancos['raça']=='Branca']['salário'] , amostra_contratatBrancos[ amostra_contratatBrancos['raça']=='Outra' ]['salário'], alternative="two-sided", usevar="unequal")

n_B=len(amostra_contratatBrancos[amostra_contratatBrancos['raça']=='Branca'])
mean_B=amostra_contratatBrancos[amostra_contratatBrancos['raça']=='Branca']['salário'].mean()
std_B=amostra_contratatBrancos[amostra_contratatBrancos['raça']=='Branca']['salário'].std()
var_B=std_B**2

n_O=len(amostra_contratatBrancos[amostra_contratatBrancos['raça']=='Outra'])
mean_O=amostra_contratatBrancos[amostra_contratatBrancos['raça']=='Outra']['salário'].mean()
std_O=amostra_contratatBrancos[amostra_contratatBrancos['raça']=='Outra']['salário'].std()
var_O=std_O**2

t_interval = t.interval( grau_confiança , gl , loc= mean_B-mean_O, scale= np.sqrt(var_B/n_B + var_O/n_O) )

print(f'Intervalo 95%: {t_interval}') 

#### Effect Size:

r=round(np.sqrt((t_obs**2)/(t_obs**2+(gl))), 3)
r_square=round(r**2, 3)
r,r_square

print(f'r: {r}')  
print(f'r_square: {r_square}')