import pygame
import sys
# =============================================================================
# CONFIGURATION DU JEU - Résolution avec Delta Time
# =============================================================================
#
# AVANT : Le mouvement dépendait du FPS → Windows et Mac avaient une vitesse
#         différente. Solution : demander à l'user son OS au démarrage.
#
# MAINTENANT : On utilise le DELTA TIME (dt).
#   dt = temps en secondes écoulé entre chaque frame.
#   → Sur Mac à 60 FPS : dt ≈ 0.016 s
#   → Sur Windows à 120 FPS : dt ≈ 0.008 s
#   
#   En multipliant la vitesse par dt :
#   - Mac    : 450 px/s × 0.016 s = 7.2 px/frame
#   - Windows: 450 px/s × 0.008 s = 3.6 px/frame
#   → Sur les deux, le personnage parcourt bien 450 px en 1 seconde !
#   
#   RÉSULTAT : Windows, Mac, Linux → Jeu identique, aucune question posée !
# =============================================================================

WIDTH  = 800
HEIGHT = 800

# FPS cible. On peut mettre 0 pour déverrouiller, le dt s'adaptera.
FPS = 120

# Vitesses en PIXELS PAR SECONDE (plus de frames par seconde !)
PLAYER_SPEED   = 450    # 450 pixels par seconde
PLAYER_GRAVITY  = 1800  # 1800 pixels/s² (gravité)
PLAYER_JUMP    = -700   # -700 px/s (vitesse initiale du saut)

# les touches sont stockées dans les différents variables
haut    = "z"
bas     = "s"
gauche  = "q"
droite  = "d"
saut    = "space"
pause   = "p"
quitter = "escape"