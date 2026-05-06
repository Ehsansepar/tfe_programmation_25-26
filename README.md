# 🎮 Pixel Adventure - Jeu de Plateforme 2D (Pygame)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Version%20Avancée-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational-blue?style=for-the-badge)

**Un jeu de plateforme 2D complet développé en Python avec Pygame, doté d'un système de niveaux, d'authentification et de sprites animés !**

_Projet de TFE (Travail de Fin d'Études) - Programmation par Ehsan Separ_

[🎯 Fonctionnalités](#-fonctionnalités) •
[🚀 Installation](#-installation) •
[🎮 Comment Jouer](#-comment-jouer) •
[📁 Structure](#-structure-du-projet) •
[🛠️ Architecture Technique](#️-architecture-technique)

</div>

---

## 📖 Description

**Pixel Adventure** est un jeu de plateforme 2D moderne et fluide fonctionnant avec une caméra fixe (single-screen) en résolution **1280x720**. Le joueur incarne un personnage (ex: Ninja Frog) et doit surmonter différents obstacles à travers plusieurs niveaux pour atteindre l'arrivée.

Cette nouvelle mise à jour majeure apporte un système de menus complet, des interfaces utilisateur professionnelles, un système de progression des niveaux (avec verrouillage), et une optimisation des performances cross-platform (Windows/Mac) !

---

## ✨ Fonctionnalités (Mise à jour majeure !)

### 🎯 Nouvelles Implémentations

- ✅ **10 Niveaux Complets** - Design unique en écran fixe avec plateformes, obstacles, et arrière-plans personnalisés.
- ✅ **Système de Progression & Verrouillage** - Sauvegarde de la progression locale (`data.txt`), les niveaux suivants sont verrouillés jusqu'à la victoire.
- ✅ **Interface Utilisateur Premium** - Menus interactifs guidés par l'image, curseurs personnalisés au survol (pointeur / cadenas pour les niveaux bloqués).
- ✅ **Système d'Authentification** - Écrans de Bienvenue, Connexion et Inscription.
- ✅ **Gestion Cross-Platform (FPS)** - Synchronisation physique personnalisée au lancement (Windows 120+ FPS vs Mac 60 FPS) pour garantir le même ressenti de jeu partout !
- ✅ **Sprites et Effets Sonores** - Personnage remplacé par des sprites animés avec des effets sonores de saut.
- ✅ **Menus Paramètres** - Pour la personnalisation et la consultation des contrôles (Z, Q, S, D, Espace).

### 🔜 Prochaines Étapes

- 🔄 Intégration d'ennemis mouvants et de pièges (scies, pics).
- 🔄 Système de score ou de pièces à collecter.
- 🔄 Musique d'ambiance globale.

---

## 🚀 Installation

### Prérequis

- Python 3.10 ou supérieur
- Bibliothèque Pygame

### Étapes d'installation

```bash
# 1. Cloner le repository
git clone https://github.com/Ehsansepar/tfe_programmation_25-26.git

# 2. Accéder au dossier du projet
cd tfe_programmation_25-26

# 3. Installer les dépendances
pip install pygame

# 4. Lancer le jeu (depuis la racine du projet)
python src/main.py
```

> **Note** : Au premier lancement, le jeu vous demandera votre système d'exploitation (Windows ou Mac) dans la console pour adapter automatiquement la vitesse et la gravité en fonction de votre taux de rafraîchissement (FPS).

---

## 🎮 Comment Jouer

### Contrôles par défaut

| Touche                   | Action                                   |
| ------------------------ | ---------------------------------------- |
| `Q` / `D` (ou `←` / `→`) | Déplacement horizontal (Gauche / Droite) |
| `Espace` / `Z` (ou `↑`)  | Sauter                                   |
| `S` (ou `↓`)             | Descendre plus vite                      |
| `M`                      | Retour au Menu Principal (en jeu)        |
| `Fin` (End)              | Quitter le jeu                           |

### Objectif

Atteindre la zone d'arrivée (bloc de fin) en évitant de tomber pour gagner le niveau et débloquer le suivant !

---

## 📁 Structure du Projet

L'architecture a été entièrement refaite pour être modulaire et propre, selon les principes de la POO (Programmation Orientée Objet) :

```text
tfe_programmation_25-26/
├── 📂 src/
│   ├── 📄 main.py               # Point d'entrée principal (Boucle de jeu et State Machine)
│   ├── 📂 classes/              # Logique métier et Interfaces
│   │   ├── personnage.py        # Physique du joueur, sprites et collisions
│   │   ├── menu.py, level.py    # Menus principaux et sélection de niveaux
│   │   ├── login.py, inscription.py # Écrans d'authentification
│   │   └── gagner.py, parametre.py, sol.py
│   ├── 📂 lvl/                  # Fichiers de niveaux (lvl01.py à lvl10.py)
│   ├── 📂 data/                 # Données de sauvegarde (data.txt) et configuration (config.py)
│   ├── 📂 assets_img/           # Assets visuels (Fonds, Personnages, Menus, Curseur)
│   └── 📂 sounds/               # Effets sonores (jump.wav)
└── 📄 README.md                 # Vous êtes ici
```

---

## 🛠️ Architecture Technique

### 1. Programmation Orientée Objet (POO)

Le code est strictement divisé en classes indépendantes. Chaque interface (Menu, Level, Settings) et chaque entité (Personnage, Sol, Niveau) possède sa propre classe. Cela permet un code clair et facile à maintenir.

### 2. Machine à États (State Machine)

La gestion des pages dans `main.py` repose sur un système d'états dynamiques (`page = "menu"`, `"game"`, `"win"`, `"level2"`, etc.) permettant une navigation fluide entre les différentes scènes de l'application (du menu aux 10 niveaux, puis à l'écran de victoire) sans surcharger la mémoire.

### 3. Adaptation du Framerate (Le Hack de Vitesse)

Face à la limitation matérielle de 60 FPS sur les écrans Mac (contre plus de 120 FPS sur Windows), une calibration est effectuée au démarrage dans `config.py`. Les constantes telles que `PLAYER_SPEED`, `PLAYER_GRAVITY` et `PLAYER_JUMP` sont ajustées pour que le personnage parcoure la même distance dans le même temps, quel que soit le PC !

---

## 👨‍💻 Auteur

<div align="center">

**Ehsan Separ**

_Étudiant en programmation_

[![GitHub](https://img.shields.io/badge/GitHub-Ehsansepar-181717?style=for-the-badge&logo=github)](https://github.com/Ehsansepar)

</div>

---

<div align="center">

**⭐ Si ce projet vous plaît, n'hésitez pas à laisser une étoile ! ⭐**

_Fait avec ❤️, beaucoup de ☕, et des dizaines de hitboxes ajustées au pixel près !_

</div>
<!-- test -->
