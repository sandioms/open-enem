from unidecode import unidecode
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def convert_data(dn):
    dna = datetime.strptime(dn, "%Y-%m-%d %H:%M:%S")
    dnn = '{}-{}-{}'.format(dna.year, dna.month, dna.day)
    return dnn

def separar_data_day(dn):
    dna = datetime.strptime(dn, "%Y-%m-%d")    
    return dna.day

def separar_data_month(dn):
    dna = datetime.strptime(dn, "%Y-%m-%d")    
    return dna.month

def separar_data_year(dn):
    dna = datetime.strptime(dn, "%Y-%m-%d")    
    return dna.year

def tratamento_data_censo1(data):
    cols = list()
    cont = 0
    controlador = True
    contrAP = False
    contrRE = False
    contrAB = False
    contrEF = True
    contrEM = True
    for i in range(data.shape[1]):
        if (pd.isnull(data.iloc[cont][i])) and controlador:
            continue
        else:
            if("Aprovação" in (" " + str(data.iloc[cont][i]) + " ")) or (contrAP and pd.isnull(data.iloc[cont][i])):
                if("Fundamental" in (" " + str(data.iloc[cont+1][i]) + " ")) or (contrEF and ("Ano" in (" " + str(data.iloc[cont+1][i]) + " "))):
                    cols.append("TAP - " + "ENS. FUN - " + "{}".format(data.iloc[cont+1][i].strip()))
                    contrEF = True
                    contrEM = False
                if("Médio" in (" " + str(data.iloc[cont+1][i]) + " ")) or (contrEM):
                    cols.append("TAP - " + "ENS. MED - " + "{}".format(data.iloc[cont+1][i].strip()))
                    contrEF = False
                    contrEM = True

                contrAP = True
                contrRE = False
                contrAB = False
                controlador = False

            elif("Reprovação" in (" " + str(data.iloc[cont][i]) + " ")) or (contrRE and pd.isnull(data.iloc[cont][i])):
                if("Fundamental" in (" " + str(data.iloc[cont+1][i]) + " ")) or (contrEF and ("Ano" in (" " + str(data.iloc[cont+1][i]) + " "))):
                    cols.append("TRE - " + "ENS. FUN - " + "{}".format(data.iloc[cont+1][i].strip()))
                    contrEF = True
                    contrEM = False
                if("Médio" in (" " + str(data.iloc[cont+1][i]) + " ")) or (contrEM):
                    cols.append("TRE - " + "ENS. MED - " + "{}".format(data.iloc[cont+1][i].strip()))
                    contrEF = False
                    contrEM = True

                contrAP = False
                contrRE = True
                contrAB = False
                controlador = False

            elif("Abandono" in (" " + str(data.iloc[cont][i]) + " ")) or (contrAB and pd.isnull(data.iloc[cont][i])):
                if("Fundamental" in (" " + str(data.iloc[cont+1][i]) + " ")) or (contrEF and ("Ano" in (" " + str(data.iloc[cont+1][i]) + " "))):
                    cols.append("TAB - " + "ENS. FUN - " + "{}".format(data.iloc[cont+1][i].strip()))
                    contrEF = True
                    contrEM = False
                if("Médio" in (" " + str(data.iloc[cont+1][i]) + " ")) or (contrEM):
                    cols.append("TAB - " + "ENS. MED - " + "{}".format(data.iloc[cont+1][i].strip()))
                    contrEF = False
                    contrEM = True

                contrAP = False
                contrRE = False
                contrAB = True
                controlador = False

            else:
                cols.append(data.iloc[cont][i])
    result = pd.DataFrame(data=data.iloc[2:].values, columns=cols)
    result = result.dropna()
    return result

def tratamento_data_censo2(data):
    cols = list()
    cont = 0
    controlador = True
    contrAP = False
    contrRE = False
    contrAB = False
    contrEF = False
    for i in range(data.shape[1]):
        if (pd.isnull(data.iloc[cont][i])) and controlador:
            continue
        else:
            if(data.iloc[cont][i] == 'Taxa de Aprovação') or (contrAP and pd.isnull(data.iloc[cont][i])):
                if(data.iloc[cont+1][i] == 'Ensino Fundamental de 8 e 9 anos') or (contrEF and pd.isnull(data.iloc[cont+1][i])):
                    cols.append("TAP - " + "ENS. FUN - " + "{}".format(data.iloc[cont+2][i].strip()))
                    contrEF = True
                else:
                    cols.append("TAP - " + "ENS. MED - " + "{}".format(data.iloc[cont+2][i].strip()))
                    contrEF = False

                contrAP = True
                contrRE = False
                contrAB = False
                controlador = False

            elif(data.iloc[cont][i] == 'Taxa de Reprovação') or (contrRE and pd.isnull(data.iloc[cont][i])):
                if(data.iloc[cont+1][i] == 'Ensino Fundamental de 8 e 9 anos') or (contrEF and pd.isnull(data.iloc[cont+1][i])):
                    cols.append("TRE - " + "ENS. FUN - " + "{}".format(data.iloc[cont+2][i].strip()))
                    contrEF = True
                else:
                    cols.append("TRE - " + "ENS. MED - " + "{}".format(data.iloc[cont+2][i].strip()))
                    contrEF = False

                contrAP = False
                contrRE = True
                contrAB = False
                controlador = False

            elif(data.iloc[cont][i] == 'Taxa de Abandono') or (contrAB and pd.isnull(data.iloc[cont][i])):
                if(data.iloc[cont+1][i] == 'Ensino Fundamental de 8 e 9 anos') or (contrEF and pd.isnull(data.iloc[cont+1][i])):
                    cols.append("TAB - " + "ENS. FUN - " + "{}".format(data.iloc[cont+2][i].strip()))
                    contrEF = True
                else:
                    cols.append("TAB - " + "ENS. MED - " + "{}".format(data.iloc[cont+2][i].strip()))
                    contrEF = False

                contrAP = False
                contrRE = False
                contrAB = True
                controlador = False

            else:
                cols.append(data.iloc[cont][i])
    result = pd.DataFrame(data=data.iloc[3:].values, columns=cols)
    result = result.dropna()
    return result

def dependencia_administrativa(x):
    z = unidecode(x.strip().lower())
    if (z  == 'estadual'):
        return 'Estadual'
    if (z == 'publico') or (z == 'publica'):
        return 'Pública'
    if (z == 'federal'):
        return 'Federal'
    if (z == 'municipal'):
        return 'Municípal'
    if (z == 'particular') or (z == 'privada'):
        return 'Privada'
    if (z == 'total'):
        return 'Total'
    
def nome_municipio(x):
    z = unidecode(x.strip().lower())
    y = z[0].upper() + z[1:]
    return y 

def plot_bars(data, l1, l2, l3):
    fig, ax = plt.subplots(figsize=(10,6))
    width = 0.25
    bar1 = ax.bar(data.Ano, data[l1], width, color = 'g')
    ax.bar_label(bar1)
    bar2 = ax.bar(data.Ano+width, data[l2], width, color='r')
    ax.bar_label(bar2)
    bar3 = ax.bar(data.Ano+width*2, data[l3], width, color = 'b')
    ax.bar_label(bar3)
    plt.xlabel("Censo Escolar")
    plt.ylabel('Porcentagem')
    plt.title("Rendimento Escolar")
    plt.legend( (bar1, bar2, bar3), ('Aprovação', 'Reprovação', 'Abandono') )
    plt.show()
    
def tp_depedencia(x):
    if x == 1:
        return 'Federal'
    if x == 2:
        return 'Estadual'
    if x == 3:
        return 'Municipal'
    if x == 4:
        return 'Privada'
    
def tp_localizacao(x):
    if x == 1:
        return 'Urbana'
    if x == 2:
        return 'Rural'
    
def tp_ocupacao_pred_escolar(x):
    if x == 1:
        return 'Próprio'
    if x == 2:
        return 'Alugado'
    if x == 3:
        return 'Cedido' 

def tp_ocupacao_galp_escolar(x):
    if x == 1:
        return 'Próprio'
    if x == 2:
        return 'Alugado'
    if x == 3:
        return 'Cedido'
    if x == 9:
        return 'Não informado'
    
def creche(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'
    
def pre_escola(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'
    
def ens_fund_an_inicias(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'

def ens_fund_an_finais(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'

def ens_med_integrado(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'
    
def ens_med_normal(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'
    
def esgoto(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'
    
def coleta_lixo(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'
    
def banheiro(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'
    
def refeitorio(x):
    if x == 0:
        return 'Não'
    if x == 1:
        return 'Sim'    
    
def status_realizacao_prova(x):
    if x == 0:
        return 'Faltou à prova'
    if x == 1:
        return 'Presente na prova'
    if x == 2:
        return 'Eliminado na prova'
    
def status_realizaco_redacao(x):
    if x == 1:
        return 'Sem problemas'
    if x == 2:
        return 'Anulada'
    if x == 3:
        return 'Cópia texto motivador'
    if x == 4:
        return 'Em branco'
    if x == 6:
        return 'Fuga do tema'
    if x == 7:
        return 'Não atendimento ao tipo textual'
    if x == 8:
        return 'Texto insuficiente'
    if x == 9:
        return 'Parte desconectada'