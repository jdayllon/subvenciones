# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
import ipdb
import traceback
import sys
from BeautifulSoup import BeautifulSoup


FILE_SUBVENCIONES = 'data/datos_subvenciones_2.csv'
FILE_FUNCIONAL_PRESUPUESTO = 'data/partidas_presupuesto_gasto.csv'
FILE_CONVOCATORIAS_BOJA = "data/datos_resoluciones_2.csv"

subvenciones = pd.read_csv(FILE_SUBVENCIONES, quotechar='"', sep='|', decimal=',')
funcional = pd.read_csv(FILE_FUNCIONAL_PRESUPUESTO, quotechar='"', sep='|', decimal=',').fillna('')
convocatorias = pd.read_csv(FILE_CONVOCATORIAS_BOJA, sep='|', encoding='utf-8')

patrones = ['\d{2}\.[a-zA-Z]$','\.\d{2}[A-Z]\.','(\d{2}\.){4}\d{3}\.\d{2}\.\d{3}','[0-9\.]*\.(\d\d[A-Z]).{0,1}',]

#'(\d{0,1}\.{0,1}){0,2}(\d{2}\.){4,5}(\d{3,5}\.)(\d{2}\w{0,1})\.\d{0,3}'
#01.12.00.01.00.773.48.610
#0.1.17.00.11.00.78201.71F.0

#0: ejercicio corriente 
#1: presupuesto de gastos 
#CLASIFICACIÓN ORGÁNICA: 
#12.00: sección 
#16: servicio (en este caso, si no recuerdo mal, Fondo social europeo) 
#00: provincia: servicios centrales 
#CLASIFICACIÓN ECONÓMICA 
#604.00: el 6 indica el capítulo, en este caso inversiones reales. el 00 final es el subconcepto que tiene dos dígitos. 
#CLASIFICACIÓN FUNCIONAL POR PROGRAMAS 
#72.B
lista_programas = []

for convocatoria in list(convocatorias.nombre_fichero):
    programas = []
    if str(convocatoria) == 'nan':
        continue
    #if convocatoria == 'boja/ORDEN_DE_31_DE_JULIO_DE_2009.html':
    #    ipdb.set_trace()
    try:
        input_html = file(convocatoria,"r")
        soup = BeautifulSoup(input_html.read())
        for line in soup.body.findAll(text=True):
            for patron in patrones:
                patrones_encontrados = re.findall(patron,line)
                if len(patrones_encontrados) > 0:
                    #ipdb.set_trace()
                    programa = patrones_encontrados[0].replace('.','')
                    if programa not in programas:
                        programas.append(programa)
                        #print "%s - %s " % (convocatoria,.replace('.',''))
        
        input_html.close()
        print "%s - %s " % (convocatoria,programas)
    except Exception, err:
        ipdb.set_trace()
        print convocatoria
        print(traceback.format_exc())
    lista_programas.append(" ".join(str(x) for x in programas))

convocatorias['programas'] = pd.Series(lista_programas)
convocatorias = convocatorias[['nombre_fichero','origen','resolucion','url','programas']]
convocatorias.to_csv("data/datos_resoluciones_2.csv", sep='|', encoding='utf-8')