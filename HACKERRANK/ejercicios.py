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