brazos = []
torso = []
piernas = []
diccionario = { "brazos": brazos, "torso": torso, "piernas": piernas }
while True: 
    
  def agregar_ejercicio(diccionario, grupo_muscular, ejercicio, peso):
    if grupo_muscular in diccionario:
        diccionario[grupo_muscular].append((ejercicio, peso))
    else:
        print("El grupo muscular no existe en el diccionario.")
    return diccionario
  for grupo, ejercicios in diccionario.items():
    print(f"{grupo.capitalize()}: {', '.join([f'{e[0]} ({e[1]})' for e in ejercicios])}")
  if __name__ == "__main__":
    grupo_muscular = input("Ingresa el grupo muscular al que deseas agregar un ejercicio (brazos, torso, piernas): ").lower()
    if grupo_muscular == "salir":
        break
    ejercicio = input("Ingresa el nombre del ejercicio que deseas agregar: ")
    peso = input("Ingresa el peso que deseas agregar para el ejercicio: ")
    diccionario_actualizado = agregar_ejercicio(diccionario, grupo_muscular, ejercicio, peso)
    print("\nDiccionario actualizado:")
  


