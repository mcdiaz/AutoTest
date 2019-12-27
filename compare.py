import sys
import os
import subprocess
import time
from os.path import *
"""
with open('output.txt','w') as output_f:
    p=subprocess.Popen('D\YOLO_CL\yolo.exe detect "D://YOLO_CL//cfg//yolov3.cfg" "D://YOLO_CL//cfg//yolov3.weights" -v  "D://YOLO_CL//2019-07-09_10-00-00.mp4"  -o "d://YOLO_CL//detections//" ', stdout=output_f,stderr=output_f, shell=False)
"""

ais={}
yolo={}

def runNeuralNet(urlFile, urlScriptAIS, threshold):



#folderTrackedBlob posee la ubicacion a la carpeta que posee cada carpeta para cada TB, que cada una de ellas contiene 5 archivos
folderTB='F://YOLO//prueba//'
def runAlg1(folderTB):
    #itera por todas las carpetitas del directorio
    for root, dirs, files in os.walk(folderTB):
        #salteando el primer directorio
        if root!=folderTB:
            print(root,"estas son root")
            print(dirs,"estas son dirs")
        #print(files, "estas son files")
runAlg1(folderTB)

#Toma la salida de la yolo densa, para eso se pasa el comando con todfos sus parametros
videoMp4='D://Videos//usina//fanless2//2018-09-02//2018-09-02_15-01-07.mp4'
backupOutputDensa='d://temp//YoloUsina15-01-07//'
def runAlg2(videoMp4):
    #el algoritmo debe ejecutar la red YOLO (densa) y obtener los resultados y completar el diccionario
    #args:
    #videoMp4 el video en formato mp4
    p=subprocess.Popen(['D:\YOLO_CL\Yolo_genTrainImages.exe', 'detect', 'D://YOLO_CL//cfg//yolov3.cfg', 'D://YOLO_CL//cfg//yolov3.weights', '-v',  videoMp4, '-o', backupOutputDensa,'-i','0','-M','0'])
    start_time=time.time()
    p.communicate()
    """
    b=subprocess.Popen(['C://Program Files//Git//git-bash.exe','bash','/F/yolo/dat.sh', '/D/Temp/YoloUsina15-01-07/videoClassifications.csv', '/D/Temp/YoloUsina15-01-07/videoClassifications.txt', '/D/yolo_cl/data/cocoNames.txt', '/D/Temp/YoloUsina15-01-07/'])
    """
    #Calcula el tiempo final de ejecucion de la red densa
    finish_time=time.time()-start_time
    print(finish_time)
