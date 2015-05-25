# -*- coding: utf-8 -*-
from googleapiclient.discovery import build
from api_secret import GOOGLE_PUBLIC_API_KEY, GOOGLE_CSE_CX_CODE
import pandas as pd
import re
import pycurl
import ipdb
import traceback
import sys

EXCLUDE_BOJA_PDFS = ' -filetype:pdf'
FILE_SUBVENCIONES = 'data/datos_subvenciones_2.csv'
subvenciones = pd.read_csv(FILE_SUBVENCIONES, quotechar='"', sep='|', decimal=',')
convocatorias = list(subvenciones[subvenciones.programa.isnull()]['convocatoria'].drop_duplicates())
patron = '\d\d\d\d'

service = build("customsearch", "v1", developerKey=GOOGLE_PUBLIC_API_KEY) # Put your own key :-D

lista_convocatorias = []

for convocatoria in convocatorias:
    try:
        #ipdb.set_trace()
        resolucion = convocatoria[0:convocatoria.find(re.findall(patron,convocatoria)[0])+4]
        res = service.cse().list(
              q='%s -filetype:pdf' % resolucion,
              cx=GOOGLE_CSE_CX_CODE,
              siteSearch="http://www.juntadeandalucia.es/boja/"
              ).execute()
        nombre_fichero = "boja/%s.html" % resolucion.replace(" ","_").replace("/","-").replace(".","_")
        url_a_descargar = res['items'][0]['link']
    
        with open(nombre_fichero, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, url_a_descargar)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()

    except Exception, err:
        print(traceback.format_exc())
        resolucion = None
        nombre_fichero = None
        url_a_descargar = None

    resultado = { 'nombre_fichero': nombre_fichero, 'resolucion' : resolucion, 'url' : url_a_descargar, 'origen' : convocatoria}
    
    lista_convocatorias.append(resultado)

        
dataframe_convocatorias = pd.DataFrame(lista_convocatorias)
dataframe_convocatorias.to_csv("data/datos_resoluciones.csv", sep='|', encoding='utf-8')