# =============================================================================
# CONFIGURATION DU JEU
# =============================================================================
# 
# POURQUOI CE CHOIX WINDOWS / MAC ?
# ---------------------------------
# Le jeu a été développé sur Windows où il tournait à ~120-150 FPS.
# Sur Mac (MacBook), le FPS est limité à 60 Hz.
#
# Le problème : le mouvement du personnage dépend du nombre de frames.
#   - Sur Windows à 120 FPS : le personnage bouge de 5 pixels × 120 = 600 px/sec
#   - Sur Mac à 60 FPS : le personnage bouge de 5 pixels × 60 = 300 px/sec
#   → Le jeu est 2x plus lent sur Mac !
#
# La solution : on demande à l'utilisateur son système et on ajuste les
# valeurs de vitesse, gravité et saut pour que le gameplay soit identique.
#
# =============================================================================

WIDTH = 800
HEIGHT = 800

# Demande du système à l'utilisateur
print("=" * 40)
print("Sur quel système tu joues ?")
print("1 - Windows")
print("2 - Mac")
print("=" * 40)
choix = input("Ton choix (1 ou 2) : ")

if choix == "2":
    # ----- MODE MAC -----
    # Mac est limité à 60 FPS (écran Retina)
    # On augmente les vitesses pour compenser le FPS plus bas
    FPS = 60
    PLAYER_SPEED = 15      # Plus rapide car moins de frames
    PLAYER_GRAVITY = 1.5   # Chute plus rapide
    PLAYER_JUMP = -22      # Saut plus puissant
    print("Mode Mac activé !")
else:
    # ----- MODE WINDOWS -----
    # Windows peut aller jusqu'à 120+ FPS
    # Valeurs originales du jeu
    FPS = 120
    PLAYER_SPEED = 5       # Vitesse normale
    PLAYER_GRAVITY = 0.5   # Gravité normale
    PLAYER_JUMP = -15      # Saut normal
    print("Mode Windows activé !")