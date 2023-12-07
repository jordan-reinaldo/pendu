import pygame
import pygame_menu
from pygame.locals import *
import random

# Initialisation de Pygame
pygame.init()

# screen settings 
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont('arial', 35) # style des textes 
font2 = pygame.font.SysFont('arial', 25)
font3 = pygame.font.SysFont('arial', 20)

# Fonction pour afficher le résultat final
def afficher_resultat(screen, gagne, mot):
    screen.fill((255, 255, 255))  # affiche l'écran
    message = "Victoire !" if gagne else f"Défaite ! Le mot était: {mot}"
    font_resultat = pygame.font.SysFont('arial', 35)
    texte_resultat = font_resultat.render(message, True, (0, 0, 0))
    screen.blit(texte_resultat, (100,200))
    pygame.display.update()
    pygame.time.wait(2000) # Attente de 2 secondes avant de continuer

def jouer_pendu():
    with open("mots.txt", "r") as fichier: # Lire les mots du fichier, en enlevant les espaces et les sauts de ligne
        mots = [ligne.strip() for ligne in fichier] #ligne.strip(): Enlève les espaces, les tabulations, et les sauts de ligne du début et de la fin de la lign

    mot = random.choice(mots) #on utilise la biblo random pour choisir un mot aléatoirement dans le fichier mots.txt qu'on a chargé précédemment avec with open 
    mot_affiche_liste = ['_' for _ in mot] # liste pour stocker les lettres trouvées


    text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0))
    text2 = font.render('Jeu du pendu', True, (0, 0, 0))
    text3 = font2.render(f'Il reste {9} tentatives', True, (0, 0, 0))

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

    # settings du jeu 

    tentatives_restantes = 9
    current_image_index = 0
    current_image = images[current_image_index]
    lettres_utilisees = set() # les sets sont souvent utilisés pour contrôler les doublons
    running = True # permet d'amorcer la boucle, running deviendra false en fonction des conditions de cette dernière ce qui l'arrêtera
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # si l'utilisateur appuie sur la croix rouge la boucle arrête de "run" et cela ferme le programme
                running = False
            elif event.type == pygame.KEYDOWN: # vérifie que l'utilisateur a appuyé sur une touche
                lettre = pygame.key.name(event.key).lower() # obtient le nom de la touche pressée
                if lettre.isalpha() and len(lettre) == 1 and lettre not in lettres_utilisees: # vérifie que la lettre n'a pas déjà utilisé, isalpha vérifie si c'est une lettre de l'alphabet et len qu'il n'y a qu'un seul caractère 
                    lettre = lettre.lower() # lower sert à mettre en minuscule
                    if lettre not in lettres_utilisees: #si la lettre n'a pas déjà été utilisé
                        lettres_utilisees.add(lettre) #si la condition ci-dessus est respectée, ajoute la lettre entrée par l'utilisateur à l'ensemble lettres_utilisées
                    if lettre in mot: #si la lettre rentrée par l'utilisateur est dans la variable mot
                        for i, l in enumerate(mot):# for i, l in enumerate(mot): est une boucle for qui parcourt chaque lettre l dans le mot, tout en conservant son index i grâce à la fonction enumerate.
                                                   # enumerate(mot) retourne une paire (index, élément) pour chaque lettre dans le mot. Par exemple, si mot est "python", la boucle itérera sur (0, 'p'), (1, 'y'), (2, 't') etc
                            if l == lettre:
                                mot_affiche_liste[i] = lettre # permet d'afficher la lettre entrer par l'utilisateur sur l'écran exemple si e pour abeille __e___e
                    else:
                        tentatives_restantes -= 1 # change la valeur de la variable tentatives_restantes en lui enlevant 1
                        current_image_index = 9 - tentatives_restantes # nous avons 10 images donc [0] à [9] vu que nous réduisons à chaque erreur la valeur de tenta...
                                                                       #imaginons que l'utilisateur ait fait un fail, l'index image serait 9-8=1 et donc images[1]
                        current_image = images[current_image_index]    #on met à jours l'image affichée
                    text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0)) # met à jour l'affichage des lettres entrées par l'utilisateur a _ e par exemple, join assemble les _ et les lettres trouvées
                    text3 = font2.render(f'Il reste {tentatives_restantes} tentatives', True, (0, 0, 0)) # met à jour le texte de tenta.. entrant la valeur de la variable tenta..

        # conditions de victoire ou de défaite
        if '_' not in mot_affiche_liste:
            menu_fin_de_partie(True, mot)
            running = False
        elif tentatives_restantes <= 0:
            menu_fin_de_partie(False, mot)
            running = False

        screen.fill((255, 255, 255))
        screen.blit(current_image, (500, 100))
        screen.blit(text1, (100, 400))
        screen.blit(text2, (300, 10))
        screen.blit(text3, (25, 100))

        lettres_utilisees_text = 'Lettres utilisées: ' + ' '.join(sorted(lettres_utilisees))
        text4 = font3.render(lettres_utilisees_text, True, (0, 0, 0))
        screen.blit(text4, (100, 500))

        pygame.display.update()

# Fonction de démarrage du jeu
def start_the_game():
    jouer_pendu()

# Menu principal
def menu_principal():
    menu = pygame_menu.Menu('Bienvenue', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input('Nom :', default='Joueur 1')
    menu.add.button('Jouer', start_the_game)
    menu.add.button('Ajouter un mot', ajouter_un_mot)
    menu.add.button('Quitter', pygame_menu.events.EXIT)
    menu.mainloop(screen)

# Menu de fin de partie
def menu_fin_de_partie(gagne, mot):
    fin_text = "Victoire!" if gagne else f"Défaite! Le mot était: {mot}"
    menu = pygame_menu.Menu(fin_text, 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Rejouer', menu_principal)
    menu.add.button('Quitter', pygame_menu.events.EXIT)
    menu.mainloop(screen)

# Fonction pour ajouter un mot au fichier
def action_ajouter(mot):
    mot = mot.lower()
    # Vérifie que le mot n'est pas vide et contient uniquement des lettres
    if mot and mot.isalpha():
        with open("mots.txt", "a") as fichier:
            fichier.write(f"\n{mot}")  # Ajoute le mot à une nouvelle ligne
        print(f"Mot '{mot}' ajouté avec succès.")
    else:
        print(f"Erreur: '{mot}' n'est pas un mot valide.")
        

# Menu pour ajouter un mot
def ajouter_un_mot():
    menu_ajout = pygame_menu.Menu('Ajouter un Mot', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    
    def onreturn(user_input):
        # Obtient le mot du champ de texte pour l'ajouter au fichier
        action_ajouter(user_input.get_value())  # Utilisez get_value() pour obtenir la valeur du champ de texte

    # Ajoute un champ de saisie avec une fonction de retour personnalisée
    user_input = menu_ajout.add.text_input('Mot :', maxchar=10)  # Vous pouvez ajuster maxchar selon vos besoins
    menu_ajout.add.button('Ajouter', lambda: onreturn(user_input))  # Utilise une lambda pour passer l'input
    
    menu_ajout.add.button('Retour', menu_principal)
    menu_ajout.mainloop(screen)



# Lancement du menu principal
menu_principal()

# Quitter Pygame
pygame.quit()
print("Merci d'avoir joué !")