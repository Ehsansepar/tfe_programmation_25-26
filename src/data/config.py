WIDTH = 800
HEIGHT = 800

# son system
print("=" * 40)
print("Sur quel système tu joues ?")
print("1 - Windows")
print("2 - Mac")
print("=" * 40)
choix = input("Ton choix (1 ou 2) : ")

if choix == "2":
    # Mac - 60 FPS, vitesses plus grandes
    FPS = 60
    PLAYER_SPEED = 15
    PLAYER_GRAVITY = 1.5
    PLAYER_JUMP = -22
    print("Mode Mac activé !")
else:
    # Windows - peut aller plus vite
    FPS = 120
    PLAYER_SPEED = 5
    PLAYER_GRAVITY = 0.5
    PLAYER_JUMP = -15
    print("Mode Windows activé !")