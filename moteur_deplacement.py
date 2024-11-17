from rich.pretty import pprint
import numpy as np
import random

pos = [1, 2]
new_pos = pos.copy()
player = 9
alive = True
lives = 5
ennemies = 0

move_up = "z"
move_down = "s"
move_left = "q"
move_right = "d"


# Demande à l'utilisateur de choisir la difficulté du jeu, en saisissant le nombre de lignes et de colonnes, pour générer la map, et le nombre de vies
def choose_difficulty():
    def get_valid_input(prompt, condition, error_message, message):
        while True:
            value = input(prompt)
            try:
                value = int(value)
                if condition(value):
                    print(f"{message} {value}")
                    return value
                else:
                    print(error_message)
            except ValueError:
                print("Please enter a valid number")

    nb_row = get_valid_input("Enter the number of rows: ", lambda x: x < 50, "This number must not exceed 50", "Number of rows: ")
    nb_level = get_valid_input("Enter the number of levels: ", lambda x: x < 50, "This number must not exceed 50", "Number of levels: ")
    nb_lives = get_valid_input("Enter the number of lives: ", lambda x: x > 0, "This number must be greater than 0", "Number of lives: ")

    return nb_row, nb_level, nb_lives

# Génère la map en fonction du nombre de lignes et de colonnes choisi par l'utilisateur
def gennerate_map(nb_row = 4, nb_level = 4):
    carte = np.array([
        [random.randint(0, 1) for _ in range(nb_row)] for _ in range(nb_level)
    ])
    
    return carte

# Compte le nombre d'ennemies sur la map
def count_enemies(carte):
    ennemies = sum(sum(row) for row in carte)
    print(f"Freaking {ennemies} ennemies out there ! ")
    return ennemies

nb_row, nb_level, lives = choose_difficulty()
carte = gennerate_map(nb_row, nb_level)
ennemies = count_enemies(carte)
x_limit = [0, len(carte[0]) - 1]
y_limit = [0, len(carte) - 1]

carte[pos[0], pos[1]] = player
print(carte)


# Fonction principale du jeu, qui permet de jouer, de se déplacer, de combattre, et de mettre à jour la carte
def play(alive, ennemies, lives = 5):
    remaining_lives = lives
    remaining_ennemies = ennemies
    fight = True
    won_fights = 0
    while alive:
        direction = ""
        while direction != "z" and direction != "s" and direction != "q" and direction != "d":
            direction = input("Enter a move: ")
            
        new_pos, error = move(direction)
        if (new_pos != pos) and (error == False):
            if carte[new_pos[0], new_pos[1]] == 1:
                fight, remaining_lives, remaining_ennemies, won_fights = combat(remaining_lives, remaining_ennemies, won_fights)
                if remaining_lives == 0:
                    print("Game over")
                    print(f"You killed {won_fights} {"ennemies" if won_fights > 1 else "ennemy"}")
                    alive = False
                    break
            update_carte(pos, new_pos, fight)
        print(carte)


# Determine la nouvelle direction sur la map en fonction de la direction saisie par le joueur
def move(direction):
    error = False
    if direction == move_up:
        error = check_boundary(new_pos[0], y_limit[0], "up")
        if not error:
            new_pos[0] -= 1
    elif direction == move_down:
        error = check_boundary(new_pos[0], y_limit[1], "down")
        if not error:
            new_pos[0] += 1
    elif direction == move_left:
        error = check_boundary(new_pos[1], x_limit[0], "left")
        if not error:
            new_pos[1] -= 1
    elif direction == move_right:
        error = check_boundary(new_pos[1], x_limit[1], "right")
        if not error:
            new_pos[1] += 1
            
    return new_pos, error

def check_boundary(pos, limit, direction):
    if pos == limit:
        print(f"Can't move {direction}")
        return True
    return False

# Met à jour la carte en fonction du combat, et change la position du joueur
def update_carte(pos, new_pos, fight):
    if fight:
        carte[pos[0], pos[1]] = 0
    else:
        carte[pos[0], pos[1]] = 1
    carte[new_pos[0], new_pos[1]] = player
    pos[0] = new_pos[0]
    pos[1] = new_pos[1]    

        

# Entre en combat, jette un dès de 6, si 1, 2 ou 3, le joueur perd une vie et retourne le nombre de vie restante et le nombre d'ennemies restants
def combat(remaining_lives, remaining_ennemies, won_fights):
    if random.randint(1, 6) <= 3:
        print("You lost the fight")
        remaining_lives -= 1
        print(f"You have {remaining_lives} lives left")
        return False, remaining_lives, remaining_ennemies, won_fights
    else:
        remaining_ennemies -= 1
        won_fights += 1
        print("You won the fight")
        print(f"You have {remaining_lives} lives left")
        print(f"{remaining_ennemies} {"ennemies" if remaining_ennemies > 1 else "ennemy"} left !")
        return True, remaining_lives, remaining_ennemies, won_fights
    

play(alive, ennemies, lives)
    

# Je n'arrive pas à faire en sorte que mon personnage ne bouge pas lorsque je perds le combat