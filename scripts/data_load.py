import numpy as np
import pandas as pd



def loadDadosCaged(): # Funcao para carregar os dados do CAGED para um dataframe

    dados_2023_7 = pd.read_csv("/home/tomas/Pacifica/CAGED/Dados/mov202307.txt", sep=";")
    return dados_2023_7

def filtro_Militares(valor): # Funcao para tirar cargos de militares
    limite_tamanho = 6
    return len(valor) >= limite_tamanho

def filtro_Publicos(valor): # Função para tirar cargos publicos
    return valor[0] != 1

def tirarPublicosMilitares(dados: pd.DataFrame):
    dados['cbo2002ocupação'] = dados['cbo2002ocupação'].astype('string')
    dados_novo = dados[dados['cbo2002ocupação'].apply(filtro_Militares)]
    dados_novo = dados[dados['cbo2002ocupação'].apply(filtro_Publicos)]
    return dados_novo

def deletarColunasInuteis(dados: pd.DataFrame):
    colunas = ['indtrabparcial','indtrabintermitente', 'origemdainformação', 'indicadordeforadoprazo','tamestabjan', 
                   'indicadoraprendiz','região', 'município', 'competênciadec', 'horascontratuais', 'subclasse', 'categoria',
                   'tipoempregador', 'tipoestabelecimento', 'tipodedeficiência','tipomovimentação','competênciamov','seção',
                   'unidadesaláriocódigo', 'valorsaláriofixo']
    
    dados.drop(columns=colunas, inplace=True)

def tratarSexo(dados: pd.DataFrame):
    dados.replace({'sexo': {np.int64(1): 'M', np.int64(3): 'F'}}, inplace=True)

def tratarUFs(dados: pd.DataFrame):

    ufs = pd.read_excel("/home/tomas/Pacifica/CAGED/Dimencoes/codigos_ufs.xlsx")
    dados_novo = pd.merge(dados, ufs, left_on="uf", right_on="Código", how="left")
    deletar_colunas = ['uf', 'Código', 'UF ']
    dados_novo.drop(columns=deletar_colunas, inplace=True)
    dados_novo.rename(columns={'Letras': 'uf'}, inplace=True)
    return dados_novo


def tratarInstruçao(dados: pd.DataFrame):

    graus = pd.read_excel("/home/tomas/Pacifica/CAGED/Dimencoes/grausdeinstrução.xlsx")
    dados_novo = pd.merge(dados, graus, left_on="graudeinstrução", right_on="Grau de Instrução", how="left")
    deletar_colunas = ["Grau de Instrução", "Nível de Escolaridade"]
    dados_novo.drop(columns=deletar_colunas, inplace=True)
    dados_novo.rename(columns={'graudeinstrução': 'cod_instrucao', 'Descrição': 'grau_de_instrução'}, inplace=True)
    return dados_novo

def trataRacaCor(dados: pd.DataFrame):

    dados_novo = dados[dados["raçacor"] != 9]
    racas = pd.read_excel("/home/tomas/Pacifica/CAGED/Dimencoes/raçacor.xlsx")
    dados_novo = pd.merge(dados_novo, racas, left_on="raçacor", right_on="codigo", how="left")
    deletar_colunas = ["codigo"]
    dados_novo.drop(columns=deletar_colunas, inplace=True)
    dados_novo.rename(columns={'raçacor': 'cod_racacor', 'descrição': 'raça'}, inplace=True)
    return dados_novo

def loadCleanDadosCaged():
    """Funcao para carregar dados limpos do CAGED

    Returns
    -------
    _type_
        _description_
    """

    dados = loadDadosCaged()

    # Deletando colunas que não vamos usar
    deletarColunasInuteis(dados)

    # Tirando cargos publicos e militares
    dados = tirarPublicosMilitares(dados)

    # Tratando os valores das UFs
    dados = tratarUFs(dados)

    # Coloca M no lugar de 1 e F no lugar de 3 na coluna sexo
    tratarSexo(dados)

    # Inserindo a descrição dos graus de instrução
    dados = tratarInstruçao(dados)

    # Inserindo a descrição das raças e etnias
    dados = trataRacaCor(dados)

    return dados


####################################################

    """
    Carregar dados das CBOs


perfilOcupacionalDF = pd.read_csv("/home/tomas/Pacifica/CAGED/CBOS/CBO2002 - PerfilOcupacional.csv", encoding='latin1', sep=";")

deletar_colunas = ['NOME_ATIVIDADE', 'Unnamed: 9', 'Unnamed: 10', 'COD_ATIVIDADE', 'SGL_GRANDE_AREA','NOME_GRANDE_AREA','COD_SUBGRUPO','COD_FAMILIA']
perfilOcupacionalDF.drop(columns=deletar_colunas, inplace=True)
    """
