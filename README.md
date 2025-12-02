# 🎮 Pixel Adventure - Jeu de Plateforme 2D

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-En%20Développement-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational-blue?style=for-the-badge)

**Un jeu de plateforme 2D développé en Python avec Pygame**

*Projet de TFE (Travail de Fin d'Études) - Programmation*

[🎯 Fonctionnalités](#-fonctionnalités) •
[🚀 Installation](#-installation) •
[🎮 Comment Jouer](#-comment-jouer) •
[📁 Structure](#-structure-du-projet) •
[🛠️ Technologies](#️-technologies-utilisées)

</div>

---

## 📖 Description

**Pixel Adventure** est un jeu de plateforme 2D développé entièrement en Python avec la bibliothèque Pygame. Ce projet démontre ma maîtrise des concepts fondamentaux de la programmation orientée objet, de la gestion d'animations, de la physique de jeu (gravité, sauts) et de la création d'interfaces utilisateur interactives.

Le joueur contrôle un personnage qui doit naviguer à travers le niveau pour atteindre la zone d'arrivée, tout en utilisant ses compétences de saut et de déplacement.

---

## ✨ Fonctionnalités

### 🎯 Implémentées
- ✅ **Système de mouvement complet** - Déplacements fluides (gauche, droite, haut, bas)
- ✅ **Physique réaliste** - Gravité et système de saut avec vélocité verticale
- ✅ **Menu principal interactif** - Navigation clavier (1, 2, 3) et souris
- ✅ **Écran de victoire** - Affichage des félicitations avec options de navigation
- ✅ **Détection de collision** - Avec le sol et la zone d'arrivée
- ✅ **Architecture modulaire** - Code organisé en classes séparées
- ✅ **Système d'animation** - Support des sprite sheets avec états (idle, run, jump, fall)
- ✅ **Retournement automatique** - Le personnage se retourne selon sa direction

### 🔜 En Développement
- 🔄 Intégration complète des sprites animés
- 🔄 Système de niveaux multiples
- 🔄 Ennemis et obstacles
- 🔄 Système de score et collectibles
- 🔄 Effets sonores et musique

---

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

```bash
# 1. Cloner le repository
git clone https://github.com/Ehsansepar/tfe_programmation_25-26.git

# 2. Accéder au dossier du projet
cd tfe_programmation_25-26

# 3. Installer les dépendances
pip install pygame

# 4. Lancer le jeu
python main.py
```

---

## 🎮 Comment Jouer

### Contrôles

| Touche | Action |
|--------|--------|
| `←` `→` | Déplacement horizontal |
| `↑` `↓` | Déplacement vertical |
| `ESPACE` | Sauter |
| `M` | Accéder au menu |
| `END` | Quitter le jeu |

### Objectif
Atteindre la zone d'arrivée (bloc coloré à droite de l'écran) pour gagner la partie !

---

## 📁 Structure du Projet

```
tfe_programmation/
│
├── 📄 main.py              # Point d'entrée - Boucle de jeu principale
├── 📄 personnage.py        # Classe du personnage avec mouvements et physique
├── 📄 menu.py              # Système de menu interactif
├── 📄 gagner.py            # Écran de victoire
├── 📄 sol.py               # Classe pour la gestion du sol
├── 📄 config.py            # Configuration globale (dimensions, FPS)
│
├── 📄 test_personnage.py   # Version avancée avec animations sprite
├── 📄 test_main.py         # Tests avec background et terrain tiles
├── 📄 test_button.py       # Prototype de système de boutons
├── 📄 example.py           # Exemple de jeu avec collisions
│
└── 📂 assets/
    └── 📂 images/
        ├── 📂 Background/      # Images de fond
        ├── 📂 Main Characters/ # Sprites des personnages
        │   ├── 📂 Ninja Frog/
        │   ├── 📂 Mask Dude/
        │   ├── 📂 Pink Man/
        │   └── 📂 Virtual Guy/
        ├── 📂 Terrain/         # Tuiles de terrain
        ├── 📂 Items/           # Objets (fruits, checkpoints, etc.)
        ├── 📂 Traps/           # Pièges (pics, scies, etc.)
        └── 📂 Menu/            # Éléments d'interface
```

---

## 🛠️ Technologies Utilisées

<div align="center">

| Technologie | Utilisation |
|-------------|-------------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Langage de programmation principal |
| ![Pygame](https://img.shields.io/badge/Pygame-3776AB?style=flat-square&logo=python&logoColor=white) | Bibliothèque de développement de jeux |
| ![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white) | Contrôle de version |
| ![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white) | Environnement de développement |

</div>

---

## 💡 Concepts Techniques Démontrés

### Programmation Orientée Objet (POO)
```python
class Personnage:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.vitesse_verticale = 0
        self.gravite = 0.5
        # ...
```

### Physique de Jeu
- **Gravité** : Simulation réaliste avec accélération constante
- **Saut** : Impulsion verticale avec vélocité négative
- **Collision au sol** : Détection et arrêt du mouvement

### Gestion d'États
- Machine à états pour les pages (game, menu, win)
- États d'animation du personnage (idle, run, jump, fall)

### Animation de Sprites
- Découpage automatique de sprite sheets
- Animation fluide avec contrôle de vitesse
- Retournement horizontal selon la direction

---

## 📸 Aperçu

> *Screenshots à venir lors de la finalisation du projet*

| Menu Principal | Gameplay | Écran de Victoire |
|----------------|----------|-------------------|
| 🖼️ | 🖼️ | 🖼️ |

---

## 🎯 Roadmap

- [x] Structure de base du jeu
- [x] Système de mouvement et gravité
- [x] Menu principal
- [x] Écran de victoire
- [x] Chargement des sprites
- [ ] Intégration complète des animations
- [ ] Niveaux multiples
- [ ] Système d'ennemis
- [ ] Collectibles et score
- [ ] Effets sonores
- [ ] Sauvegarde de progression

---

## 👨‍💻 Auteur

<div align="center">

**Ehsan Separ**

*Étudiant en programmation*

[![GitHub](https://img.shields.io/badge/GitHub-Ehsansepar-181717?style=for-the-badge&logo=github)](https://github.com/Ehsansepar)

</div>

---

## 📝 Notes de Développement

Ce projet est développé dans le cadre de mon TFE (Travail de Fin d'Études) en programmation. Il représente mon apprentissage continu du développement de jeux vidéo et de la programmation en Python.

### Ce que j'ai appris :
- 🧠 Programmation orientée objet en Python
- 🎮 Développement de jeux avec Pygame
- 🔧 Gestion de projet avec Git/GitHub
- 🎨 Manipulation de sprites et animations
- 📐 Implémentation de physique de jeu

---

## 📄 License

Ce projet est développé à des fins éducatives dans le cadre d'un travail de fin d'études.

---

<div align="center">

**⭐ Si ce projet vous plaît, n'hésitez pas à laisser une étoile ! ⭐**

*Fait avec ❤️ et beaucoup de ☕*

</div>
