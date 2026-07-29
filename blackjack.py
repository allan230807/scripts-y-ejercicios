import random 
import time 
palo = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
mazo = palo * 4
random.shuffle(mazo)
mis_cartas = []
cartas_dealer = []
print("===PARTIDA BLACKJACK SE INICIA===")
print("barajando cartas...")
time.sleep(2)
print("entregando las cartas...")
time.sleep(1)
mis_cartas.append(mazo.pop())
mis_cartas.append(mazo.pop())

cartas_dealer.append(mazo.pop())
cartas_dealer.append(mazo.pop())
print("jugador tiene...")
time.sleep(2)
print(mis_cartas[0])
time.sleep(1)
print("dealer_tiene...")
time.sleep(2)
print(cartas_dealer[0])
time.sleep(1)
print("jugador empieza con...")
time.sleep(1)
print(sum(mis_cartas))
time.sleep(1)
print("el dealer coloca su segunda carta boca abajo...")

while True:
    time.sleep(3)
    print("\n[TU TURNO]")
    print(f"1. pedir otra carta")
    print(f"2. plantarse")
    opcion = input("Elige tu jugada (1 o 2): ")
    
    if opcion == "1":
        mis_cartas.append(mazo.pop())
        print("el dealer mueve su mano hacia al mazo...")
        time.sleep(2)
        print("toma una carta y te la entrega")
        time.sleep(1)
        print(f"tu carta es un {mis_cartas[-1]}...")
        time.sleep(1)
        if sum(mis_cartas) > 21:
            print(f"ahora tienes {sum(mis_cartas)}, te haz pasado!!")
            break
        else:
            print(f"ahora tienes {sum(mis_cartas)}")
    if opcion == "2":
        print(f"te plantas con un {sum(mis_cartas)}")
        time.sleep(1)
        print("tocas la mesa...")
        time.sleep(2)
        print("el dealer se prepara para jugar...")
        time.sleep(1)
    if sum(mis_cartas) <= 21:
      print("\n turno del dealer")
      time.sleep(1)
      print(f"el dealer voltea su segunda carta teniendo ahora un {sum(cartas_dealer)}...")
      while True:
       if sum(cartas_dealer) >= 17 <= sum(cartas_dealer):
        time.sleep(1)
        print("el dealer decide plantarse...")
        break
       else:
        cartas_dealer.append(mazo.pop())
        print("el dealer decide tomar una carta...")
        time.sleep(1)
        print(f"el dealer saca un {cartas_dealer[-1]}!!")
        print(f"el dealer ahora tiene {sum(cartas_dealer)}")
      if sum(cartas_dealer) > 21:
       time.sleep(2)
       print("HAZ GANADO EL DEALER SE HA PASADO")
    print("===RESULTADO FINAL===")
    if sum(mis_cartas) > sum(cartas_dealer) and sum(mis_cartas) <= 21:
         print("HAZ GANADO!!!")
         time.sleep(2)
         print("recogiendo las cartas para el siguiente juego...")
         break
    elif sum(mis_cartas) < sum(cartas_dealer) and sum(cartas_dealer) <= 21:
       print("HAZ PERDIDO")
       time.sleep(2)
       print("recogiendo las cartas para el siguiente juego...")
       break
    else:
       print("empate...")
       time.sleep(2)
       print("recogiendo las cartas para el siguiente juego...")
       break
while True:
    time.sleep(2)
    print("\n" + "="*30)
    print("3. Reintentar?")
    print("4. Irse")
    decision = input("Elige 3 o 4: ")

    if decision == "3":
        print("\nReiniciando la mesa y barajando de nuevo...\n")
        time.sleep(2)
        continue  
    elif decision == "4":
        print("Te levantas de la mesa y te retiras del casino...")
        break  
    else:
        print("Opción no válida. Te levantas de la mesa por defecto.")
        break
      




   



