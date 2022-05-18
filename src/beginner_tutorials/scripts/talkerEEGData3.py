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
    msg0.angular.z = 0.0
    msg0.linear.x = 0.1
   
    #gira izquierda
    msg1 = Twist()
    msg1.angular.z = 5
    msg1.linear.x = 0.0

    #gira derecha
    msg2 = Twist()
    msg2.angular.z = -5
    msg2.linear.x = 0.0


    if direccion == 0:
        #Mandamos avanzar
        for i in range(10):
            gPub.publish(msg0)
    if direccion == 1:
        #Mandamos izquierda
        for i in range(3):
            gPub.publish(msg1)
        gPub.publish(msg0)
    if direccion == 2:
        #Mandamos derecha
        for i in range(3):
            gPub.publish(msg2)
        gPub.publish(msg0)




    
    




######################################
def main():
    F7_electrode_pos = 9
    F8_electrode_pos = 10
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


    while len(current_values) > 0:
        i = 0
        F7_buffer.clear()
        F8_buffer.clear()
        while (len(current_values) > 0) and (i < buffer_size):
            F7_buffer.push(current_values[F7_electrode_pos])
            F8_buffer.push(current_values[F8_electrode_pos])
            i = i + 1
            current_values = SR.get_row()
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
        sos = SIGNAL.butter(10, 15, 'hp', fs=1000, output='sos')
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

            if subtracted_filtered_signal[i] > threshold :
                print("pico encontrado izquierda")
                try:
                    talker(1)
                except rospy.ROSInterruptException as e:
                    print(e)
                    main()
            if subtracted_filtered_signal[i] < -threshold :
                print("pico encontrado derecha")
                try:
                    talker(2)
                except rospy.ROSInterruptException as e:
                    print(e)
                    main()                  

        #Se da un paso en el archivo para continuar con el siguiente lote de datos
        #es decir llenar la cola nuevamente y repetir el proceso
        current_values = SR.get_row()





    

if __name__ == '__main__':
    main()