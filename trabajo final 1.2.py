import pandas as pd
import os
import numpy as np
import logging
import datetime
from openpyxl import Workbook
import xlsxwriter


log_data = []
log_file = "mi_log.log"

# Lee el archivo CSV
df = pd.read_csv("ar_semestres.csv")
cre = pd.read_csv("creditos.csv")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("mi_log.log"), logging.StreamHandler()]) # Esto guarda los logs en un archivo

logger = logging.getLogger(__name__)

try:
    # Lee el archivo CSV
    df = pd.read_csv("ar_semestres.csv")
    cre = pd.read_csv("creditos.csv")
    logger.info("Archivos CSV leídos correctamente.")
except FileNotFoundError as e:
    logger.error("el archivo csv no se pudo leer")
    raise

carpeta_principal = "universidad"
os.makedirs(carpeta_principal, exist_ok=True)
logger.info(f"Carpeta principal creada: {carpeta_principal}")
# Crea una carpeta para cada semestre
for semestre in range(1, 11):
    carpeta = os.path.join(carpeta_principal,f"semestre_{semestre}")
    os.makedirs(carpeta, exist_ok=True)
    logger.info(f"carpeta exitosamente creada:{carpeta}")
    
    # Filtra los estudiantes del semestre actual
    estudiantes_semestre = df[df["semestre"] == semestre]
    logger.debug(f"estudiantes filtrados para el semestre {semestre}: {len(estudiantes_semestre)} estudiantes")
    
# para crear carpetas de cada una de las asignaturas del semestres
# se creo un diccionario con todas las asignaturas
semestres = {1: ["AYT-HM","CD-HM", "GV-HM","VLU-HM","IN1-HM", "LET-HM","IG-HM"],
    2: ["GO-HM","HG-HM","AL-HM","CI-HM","DF-HM","IN2-HM"],
    3: ["GC-HM","FM-HM","IN3-HM","AP-HM","PIE-HM","TGS-HM"],
    4: ["INE-HM","EF-HM","IN4-HM","DEX-HM","OPZ-HM","GMT-HM"],
    5: ["GEF-HM","LAF-HM","IN5-HM","FCC-HM","DS-HM","MST-HM","PES-HM","GPP-HM"],
    6: ["GT-HM","LGN-HM","EH1-HM","IN6-HM","SD-HM","FPI-HM","NCC-HM"],
    7: ["FIN-HM","EMP-HM","EH2-HM","EP1-HM","EC1-HM","DSP-HM"],
    8: ["GPR-HM","EH3-HM","EP2-HM","EC2-HM","APS-HM"],
    9: ["EH4-HM","EP3-HM","EC3-HM","GCA-HM","INM-HM"],
    10: ["PP-HM"]}

#diccionario de creditos de cada materia

credito_materia ={"AYT-HM":3,"CD-HM":3, "GV-HM":3,"VLU-HM":1,"IN1-HM":1, "LET-HM":3,"IG-HM":1,
    "GO-HM":3,"HG-HM":3,"AL-HM":3,"CI-HM":3,"DF-HM":3,"IN2-HM":1,
    "GC-HM":3,"FM-HM":3,"IN3-HM":1,"AP-HM":3,"PIE-HM":3,"TGS-HM":3,
    "INE-HM":3,"EF-HM":3,"IN4-HM":1,"DEX-HM":3,"OPZ-HM":3,"GMT-HM":4,
    "GEF-HM":3,"LAF-HM":1,"IN5-HM":1,"FCC-HM":1,"DS-HM":3,"MST-HM":3,"PES-HM":3,"GPP-HM":3,
    "GT-HM":3,"LGN-HM":3,"EH1-HM":3,"IN6-HM":1,"SD-HM":3,"FPI-HM":3,"NCC-HM":3,
    "FIN-HM":3,"EMP-HM":2,"EH2-HM":3,"EP1-HM":3,"EC1-HM":3,"DSP-HM":3,
    "GPR-HM":3,"EH3-HM":3,"EP2-HM":3,"EC2-HM":3,"APS-HM":3,
    "EH4-HM":3,"EP3-HM":3,"EC3-HM":3,"GCA-HM":3,"INM-HM":3,
    "PP-HM":12}

#diccionario que especifica los salones por semestre, y lista que indica el nombre los salones
num_salones = { 1:5, 2:5, 3:4, 4:5, 5:4, 6:4, 7:4, 8:4, 9:4, 10:6}
salones= ["salon-1","salon-2", "salon-3","salon-4","salon-5"]
estudiantes_por_salon = {1:30, 2:30, 3:30, 4:25, 5:25, 6:25, 7:20, 8:20, 9:20, 10:10}

def htd(creditos):
    if creditos == 4:
        return 96
    elif creditos == 3:
        return 64
    elif creditos == 2:
        return 32
    elif creditos == 1:
        return 16
    return 0

def hti(creditos):
    if creditos == 4:
        return 120
    elif creditos == 3:
        return 80
    elif creditos == 2:
        return 64
    elif creditos == 1:
        return 32

for semestre, cursos in semestres.items():  # .items para recorrer cada uno de los pares del diccionario
    for curso in cursos:
        t = os.path.join(carpeta_principal,f"semestre_{semestre}/{curso}, curso")
        os.makedirs(t, exist_ok=True)
        estudiantes_semestre = df[df["semestre"] == semestre]
        estudiantes = estudiantes_semestre["name"].tolist()
        np.random.shuffle(estudiantes)  # Mezcla los estudiantes aleatoriamente
        total_estudiantes = len(estudiantes)
        capacidad_salon = estudiantes_por_salon[semestre]
        estudiantes_asignados = 0     
        logger.info(f"carpeta creada para curso: {t}")   
        for salon in range(1, num_salones[semestre] + 1):
            salon_carpeta = os.path.join(t, f"Salon_{salon}")
            os.makedirs(salon_carpeta, exist_ok=True) 
            logger.info(f"carpeta creada para el salon: {salon_carpeta}")           
            if estudiantes_asignados < total_estudiantes:
                num_estudiantes_asignar = min(capacidad_salon, total_estudiantes - estudiantes_asignados)
                estudiantes_salon = estudiantes[estudiantes_asignados:estudiantes_asignados + num_estudiantes_asignar]
                estudiantes_asignados += num_estudiantes_asignar
                archivo_salon = os.path.join(salon_carpeta, f"Salon_estudiantes_{salon}.csv")
                #pd.DataFrame(estudiantes_salon, columns=["name"]).to_csv(archivo_salon, index=False)
                #logger.debug(f"archivo creado: {archivo_salon} con {len(estudiantes_salon)} estudiantes")


                codigo_materia= f"S{semestre}_C{curso}_S{salon}_CR{credito_materia[curso]}"
                htd_= htd(credito_materia[curso])
                hti_ = hti(credito_materia[curso])
                fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                num_alumnos = len(estudiantes_salon)
                archivo_salon = os.path.join(salon_carpeta, f"Salon_estudiantes_{salon}.xlsx")

                # Crear el archivo Excel y agregar los registros de estudiantes
                workbook = xlsxwriter.Workbook(archivo_salon)
                worksheet = workbook.add_worksheet()
                # Escribir los encabezados
                en = ["name", "codigo_curso", "HTD", "HTI", "fecha_creacion", "num_alumnos"]
                for col_num, enca in enumerate(en):
                    worksheet.write(0, col_num, enca)

                for _num, estudiante in enumerate(estudiantes_salon, 1):
                    worksheet.write(_num, 0, estudiante)
                    worksheet.write(_num, 1, codigo_materia)
                    worksheet.write(_num, 2, htd_)
                    worksheet.write(_num, 3, hti_)
                    worksheet.write(_num, 4, fecha_creacion)
                    worksheet.write(_num, 5, num_alumnos)
                            
                workbook.close()
                logger.debug(f"Archivo creado: {archivo_salon} con {num_alumnos} estudiantes y código especial {codigo_materia}")

with open(log_file, "r") as file:
    for line in file:
        log_data.append(line.strip())

log_df = pd.DataFrame(log_data, columns=["log"])
log_df.to_excel("log_registros.xlsx", index=False)


logger.info("felicitacion parcero, el codigo le corrio")
print("Proceso completado exitosamente.")