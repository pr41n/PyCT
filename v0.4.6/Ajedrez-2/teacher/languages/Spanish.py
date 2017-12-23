#!/usr/bin/python
# -*- coding: utf-8 -*-

babel = 'spanish'
name_of_the_button = u'Español'


calibration = u"Marca los puntos siguiendo este orden y desde el punto\n" \
              u"de vista del jugador blanco:\n\n" \
              u"     1- Casilla A1: esquina inferior izquierda\n" \
              u"     2- Casilla H1: esquina inferior derecha\n" \
              u"     3- Casilla H8: esquina superior derecha\n" \
              u"     4- Casilla A8: esquina superior izquierda\n\n" \
              u"Mi recomendación es que marques las esquinas interiores en\n" \
              u"vez de las líneas. Al acabar, pulsa enter y aparecerán el resto\n" \
              u"de puntos del tablero."

player_1 = "Blancas"
player_2 = "Negras"
record = "Grabar partida"
start = "Empezar"
out = "Salir"

promote_1 = "Pieza en la que corona"
promote_2 = "Pieza: "

move_1 = "Escriba las casillas respectivas"
move_2 = "Antes: "
move_3 = "Ahora: "

open_cv_1 = "Coloca el tablero"
open_cv_2 = u"Calibración"
open_cv_3 = "Sobre esta ventana pulsa:"

sort_of_detection = u"Escoge el tipo de detección que prefieras"
sort_of_detection_1 = "Manual"
sort_of_detection_2 = u"Semi-Automática"
sort_of_detection_3 = u"Automática"

detection_description_1 = u"La más segura.\n" \
                          u"Debes pulsar espacio antes y\n" \
                          u"despues de realizar la jugada."

detection_description_2 = u"Menos segura que manual.\n" \
                          u"Debes pulsar espacio despues\n" \
                          u"de realizar la jugada."

detection_description_3 = u"La menos segura.\n" \
                          u"La detección se realiza automáticamente\n" \
                          u"despues de realizar la jugada."

turn = "Turno"
player = "Jugador"

pawn = u"Peon"
rook = u"Torre"
knight = u"Caballo"
bishop = u"Alfil"
queen = u"Reina"
king = u"Rey"

incorrect_move_000 = u"Jugada incorrecta: \n"
incorrect_move_001 = u"     La única pieza que puede saltar a otras es el caballo."

incorrect_move_002 = u"     El peón avanza en línea recta y come en diagonal. Siempre \n" \
                     u"   avanzando una fila. Si es la primera vez que lo mueves, \n" \
                     u"   puede avanzar dos casillas en línea recta."

incorrect_move_003 = u"     La torre se mueve en línea recta."

incorrect_move_004 = u"     El caballo se mueve dos casillas horizontalmente y una\n" \
                     u"   vertical o viceversa, de modo que forme una L."

incorrect_move_005 = u"     El alfil se mueve en diagonal."

incorrect_move_006 = u"     La reina se mueve como un alfil y una torre a la vez, es decir,\n" \
                     u"   recto o en diagonal."

incorrect_move_007 = u"     El rey solo puede avanzar una casilla en todas direcciones."

incorrect_move_008 = u"     El rey solo puede enrocar si ni él ni la torre del lado en el\n" \
                     u"   que se va a enrocar se han movido antes,\npor lo que es en la\n" \
                     u"   misma fila. Además, no debe haber ninguna pieza entre la torre\n" \
                     u"   y el rey. Existen dos enroques:\n" \
                     u"       Enroque corto: el rey se mueve a la columna G y la torre a la F.\n" \
                     u"       Enroque largo: el rey se mueve a la columna C y la torre a la D."

aud_001 = u"Hola, soy Pict."
aud_002 = u"Lo siento por mi voz."
aud_003 = u"Empecemos calibrando la cámara."
aud_004 = u"Coloca el tablero de modo que pueda ver las cuatro esquinas interiores."
aud_005 = u"Te recomiendo mover hacia delante las torres más alejadas."
aud_006 = u"Cuando lo hayas hecho, pulsa énter."
aud_007 = u"Ahora, haz click en las cuatro esquinas siguiendo las instrucciones."
aud_008 = u"Puedes ampliar la ventana si lo necesitas."
aud_009 = u"Hay conexión con Arduino."
aud_010 = u"No hay conexión con Arduino."
aud_011 = u"El orden es torre, caballo y alfil."
aud_012 = u"Recuerda que los reyes van en la columna E."
aud_013 = u"Empiezan las blancas."
aud_014 = u"%s por %s"
aud_015 = u"%s a %s"
aud_016 = u'Si estás de acuerdo con los puntos, pulsa énter. Si no, escape'
aud_017 = u'Selecciona la cámara que vayas a usar.'
aud_018 = u'Por cierto, escoge el tipo de detección'
aud_019 = u"Error en la detección. Pulse cualquier tecla cuando haya  vuelto a colocar las piezas."
aud_020 = u"Si prefieres introducir el movimiento manualmente, pulsa escape."
aud_021 = u"Error de detección, introduzca el movimiento manulamente."
aud_022 = u"Jaque mate, ganan %s en el turno %s, ¡felicidades!."
aud_023 = u"%s corona"
aud_024 = u"Enroque corto"
aud_025 = u"Enroque largo"
aud_026 = u"Repite el movimiento."
aud_027 = u"Cuando hayas devuelto las piezas a su posición inicial, pulsa cualquier tecla para continuar."

aud_A01 = u"No muevas tanto los peones."
aud_A02 = u"Usa más los peones."
aud_A03 = u"Para conseguir una mejor movilidad de los caballos, evita llevarlos a los lados."
