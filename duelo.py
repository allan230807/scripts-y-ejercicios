import random 
import time 

vida_jugador = 50
jugador_escudos = 4
damage_espadas = 10
vida_bot = 50
bot_escudos = 4

print("=== DUELO DE CABALLEROS ===")
time.sleep(1)
print("observas como se aproxima un caballero...")
time.sleep(1)
print("ambos se preparan para la lucha...")
time.sleep(2)

while True:
    print("\n[TU TURNO]")
    print(f" A. atacar!")
    print(f" D. defender! (usos: {jugador_escudos})")
    eleccion = input("elige tu jugada A o D:").upper()
    eleccion_bot = random.choice(["A", "D"])
    if eleccion == "A" and eleccion_bot == "A":
        time.sleep(1)
        print("decides atacar al rival!")
        time.sleep(1)
        print("atacas y...")
        time.sleep(2)
        print("AMBOS CABALLEROS SE ATACAN!")
        vida_bot = vida_bot - damage_espadas
        vida_jugador = vida_jugador - damage_espadas
        time.sleep(2)
        print(f"el jugador ahora tiene {vida_jugador} puntos de vida!")
        print(f"el bot ahora tiene {vida_bot} puntos de vida!")
    elif eleccion == "A" and eleccion_bot == "D":
        time.sleep(1)
        print("decides atacar al rival!")
        time.sleep(1)
        print("atacas y...")
        time.sleep(2)
        print("EL BOT HA PARADO TU ATAQUE!")
        vida_bot = vida_bot + damage_espadas
        vida_jugador = vida_jugador - damage_espadas
        bot_escudos = bot_escudos - 1
        time.sleep(2)
        print(f"el jugador ahora tiene {vida_jugador} puntos de vida!")
        print(f"el bot ahora tiene {vida_bot} puntos de vida!")
        print(f"el bot ahora tiene {bot_escudos}...")
    elif eleccion == "D" and eleccion_bot == "A":
        time.sleep(1)
        print("decides defenderte del rival")
        time.sleep(1)
        print("colocas tu escudo y...")
        time.sleep(2)
        print("HAZ PARADO EL ATAQUE DEL BOT!")
        jugador_escudos = jugador_escudos - 1
        vida_bot = vida_bot - damage_espadas
        vida_jugador = vida_jugador + damage_espadas
        time.sleep(2)
        print(f"el jugador ahora tiene {vida_jugador} puntos de vida!")
        print(f"el bot ahora tiene {vida_bot} puntos de vida!")
        print(f"ahora te quedan{jugador_escudos}...")
    else:
         time.sleep(1)
         print("decides defenderte del rival")
         time.sleep(1)
         print("colocas tu escudo y...")
         time.sleep(2)
         print("AMBOS CABALLEROS SE HAN DEFENDIDO!")
         vida_bot = vida_bot 
         vida_jugador = vida_jugador 
         time.sleep(2)
         print(f"el jugador ahora tiene {vida_jugador} puntos de vida!")
         print(f"el bot ahora tiene {vida_bot} puntos de vida!")
    if vida_jugador <= 0:
        time.sleep(3)
        print("haz perdido la vida en combate!")
        break
    elif vida_bot <= 0:
        time.sleep(3)
        print("el bot cae en batalla haz ganado")
        break

    





        

