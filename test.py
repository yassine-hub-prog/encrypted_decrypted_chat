import os
import time
from supabase import create_client, Client

# Configuration Supabase
url: str = "https://eftdciuyoqhchrurpnmg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmdGRjaXV5b3FoY2hydXJwbm1nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1ODUwMTIsImV4cCI6MjA0NjE2MTAxMn0.5RJms-hyR52Cmi9MvFutHwJj1wqhBINdlWBFDMN2RtI"

# Initialiser le client Supabase
supabase: Client = create_client(url, key)
user_uuid = None  # Variable pour stocker l'UUID de l'utilisateur

# Fonction pour effacer la console (compatible Windows, macOS, Linux)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction de connexion anonyme
def connect_anonymously():
    global user_uuid
    try:
        response = supabase.auth.sign_in_anonymously()
        user = response.user  # Accède directement à l'attribut 'user'
        if user:
            user_uuid = user.id  # Accède à l'ID de l'utilisateur via l'attribut 'id'
            print("Inscription anonyme réussie !")
            return response
        else:
            print("Erreur : utilisateur non trouvé dans la réponse.")
    except Exception as e:
        print("Erreur lors de l'inscription anonyme:", e)
    return None


# Fonction pour mettre à jour le nom d'utilisateur
def update_username(new_username):
    global user_uuid
    if user_uuid:
        try:
            response = supabase.table("users").update({"username": new_username}).eq("uuid", user_uuid).execute()
            print(f"Nom d'utilisateur mis à jour avec succès en : {new_username}")
            return response
        except Exception as e:
            print("Erreur lors de la mise à jour du nom d'utilisateur:", e)
    else:
        print("Erreur : Aucun utilisateur connecté.")
    return None

# Fonction pour afficher le menu de gestion du compte
def account_management_menu():
    while True:
        clear_console()
        print("Account Management :")
        print("{:<10} {:<20}".format("Key", "| Option"))
        print("-" * 11 + '|'  + "-" * 25)
        print("{:<10} {:<20}".format("1", "| Edite Username"))
        print("{:<10} {:<20}".format("2", "| Logout and delete account"))
        print("{:<10} {:<20}".format("99", "| Back"))

        choice = input("Choisissez une option : ")
        if choice == '1':
            new_username = input("Entrez le nouveau nom d'utilisateur : ")
            update_username(new_username)
            time.sleep(2)
        elif choice == '2':
            print("successfully Logout.")
            return False  # Déconnecte l'utilisateur
        elif choice == '99':
            break
        else:
            print("Invalid choice, please try again.")
            time.sleep(1)
    return True  # Utilisateur toujours connecté

# Fonction pour afficher le menu principal
def display_menu(user_connected):
    print("Menu :")
    print("{:<10} {:<20}".format("Key", "| Service"))
    print("-" * 11 + '|'  + "-" * 25)

    if user_connected:
        print("{:<10} {:<20}".format("1", "| \033[92mUser Connected\033[0m"))  # Affiche en vert si connecté
    else:
        print("{:<10} {:<20}".format("1", "| Log in as an anonymous user"))
        
    print("{:<10} {:<20}".format("2", "| Account management"))
    print("{:<10} {:<20}".format("3", "| See all users"))
    print("{:<10} {:<20}".format("4", "| Leave and delete account"))

    choice = input("Choisissez une option : ")
    return choice


def display_users():
    page = 0
    users_per_page = 10

    # ANSI color codes
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    while True:
        clear_console()
        print("Users List (page {}) :".format(page + 1))

        # Retrieve users from the database with pagination
        response = supabase.table("users").select("uuid, username, online").range(page * users_per_page, (page + 1) * users_per_page - 1).execute()
        users = response.data  # List of retrieved users

        if not users:
            print("No users found.")
            return

        # Sort users so that Online users appear first
        users = sorted(users, key=lambda user: not user.get('online'))

        # Display users with keys
        for i, user in enumerate(users):
            status = f"{GREEN}Online{RESET}" if user.get('online') else f"{RED}Offline{RESET}"
            print("{:<10} {:<20}".format(i + 1, f"UUID: {user['uuid']}, Username: {user['username']}, Online: {status}"))

        print("\nOptions :")
        print("'Press Enter' - Next Page")
        print("'99' - Retour au menu principal")
        print("Numéro de clé d'un utilisateur pour afficher le profil")

        choice = input("Choisissez une option : ")

        # Handle user choice
        if choice == "":
            page += 1  # Go to the next page
        elif choice == "99":
            break  # Return to the main menu
        elif choice.isdigit() and 1 <= int(choice) <= len(users):
            user_index = int(choice) - 1
            show_user_profile(users[user_index])  # Display the selected user's profile
            input("Appuyez sur Entrée pour revenir à la liste...")
        else:
            print("Choix invalide, veuillez réessayer.")
            time.sleep(2)


def show_user_profile(user):
    clear_console()
    print("Profil de l'Utilisateur :")
    print("UUID     :", user['uuid'])
    print("Username :", user['username'])
    print("\nFin du profil")

# Mettre à jour la gestion du menu principal pour inclure le service B
def main():
    user_connected = False
    while True:
        clear_console()
        choice = display_menu(user_connected)
        
        if choice == '1':
            if not user_connected:
                # Se connecter en tant qu'utilisateur anonyme
                response = connect_anonymously()
                if response:
                    user_connected = True
                    print("Vous êtes maintenant connecté.")
                time.sleep(2)  # Pause pour afficher le message
            else:
                print("Vous êtes déjà connecté.")
                time.sleep(2)
        elif choice == '2':
            if user_connected:
                clear_console()
                print("Service A : Gestion du compte")
                user_connected = account_management_menu()  # Appelle le menu de gestion de compte
            else:
                print("Veuillez d'abord vous connecter.")
            time.sleep(2)
        elif choice == '3':
            if user_connected:
                clear_console()
                print("Service B : Afficher la liste des utilisateurs")
                display_users()  # Afficher les utilisateurs
            else:
                print("Veuillez d'abord vous connecter.")
            time.sleep(2)
        elif choice == '4':
            print("Au revoir !")
            break
        else:
            print("Choix invalide, veuillez réessayer.")
            time.sleep(2)

# Exécution du programme principal
if __name__ == "__main__":
    main()