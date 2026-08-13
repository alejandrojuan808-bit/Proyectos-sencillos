from app.auth import AuthError, InvalidCredentialsError, UserAlreadyExistsError, login_user, register_user


def menu() -> None:
    print("=== Autenticador de usuarios ===")
    while True:
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        option = input("Elige una opción: ").strip()

        if option == "1":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            try:
                result = register_user(username, password)
                print(result["message"])
            except (AuthError, ValueError) as exc:
                print(f"Error: {exc}")

        elif option == "2":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            try:
                result = login_user(username, password)
                print(result["message"])
            except (InvalidCredentialsError, ValueError) as exc:
                print(f"Error: {exc}")

        elif option == "3":
            print("Hasta luego.")
            break

        else:
            print("Opción inválida. Intenta otra vez.")


if __name__ == "__main__":
    menu()
