import pygame
from pygame.locals import *
import random

# Initialiser Pygame
pygame.init()

# Paramètres de l'écran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont('arial', 35)
font2 = pygame.font.SysFont('arial', 25)
font3 = pygame.font.SysFont('arial', 20)  # Police pour afficher les lettres utilisées

# Lire les mots du fichier, en enlevant les espaces et les sauts de ligne
with open("mots.txt", "r") as fichier:
    mots = [ligne.strip().replace(' ', '') for ligne in fichier]

# Choisir un mot aléatoire et créer la représentation affichée du mot
mot = random.choice(mots)
mot_affiche_liste = ['_' for _ in mot]  # Liste pour stocker les lettres trouvées

# Création des textes
text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0))
text2 = font.render('Jeu du pendu', True, (0, 0, 0))
text3 = font2.render(f'Il reste {9} tentatives', True, (0, 0, 0))

# Chargement des images
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

# Paramètres du jeu
tentatives_restantes = 9
current_image_index = 0
current_image = images[current_image_index]
lettres_utilisees = set()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            lettre = pygame.key.name(event.key)
            if lettre.isalpha() and len(lettre) == 1:  # Vérifier que c'est une lettre unique
                lettre = lettre.lower()  # Convertir en minuscule
                if lettre not in lettres_utilisees:
                    lettres_utilisees.add(lettre)
                    if lettre in mot:
                        for i, l in enumerate(mot):
                            if l == lettre:
                                mot_affiche_liste[i] = lettre
                    else:
                        tentatives_restantes -= 1
                        current_image_index = 9 - tentatives_restantes
                        current_image = images[current_image_index]
                    text1 = font.render(" ".join(mot_affiche_liste), True, (0, 0, 0))
                    text3 = font2.render(f'Il reste {tentatives_restantes} tentatives', True, (0, 0, 0))

    # Vérifier les conditions de victoire ou de défaite
    if '_' not in mot_affiche_liste:
        print("Victoire !")
        running = False
    elif tentatives_restantes <= 0:
        print("Défaite ! Le mot était:", mot)
        running = False

    # Mettre à jour l'écran
    screen.fill((255, 255, 255))
    screen.blit(current_image, (500, 100))
    screen.blit(text1, (100, 400))
    screen.blit(text2, (300, 10))
    screen.blit(text3, (25, 100))

    # Afficher les lettres déjà utilisées
    lettres_utilisees_text = 'Lettres utilisées: ' + ' '.join(sorted(lettres_utilisees))
    text4 = font3.render(lettres_utilisees_text, True, (0, 0, 0))
    screen.blit(text4, (100, 500))  # Ajuster la position selon vos besoins

    pygame.display.update()

pygame.quit()