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
        
    