"""
================================================================
  JEU D'AVENTURE TOP-DOWN — Prototype v2
================================================================
  - Grande carte 40x38 tuiles avec village complet
  - 6 PNJ qui se baladent avec dialogues (touche E)
  - Lac, forêt, maisons, grand bâtiment central
  - Caméra qui suit le joueur
  - Mini-carte en bas à droite
  Contrôles : Z Q S D / Flèches = bouger | E = parler | ESC = quitter
================================================================
"""
import pygame
import sys
import random
import math

# ── CONFIG ──────────────────────────────────────────────────────
LARGEUR = 800
HAUTEUR = 800
FPS     = 60
T       = 48          # taille d'une tuile en pixels
VITESSE = 3
COLS    = 40
ROWS    = 38

# ── IDs TUILES ──────────────────────────────────────────────────
HERBE, MUR, EAU, ARBRE, CHEMIN = 0, 1, 2, 3, 4
SOL_MAI, OBJECTIF, SABLE, PONT, FLEUR = 5, 6, 7, 8, 9
MUR_MAI, PORTE_MAI = 10, 11

SOLIDES = {MUR, EAU, ARBRE, MUR_MAI}

COUL_TUILE = {
    HERBE:    (55,  130,  55),
    MUR:      (90,   90,  90),
    EAU:      (40,  110, 210),
    ARBRE:    (25,   80,  25),
    CHEMIN:   (195, 158, 105),
    SOL_MAI:  (160, 120,  80),
    OBJECTIF: (255, 215,   0),
    SABLE:    (210, 182, 130),
    PONT:     (150, 100,  60),
    FLEUR:    (75,  148,  60),
    MUR_MAI:  (120,  80,  50),
    PORTE_MAI:(175, 115,  60),
}

# ── GÉNÉRATION DE LA MAP ────────────────────────────────────────
def creer_map():
    random.seed(2025)
    m = [[HERBE] * COLS for _ in range(ROWS)]

    # Bordure d'arbres
    for c in range(COLS):
        m[0][c] = m[1][c] = ARBRE
        m[ROWS-1][c] = m[ROWS-2][c] = ARBRE
    for r in range(ROWS):
        m[r][0] = m[r][1] = ARBRE
        m[r][COLS-1] = m[r][COLS-2] = ARBRE

    # Lac coin haut-droite
    for r in range(3, 13):
        for c in range(30, 38):
            m[r][c] = EAU
    for r in range(2, 14):
        for c in range(28, 38):
            if m[r][c] == HERBE:
                m[r][c] = SABLE
    for r in range(3, 13):
        m[r][29] = PONT

    # Routes principales
    for c in range(2, COLS-2):
        if m[19][c] not in (EAU, ARBRE, MUR_MAI, SOL_MAI):
            m[19][c] = CHEMIN
    for r in range(2, ROWS-2):
        if m[r][19] not in (EAU, ARBRE, MUR_MAI, SOL_MAI):
            m[r][19] = CHEMIN

    # Placer une maison
    def maison(r0, c0, h, w, obj=False):
        for dr in range(h):
            for dc in range(w):
                r, c = r0+dr, c0+dc
                if 0 <= r < ROWS and 0 <= c < COLS:
                    m[r][c] = MUR_MAI if (dr==0 or dr==h-1 or dc==0 or dc==w-1) else SOL_MAI
        pc = c0 + w//2
        if 0 <= r0+h-1 < ROWS and 0 <= pc < COLS:
            m[r0+h-1][pc] = OBJECTIF if obj else PORTE_MAI

    # Maisons du village
    maison(4,  4,  5, 5)
    maison(4,  12, 5, 5)
    maison(4,  22, 5, 5)
    maison(22, 4,  5, 5)
    maison(22, 12, 5, 5)
    maison(22, 22, 5, 5)
    maison(10, 13, 7, 13, obj=True)  # Grand bâtiment central

    # Chemins secondaires
    for r in range(9, 22):
        for c in (6, 14, 24):
            if 0<=r<ROWS and 0<=c<COLS and m[r][c] == HERBE:
                m[r][c] = CHEMIN
    for c in range(4, 27):
        for r in (8, 21):
            if 0<=r<ROWS and 0<=c<COLS and m[r][c] == HERBE:
                m[r][c] = CHEMIN

    # Arbres épars
    for (r, c) in [(3,9),(3,25),(6,27),(9,28),(13,4),(13,28),(16,5),(16,28),
                   (27,4),(27,26),(30,8),(30,15),(30,25),(32,10),(33,18),(34,28),(35,6),(35,22)]:
        if 0<=r<ROWS and 0<=c<COLS and m[r][c] == HERBE:
            m[r][c] = ARBRE

    # Fleurs aléatoires
    for _ in range(90):
        r = random.randint(2, ROWS-3)
        c = random.randint(2, COLS-3)
        if m[r][c] == HERBE:
            m[r][c] = FLEUR

    return m

# ── CLASSE JOUEUR ───────────────────────────────────────────────
class Joueur:
    def __init__(self):
        self.x = 3.0 * T
        self.y = 17.0 * T
        self.taille = 32
        self.direction = "bas"

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.taille, self.taille)

    def bouger(self, touches, carte):
        dx, dy = 0, 0
        if touches[pygame.K_z] or touches[pygame.K_UP]:    dy = -VITESSE; self.direction = "haut"
        if touches[pygame.K_s] or touches[pygame.K_DOWN]:  dy = +VITESSE; self.direction = "bas"
        if touches[pygame.K_q] or touches[pygame.K_LEFT]:  dx = -VITESSE; self.direction = "gauche"
        if touches[pygame.K_d] or touches[pygame.K_RIGHT]: dx = +VITESSE; self.direction = "droite"

        self.x += dx
        if self._touche_mur(carte): self.x -= dx
        self.y += dy
        if self._touche_mur(carte): self.y -= dy

    def _touche_mur(self, carte):
        r = self.rect()
        coins = [(r.left, r.top), (r.right-1, r.top), (r.left, r.bottom-1), (r.right-1, r.bottom-1)]
        for (px, py) in coins:
            col = int(px // T)
            lig = int(py // T)
            if not (0 <= lig < ROWS and 0 <= col < COLS): return True
            if carte[lig][col] in SOLIDES: return True
        return False

    def tuile_actuelle(self, carte):
        cx = int((self.x + self.taille/2) // T)
        cy = int((self.y + self.taille/2) // T)
        if 0 <= cy < ROWS and 0 <= cx < COLS:
            return carte[cy][cx]
        return HERBE

    def dessiner(self, ecran, cx, cy):
        px = int(self.x - cx)
        py = int(self.y - cy)
        r = pygame.Rect(px, py, self.taille, self.taille)

        # Ombre
        ombre = pygame.Surface((self.taille, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(ombre, (0, 0, 0, 80), ombre.get_rect())
        ecran.blit(ombre, (px, py + self.taille - 4))

        # Corps
        pygame.draw.rect(ecran, (0, 160, 255), r, border_radius=8)
        pygame.draw.rect(ecran, (0, 80, 180), r, 2, border_radius=8)

        # Tête
        hx = px + self.taille // 2
        hy = py - 10
        pygame.draw.circle(ecran, (255, 220, 180), (hx, hy), 10)
        pygame.draw.circle(ecran, (180, 130, 80), (hx, hy), 10, 2)

        # Yeux
        pygame.draw.circle(ecran, (30,30,30), (hx-4, hy-2), 2)
        pygame.draw.circle(ecran, (30,30,30), (hx+4, hy-2), 2)

        # Flèche de direction
        d = 9
        cx2, cy2 = px + self.taille//2, py + self.taille//2
        if self.direction == "haut":    pts = [(cx2, cy2-d),(cx2-5,cy2+4),(cx2+5,cy2+4)]
        elif self.direction == "bas":   pts = [(cx2, cy2+d),(cx2-5,cy2-4),(cx2+5,cy2-4)]
        elif self.direction == "gauche":pts = [(cx2-d,cy2),(cx2+4,cy2-5),(cx2+4,cy2+5)]
        else:                           pts = [(cx2+d,cy2),(cx2-4,cy2-5),(cx2-4,cy2+5)]
        pygame.draw.polygon(ecran, (255,255,255), pts)

# ── CLASSE PNJ ──────────────────────────────────────────────────
COULEURS_PNJ = [(220,100,100),(100,100,220),(220,160,60),(160,60,220),(60,180,120),(220,80,160)]

class PNJ:
    def __init__(self, tx, ty, nom, dialogues, coul_idx, zone_t):
        self.x = float(tx * T)
        self.y = float(ty * T)
        self.nom = nom
        self.dialogues = dialogues
        self.dial_idx = 0
        self.couleur = COULEURS_PNJ[coul_idx % len(COULEURS_PNJ)]
        self.taille = 28
        z = zone_t
        self.zone = (z[0]*T, z[1]*T, z[2]*T, z[3]*T)
        self.vitesse = random.uniform(0.5, 0.9)
        self.dx = 0.0
        self.dy = 0.0
        self.timer = random.randint(60, 180)

    def prochain_dialogue(self):
        d = self.dialogues[self.dial_idx]
        self.dial_idx = (self.dial_idx + 1) % len(self.dialogues)
        return d

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            choix = [(0,0),(1,0),(-1,0),(0,1),(0,-1),(0,0)]
            self.dx, self.dy = random.choice(choix)
            self.timer = random.randint(80, 200)

        nx = self.x + self.dx * self.vitesse
        ny = self.y + self.dy * self.vitesse
        x1, y1, x2, y2 = self.zone
        self.x = nx if x1 <= nx <= x2 - self.taille else self.x
        self.y = ny if y1 <= ny <= y2 - self.taille else self.y

    def distance(self, joueur):
        dx = (self.x + self.taille/2) - (joueur.x + joueur.taille/2)
        dy = (self.y + self.taille/2) - (joueur.y + joueur.taille/2)
        return math.sqrt(dx*dx + dy*dy)

    def dessiner(self, ecran, cx, cy, pf, proche):
        px = int(self.x - cx)
        py = int(self.y - cy)

        # Ombre
        ombre = pygame.Surface((self.taille, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(ombre, (0,0,0,70), ombre.get_rect())
        ecran.blit(ombre, (px, py + self.taille - 3))

        # Corps
        r = pygame.Rect(px, py, self.taille, self.taille)
        pygame.draw.rect(ecran, self.couleur, r, border_radius=6)
        pygame.draw.rect(ecran, (30,30,30), r, 2, border_radius=6)

        # Tête
        hx = px + self.taille//2
        hy = py - 9
        pygame.draw.circle(ecran, (255, 220, 180), (hx, hy), 9)
        pygame.draw.circle(ecran, (160,110,70), (hx, hy), 9, 2)
        pygame.draw.circle(ecran, (30,30,30), (hx-3, hy-2), 2)
        pygame.draw.circle(ecran, (30,30,30), (hx+3, hy-2), 2)

        # Nom
        ns = pf.render(self.nom, True, (255,255,255))
        nr = ns.get_rect(centerx=px+self.taille//2, bottom=py-20)
        fond = pygame.Surface((nr.width+8, nr.height+2), pygame.SRCALPHA)
        fond.fill((0,0,0,150))
        ecran.blit(fond, (nr.x-4, nr.y-1))
        ecran.blit(ns, nr)

        # Indicateur E
        if proche:
            es = pf.render("[E] Parler", True, (255,255,180))
            er = es.get_rect(centerx=px+self.taille//2, bottom=py-35)
            ef = pygame.Surface((er.width+10, er.height+4), pygame.SRCALPHA)
            ef.fill((60,50,0,190))
            ecran.blit(ef, (er.x-5, er.y-2))
            ecran.blit(es, er)

# ── CLASSE CAMÉRA ───────────────────────────────────────────────
class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.larg_map = COLS * T
        self.haut_map = ROWS * T

    def suivre(self, joueur):
        cx = joueur.x + joueur.taille/2 - LARGEUR/2
        cy = joueur.y + joueur.taille/2 - HAUTEUR/2
        self.x = max(0, min(cx, self.larg_map - LARGEUR))
        self.y = max(0, min(cy, self.haut_map - HAUTEUR))

# ── DESSIN MAP ──────────────────────────────────────────────────
def dessiner_map(ecran, carte, cx, cy, pf, tick):
    col0 = max(0, int(cx // T))
    col1 = min(COLS, col0 + LARGEUR//T + 2)
    lig0 = max(0, int(cy // T))
    lig1 = min(ROWS, lig0 + HAUTEUR//T + 2)

    for lig in range(lig0, lig1):
        for col in range(col0, col1):
            t = carte[lig][col]
            coul = COUL_TUILE.get(t, (255,0,255))
            sx = col * T - int(cx)
            sy = lig * T - int(cy)
            rect = pygame.Rect(sx, sy, T, T)
            pygame.draw.rect(ecran, coul, rect)

            if t == ARBRE:
                # Herbe sous l'arbre
                pygame.draw.rect(ecran, (55,130,55), rect)
                # Ombre de l'arbre
                pygame.draw.ellipse(ecran, (30,70,30), pygame.Rect(sx+4, sy+T-12, T-8, 10))
                # Tronc
                pygame.draw.rect(ecran, (100,65,30), pygame.Rect(sx+T//2-4, sy+T//2, 8, T//2))
                # Feuillage (3 cercles)
                pygame.draw.circle(ecran, (20,90,20), (sx+T//2, sy+T//2-4), 18)
                pygame.draw.circle(ecran, (30,110,30), (sx+T//2-8, sy+T//2-8), 12)
                pygame.draw.circle(ecran, (40,130,40), (sx+T//2+6, sy+T//2-10), 10)

            elif t == EAU:
                # Animation eau avec tick
                off = int(math.sin(tick * 0.05 + col * 0.5) * 3)
                for i in range(3):
                    wx = sx + 5 + i * 14
                    wy = sy + T//2 + off
                    pygame.draw.line(ecran, (80,170,255), (wx, wy), (wx+9, wy-3), 2)

            elif t == FLEUR:
                # Petite fleur
                pygame.draw.circle(ecran, (255,200,50), (sx+T//2, sy+T//2), 5)
                for angle in range(0, 360, 60):
                    fx = sx + T//2 + int(math.cos(math.radians(angle)) * 8)
                    fy = sy + T//2 + int(math.sin(math.radians(angle)) * 8)
                    pygame.draw.circle(ecran, (255,100,150), (fx, fy), 3)

            elif t == MUR_MAI:
                # Briques
                pygame.draw.rect(ecran, (90,55,30), rect, 1)
                pygame.draw.line(ecran, (90,55,30), (sx, sy+T//2), (sx+T, sy+T//2), 1)
                pygame.draw.line(ecran, (90,55,30), (sx+T//2, sy), (sx+T//2, sy+T//2), 1)
                pygame.draw.line(ecran, (90,55,30), (sx+T//4, sy+T//2), (sx+T//4, sy+T), 1)
                pygame.draw.line(ecran, (90,55,30), (sx+3*T//4, sy+T//2), (sx+3*T//4, sy+T), 1)

            elif t == SOL_MAI:
                # Plancher de bois (lignes)
                for i in range(0, T, 12):
                    pygame.draw.line(ecran, (140,100,60), (sx, sy+i), (sx+T, sy+i), 1)

            elif t == OBJECTIF:
                # Effet brillant animé
                glow = int(math.sin(tick * 0.08) * 30 + 180)
                pygame.draw.rect(ecran, (glow, glow//2, 0), rect)
                pygame.draw.circle(ecran, (255,255,200), (sx+T//2, sy+T//2), 14)
                pygame.draw.circle(ecran, (255,215,0), (sx+T//2, sy+T//2), 10)
                star = pf.render("★", True, (160,80,0))
                sr = star.get_rect(center=(sx+T//2, sy+T//2))
                ecran.blit(star, sr)

            elif t == PONT:
                # Planches de pont
                pygame.draw.rect(ecran, (120,80,40), rect, 2)
                for i in range(4):
                    pygame.draw.line(ecran, (100,65,30), (sx+i*12+4, sy+2), (sx+i*12+4, sy+T-2), 2)

            elif t == CHEMIN:
                # Texture sable (petits points)
                pygame.draw.rect(ecran, (215,172,115), rect)
                for i in range(3):
                    for j in range(3):
                        pygame.draw.circle(ecran, (180,145,90), (sx+8+i*14, sy+8+j*14), 1)

            elif t == SABLE:
                # Plage (légères vagues de sable)
                pygame.draw.line(ecran, (200,170,120), (sx+4, sy+T//3), (sx+T-4, sy+T//3), 1)
                pygame.draw.line(ecran, (200,170,120), (sx+4, sy+2*T//3), (sx+T-4, sy+2*T//3), 1)

            elif t == HERBE:
                # Petits brins d'herbe
                if (lig + col) % 5 == 0:
                    pygame.draw.line(ecran, (70,150,60), (sx+T//4, sy+T//2+6), (sx+T//4+2, sy+T//2-4), 1)
                if (lig + col) % 7 == 0:
                    pygame.draw.line(ecran, (65,140,55), (sx+3*T//4, sy+T//2+6), (sx+3*T//4-2, sy+T//2-4), 1)

            # Ligne de grille subtile
            pygame.draw.rect(ecran, (0,0,0,20), rect, 1)

# ── BOÎTE DE DIALOGUE ───────────────────────────────────────────
def dessiner_dialogue(ecran, nom, texte, pf_titre, pf):
    bx, by, bw, bh = 40, HAUTEUR-160, LARGEUR-80, 120
    fond = pygame.Surface((bw, bh), pygame.SRCALPHA)
    fond.fill((20, 15, 35, 220))
    ecran.blit(fond, (bx, by))
    pygame.draw.rect(ecran, (200,160,80), (bx,by,bw,bh), 3, border_radius=10)

    # Nom
    ns = pf_titre.render(f"[ {nom} ]", True, (255,215,0))
    ecran.blit(ns, (bx+15, by+12))

    # Texte (retour à la ligne automatique)
    mots = texte.split(" ")
    lignes, ligne_actuelle = [], ""
    for mot in mots:
        test = ligne_actuelle + (" " if ligne_actuelle else "") + mot
        if pf.size(test)[0] < bw - 30:
            ligne_actuelle = test
        else:
            lignes.append(ligne_actuelle)
            ligne_actuelle = mot
    if ligne_actuelle: lignes.append(ligne_actuelle)

    for i, l in enumerate(lignes[:3]):
        ts = pf.render(l, True, (230,230,230))
        ecran.blit(ts, (bx+15, by+50+i*26))

    cont = pf.render("[ Appuie sur E pour fermer ]", True, (150,150,150))
    ecran.blit(cont, (bx+bw-cont.get_width()-15, by+bh-24))

# ── MINI-CARTE ──────────────────────────────────────────────────
def dessiner_minimap(ecran, carte, joueur):
    px, py, pw, ph = LARGEUR-145, HAUTEUR-145, 130, 130
    fond = pygame.Surface((pw, ph), pygame.SRCALPHA)
    fond.fill((0,0,0,160))
    ecran.blit(fond, (px, py))
    pygame.draw.rect(ecran, (200,160,80), (px,py,pw,ph), 2)

    tw = pw / COLS
    th = ph / ROWS

    for lig in range(ROWS):
        for col in range(COLS):
            t = carte[lig][col]
            if t == HERBE:    c = (55,130,55)
            elif t == EAU:    c = (40,110,210)
            elif t == ARBRE:  c = (25,80,25)
            elif t == CHEMIN: c = (195,158,105)
            elif t == SABLE:  c = (210,182,130)
            elif t == PONT:   c = (150,100,60)
            elif t in (SOL_MAI, PORTE_MAI): c = (160,120,80)
            elif t == MUR_MAI: c = (120,80,50)
            elif t == OBJECTIF: c = (255,215,0)
            elif t == FLEUR:  c = (75,148,60)
            else: c = (90,90,90)
            mx = int(px + col * tw)
            my = int(py + lig * th)
            mw = max(1, int(tw))
            mh = max(1, int(th))
            pygame.draw.rect(ecran, c, (mx, my, mw, mh))

    # Joueur sur la mini-carte
    jx = int(px + (joueur.x / (COLS*T)) * pw)
    jy = int(py + (joueur.y / (ROWS*T)) * ph)
    pygame.draw.circle(ecran, (0,200,255), (jx, jy), 3)
    pygame.draw.circle(ecran, (255,255,255), (jx, jy), 3, 1)

# ── HUD ─────────────────────────────────────────────────────────
def dessiner_hud(ecran, pf, joueur):
    hud = pygame.Surface((LARGEUR, 36), pygame.SRCALPHA)
    hud.fill((0,0,0,150))
    ecran.blit(hud, (0,0))
    jcol = int(joueur.x // T)
    jlig = int(joueur.y // T)
    ts = pf.render(f"  Position : ({jcol}, {jlig})   |   Z/Q/S/D ou Flèches = bouger   |   E = parler   |   ESC = quitter", True, (220,220,200))
    ecran.blit(ts, (0, 9))

# ── ÉCRAN VICTOIRE ──────────────────────────────────────────────
def ecran_victoire(ecran, pf_titre, pf):
    for alpha in range(0, 255, 5):
        ecran.fill((20,15,35))
        s = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        s.fill((0,0,0,alpha))
        ecran.blit(s, (0,0))
        pygame.display.flip()
        pygame.time.delay(10)

    ecran.fill((20, 15, 35))
    t1 = pf_titre.render("🏆  TU AS GAGNÉ !  🏆", True, (255,215,0))
    t2 = pf.render("Tu as trouvé le Grand Temple du village !", True, (255,255,255))
    t3 = pf.render("Appuie sur ESC pour quitter", True, (160,160,160))
    ecran.blit(t1, t1.get_rect(center=(LARGEUR//2, 280)))
    ecran.blit(t2, t2.get_rect(center=(LARGEUR//2, 370)))
    ecran.blit(t3, t3.get_rect(center=(LARGEUR//2, 450)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

# ── CRÉER LES PNJ ───────────────────────────────────────────────
def creer_pnj():
    return [
        PNJ(6, 10, "Thomas", [
            "Bienvenue dans notre village, étranger !",
            "Je suis forgeron depuis 20 ans ici.",
            "Le grand temple au centre est très ancien..."
        ], 0, (3, 9, 10, 15)),

        PNJ(14, 10, "Marie", [
            "Bonjour ! Tu veux acheter du pain ?",
            "Mes croissants sont les meilleurs du royaume !",
            "Evite le lac la nuit, c'est dangereux."
        ], 1, (11, 9, 18, 15)),

        PNJ(6, 24, "Pierre", [
            "Cette saison les récoltes sont bonnes.",
            "J'ai vu quelque chose de bizarre près du temple.",
            "Fais attention aux arbres la nuit..."
        ], 2, (3, 21, 10, 27)),

        PNJ(24, 24, "Sophie", [
            "Je vends des herbes magiques !",
            "Le lac au nord est magnifique au lever du soleil.",
            "Le temple central cache un grand secret..."
        ], 3, (21, 21, 28, 27)),

        PNJ(19, 15, "Louis", [
            "Je garde le temple depuis toujours.",
            "Seuls les courageux peuvent entrer.",
            "La porte dorée, c'est la fin de ta quête !"
        ], 4, (16, 12, 22, 18)),

        PNJ(14, 24, "Emma", [
            "J'adore me promener dans ce village.",
            "Tu viens d'où, toi ?",
            "Un jour je partirai à l'aventure moi aussi !"
        ], 5, (11, 21, 18, 27)),
    ]

# ── BOUCLE PRINCIPALE ───────────────────────────────────────────
def main():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("🗺️ Village Adventure — Prototype")
    clock = pygame.time.Clock()

    pf_titre = pygame.font.SysFont("Arial", 46, bold=True)
    pf_hud   = pygame.font.SysFont("Arial", 22, bold=True)
    pf_grand = pygame.font.SysFont("Arial", 28, bold=True)
    pf_petit = pygame.font.SysFont("Arial", 15)

    carte  = creer_map()
    joueur = Joueur()
    camera = Camera()
    pnjs   = creer_pnj()

    dialogue_actif = None   # (nom, texte) ou None
    tick = 0

    running = True
    while running:
        tick += 1

        # ── ÉVÉNEMENTS ──────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if dialogue_actif:
                        dialogue_actif = None
                    else:
                        running = False

                if event.key == pygame.K_e:
                    if dialogue_actif:
                        dialogue_actif = None
                    else:
                        # Cherche le PNJ le plus proche
                        for pnj in pnjs:
                            if pnj.distance(joueur) < 70:
                                dialogue_actif = (pnj.nom, pnj.prochain_dialogue())
                                break

        # ── MISE À JOUR ─────────────────────────────────────────
        if not dialogue_actif:
            touches = pygame.key.get_pressed()
            joueur.bouger(touches, carte)

        for pnj in pnjs:
            if not dialogue_actif:
                pnj.update()

        camera.suivre(joueur)

        # ── VICTOIRE ? ──────────────────────────────────────────
        if joueur.tuile_actuelle(carte) == OBJECTIF:
            ecran_victoire(ecran, pf_titre, pf_grand)
            running = False

        # ── DESSIN ──────────────────────────────────────────────
        ecran.fill((10, 20, 10))

        dessiner_map(ecran, carte, camera.x, camera.y, pf_petit, tick)

        for pnj in sorted(pnjs, key=lambda p: p.y):
            proche = pnj.distance(joueur) < 70
            pnj.dessiner(ecran, camera.x, camera.y, pf_petit, proche)

        joueur.dessiner(ecran, camera.x, camera.y)
        dessiner_hud(ecran, pf_petit, joueur)
        dessiner_minimap(ecran, carte, joueur)

        if dialogue_actif:
            dessiner_dialogue(ecran, dialogue_actif[0], dialogue_actif[1], pf_grand, pf_hud)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
