# -*- coding: utf-8 -*-

import math

print("\n-----INFORMACION INICIAL-----\n")

direccion_red = input("Ingresa la direccion de la red: ")
prefijo_red = int(input("Ingresa el valor del prefijo de la red: "))

n_subredes = int(input("Ingresa la cantidad de subredes: "))
host_subred = []

n_tipo = int(input("A continuacion, ingresa 0 si quieres realizar la division de la red mediante FLSM o ingresa 1 si por el contrario, lo quieres hacer mediante VLSM: "))

def insertar_ordenado(n_host):
    n_host_subred = len(host_subred)
    if (n_host_subred > 0):
        if (n_host_subred != 1):
                for i in range(0, n_host_subred):
                    if (host_subred[i] <= n_host):
                        host_subred.insert(i, n_host)
                        return
        else:
            if (host_subred[0] < n_host):
                host_subred.insert(0, n_host)
                return
    host_subred.append(n_host)

if (n_tipo == 1):
    print("\n\n-----INFORMACION DE LAS SUBREDES-----\n")
    for i in range(n_subredes):
        insertar_ordenado(int(input("Ingresa la cantidad de host para la subred " + str(i + 1) + ": ")))

print("\n\n-----DESARROLLO DE LAS SUBREDES-----\n\n")

def Binario_decimal(num_binario):
    posicion_bit = len(num_binario) - 1
    decimal = 0
    for bit in num_binario:
        decimal += (2 ** posicion_bit) * int(bit)
        posicion_bit -= 1
    return decimal

def Decimal_binario(num_decimal):
    binario = ''
    while(num_decimal > 1):
        binario += str(num_decimal % 2)
        num_decimal = math.floor(num_decimal / 2) 
    return (binario + str(num_decimal))[::-1]

def Calcular_mascara(prefijo_red):
    mascara = ''
    octeto = ''
    for i in range(1,33):
        if (i <= prefijo_red):
            octeto += str(1)
        else:
            octeto += str(0)
        if (i % 8 == 0):
            mascara += str(Binario_decimal(octeto)) + '.'
            octeto = ''
    return mascara[:-1]  

def Obtener_ultimo_octeto(direccion):
    return int(direccion[direccion.rfind('.') + 1:])

def Cambiar_ultimo_octeto(direccion, nuevo_octeto):
    nueva_direccion = direccion[:direccion.rfind('.') + 1] + nuevo_octeto
    return nueva_direccion

def Calcular_direccion_binario(direccion_decimal):
    direccion_decimal += '.'
    binario = ''
    valor_octeto = ''
    for i in direccion_decimal:
        if (i != '.'):
            valor_octeto += str(i)
        else:
            binario += str(Decimal_binario(int(valor_octeto))) + '.'
            valor_octeto = ''
    return binario[:-1]

def Calcular_direccion_decimal(direccion_binario):
    direccion_binario += '.'
    decimal = ''
    octeto_binario = ''
    for i in direccion_binario:
        if (i != '.'):
            octeto_binario += str(i)
        else:
            decimal += str(Binario_decimal(octeto_binario)) + '.'
            octeto_binario = ''
    return decimal[:-1]

def Ajustar_direccion(direccion):
    direccion += '.'
    direccion_ajustada = ''
    octeto_binario = ''
    for i in direccion:
        if (i != '.'):
            octeto_binario += i
        else:
            if (len(octeto_binario) != 8):
                cadena_ceros = ''
                for i in range(0, 8 - len(octeto_binario)):
                    cadena_ceros += '0'
                direccion_ajustada += cadena_ceros + octeto_binario + '.'
            else:
                direccion_ajustada += octeto_binario + '.'
            octeto_binario = ''

    return direccion_ajustada[:-1]

def Calcular_primera_ultima_utilizable(direccion, mascara_red, primera_ultima):
    mascara_red_binario_ajustada = Ajustar_direccion(Calcular_direccion_binario(mascara_red))
    direccion_binario_ajustada = Ajustar_direccion(direccion)
    direccion_primera_ultima_utilizable = ''
    
    for i in range (0,35):
        bit_direccion = direccion_binario_ajustada[i:i+1]
        bit_mascara = mascara_red_binario_ajustada[i:i+1]
        
        if (bit_direccion != '.'):
            if (bit_mascara == bit_direccion and bit_mascara == '1'):
                direccion_primera_ultima_utilizable += '1'
            elif (bit_mascara == '0'):
                if (primera_ultima == 'primera'):
                    if (i != 34):
                        direccion_primera_ultima_utilizable += '0'
                    else:
                        direccion_primera_ultima_utilizable += '1'
                elif (primera_ultima == 'ultima'):
                    if (i != 34):
                        direccion_primera_ultima_utilizable += '1'
                    else:
                        direccion_primera_ultima_utilizable += '0'
            else:
                direccion_primera_ultima_utilizable += '0' 
        else:
            direccion_primera_ultima_utilizable += '.' 
        
    return Calcular_direccion_decimal(direccion_primera_ultima_utilizable)

def Calcular_broadcast(ultima_utilizable):
    ultima_utilizable_binario = Calcular_direccion_binario(ultima_utilizable)
    return Calcular_direccion_decimal(ultima_utilizable_binario[:len(ultima_utilizable_binario) - 1] + '1') 

def Calcular_siguiente_direccion_red(broadcast, mascara_red):
    
    mascara_red = Ajustar_direccion(Calcular_direccion_binario(mascara_red))
    broadcast = Ajustar_direccion(Calcular_direccion_binario(broadcast))
    direccion_red = ''

    i = len(broadcast) - 1

    while broadcast[i] != '0':
        if (broadcast[i] != '.'):
            direccion_red = '0' + direccion_red
        else:
            direccion_red = '.' + direccion_red
        i -= 1
    
    direccion_red = broadcast[:i] + '1' + direccion_red
    
    return Calcular_direccion_decimal(direccion_red)

def Calcular_direccion_FLSM(direccion, prefijo_red, prefijo_subred, sub_red_binario):
    direccion_binario_ajustada = Ajustar_direccion(direccion)
    direccion_binario_ajustada = direccion_binario_ajustada[:prefijo_red] + '.' +sub_red_binario + direccion_binario_ajustada[prefijo_subred:]
    
    return Calcular_direccion_decimal(direccion_binario_ajustada)

if (n_tipo == 1):
    
    mascara_red = Calcular_mascara(prefijo_red)

    for i in range(0, n_subredes):
        
        host_requeridos = host_subred[i]
        
        n_bits = math.ceil(math.log2(host_subred[i]))
        if ((2 ** n_bits) - 2 >= host_subred[i]):
            host_subred[i] = (2 ** n_bits) - 2
        else:
            n_bits += 1
            host_subred[i] = (2 ** n_bits) - 2
        
        n_bits_subred = (32 - prefijo_red) - n_bits
        prefijo_subred = prefijo_red + n_bits_subred
        mascara_subred = Calcular_mascara(prefijo_subred)
        
        
        print('Subred ' + str(i + 1) + ':')
        print('\tHost disponibles: ' + str(host_subred[i]))
        print('\tHost requeridos: ' + str(host_requeridos))
        print('\tDireccion de red: ' + direccion_red + '/' +str(prefijo_subred))
        direccion_binario = Calcular_direccion_binario(direccion_red)
        print('\tMascara de red: ' + mascara_subred)
        primera_utilizable = Calcular_primera_ultima_utilizable(direccion_binario, mascara_subred, 'primera')
        print('\tPrimera utilizable: ' + primera_utilizable)
        ultima_utilizable = Calcular_primera_ultima_utilizable(direccion_binario, mascara_subred, 'ultima')
        print('\tUltima utilizable: ' + ultima_utilizable)
        broadcast = Calcular_broadcast(ultima_utilizable)
        print('\tBroadcast: ' + broadcast + '\n')
        
    
        direccion_red = Calcular_siguiente_direccion_red(broadcast, mascara_red)
        
else:
    
    n_bits = math.ceil(math.log2(n_subredes))
    prefijo_subred = prefijo_red + n_bits
    mascara_red = Calcular_mascara(prefijo_subred)
    
    for i in range(0, n_subredes):
        
        sub_red_binario = Decimal_binario(i)
        direccion_binario = Calcular_direccion_binario(direccion_red)
        direccion = Calcular_direccion_FLSM(direccion_binario,prefijo_red,prefijo_subred,sub_red_binario)
        
        print('Subred ' + str(i + 1) + ':')
        print('\tHost disponibles: ' + str((2 ** (32 - prefijo_subred)) - 2))
        print('\tDireccion de red: ' + direccion_red + '/' +str(prefijo_subred))
        print('\tMascara de red: ' + mascara_red)
        primera_utilizable = Calcular_primera_ultima_utilizable(direccion_binario, mascara_red, 'primera')
        print('\tPrimera utilizable: ' + primera_utilizable)
        ultima_utilizable = Calcular_primera_ultima_utilizable(direccion_binario, mascara_red, 'ultima')
        print('\tUltima utilizable: ' + ultima_utilizable)
        broadcast = Calcular_broadcast(ultima_utilizable)
        print('\tBroadcast: ' + broadcast + '\n')
    
        direccion_red = Calcular_siguiente_direccion_red(broadcast, mascara_red)

"""
Created on Sun Mar  6 10:31:13 2022

@author: Cristian Julian Munoz Buenahora
"""