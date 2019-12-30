import sys
import os
import subprocess
import time
from os.path import *
import csv

"""
with open('output.txt','w') as output_f:
    p=subprocess.Popen('D\YOLO_CL\yolo.exe detect "D://YOLO_CL//cfg//yolov3.cfg" "D://YOLO_CL//cfg//yolov3.weights" -v  "D://YOLO_CL//2019-07-09_10-00-00.mp4"  -o "d://YOLO_CL//detections//" ', stdout=output_f,stderr=output_f, shell=False)
"""

#{etiqueta, cantidad de objetos detectados}
#en un principio los diccionarios estarian inicializados con todas las etiquetas posibles y 0 como valor
ais=dict([('car',0),('human',0),('bus',0),('motorbike',0),('person',0),('truck',0),('bird',0),('bicycle',0)])
yolo=dict([('car',0),('human',0),('bus',0),('motorbike',0),('person',0),('truck',0),('bird',0),('bicycle',0)])

#def runNeuralNet(urlFile, urlScriptAIS, threshold):



#folderTrackedBlob posee la ubicacion a la carpeta que posee cada carpeta para cada TB, que cada una de ellas contiene 5 archivos

folderTB='F://YOLO//prueba//'
def runAlg1(folderTB):
    #itera por todas las carpetitas del directorio
    #busca la carpeta snapshot y llamo a runneuralnet --> los resultados los huelco al diccionario ais (clave,valor) como {etiqueta,cantidad de objetos detectados}
    for root, dirs, files in os.walk(folderTB):
        #salteando el primer directorio
        if root!=folderTB:
            print(root,"estas son root")
            print(dirs,"estas son dirs")
        #print(files, "estas son files")
#runAlg1(folderTB)

#Toma la salida de la yolo densa, para eso se pasa el comando con todfos sus parametros
videoMp4='D://Videos//usina//fanless2//2018-09-02//2018-09-02_15-01-07.mp4'
backupOutputDensa='d://temp//YoloUsina15-01-07//'

def loadDicYOLO(folderYOLO):
    with open(folderYOLO) as csvYOLO:
        readYOLO=csv.reader(csvYOLO, delimiter=";")
        for row in readYOLO:
            cant1=int(yolo.get(row[6]) or 0)#por NonType del diccionario
            yolo[row[6]] = cant1 + 1
            if 8 < len(row):
                cant2 = int(yolo.get(row[8]) or 0)
                yolo[row[8]] = cant2 + 1
                if 10 < len(row):
                    cant3 = int(yolo.get(row[10]) or 0)
                    yolo[row[10]] = cant3 + 1
                if 12 < len(row):
                    cant4 = int(yolo.get(row[12]) or 0)
                    yolo[row[12]] = cant4 + 1
    print(yolo)

    #print(yolo)

def runAlg2(videoMp4):
    #el algoritmo debe ejecutar la red YOLO (densa) y obtener los resultados y completar el diccionario
    #args:
    #videoMp4 el video en formato mp4
    #p=subprocess.Popen(['D:\YOLO_CL\Yolo_genTrainImages.exe', 'detect', 'D://YOLO_CL//cfg//yolov3.cfg', 'D://YOLO_CL//cfg//yolov3.weights', '-v',  videoMp4, '-o', backupOutputDensa,'-i','0','-M','0'])
    start_time=time.time()
    #p.communicate()
    """
    b=subprocess.Popen(['C://Program Files//Git//git-bash.exe','bash','/F/yolo/dat.sh', '/D/Temp/YoloUsina15-01-07/videoClassifications.csv', '/D/Temp/YoloUsina15-01-07/videoClassifications.txt', '/D/yolo_cl/data/cocoNames.txt', '/D/Temp/YoloUsina15-01-07/'])
    """
    files=backupOutputDensa+"videoClassifications.csv"
    file = open(backupOutputDensa+"videoClassifications.csv","r")
    print(file.read())
    loadDicYOLO(files)
    #Calcula el tiempo final de ejecucion de la red densa
    finish_time=time.time()-start_time
    print(finish_time)

runAlg2(videoMp4)

def printValues():
    print("{4}{0:10s}{4}{4}{2:^10s}{4}{4}{3:^10s}{4}".format(" ","\n","YOLO","AIS","|"))
    print("{2}{0:^10s}{2}{2}{1:^22s}{2}".format("Etiqueta","Valor","|"))
    for etiqueta, valor in yolo.items():
        auxvalor=int(valor or 0)
        print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(etiqueta, auxvalor,"|",ais.get(etiqueta)))
printValues()