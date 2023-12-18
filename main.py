import pygame
import pygame_menu
from pygame.locals import *
import random

# Initialisation de Pygame
pygame.init()

# Réglages de l'écran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Styles de texte
font = pygame.font.SysFont('arial', 35)
font2 = pygame.font.SysFont('arial', 25)
font3 = pygame.font.SysFont('arial', 20) # Mise à jour de font3 ici si nécessaire

# Variables globales pour le mode de jeu et le nom du joueur
difficulte = "normal"
nom_joueur = "Joueur 1"

# Fonction pour afficher le résultat final
def afficher_resultat(screen, gagne, mot, score): 
    screen.fill((255, 255, 255))
    message = "Victoire !" if gagne else f"Défaite ! Le mot était: {mot}" 
    font_resultat = pygame.font.SysFont('arial', 35)
    texte_resultat = font_resultat.render(message, True, (0, 0, 0))
    screen.blit(texte_resultat, (100, 200))
    pygame.display.update()
    pygame.time.wait(2000) # Attente de 2 secondes avant de continuer
    enregistrer_score(score)

# Fonction pour jouer au pendu
def jouer_pendu():
    global difficulte, nom_joueur
    score = 0
    multiplicateur = 2 if difficulte == "difficile" else 1
    with open("mots.txt", "r") as fichier: # Lire les mots du fichier, en enlevant les espaces et les sauts de ligne
        mots = [ligne.strip() for ligne in fichier] # ligne.strip(): Enlève les espaces, les tabulations, et les sauts de ligne du début et de la fin de la ligne
    mot = random.choice(mots) # on utilise la biblo random pour choisir un mot aléatoirement dans le fichier mots.txt qu'on a chargé précédemment avec with open 
    mot_affiche_liste = ['_' for _ in mot] # liste pour stocker les lettres trouvées

    #on met les images de notre dossier images dans une liste en les chargeant, cela permettra de faire évoluer l'indice des images sous certaines conditions 
    #pour que lorsque l'utilisateur se trompe, images[0] passe à images[1]
    images = [
        pygame.image.load('images\\pendu0.jpg'), #[0]
        pygame.image.load('images\\pendu1.jpg'), #[1]
        pygame.image.load('images\\pendu2.jpg'), #[2]
        pygame.image.load('images\\pendu3.jpg'), #[3]
        pygame.image.load('images\\pendu4.jpg'), #[4]
        pygame.image.load('images\\pendu5.jpg'), #[5]
        pygame.image.load('images\\pendu6.jpg'), #[6]
        pygame.image.load('images\\pendu7.jpg'), #[7]
        pygame.image.load('images\\pendu8.jpg'), #[8]
        pygame.image.load('images\\pendu9.jpg'), #[9]
    ]

    tentatives_restantes = 6 if difficulte == "difficile" else 9
    current_image_index = 3 if difficulte == "difficile" else 0

    current_image = images[current_image_index]
    lettres_utilisees = set()
    running = True

    while running:
        text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0))
        text2 = font.render('Jeu du pendu', True, (0, 0, 0))   #texte qui va s'afficher dans pygame texte/aliasing/couleur du texte
        text_nom_joueur = font2.render(f'Joueur: {nom_joueur}', True, (0, 0, 0))
        text_score = font3.render(f'Score: {score}', True, (0, 0, 0))
        text_tentatives = font2.render(f'Tentatives: {tentatives_restantes}', True, (0, 0, 0))
        lettres_utilisees_text = 'Lettres utilisées: ' + ' '.join(sorted(lettres_utilisees))
        text4 = font3.render(lettres_utilisees_text, True, (0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # si l'utilisateur appuie sur la croix rouge la boucle arrête de "run" et cela ferme le programme
                running = False
            elif event.type == pygame.KEYDOWN: # vérifie que l'utilisateur a appuyé sur une touche
                lettre = pygame.key.name(event.key).lower() # obtient le nom de la touche pressée en minuscule
                if lettre.isalpha() and len(lettre) == 1 and lettre not in lettres_utilisees:  # vérifie que la lettre n'a pas déjà utilisé, isalpha vérifie si c'est une lettre de l'alphabet et len qu'il n'y a qu'un seul caractère 
                    lettres_utilisees.add(lettre)  # si la condition ci-dessus est respectée, ajoute la lettre entrée par l'utilisateur à l'ensemble lettres_utilisées
                    if lettre in mot: # si la lettre rentrée par l'utilisateur est dans la variable mot
                        score += 10 * multiplicateur
                        for i, l in enumerate(mot): # for i, l in enumerate(mot): est une boucle for qui parcourt chaque lettre l dans le mot, tout en conservant son index i grâce à la fonction enumerate.
                                                    # enumerate(mot) retourne une paire (index, élément) pour chaque lettre dans le mot. Par exemple, si mot est "python", la boucle itérera sur (0, 'p'), (1, 'y'), (2, 't') etc
                            if l == lettre:
                                mot_affiche_liste[i] = lettre  # permet d'afficher la lettre entrer par l'utilisateur sur l'écran exemple si e pour abeille __e___e
                        text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0))
                    else:
                        score -= 5 * multiplicateur
                        tentatives_restantes -= 1 # change la valeur de la variable tentatives_restantes en lui enlevant 1
                        if difficulte == "normal":
                            current_image_index = 9 - tentatives_restantes
                        else:
                            current_image_index = 6 - tentatives_restantes + 3
                            
                        if current_image_index < 0:
                            current_image_index = 0
                        if current_image_index >= len(images):
                            current_image_index = len(images) - 1
                        current_image = images[current_image_index]

        if '_' not in mot_affiche_liste:  # Condition de victoire
            afficher_resultat(screen, True, mot, score)
            running = False
        elif tentatives_restantes <= 0:  # Condition de défaite
            afficher_resultat(screen, False, mot, score)
            running = False

        screen.fill((255, 255, 255))
        screen.blit(current_image, (500, 100))
        screen.blit(text1, (100, 400))
        screen.blit(text2, (300, 10))
        screen.blit(text_nom_joueur, (25, 50))
        screen.blit(text_score, (25, 80))
        screen.blit(text_tentatives, (25, 110))
        screen.blit(text4, (100, 500))

        pygame.display.update()

# Fonction pour enregistrer le score
def enregistrer_score(score):
    global nom_joueur
    try:
        with open("scores.txt", "a") as fichier:
            fichier.write(f"{nom_joueur}: {score}\n")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'enregistrement du score : {e}")

# Fonction pour afficher les scores
def afficher_scores():
    try:
        with open("scores.txt", "r") as fichier:
            scores = fichier.readlines()
    except FileNotFoundError:
        scores = ["Aucun score enregistré.\n"]

    menu_scores = pygame_menu.Menu('Tableau des Scores', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    for score in scores:
        menu_scores.add.label(score.strip(), align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    menu_scores.add.button('Retour', menu_principal)
    menu_scores.mainloop(screen)


# Menu pour ajouter un mot
def ajouter_un_mot():
    menu_ajout = pygame_menu.Menu('Ajouter un Mot', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    user_input = menu_ajout.add.text_input('Mot :', maxchar=10)
    menu_ajout.add.button('Ajouter', lambda: onreturn(menu_ajout, user_input))
    menu_ajout.add.button('Retour', menu_principal)
    menu_ajout.mainloop(screen)

def onreturn(menu_ajout, user_input):
    action_ajouter(user_input.get_value())
    menu_ajout.reset(1)



# Fonction pour ajouter un mot au fichier
def action_ajouter(mot):
    mot = mot.lower()
    if mot and mot.isalpha():
        with open("mots.txt", "a") as fichier:
            fichier.write(f"\n{mot}")
        afficher_message_temporaire(f"Le mot '{mot}' a été ajouté.")
    else:
        afficher_message_temporaire(f"Le mot '{mot}' n'a pas pu être ajouté, veuillez utiliser seulement des lettres minuscules svp.")


# Fonction pour afficher un message temporaire
def afficher_message_temporaire(message, duree=2000):
    text_message = font2.render(message, True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text_message, (screen_width // 2 - text_message.get_width() // 2, screen_height // 2 - text_message.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(duree)


# Fonction de démarrage du jeu
def start_the_game(mode):
    global difficulte, nom_joueur
    difficulte = mode
    nom_joueur = menu.get_input_data()['Nom :']
    if not nom_joueur.strip():
        nom_joueur = "Joueur 1"
    jouer_pendu()

# Menu principal
def menu_principal():
    global menu
    menu = pygame_menu.Menu('Jeu du pendu', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Nom :', default='Joueur 1', textinput_id='Nom :')
    menu.add.button('Mode Normal', lambda: start_the_game("normal"))
    menu.add.button('Mode Difficile', lambda: start_the_game("difficile"))
    menu.add.button('Tableau des Scores', afficher_scores)
    menu.add.button('Ajouter un mot', ajouter_un_mot)
    menu.add.button('Quitter', pygame_menu.events.EXIT)
    menu.mainloop(screen)

# Lancement du menu principal
menu_principal()

# Quitter Pygame
pygame.quit()
print("Merci d'avoir joué !")