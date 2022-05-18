#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

#Para la lectura y procesado de datos de EEG
#import signals_reader     as SR

#Para esta version se intenta mejorar la eficiencia de los mensajes que se envian a ros
#Esto se pretende quitando tantos mensajes enviados de un solo momento y que se anulan al enviar el mensaje avanzar
#Y cambiando este esquema con el envio de un solo mesaje de giro que tarde más tiempo en procesarse
#tambien se aumenta el gap entre distintas señales de movimiento ocular



import EEG_signals_reader as SR
import queue              as QUEUE
import scipy.signal       as SIGNAL


#Para el control del robot
import rospy
from std_msgs.msg import Float32MultiArray
# include <geometry_msgs/Twist.h>
from geometry_msgs.msg import Twist
from rosgraph_msgs.msg import Clock
from rospy.numpy_msg import numpy_msg
import numpy as np
from std_msgs.msg import Int32MultiArray
from arlo_nn_controller.srv import EvaluateDriver, EvaluateDriverResponse
import rospy


#Para la lectura y procesado de datos de EEG
def get_baseline(array):
    suma = np.sum(array)
    average = np.divide(suma, len(array)) 
    return average



def talker(direccion):
    
    pub = rospy.Publisher('gp_test', Float32MultiArray, queue_size=10)
    gPub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(50) # 10hz
    
   
    #avanza
    msg0 = Twist()
    msg0.linear.x = 0.3
    msg0.angular.z = 0.0
   
    #gira izquierda
    msg1 = Twist()
    msg1.linear.x = 0.3
    msg1.angular.z = 0.3

    #gira derecha
    msg2 = Twist()
    msg2.linear.x = 0.3
    msg2.angular.z = -0.3

    if direccion == 0:
        #Mandamos avanzar
        gPub.publish(msg0)

    if direccion == 1:
        #Mandamos izquierda
        gPub.publish(msg1)

    if direccion == 2:
        #Mandamos derecha
        gPub.publish(msg2)




    
    




######################################
def main():
    num_picos_izq = 0
    num_picos_der = 0
    ultima_dir = 0
    
    contador_ventana_w = 0
    tam_ventana_w = 80

    F7_electrode_pos = 1
    F8_electrode_pos = 2
    threshold        = 200

    ##Mandamos a avanzar al robot en primer lugar
    talker(0)

    buffer_size       = 640
    F7_buffer         = QUEUE.Queue(buffer_size)
    F8_buffer         = QUEUE.Queue(buffer_size)
    current_values    = []  #arreglo con los valores que representan los voltajes datos por los electrodos
    i                 = 0 
    F7_processed_data = []
    F8_processed_data = []


    
    SR.open_file("/home/enrique/Escritorio/raw_data_file.txt")
    current_values = SR.get_row()
    while len(current_values) < 16: current_values = SR.get_row()

    

    #Para esta version vamos a suponer que nunca llegan arreglos vacios
    while 1:
        i = 0
        F7_buffer.clear()
        F8_buffer.clear()
        while (i < buffer_size):
            F7_buffer.push(current_values[F7_electrode_pos])
            F8_buffer.push(current_values[F8_electrode_pos])
            i = i + 1

            #Obtenemos vamos por un nuevo valor mientras regresen arreglos vacios
            current_values = SR.get_row()
            while len(current_values) < 16: current_values = SR.get_row()
        #end_while

        if i < buffer_size:
            print("No hay suficientes datos para llenar el buffer")
            exit()
        

        ##PROCESSING THE DATA
        F7_array = F7_buffer.get_as_array()
        F8_array = F8_buffer.get_as_array()        
        F7_baseline = get_baseline(F7_array)
        F8_baseline = get_baseline(F8_array)

        #removing baseline
        for index in range(buffer_size):
            F7_array[index] = F7_array[index] - F7_baseline
            F8_array[index] = F8_array[index] - F8_baseline

        #applying butterworth filtter
        sos = SIGNAL.butter(8, 60, 'lp', fs=125, output='sos')
        filtered_F7 = SIGNAL.sosfilt(sos, F7_array)
        filtered_F8 = SIGNAL.sosfilt(sos, F8_array)

        subtracted_filtered_signal = np.subtract(filtered_F7, filtered_F8)
        
        ##En este punto se tienen las señales ya filtradas y restadas
        #ahora solo hay que detectar los picos
        #Recorremos el arreglo para ver si hay un pico y si sí hay mandamos a moverse al robot
        for i in range(len(subtracted_filtered_signal)):

            #Dependiendo de la señal encontrada va a girar a la izquierda o a la derecha
            #0 avanza
            #1 izquierda
            #2 derecha
            #talker(0)
            print("picos izq:", end=" ")
            print(num_picos_izq, end=", ")
            print("picos der:", end=" ")
            print(num_picos_der)
            #if ultima_dir == 1:
            #    print("izquierda")
            #if ultima_dir == 2:
            #    print("derecha")

            #si se el contador de w es mayor a cero es que se encontro un pico cerca
            #contamos tam_ventana_w veces w para asegurar la separacion entre dos picos consecutivos
            #cuando el contador de la ventana w alcanza el tamaño maximo reiniciamos el contador de w 

            if contador_ventana_w > 0 and contador_ventana_w < tam_ventana_w:
                contador_ventana_w = contador_ventana_w + 1
            elif contador_ventana_w == tam_ventana_w:
                contador_ventana_w = 0
            
            

            if (subtracted_filtered_signal[i] > threshold)  and  (contador_ventana_w == 0):
                #print("pico encontrado izquierda")
                contador_ventana_w = 1
                num_picos_izq = num_picos_izq + 1
                ultima_dir = 1
                try:
                    talker(1)
                except rospy.ROSInterruptException as e:
                    print(e)
                    main()
            if (subtracted_filtered_signal[i] < -threshold) and (contador_ventana_w == 0):
                #print("pico encontrado derecha")
                contador_ventana_w = 1
                num_picos_der = num_picos_der + 1
                ultima_dir = 2
                try:
                    talker(2)
                except rospy.ROSInterruptException as e:
                    print(e)
                    main()                  

        #Se da un paso en el archivo para continuar con el siguiente lote de datos
        #es decir llenar la cola nuevamente y repetir el proceso
        current_values = SR.get_row()
        while len(current_values) < 16: current_values = SR.get_row()



if __name__ == '__main__':
    main()