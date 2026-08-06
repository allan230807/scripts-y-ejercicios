if __name__ == '__main__':
    a = int(input())
    b = int(input())
    division = a // b 
    print(division)
    dividir = a%b
    print(dividir)
    print(divmod(a,b))



    #ejercicio 8

if __name__ == '__main__':
    a = int(input())
    b = int(input())
    m = int(input())
    print(pow(a,b))
    print(pow(a,b,m))

    #ejercicio 9 

if __name__ == '__main__':
    x = int(input())
    y = int(input())
    z = int(input())
    n = int(input())
    
    result = [[i, j, k] for i in range(x + 1) for j in range(y + 1) for k in range(z + 1) if i + j + k != n]
    
    print(result)

    #ejercicio 10

if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())
    unique_scores = sorted(set(arr))
    print(unique_scores[-2])

#ejercicio 11
if __name__ == '__main__':
    students = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        students.append([name, score])
    scores = sorted(set(student[1] for student in students))
    second_lowest_score = scores[1]
    second_lowest_students = sorted([
        student[0] for student in students if student[1] == second_lowest_score
    ])
    for name in second_lowest_students:
        print(name)

#ejercicio 12
if __name__ == '__main__':
    n = int(input())
    student_marks = {}
    for _ in range(n):
        name, *line = input().split()
        scores = list(map(float, line))
        student_marks[name] = scores
    query_name = input()
    query_scores = student_marks[query_name]
    average = sum(query_scores) / len(query_scores)
    print(f"{average:.2f}")

#ejercicio 13
if __name__ == '__main__':
    t = int(input()) 
    
    for _ in range(t):
        n = int(input())
        bloques = list(map(int, input().split()))
        
        left = 0
        right = len(bloques) - 1
        current_top = float('inf')
        posible = True
        
        while left <= right:
            if bloques[left] >= bloques[right]:
                cubo_elegido = bloques[left]
                left += 1
            else:
                cubo_elegido = bloques[right]
                right -= 1
                
            if cubo_elegido <= current_top:
                current_top = cubo_elegido  
            else:
                posible = False 
                break
    
        print("Yes" if posible else "No")
#ejercicio 14
import math
import os
import random
import re
import sys
import collections 



if __name__ == '__main__':
    s = input()
    cantidad = collections.Counter(s)
    mas_comunes = sorted(cantidad.items(), key = lambda x: (-x[1], x[0]))
    for letra, cantidad in mas_comunes[:3]:
       print(letra, cantidad)

#ejercicio 15

from collections import Counter

if __name__ == '__main__':
    num_zapatos = int(input())
    tallas_disponibles = list(map(int, input().split()))
    
    inventario = Counter(tallas_disponibles)
    num_clientes = int(input())
    ganancia_total = 0
    for _ in range(num_clientes):
        talla, precio = map(int, input().split())
        if inventario[talla] > 0:
            ganancia_total += precio
            inventario[talla] -= 1
    print(ganancia_total)

#ejercicio 16
if __name__ == '__main__':
    N = int(input())
    mi_lista = []
    
    for _ in range(N):
        partes = input().split()
        comando = partes[0]
        if comando == "insert":
            i = int(partes[1])
            e = int(partes[2])
            mi_lista.insert(i, e)
        elif comando == "print":
            print(mi_lista)
        elif comando == "remove":
            e = int(partes[1])
            mi_lista.remove(e)
        elif comando == "append":
            e = int(partes[1])
            mi_lista.append(e)
        elif comando == "sort":
            mi_lista.sort()
        elif comando == "pop":
            mi_lista.pop()
        elif comando == "reverse":
            mi_lista.reverse()

#ejercicio 17
from itertools import groupby
if __name__ == '__main__':
    cadena = input()
    resultados = []
    
    for caracter, grupo in groupby(cadena):
       cantidad = len(list(grupo))   
       numero = int(caracter)
       resultados.append((cantidad, numero))
    print(*resultados)

             
    
        
        
    