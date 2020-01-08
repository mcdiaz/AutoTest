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

class ContainerRN:
    def __init__(self):
        self.amount=0
        self.initTime=0
        self.finalTime=0
        self.dict=0

#{etiqueta, cantidad de objetos detectados}
#en un principio los diccionarios estarian inicializados con todas las etiquetas posibles y 0 como valor
ais=ContainerRN()
ais.dict=dict([('animal',0),('bus',0),('car',0),('cyclist',0),('human',0),('other',0),('pickup',0),('truck',0),('van',0)])
yolo=ContainerRN()
yolo.dict=dict([('animal',0),('bus',0),('car',0),('cyclist',0),('human',0),('other',0),('pickup',0),('truck',0),('van',0)])
LABELS={'animal','bus','car','cyclist','human','other','pickup','truck','van'}

labelsObj="CAR;0.8|BUS;0.1|TRUCK;0.1"

def readClasificate(labelsObj):
    listLabels=labelsObj.split("|")
    valuePrecission=0.0
    originalLabel=""
    print(listLabels)
    for i in range(0,len(listLabels),1):
        listLabels[i]=listLabels[i].split(";")
        if( valuePrecission < float(listLabels[i][1]) ):
            valuePrecission=float(listLabels[i][1])
            originalLabel=listLabels[i][0]
    print(originalLabel)
    ais.dict[originalLabel.lower()]+=1
    print(listLabels)

def runNeuralNet(urlFile, urlScriptAIS, threshold):
    print(urlFile)
    readClasificate(labelsObj)

#folderTrackedBlob posee la ubicacion a la carpeta que posee cada carpeta para cada TB, que cada una de ellas contiene 5 archivos
#folderTB='F://YOLO//prueba//'
def runAlg1(folderTB):
    #itera por todas las carpetitas del directorio
    #busca la carpeta snapshot y llamo a runneuralnet --> los resultados los huelco al diccionario ais (clave,valor) como {etiqueta,cantidad de objetos detectados}
    for root, dirs, files in os.walk(folderTB):
        #salteando el primer directorio
        if root!=folderTB:
            #print(root,"estas son root")
            ais.amount+=1
            #print(files, "estas son listas de files")
            image=""
            try:
                for x in files:
                    if x.find('clasificate')>-1:
                        image=x
                        break
                if image=="":
                    raise FileNotFoundError("el archivo clasificate no se encuentra")
                runNeuralNet(root + "//" + image, "holi", 8)
            except FileNotFoundError:
                print("LA IMAGEN A CLASIFICAR NO SE ENCUENTRA DENTRO DE "+root)
    print(ais.amount)

#Toma la salida de la yolo densa, para eso se pasa el comando con todfos sus parametros
#videoMp4='D://Videos//usina//fanless2//2018-09-02//2018-09-02_15-01-07.mp4'
#backupOutputDensa='d://temp//YoloUsina15-01-07//'

def checkLabel(objectLabel, value):
    if objectLabel in LABELS:
        yolo.dict[objectLabel]=value+1
    else:
        if objectLabel=='motorbike' or objectLabel=='bicycle':
            yolo.dict['cyclist']=value+1
        else:
            if objectLabel=='person':
                yolo.dict['human']=value+1
            else:
                if objectLabel=='dog' or objectLabel=='horse':
                    yolo.dict['animal']=value+1
                else:
                    yolo.dict[objectLabel]=value+1#podria ser etiquetado como other

def getLabelDicYolo(label):
    if label in yolo.dict.keys():
        return label
    else:
        if label=='motorbike' or label=='bicycle':
            return 'cyclist'
        else:
            if label=='person':
                return 'human'
            else:
                if label=='dog' or label=='horse':
                    return 'animal'
                else:
                    return label

def loadDicYOLO(folderYOLO):
    try:
        with open(folderYOLO) as csvYOLO:
            readYOLO=csv.reader(csvYOLO, delimiter=";")
            for row in readYOLO:
                #lee por fila las lineas del file csv que contiene la informacion del video procesado por la red densa
                labelobj=getLabelDicYolo(row[6].lower())
                cant1=int(yolo.dict.get(labelobj) or 0)#por NonType del diccionario
                checkLabel(labelobj,cant1)
                if 8 < len(row):
                    getLabelDicYolo(row[8].lower())
                    cant2 = int(yolo.dict.get(labelobj) or 0)
                    checkLabel(labelobj,cant2)
                    if 10 < len(row):
                        labelobj=getLabelDicYolo(row[10].lower())
                        cant3 = int(yolo.dict.get(labelobj) or 0)
                        checkLabel(labelobj,cant3)
                        if 12 < len(row):
                            labelobj=getLabelDicYolo(row[12].lower())
                            cant4 = int(yolo.dict.get(labelobj) or 0)
                            checkLabel(labelobj,cant4)
    except FileNotFoundError:
        print("No se encuentra el archivo csv generado por la red yolo")

def runAlg2(videoMp4,backupOutputDensa):
    #el algoritmo debe ejecutar la red YOLO (densa) y obtener los resultados y completar el diccionario
    #args:
    #videoMp4 el video en formato mp4
    #p=subprocess.Popen(['D:\YOLO_CL\Yolo_genTrainImages.exe', 'detect', 'D://YOLO_CL//cfg//yolov3.cfg', 'D://YOLO_CL//cfg//yolov3.weights', '-v',  videoMp4, '-o', backupOutputDensa,'-i','0','-M','0'])
    yolo.initTime=time.time()
    #p.communicate()
    files=backupOutputDensa+"videoClassifications.csv"
    loadDicYOLO(files)
    #Calcula el tiempo final de ejecucion de la red densa
    yolo.finalTime=time.time()-yolo.initTime
    print(yolo.finalTime)

def printValues():
    print("{4}{0:10s}{4}{4}{2:^10s}{4}{4}{3:^10s}{4}".format(" ","\n","YOLO","AIS","|"))
    print("{2}{0:^10s}{2}{2}{1:^22s}{2}".format("Etiqueta","Valor","|"))
    cantYolo=0
    for etiqueta, valor in yolo.dict.items():
        #por todos los items dentro del diccionario correspondiente a la red densa, itero por su etiqueta y valor correspondiente
        auxvalorYolo=int(valor or 0)
        auxValorAis=int(ais.dict.get(etiqueta) or 0)
        yolo.amount+=auxvalorYolo
        print("{2}{0:^10s}{2}{2}{1:^10d}{2}{2}{3:^10d}{2}".format(etiqueta, auxvalorYolo,"|",auxValorAis))
    print("{0}{1:^10s}{0}{0}{1:^10s}{0}{0}{1:^10s}{0}".format("|", "_"))
    print("{0}{1:^10s}{0}{0}{2:^10d}{0}{0}{3:^10d}{0}".format("|", "Total", yolo.amount, ais.amount))
    print("{0}{1:^10s}{0}{0}{2:^10f}{0}{0}{3:^10f}{0}".format("|", "Tiempo", yolo.finalTime, ais.finalTime))

if __name__ == "__main__":
    print(sys.argv[0],sys.argv[1],sys.argv[2])
    folderTB=sys.argv[1] #ubicacion de todos los tb
    runAlg1(folderTB)
    videoMp4=sys.argv[2] #ubicacion del video a procesar por yolo
    backupOutputDensa=sys.argv[3] #ubicacion de donde se guarda los frames y el csv de la clasificacion por la red densa
    runAlg2(videoMp4, backupOutputDensa)
    printValues()