import random
import time

bala = random.randint(1, 6)
posicion_actual = 1

jugador_disparos_a_rival = 1
jugador_disparos_a_si_mismo = 2

terminal_disparos_a_rival = 1
terminal_disparos_a_si_mismo = 2

print("=== RULETA RUSA CONTRA LA TERMINAL ===")
print("Cargando una bala en el tambor...")
time.sleep(2)
print("Girando el tambor...\n")
time.sleep(2)

while True:
    print(f"--- RECÁMARA ACTUAL: {posicion_actual} de 6 ---")
    time.sleep(1)
    
    print("\n[TU TURNO]")
    print(f"1. Disparar a la Terminal (Usos: {jugador_disparos_a_rival})")
    print(f"2. Dispararte a ti mismo (Usos: {jugador_disparos_a_si_mismo})")
    
    opcion = input("Elige tu jugada (1 o 2): ")
    
    if opcion == "1":
        if jugador_disparos_a_rival > 0:
            jugador_disparos_a_rival -= 1
            print("\nApuntas a la Terminal...")
            time.sleep(2)
            print("Aprietas el gatillo...")
            time.sleep(2)
            
            if posicion_actual == bala:
                print("¡BANG! Le diste a la Terminal. ¡HAS GANADO!")
                break
            else:
                print("*click*... La recámara estaba vacía.")
                posicion_actual += 1
        else:
            print("\nYa no te quedan disparos al rival. Pierdes el turno por dudar.")
            
    elif opcion == "2":
        if jugador_disparos_a_si_mismo > 0:
            jugador_disparos_a_si_mismo -= 1
            print("\nTe apuntas a ti mismo...")
            time.sleep(2)
            print("Aprietas el gatillo...")
            time.sleep(2)
            
            if posicion_actual == bala:
                print("¡BANG! Te has disparado. ¡HAS PERDIDO!")
                break
            else:
                print("*click*... La recámara estaba vacía. Sobrevives.")
                posicion_actual += 1
        else:
            print("\nYa no te quedan disparos a ti mismo. Pierdes el turno por dudar.")
    else:
        print("\nOpción inválida. Pierdes tu turno.")

    time.sleep(2.5)

    print("\nturno del terminal")
    time.sleep(1.5)
    print("La Terminal está pensando su jugada...")
    time.sleep(3)
    
    opciones_terminal = []
    if terminal_disparos_a_rival > 0:
        opciones_terminal.append("rival")
    if terminal_disparos_a_si_mismo > 0:
        opciones_terminal.append("si_mismo")
        
    if not opciones_terminal:
        print("La Terminal no tiene opciones válidas y pasa su turno.")
    else:
        eleccion_terminal = random.choice(opciones_terminal)
        
        if eleccion_terminal == "rival":
            terminal_disparos_a_rival -= 1
            print("La Terminal te apunta directamente...")
            time.sleep(2)
            print("Lentamente aprieta el gatillo...")
            time.sleep(2)
            
            if posicion_actual == bala:
                print("¡BANG! La Terminal te ha disparado. ¡HAS PERDIDO!")
                break
            else:
                print("*click*... La recámara estaba vacía.")
                posicion_actual += 1
                
        elif eleccion_terminal == "si_mismo":
            terminal_disparos_a_si_mismo -= 1
            print("La Terminal decide apuntarse a sí misma...")
            time.sleep(2)
            print("Aprieta el gatillo...")
            time.sleep(2)
            
            if posicion_actual == bala:
                print("¡BANG! La Terminal se ha destruido. ¡HAS GANADO!")
                break
            else:
                print("*click*... La recámara estaba vacía. La Terminal sobrevive.")
                posicion_actual += 1

    time.sleep(3)
    print("\n" + "="*35 + "\n")

