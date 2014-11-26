# -*- coding: utf-8 -*-
"""
ev3dev

"""
from ev3.lego import *
import numpy as np
import neurolab as nl
import time
#----------------------
#Hopfield network stuff
#----------------------
# ?, BLACK, BLUE, GREEN
target =  [[1,0,0,0,1,1,1,0,0,1,1,0,1,0,1,1,0,0,1,1,1,0,0,0,1],
          [1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1],
          [1,1,1,1,0,1,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,0,0,0,1],
          [0,1,1,1,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,0,1,1,1,0]]
           

colors = ["?","BLACK", "BLUE", "GREEN"]
target = np.asfarray(target)
target[target == 0] = -1



def code_colors(number):
    if number == 0:
        return [1,0,0,0,1,1,1,0,0,1,1,0,1,0,1,1,0,0,1,1,1,0,0,0,1]
    if number == 1:
		return [1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1]
    if number == 2:
		return [1,1,1,1,0,1,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,0,0,0,1]
    if number == 3:
		return [0,1,1,1,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,0,1,1,1,0]

def train_hf_network():
    net = nl.net.newhop(target)
    return net

def test_network(arg):    
    output = arg.sim(target)
    print("Test on train samples:")
    for i in range(len(target)):
        print(colors[i], (output[i] == target[i]).all())
        
def match_color(arg):
    for i in range(0,4):
        if (arg[0] == target[i]).all():
            return i

def hopfield(net, color):
    print "Input color is", colors[color]
    test = code_colors(color)
    test = np.asfarray(test)
    test[test==0] = -1
    out = net.sim([test])
    print "Recovered color is", colors[match_color(out)], "\n"
    return match_color(out)

#---------------------
#XOR stuff
#---------------------

def decimal_to_binary(number):
    if number == 0:
        return [0,0,0,0]
    if number == 1:
        return [0,0,0,1]
    if number == 2:
        return [0,0,1,0]
    if number == 3:
        return [0,0,1,1]
        
def make_input(number1, number2):
    return [[number1[0], number2[0]],
            [number1[1], number2[1]],
            [number1[2], number2[2]],
            [number1[3], number2[3]]]

def result(arg):
    res = True
    for i in range(0,4):
        if arg[i] > 0.5:
            res = False
    return res

def train_ff_network():    
    #XOR
    input = [[0, 0], [0, 1], [1, 0], [1, 1]]
    target = [[0], [1], [1], [0]]

    #Create net with 2 inputs and 2 layers
    net = nl.net.newff([[0, 1],[0, 1]], [2,1])

    # train with delta rule
    # see net.trainf
    error = net.train(input, target, epochs=100, show=10)
    
    return net  
    
def XOR(n1, n2, net):
    n11 = decimal_to_binary(n1)
    n22 = decimal_to_binary(n2)
    out = net.sim(make_input(n11,n22))
    print "\nBoth colors are the same: ", result(out)
#-------------------------------

def main(color1, color2):
    hopnet = train_hf_network()
    n1 = hopfield(hopnet,color1)
    n2 = hopfield(hopnet,color2)

    xornet = train_ff_network()
    XOR(n1,n2, xornet)
    
def main2():
    print "First Color..."    
    CS = ColorSensor(port=1)
    color1 = CS.color
    print color1
    time.Sleep(5)
    print "Second Color to detect..."
    CS = ColorSensor(port=1)
    color2 = CS.color
    print color2
    
    hopnet = train_hf_network()
    #Recover colors from trained Hopfield network
    n1 = hopfield(hopnet,color1)
    n2 = hopfield(hopnet,color2)

    #Test whether the two colors were the same or different.
    #Might return false positives, but no false negatives.
    xornet = train_ff_network()
    XOR(n1,n2, xornet)
    

#main(1,2)
main2()

