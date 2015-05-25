# -*- coding: utf-8 -*-
__author__ = 'jdayllon'

import csv,calendar, datetime
import time, locale, re

data_file = open("./data/datos_subvenciones.csv")

def get_programa_partida_pres(x):
    patron = "\/(\d\d\D)\/"
    matches = re.findall(patron,x)
    if len(matches) > 0:
        return matches[0]
    else:
        return ""
        
def get_resumen_convocatoria(x):
    patron = '\d\d\d\d'
    try:
        return x[0:x.find(re.findall(patron,x)[0])+4]
    except:
        return ""

def string_to_timestamp(str_date):
    month = int(str_date.split("/")[1])
    year = int(str_date.split("/")[2])
    day = calendar.monthrange(year,month)[1]
    dtt = datetime.date(year,month,day)
    return time.mktime(dtt.timetuple()) * 1000
    
def listar_subvenciones_mes_grupo(datos, grupo):
    query_importes_mes_grupo = "grupo_pres == '%s'" % grupo
    importes = datos.query(query_importes_mes_grupo)\
        .sort('mes_concesion_timestamp')\
        .set_index('mes_concesion_timestamp')['importe']
    return list(importes)    

def filtra_importes_grupo(row, grupo):
    if row['grupo_pres'] == grupo:
        return row['importe']
    else:
        return 0
    

def obtener_tipo_cif(CIF):
    cif_tipo_mapping = {
    "A": "Sociedades anónimas",
    "B": "Sociedades de responsabilidad limitada",
    "C": "Sociedades colectivas",
    "D": "Sociedades comanditarias",
    "E": "Comunidades de bienes",
    "F": "Sociedades cooperativas",
    "G": "Asociaciones",
    "H": "Comunidades de propietarios en régimen de propiedad horizontal",
    "J": "Sociedades civiles",
    "K": "Formato antiguo",
    "L": "Formato antiguo",
    "M": "Formato antiguo",
    "N": "Entidades no residentes",
    "P": "Corporaciones locales",
    "Q": "Organismos autónomos, estatales o no, y asimilados, y congregaciones e instituciones religiosas",
    "R": "Congregaciones e instituciones religiosas (desde 2008, ORDEN EHA/451/2008)",
    "S": "Órganos de la Administración del Estado y comunidades autónomas",
    "V": "Sociedad Agraria de Transformación",
    "W": "Establecimientos permanentes de entidades no residentes en España",
    }
    try:
        tipo = cif_tipo_mapping[("%s" % CIF)[0]]
    except:
        tipo = "Personas"
        
    return tipo
    
def obtener_tipo_cif_resumen(CIF):
    cif_tipo_mapping = {
    "A": "Empresa",
    "B": "Empresa",
    "C": "Empresa",
    "D": "Empresa",
    "E": "Empresa",
    "F": "Empresa",
    "G": "Personas",
    "H": "Personas",
    "J": "Empresa",
    "K": "Formato antiguo",
    "L": "Formato antiguo",
    "M": "Formato antiguo",
    "N": "Empresa",
    "P": "Administración",
    "Q": "Administración/Iglesia",
    "R": "Iglesia",
    "S": "Administracion",
    "V": "Empresa",
    "W": "Empresa",
    }
    try:
        tipo = cif_tipo_mapping[("%s" % CIF)[0]]
    except:
        tipo = "Personas"
        
    return tipo
    

def obtener_provincia_cif(CIF):
    cif_mapping = {
    "01":	"Álava",
    "02":	"Albacete",
    "03":   "Alicante",
    "53":	"Alicante",
    "54":	"Alicante",
    "04":	"Almería",
    "05":	"Ávila",
    "06":	"Badajoz",
    "07":   "Islas Baleares",
    "57":   "Islas Baleares",
    "08":	"Barcelona",
    "58":	"Barcelona",
    "59":	"Barcelona",
    "60":	"Barcelona",
    "61":	"Barcelona",
    "62":	"Barcelona",
    "63":	"Barcelona",
    "64":	"Barcelona",
    "65":	"Barcelona",
    "66":	"Barcelona",
    "68":	"Barcelona",
    "09":	"Burgos",
    "10":	"Cáceres",
    "11":   "Cádiz",
    "72":	"Cádiz",
    "12":	"Castellón",
    "13":	"Ciudad Real",
    "14":   "Córdoba",
    "56":	"Córdoba",
    "15":	"La Coruña",
    "70":	"La Coruña",
    "16":	"Cuenca",
    "17":   "Gerona",
    "55":	"Gerona",
    "18":   "Granada",
    "19":	"Granada/Guadalajara",
    "20":   "Guipúzcoa",
    "75":	"Guipúzcoa",
    "21":	"Huelva",
    "22":	"Huesca",
    "23":	"Jaén",
    "24":	"León",
    "25":	"Lérida",
    "26":	"La Rioja",
    "27":	"Lugo",
    "28":   "Madrid",
    "78":   "Madrid",
    "79":   "Madrid",
    "80":   "Madrid",
    "81":   "Madrid",
    "82":   "Madrid",
    "83":   "Madrid",
    "84":   "Madrid",
    "85":   "Madrid",
    "86":   "Madrid",
    "29":   "Málaga",
    "92":	"Málaga",
    "93":	"Málaga",
    "30":   "Murcia",
    "73":	"Murcia",
    "31":   "Navarra",
    "71":	"Navarra",
    "32":	"Orense",
    "33":   "Orense",
    "74":	"Asturias",
    "34":	"Palencia",
    "35":	"Las Palmas",
    "76":	"Las Palmas",
    "36":   "Pontevedra",
    "27":   "Pontevedra",
    "94":   "Pontevedra",
    "37":	"Salamanca",
    "38":	"Santa Cruz de Tenerife",
    "75":	"Santa Cruz de Tenerife",
    "39":	"Cantabria",
    "40":	"Segovia",
    "41":	"Sevilla",
    "90":	"Sevilla",
    "91":	"Sevilla",
    "42":	"Soria",
    "43":	"Tarragona",
    "77":	"Tarragona",
    "44":	"Teruel",
    "45":	"Toledo",
    "46":	"Valencia",
    "96":	"Valencia",
    "97":	"Valencia",
    "98":	"Valencia",
    "47":	"Valladolid",
    "48":	"Vizcaya",
    "95":	"Vizcaya",
    "49":	"Zamora",
    "50":	"Zaragoza",
    "99":	"Zaragoza",
    "51":	"Ceuta",
    "52":	"Melilla",
    }
    try:
        if cif_tipo_mapping(CIF) != "NA":
            provincia = cif_mapping[("%s" % CIF)[1:3]]
        else:
            provincia = "ND"
    except:
        provincia = "NA"
    
    return provincia