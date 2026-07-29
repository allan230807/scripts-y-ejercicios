import random 
def generate_password(length=10):
    if length < 10:
        raise ValueError("Password length should be at least 10 characters.")
    characters = "asdfghjklpoiuytrewqzxcvbnmASDFGHJKLPOIUYTREWQZXCVBNM1234567890!@#$%^&*()_+-=[]{}|;:',.<>/?"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
if __name__ == "__main__":
        try:
            user_length = int(input("Ingresa la longitud de la contraseña (mínimo 10): "))
            print("Tu contraseña generada es:", generate_password(user_length))
        except ValueError as e:
            print(f"Error: {e}")

  

