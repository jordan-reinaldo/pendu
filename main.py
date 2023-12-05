import pygame
from pygame.locals import *
import random

pygame.init()

# screen settings 
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont('arial', 35) #style des textes 
font2 = pygame.font.SysFont('arial', 25)
font3 = pygame.font.SysFont('arial', 20) 

def jouer_pendu():

    # Lire les mots du fichier, en enlevant les espaces et les sauts de ligne
    with open("mots.txt", "r") as fichier:
        mots = [ligne.strip().replace(' ', '') for ligne in fichier]

    mot = random.choice(mots) #on utilise la biblo random pour choisir un mot aléatoirement dans le fichier mots.txt qu'on a chargé précédemment avec with open 
    mot_affiche_liste = ['_' for _ in mot]  # liste pour stocker les lettres trouvées

    # textes
    text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0))
    text2 = font.render('Jeu du pendu', True, (0, 0, 0))
    text3 = font2.render(f'Il reste {9} tentatives', True, (0, 0, 0))


    #on met les images de notre dossier images dans une liste en les chargeant, cela permettra de faire évoluer l'indice des images sous certaines conditions 
    #pour que lorsque l'utilisateur se trompe, images[0] passe à images[1]
    images = [
        pygame.image.load('images\\pendu0.jpg'),
        pygame.image.load('images\\pendu1.jpg'),
        pygame.image.load('images\\pendu2.jpg'),
        pygame.image.load('images\\pendu3.jpg'),
        pygame.image.load('images\\pendu4.jpg'),
        pygame.image.load('images\\pendu5.jpg'),
        pygame.image.load('images\\pendu6.jpg'),
        pygame.image.load('images\\pendu7.jpg'),
        pygame.image.load('images\\pendu8.jpg'),
        pygame.image.load('images\\pendu9.jpg'),
    ]

    # settings du jeu 
    tentatives_restantes = 9
    current_image_index = 0
    current_image = images[current_image_index]
    lettres_utilisees = set() #les sets sont souvent utilisés pour contrôler les doublons

    running = True #permet d'amorcer la boucle, running deviendra false en fonction des conditions de cette dernière ce qui l'arrêtera
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #si l'utilisateur appuie sur la croix rouge la boucle arrête de "run" et cela ferme le programme
                running = False
            elif event.type == pygame.KEYDOWN: #vérifie que l'utilisateur a appuyé sur une touche
                lettre = pygame.key.name(event.key) #obtient le nom de la touche pressée
                if lettre.isalpha() and len(lettre) == 1:  # vérifie que la lettre n'a pas déjà utilisé, isalpha vérifie si c'est une lettre de l'alphabet et len qu'il n'y a qu'un seul caractère 
                    lettre = lettre.lower()  # lower sert à mettre en minuscule
                    if lettre not in lettres_utilisees: #si la lettre n'a pas déjà été utilisé
                        lettres_utilisees.add(lettre) #si la condition ci-dessus est respectée, ajoute la lettre entrée par l'utilisateur à l'ensemble lettres_utilisées
                        if lettre in mot: #si la lettre rentrée par l'utilisateur est dans la variable mot
                            for i, l in enumerate(mot):#for i, l in enumerate(mot): est une boucle for qui parcourt chaque lettre l dans le mot, tout en conservant son index i grâce à la fonction enumerate.
                                                    #enumerate(mot) retourne une paire (index, élément) pour chaque lettre dans le mot. Par exemple, si mot est "python", la boucle itérera sur (0, 'p'), (1, 'y'), (2, 't') etc
                                if l == lettre:
                                    mot_affiche_liste[i] = lettre #permet d'afficher la lettre entrer par l'utilisateur sur l'écran exemple si e pour abeille __e___e
                        else:
                            tentatives_restantes -= 1 #change la valeur de la variable tentatives_restantes en lui enlevant 1
                            current_image_index = 9 - tentatives_restantes #nous avons 10 images donc [0] à [9] vu que nous réduisons à chaque erreur la valeur de tenta...
                                                                        #imaginons que l'utilisateur ait fait un fail, l'index image serait 9-8=1 et donc images[1]
                            current_image = images[current_image_index]    #on met à jours l'image affichée
                        text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0)) #met à jour l'affichage des lettres entrées par l'utilisateur a _ e par exemple, join assemble les _ et les lettres trouvées
                        text3 = font2.render(f'Il reste {tentatives_restantes} tentatives', True, (0, 0, 0)) #met à jour le texte de tenta.. entrant la valeur de la variable tenta..

        # conditions de victoire ou de défaite (les prints s'affichent dans le terminal)
        if '_' not in mot_affiche_liste:
            print("Victoire !")
            running = False
        elif tentatives_restantes <= 0:
            print(f"Défaite ! Le mot était: {mot}")
            running = False
        
        # si aucune des deux conditions n'est respectée, la boucle redémarre. 

        # mettre à jour l'écran
        screen.fill((255, 255, 255))
        screen.blit(current_image, (500, 100)) #screen.blit permet de placer l'image 
        screen.blit(text1, (100, 400))#screen.blit permet de placer le texte, il permet de placer en quelque sorte l'élément
        screen.blit(text2, (300, 10))
        screen.blit(text3, (25, 100))

        lettres_utilisees_text = 'Lettres utilisées: ' + ' '.join(sorted(lettres_utilisees))
        text4 = font3.render(lettres_utilisees_text, True, (0, 0, 0))
        screen.blit(text4, (100, 500))  # Ajuster la position selon vos besoins

        pygame.display.update()

def demander_rejouer(screen):
    # Affiche une question sur l'écran avec Pygame
    
    font = pygame.font.SysFont('arial', 25)
    demande = font.render("Voulez-vous jouer à nouveau ? (O/N)", True, (0, 0, 0))
    screen.blit(demande, (100, 300))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    return True
                elif event.key == pygame.K_n:
                    return False

# Dans la boucle principale du programme
continuer = True
while continuer:
    jouer_pendu()
    continuer = demander_rejouer(screen)

pygame.quit()
print("Merci d'avoir joué !")