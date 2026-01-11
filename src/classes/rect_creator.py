"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎮 OUTIL PROFESSIONNEL DE CRÉATION DE RECTANGLES 🎮        ║
║                              Version 4.0 - Améliorée                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Fonctionnalités:
- Demande la taille de l'écran au démarrage
- Dessiner des rectangles par glisser-déposer
- AJOUTER DES TEXTES/ANNOTATIONS sur l'écran
- REDIMENSIONNER les rectangles avec des poignées visuelles
- Charger une image de fond
- Grille magnétique (snap-to-grid)
- Sélection et suppression de rectangles individuels
- AFFICHAGE DU CODE DIRECTEMENT DANS LE TERMINAL
- Modes de couleurs multiples
- Déplacement de rectangles existants
- Interface utilisateur intégrée
"""

import pygame
import sys
import os
import re
from datetime import datetime
from pathlib import Path

# Essayer d'importer pyperclip pour le presse-papiers
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# Importer tkinter pour le sélecteur de fichier
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


def open_file_dialog(title="Choisir une image", filetypes=None):
    """Ouvre un dialogue pour sélectionner un fichier image."""
    if not TKINTER_AVAILABLE:
        return None
    
    # Sur Mac, tkinter peut causer des problèmes avec pygame
    # On utilise une approche différente
    if USER_OS == 'mac':
        # Utiliser osascript sur Mac (AppleScript)
        try:
            import subprocess
            script = '''
            tell application "System Events"
                activate
                set theFile to choose file with prompt "Choisir une image" of type {"png", "jpg", "jpeg", "gif", "bmp"}
                return POSIX path of theFile
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"  ⚠ Erreur sélecteur Mac: {e}")
            return None
    
    if filetypes is None:
        filetypes = [
            ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg *.jpeg"),
            ("Tous les fichiers", "*.*")
        ]
    
    try:
        # Créer une fenêtre tkinter cachée
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        root.attributes('-topmost', True)  # Mettre au premier plan
        
        # Ouvrir le dialogue
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )
        
        root.destroy()
        
        return file_path if file_path else None
    except Exception as e:
        print(f"  ⚠ Erreur: {e}")
        return None


def parse_python_file(filepath: str) -> dict:
    """
    Analyse un fichier Python pour extraire les pygame.Rect et autres éléments.
    Retourne un dictionnaire avec les rectangles, textes, et dimensions trouvés.
    """
    result = {
        'rectangles': [],  # [(rect, type, color), ...]
        'texts': [],       # [(pos, text, color, size), ...]
        'width': None,     # Sera demandé si non trouvé
        'height': None,
        'bg_color': None,  # Couleur de fond détectée
        'source_file': filepath,
        'raw_rects': [],   # Pour garder les noms de variables
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher les dimensions (WIDTH, HEIGHT ou des valeurs directes)
        # Pattern: WIDTH = 800 ou self.width = 800
        width_match = re.search(r'(?:WIDTH|width|LARGEUR|largeur)\s*=\s*(\d+)', content)
        height_match = re.search(r'(?:HEIGHT|height|HAUTEUR|hauteur)\s*=\s*(\d+)', content)
        
        if width_match:
            result['width'] = int(width_match.group(1))
        if height_match:
            result['height'] = int(height_match.group(1))
        
        # Chercher la couleur de fond: self.ecran.fill((r, g, b)) ou screen.fill((r, g, b))
        bg_pattern = r'(?:self\.)?(?:ecran|screen|surface)\.fill\s*\(\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
        bg_match = re.search(bg_pattern, content, re.IGNORECASE)
        if bg_match:
            r, g, b = int(bg_match.group(1)), int(bg_match.group(2)), int(bg_match.group(3))
            result['bg_color'] = (r, g, b)
            print(f"    → Couleur de fond détectée: RGB({r}, {g}, {b})")
        
        # Chercher tous les pygame.Rect(x, y, w, h)
        rect_pattern = r'pygame\.Rect\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\)'
        
        # Chercher les rectangles avec leur contexte (nom de variable ou liste)
        lines = content.split('\n')
        current_list_name = None
        
        for i, line in enumerate(lines):
            # Détecter le début d'une liste
            list_match = re.search(r'(self\.)?(\w+)\s*=\s*\[', line)
            if list_match:
                current_list_name = list_match.group(2)
            
            # Si on ferme une liste
            if ']' in line and '[' not in line:
                if current_list_name:
                    current_list_name = None
            
            # Chercher les pygame.Rect dans cette ligne
            rect_matches = re.findall(rect_pattern, line)
            for match in rect_matches:
                x, y, w, h = int(match[0]), int(match[1]), int(match[2]), int(match[3])
                rect = pygame.Rect(x, y, w, h)
                
                # Déterminer le type basé sur le contexte
                rect_type = 'sol'  # Par défaut
                line_lower = line.lower()
                
                if current_list_name:
                    name_lower = current_list_name.lower()
                    if 'plateforme' in name_lower or 'platform' in name_lower:
                        rect_type = 'sol'
                    elif 'obstacle' in name_lower or 'enemy' in name_lower or 'ennemi' in name_lower:
                        rect_type = 'obstacle'
                    elif 'zone' in name_lower or 'trigger' in name_lower:
                        rect_type = 'zone'
                    elif 'spawn' in name_lower or 'start' in name_lower:
                        rect_type = 'spawn'
                    elif 'collect' in name_lower or 'coin' in name_lower or 'item' in name_lower:
                        rect_type = 'collectible'
                else:
                    # Vérifier le nom de variable sur la même ligne
                    if 'finish' in line_lower or 'end' in line_lower or 'goal' in line_lower:
                        rect_type = 'zone'
                    elif 'spawn' in line_lower or 'start' in line_lower:
                        rect_type = 'spawn'
                    elif 'obstacle' in line_lower or 'enemy' in line_lower:
                        rect_type = 'obstacle'
                    elif 'sol' in line_lower or 'ground' in line_lower or 'floor' in line_lower:
                        rect_type = 'sol'
                
                # Couleur selon le type
                colors = {
                    'sol': (0, 255, 100),
                    'obstacle': (255, 80, 80),
                    'zone': (100, 200, 255),
                    'spawn': (255, 200, 0),
                    'collectible': (255, 100, 255),
                }
                color = colors.get(rect_type, (0, 255, 100))
                
                result['rectangles'].append([rect, rect_type, color])
                result['raw_rects'].append({
                    'rect': rect,
                    'type': rect_type,
                    'line': i + 1,
                    'context': current_list_name or 'standalone'
                })
        
        # ========== PARSING DES TEXTES ==========
        # Pattern pour afficher_text("texte", font, (r,g,b), x, y)
        text_pattern1 = r'afficher_text\s*\(\s*["\']([^"\']+)["\']\s*,\s*[^,]+\s*,\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*,\s*([^,]+)\s*,\s*(\d+)'
        
        # Pattern pour font.render("texte", True, (r,g,b))
        text_pattern2 = r'\.render\s*\(\s*["\']([^"\']+)["\']\s*,\s*True\s*,\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
        
        for i, line in enumerate(lines):
            # Chercher afficher_text()
            match1 = re.search(text_pattern1, line)
            if match1:
                text = match1.group(1)
                r, g, b = int(match1.group(2)), int(match1.group(3)), int(match1.group(4))
                # Essayer de parser x (peut être WIDTH // 2 ou un nombre)
                x_str = match1.group(5).strip()
                y = int(match1.group(6))
                
                # Essayer de convertir x
                try:
                    if '//' in x_str or '/' in x_str:
                        # C'est une expression comme WIDTH // 2
                        if result['width']:
                            x = result['width'] // 2
                        else:
                            x = 400  # Valeur par défaut
                    else:
                        x = int(x_str)
                except:
                    x = 400  # Valeur par défaut
                
                # Essayer de détecter la taille de police
                size = 24  # Par défaut
                if 'titre' in line.lower() or 'title' in line.lower():
                    size = 32
                elif 'small' in line.lower() or 'petit' in line.lower():
                    size = 16
                
                result['texts'].append([(x, y), text, (r, g, b), size])
            
            # Chercher aussi les font.render() avec blit
            match2 = re.search(text_pattern2, line)
            if match2 and 'afficher_text' not in line:
                text = match2.group(1)
                r, g, b = int(match2.group(2)), int(match2.group(3)), int(match2.group(4))
                
                # Position par défaut (on ne peut pas facilement la détecter)
                x, y = 100, 100 + len(result['texts']) * 30
                size = 24
                
                result['texts'].append([(x, y), text, (r, g, b), size])
        
        if result['texts']:
            print(f"    → {len(result['texts'])} textes trouvés")
        
        print(f"  ✓ Fichier analysé: {os.path.basename(filepath)}")
        print(f"    → {len(result['rectangles'])} rectangles trouvés")
        print(f"    → Dimensions détectées: {result['width']}x{result['height']}")
        
    except Exception as e:
        print(f"  ✗ Erreur d'analyse: {e}")
    
    return result


def select_python_file() -> str:
    """Ouvre un dialogue pour sélectionner un fichier Python."""
    global USER_OS
    
    if USER_OS == 'mac':
        try:
            import subprocess
            script = '''
            tell application "System Events"
                activate
                set theFile to choose file with prompt "Choisir un fichier Python" of type {"py", "python"}
                return POSIX path of theFile
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            return None
        except Exception as e:
            print(f"  ⚠ Erreur: {e}")
            return None
    elif TKINTER_AVAILABLE:
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            file_path = filedialog.askopenfilename(
                title="Choisir un fichier Python",
                filetypes=[("Python files", "*.py"), ("Tous les fichiers", "*.*")]
            )
            root.destroy()
            return file_path if file_path else None
        except:
            return None
    return None


# Variable globale pour l'OS
USER_OS = None

def ask_os():
    """Demande le système d'exploitation à l'utilisateur."""
    global USER_OS
    
    print("\n" + "="*60)
    print("🎮 RECT CREATOR PRO - Configuration")
    print("="*60)
    
    print("\n💻 Quel est votre système d'exploitation?")
    print("  [1] 🍎 Mac (macOS)")
    print("  [2] 🐧 Linux")
    print("  [3] 🪟 Windows")
    print()
    
    while True:
        choice = input("Votre choix (1-3): ").strip()
        
        if choice == '1':
            USER_OS = 'mac'
            print("✓ Système: macOS")
            return 'mac'
        elif choice == '2':
            USER_OS = 'linux'
            print("✓ Système: Linux")
            return 'linux'
        elif choice == '3':
            USER_OS = 'windows'
            print("✓ Système: Windows")
            return 'windows'
        else:
            print("❌ Choix invalide, entrez 1, 2 ou 3.")


def ask_screen_size():
    """Demande la taille de l'écran à l'utilisateur au démarrage."""
    print("\n" + "="*60)
    print("🎮 RECT CREATOR PRO - Configuration de l'écran")
    print("="*60)
    
    # Tailles prédéfinies
    presets = {
        '1': (800, 600, "800x600 (Standard)"),
        '2': (1024, 768, "1024x768 (XGA)"),
        '3': (1280, 720, "1280x720 (HD)"),
        '4': (1920, 1080, "1920x1080 (Full HD)"),
        '5': (800, 800, "800x800 (Carré)"),
        '6': (1000, 800, "1000x800 (Custom)"),
    }
    
    print("\n📐 Choisissez une taille d'écran prédéfinie:")
    for key, (w, h, name) in presets.items():
        print(f"  [{key}] {name}")
    print("  [C] Taille personnalisée")
    print()
    
    while True:
        choice = input("Votre choix (1-6 ou C): ").strip().upper()
        
        if choice in presets:
            width, height, _ = presets[choice]
            print(f"✓ Taille sélectionnée: {width}x{height}")
            return width, height
        
        elif choice == 'C':
            try:
                width = int(input("Largeur en pixels: ").strip())
                height = int(input("Hauteur en pixels: ").strip())
                if width > 0 and height > 0:
                    print(f"✓ Taille personnalisée: {width}x{height}")
                    return width, height
                else:
                    print("❌ Les dimensions doivent être positives!")
            except ValueError:
                print("❌ Veuillez entrer des nombres valides!")
        else:
            print("❌ Choix invalide, réessayez.")


class RectCreator:
    """Outil professionnel de création de rectangles pour Pygame."""
    
    # Taille des poignées de redimensionnement
    HANDLE_SIZE = 10
    
    # Couleurs
    COLORS = {
        'background': (30, 30, 30),
        'grid': (50, 50, 50),
        'grid_major': (70, 70, 70),
        'rect_normal': (0, 255, 100),
        'rect_selected': (255, 200, 0),
        'rect_drawing': (255, 80, 80),
        'rect_hover': (100, 200, 255),
        'handle': (255, 255, 255),
        'handle_active': (255, 100, 100),
        'text': (255, 255, 255),
        'text_dim': (150, 150, 150),
        'panel_bg': (40, 40, 45),
        'button': (60, 60, 70),
        'button_hover': (80, 80, 95),
        'success': (0, 255, 100),
        'warning': (255, 200, 0),
        'error': (255, 80, 80),
    }
    
    # Types de rectangles avec couleurs personnalisées
    RECT_TYPES = {
        'sol': (0, 255, 100),       # Vert - Plateformes
        'obstacle': (255, 80, 80),   # Rouge - Obstacles
        'zone': (100, 200, 255),     # Bleu - Zones spéciales
        'spawn': (255, 200, 0),      # Jaune - Points de spawn
        'collectible': (255, 100, 255),  # Rose - Collectibles
    }
    
    # Positions des poignées: (nom, position_x_ratio, position_y_ratio)
    HANDLE_POSITIONS = [
        ('top_left', 0, 0),
        ('top', 0.5, 0),
        ('top_right', 1, 0),
        ('right', 1, 0.5),
        ('bottom_right', 1, 1),
        ('bottom', 0.5, 1),
        ('bottom_left', 0, 1),
        ('left', 0, 0.5),
    ]
    
    def __init__(self, width: int = 800, height: int = 800, image_path: str = None, bg_color: tuple = None):
        pygame.init()
        
        # Configuration de l'écran
        self.LARGEUR_ECRAN = width
        self.HAUTEUR_ECRAN = height
        self.GRID_SIZE = 20  # Taille de la grille en pixels
        
        # Couleur de fond (depuis fichier ou par défaut)
        if bg_color:
            self.COLORS['background'] = bg_color
            self.custom_bg_color = bg_color
        else:
            self.custom_bg_color = None
        
        self.screen = pygame.display.set_mode(
            (self.LARGEUR_ECRAN, self.HAUTEUR_ECRAN),
            pygame.RESIZABLE
        )
        pygame.display.set_caption(f"🎮 Rect Creator Pro - {width}x{height}")
        self.clock = pygame.time.Clock()
        
        # Polices
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # État de l'application
        self.running = True
        self.rectangles = []  # Liste de tuples (rect, type, color)
        self.texts = []  # Liste de tuples (position, texte, couleur)
        self.selected_rect_index = None
        self.selected_text_index = None
        self.hovered_rect_index = None
        
        # Mode actuel: 'rect' ou 'text'
        self.mode = 'rect'
        
        # État du dessin
        self.is_drawing = False
        self.is_moving = False
        self.is_resizing = False
        self.is_moving_text = False
        self.resize_handle = None  # Quelle poignée est utilisée
        self.start_pos = (0, 0)
        self.move_offset = (0, 0)
        self.current_rect = None
        self.current_type = 'sol'
        self.original_rect = None  # Pour le redimensionnement
        self.current_text_color = (255, 255, 255)  # Blanc par défaut
        self.current_text_size = 24  # Taille de texte par défaut
        self.TEXT_SIZES = [12, 16, 20, 24, 32, 40, 48, 64]  # Tailles disponibles
        
        # Options
        self.show_grid = True
        self.snap_to_grid = False  # Désactivé par défaut pour précision au pixel
        self.show_coordinates = True
        self.show_help = True
        self.show_panel = True
        self.show_alignment_guides = True  # Guides d'alignement
        
        # Image de fond
        self.background = None
        self.background_path = None
        if image_path:
            self.load_background(image_path)
        
        # Messages de notification
        self.notifications = []
        
        # Historique pour undo/redo
        self.history = []
        self.redo_stack = []
        self.max_history = 50
        
        # Presse-papiers interne (copier/coller)
        self.clipboard_rect = None   # (rect, type, color)
        self.clipboard_text = None   # (text, color)
        
        # Fichier source (si chargé depuis un .py)
        self.source_file = None
        
        self._print_welcome()
    
    def _print_welcome(self):
        """Affiche le message de bienvenue."""
        # Touche modificateur selon l'OS
        mod = "⌘Cmd" if USER_OS == 'mac' else "Ctrl"
        
        print("\n" + "="*70)
        print("🎮 RECT CREATOR PRO - Outil de Placement Professionnel")
        print("="*70)
        print("\n📋 RACCOURCIS CLAVIER:")
        print("  • Clic gauche + glisser : Dessiner un rectangle")
        print("  • Clic gauche sur rect  : Sélectionner / Déplacer")
        print("  • Suppr / Backspace     : Supprimer la sélection")
        print(f"  • {mod}+Z                : Annuler")
        print(f"  • {mod}+Y                : Rétablir")
        print(f"  • {mod}+C                : Copier")
        print(f"  • {mod}+V                : Coller")
        print(f"  • {mod}+D                : Dupliquer")
        print("  • G                     : Afficher/Masquer la grille")
        print("  • S                     : Activer/Désactiver snap-to-grid")
        print("  • H                     : Afficher/Masquer l'aide")
        print("  • P                     : Afficher/Masquer le panneau")
        print("  • T                     : Mode TEXTE (ajouter des annotations)")
        print("  • R                     : Mode RECTANGLE")
        print("  • 1-5                   : Changer le type de rectangle")
        print("  • Échap                 : Désélectionner")
        print("  • L                     : Charger une image de fond")
        print("  • I                     : 📂 IMPORTER un fichier Python")
        print("  • Q                     : QUITTER et afficher le code")
        print("="*70 + "\n")
    
    def load_background(self, path: str) -> bool:
        """Charge une image de fond."""
        try:
            if os.path.exists(path):
                self.background = pygame.image.load(path)
                self.background = pygame.transform.scale(
                    self.background, 
                    (self.LARGEUR_ECRAN, self.HAUTEUR_ECRAN)
                )
                self.background_path = path
                # Vérifier si notifications existe (peut être appelé pendant __init__)
                if hasattr(self, 'notifications'):
                    self.add_notification(f"✓ Image chargée: {os.path.basename(path)}", 'success')
                else:
                    print(f"  ✓ Image chargée: {os.path.basename(path)}")
                return True
            else:
                print(f"  ⚠ Fichier non trouvé: {path}")
        except Exception as e:
            if hasattr(self, 'notifications'):
                self.add_notification(f"✗ Erreur: {e}", 'error')
            else:
                print(f"  ✗ Erreur: {e}")
        return False
    
    def load_from_python_file(self, parsed_data: dict):
        """Charge les rectangles et textes depuis un fichier Python analysé."""
        if not parsed_data:
            return False
        
        self.rectangles = parsed_data.get('rectangles', [])
        self.texts = parsed_data.get('texts', [])
        self.source_file = parsed_data.get('source_file', None)
        
        # Charger la couleur de fond si détectée
        bg_color = parsed_data.get('bg_color')
        if bg_color:
            self.bg_color = bg_color
        
        # Afficher un résumé
        if hasattr(self, 'notifications'):
            msg = f"📂 Chargé: {len(self.rectangles)} rects"
            if self.texts:
                msg += f", {len(self.texts)} textes"
            msg += f" depuis {os.path.basename(self.source_file)}"
            self.add_notification(msg, 'success')
        
        return True
    
    def import_python_file(self):
        """Importe les rectangles et textes depuis un fichier Python."""
        self.add_notification("📂 Sélection du fichier Python...", 'info')
        
        py_file = select_python_file()
        
        if py_file and os.path.exists(py_file):
            parsed_data = parse_python_file(py_file)
            
            if parsed_data and (parsed_data['rectangles'] or parsed_data['texts']):
                # Demander si on veut remplacer ou ajouter
                print("\n" + "="*50)
                print("📂 Fichier analysé avec succès!")
                print(f"   {len(parsed_data['rectangles'])} rectangles trouvés")
                print(f"   {len(parsed_data['texts'])} textes trouvés")
                if parsed_data.get('bg_color'):
                    print(f"   Couleur de fond: RGB{parsed_data['bg_color']}")
                print("\n  [R] Remplacer tout")
                print("  [A] Ajouter aux éléments existants")
                print("  [C] Annuler")
                choice = input("  > ").strip().upper()
                print("="*50 + "\n")
                
                if choice == 'R':
                    self.save_state()
                    self.load_from_python_file(parsed_data)
                    msg = f"✓ Remplacé: {len(self.rectangles)} rects"
                    if self.texts:
                        msg += f", {len(self.texts)} textes"
                    self.add_notification(msg, 'success')
                elif choice == 'A':
                    self.save_state()
                    new_rects = parsed_data.get('rectangles', [])
                    new_texts = parsed_data.get('texts', [])
                    self.rectangles.extend(new_rects)
                    self.texts.extend(new_texts)
                    self.source_file = parsed_data.get('source_file', None)
                    self.add_notification(f"✓ Ajouté {len(new_rects)} rects, {len(new_texts)} textes", 'success')
                else:
                    self.add_notification("Import annulé", 'warning')
            else:
                self.add_notification("⚠ Aucun élément trouvé", 'warning')
        else:
            self.add_notification("⚠ Aucun fichier sélectionné", 'warning')
    
    def add_notification(self, message: str, type_: str = 'info'):
        """Ajoute une notification temporaire."""
        color = {
            'success': self.COLORS['success'],
            'warning': self.COLORS['warning'],
            'error': self.COLORS['error'],
            'info': self.COLORS['text'],
        }.get(type_, self.COLORS['text'])
        
        self.notifications.append({
            'message': message,
            'color': color,
            'time': pygame.time.get_ticks(),
            'duration': 3000
        })
        print(f"[{type_.upper()}] {message}")
    
    def snap_position(self, pos: tuple) -> tuple:
        """Aligne une position sur la grille si snap activé."""
        if self.snap_to_grid:
            x = round(pos[0] / self.GRID_SIZE) * self.GRID_SIZE
            y = round(pos[1] / self.GRID_SIZE) * self.GRID_SIZE
            return (x, y)
        return pos
    
    def save_state(self):
        """Sauvegarde l'état actuel pour undo."""
        state = [(r.copy(), t, c) for r, t, c in self.rectangles]
        self.history.append(state)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.redo_stack.clear()
    
    def undo(self):
        """Annule la dernière action."""
        if self.history:
            # Sauvegarder l'état actuel pour redo
            current_state = [(r.copy(), t, c) for r, t, c in self.rectangles]
            self.redo_stack.append(current_state)
            
            # Restaurer l'état précédent
            self.rectangles = self.history.pop()
            self.selected_rect_index = None
            self.add_notification("↶ Action annulée", 'info')
    
    def redo(self):
        """Rétablit la dernière action annulée."""
        if self.redo_stack:
            # Sauvegarder l'état actuel pour undo
            current_state = [(r.copy(), t, c) for r, t, c in self.rectangles]
            self.history.append(current_state)
            
            # Restaurer l'état suivant
            self.rectangles = self.redo_stack.pop()
            self.selected_rect_index = None
            self.add_notification("↷ Action rétablie", 'info')
    
    def get_rect_at_pos(self, pos: tuple) -> int:
        """Retourne l'index du rectangle sous la position donnée."""
        for i in range(len(self.rectangles) - 1, -1, -1):
            if self.rectangles[i][0].collidepoint(pos):
                return i
        return None
    
    def get_handle_rects(self, rect: pygame.Rect) -> dict:
        """Retourne les rectangles des poignées de redimensionnement."""
        handles = {}
        hs = self.HANDLE_SIZE
        
        for name, rx, ry in self.HANDLE_POSITIONS:
            x = rect.x + rect.width * rx - hs // 2
            y = rect.y + rect.height * ry - hs // 2
            handles[name] = pygame.Rect(x, y, hs, hs)
        
        return handles
    
    def get_handle_at_pos(self, pos: tuple, rect_index: int) -> str:
        """Retourne le nom de la poignée sous la position, ou None."""
        if rect_index is None or rect_index >= len(self.rectangles):
            return None
        
        rect = self.rectangles[rect_index][0]
        handles = self.get_handle_rects(rect)
        
        for name, handle_rect in handles.items():
            if handle_rect.collidepoint(pos):
                return name
        return None
    
    def resize_rect_with_handle(self, rect: pygame.Rect, handle: str, mouse_pos: tuple, original: pygame.Rect):
        """Redimensionne un rectangle selon la poignée utilisée - PRECISION AU PIXEL."""
        # Pas de snap pour le redimensionnement - précision au pixel
        mx, my = mouse_pos[0], mouse_pos[1]
        
        new_rect = original.copy()
        
        if 'left' in handle:
            new_width = original.right - mx
            if new_width > 5:  # Minimum 5 pixels
                new_rect.x = mx
                new_rect.width = new_width
        
        if 'right' in handle:
            new_width = mx - original.x
            if new_width > 5:
                new_rect.width = new_width
        
        if 'top' in handle:
            new_height = original.bottom - my
            if new_height > 5:
                new_rect.y = my
                new_rect.height = new_height
        
        if 'bottom' in handle:
            new_height = my - original.y
            if new_height > 5:
                new_rect.height = new_height
        
        return new_rect

    def delete_selected(self):
        """Supprime le rectangle ou texte sélectionné."""
        if self.selected_rect_index is not None:
            self.save_state()
            removed = self.rectangles.pop(self.selected_rect_index)
            self.add_notification(f"🗑 Rectangle supprimé: {removed[1]}", 'warning')
            self.selected_rect_index = None
        elif self.selected_text_index is not None:
            self.save_state()
            removed = self.texts.pop(self.selected_text_index)
            self.add_notification(f"🗑 Texte supprimé: {removed[1][:20]}...", 'warning')
            self.selected_text_index = None
    
    def copy_selected(self):
        """Copie le rectangle ou texte sélectionné dans le presse-papiers."""
        if self.selected_rect_index is not None:
            rect, type_, color = self.rectangles[self.selected_rect_index]
            self.clipboard_rect = (rect.copy(), type_, color)
            self.clipboard_text = None
            self.add_notification(f"📋 Rectangle copié: {type_}", 'success')
        elif self.selected_text_index is not None:
            pos, text, color = self.texts[self.selected_text_index]
            self.clipboard_text = (text, color)
            self.clipboard_rect = None
            self.add_notification(f"📋 Texte copié: {text[:20]}...", 'success')
        else:
            self.add_notification("⚠ Rien à copier", 'warning')
    
    def paste_clipboard(self):
        """Colle le contenu du presse-papiers à la position de la souris."""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.clipboard_rect is not None:
            self.save_state()
            rect, type_, color = self.clipboard_rect
            new_rect = rect.copy()
            new_rect.x = mouse_pos[0]
            new_rect.y = mouse_pos[1]
            self.rectangles.append([new_rect, type_, color])
            self.selected_rect_index = len(self.rectangles) - 1
            self.add_notification(f"📋 Rectangle collé: {type_}", 'success')
        elif self.clipboard_text is not None:
            self.save_state()
            text, color = self.clipboard_text
            self.texts.append([mouse_pos, text, color])
            self.selected_text_index = len(self.texts) - 1
            self.add_notification(f"📋 Texte collé: {text[:20]}...", 'success')
        else:
            self.add_notification("⚠ Presse-papiers vide", 'warning')
    
    def duplicate_selected(self):
        """Duplique le rectangle ou texte sélectionné (décalage de 20 pixels)."""
        offset = 20
        
        if self.selected_rect_index is not None:
            self.save_state()
            rect, type_, color = self.rectangles[self.selected_rect_index]
            new_rect = rect.copy()
            new_rect.x += offset
            new_rect.y += offset
            self.rectangles.append([new_rect, type_, color])
            self.selected_rect_index = len(self.rectangles) - 1
            self.add_notification(f"✂ Rectangle dupliqué: {type_}", 'success')
        elif self.selected_text_index is not None:
            self.save_state()
            pos, text, color = self.texts[self.selected_text_index]
            new_pos = (pos[0] + offset, pos[1] + offset)
            self.texts.append([new_pos, text, color])
            self.selected_text_index = len(self.texts) - 1
            self.add_notification(f"✂ Texte dupliqué: {text[:20]}...", 'success')
        else:
            self.add_notification("⚠ Rien à dupliquer", 'warning')

    def add_text_at_position(self, pos: tuple):
        """Ajoute un texte à la position donnée."""
        # Demander le texte dans la console
        print("\n" + "="*50)
        text = input("📝 Entrez votre texte: ").strip()
        if text:
            self.save_state()
            snapped_pos = self.snap_position(pos)
            # Format: [position, texte, couleur, taille]
            self.texts.append([snapped_pos, text, self.current_text_color, self.current_text_size])
            self.add_notification(f"✓ Texte ajouté (taille {self.current_text_size}): {text[:30]}...", 'success')
        print("="*50 + "\n")
    
    def get_text_at_pos(self, pos: tuple) -> int:
        """Retourne l'index du texte sous la position donnée."""
        for i in range(len(self.texts) - 1, -1, -1):
            text_data = self.texts[i]
            text_pos = text_data[0]
            text = text_data[1]
            color = text_data[2]
            size = text_data[3] if len(text_data) > 3 else 24
            # Créer un rectangle approximatif pour le texte
            font = pygame.font.Font(None, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(topleft=text_pos)
            if text_rect.collidepoint(pos):
                return i
        return None
    
    def generate_code(self) -> str:
        """Génère le code Python SIMPLE avec juste les rectangles et textes."""
        lines = []
        lines.append("import pygame")
        lines.append("")
        lines.append(f"# Taille écran: {self.LARGEUR_ECRAN}x{self.HAUTEUR_ECRAN}")
        
        # Couleur de fond si personnalisée
        if self.custom_bg_color:
            lines.append(f"# Couleur de fond: {self.custom_bg_color}")
            lines.append(f"BG_COLOR = {self.custom_bg_color}")
        lines.append("")
        
        # Rectangles groupés par type
        if self.rectangles:
            lines.append("# ============= RECTANGLES =============")
            
            # Grouper par type
            by_type = {}
            for rect, type_, color in self.rectangles:
                if type_ not in by_type:
                    by_type[type_] = []
                by_type[type_].append((rect, color))
            
            for type_, rects in by_type.items():
                lines.append(f"")
                lines.append(f"# {type_.upper()}")
                lines.append(f"{type_}_rects = [")
                for rect, color in rects:
                    lines.append(f"    pygame.Rect({rect.x}, {rect.y}, {rect.width}, {rect.height}),")
                lines.append(f"]")
        
        # Textes
        if self.texts:
            lines.append("")
            lines.append("# ============= TEXTES =============")
            lines.append("# Format: (x, y, texte, couleur, taille)")
            lines.append("textes = [")
            for text_data in self.texts:
                pos = text_data[0]
                text = text_data[1]
                color = text_data[2]
                size = text_data[3] if len(text_data) > 3 else 24
                lines.append(f'    ({pos[0]}, {pos[1]}, "{text}", {color}, {size}),')
            lines.append("]")
        
        return "\n".join(lines)
    
    def print_code_to_terminal(self):
        """Affiche le code généré directement dans le terminal."""
        code = self.generate_code()
        
        print("\n")
        print("=" * 60)
        print("📋 CODE PYTHON - COPIER CI-DESSOUS")
        print("=" * 60)
        print()
        print(code)
        print()
        print("=" * 60)
        print(f"✅ {len(self.rectangles)} rectangles | {len(self.texts)} textes")
        print("=" * 60)
        print()
        
        # Copier dans le presse-papiers si disponible
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(code)
                print("✅ Code copié dans le presse-papiers!")
            except:
                pass
    
    def save_to_file(self):
        """Sauvegarde les données dans un fichier Python simple."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"rects_{timestamp}.py"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.generate_code())
            
            print(f"\n✅ Fichier créé: {filename}")
            print(f"   {len(self.rectangles)} rectangles | {len(self.texts)} textes\n")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def copy_to_clipboard(self):
        """Copie le code généré dans le presse-papiers."""
        code = self.generate_code()
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(code)
                self.add_notification("📋 Code copié dans le presse-papiers!", 'success')
            except Exception as e:
                self.add_notification(f"✗ Erreur presse-papiers: {e}", 'error')
        else:
            self.add_notification("⚠ pyperclip non installé (pip install pyperclip)", 'warning')
            print("\n" + "="*50)
            print("CODE GÉNÉRÉ (copier manuellement):")
            print("="*50)
            print(code)
            print("="*50 + "\n")
    
    def save_to_file(self):
        """Sauvegarde les rectangles dans un fichier Python COMPLET."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"level_rects_{timestamp}.py"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.generate_code())
            
            self.add_notification(f"💾 Fichier complet sauvegardé: {filename}", 'success')
            print(f"\n{'='*60}")
            print(f"✅ FICHIER CRÉÉ: {filename}")
            print(f"   Contient: {len(self.rectangles)} rectangles")
            print(f"   Taille écran: {self.LARGEUR_ECRAN}x{self.HAUTEUR_ECRAN}")
            print(f"   Code Python complet avec fonctions de dessin et collision!")
            print(f"{'='*60}\n")
        except Exception as e:
            self.add_notification(f"✗ Erreur sauvegarde: {e}", 'error')
    
    def handle_events(self):
        """Gère tous les événements."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Afficher le code dans le terminal avant de quitter
                if self.rectangles or self.texts:
                    self.print_code_to_terminal()
                self.running = False
            
            elif event.type == pygame.VIDEORESIZE:
                self.LARGEUR_ECRAN = event.w
                self.HAUTEUR_ECRAN = event.h
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if self.background and self.background_path:
                    self.load_background(self.background_path)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    # Mode TEXTE
                    if self.mode == 'text':
                        # Vérifier si on clique sur un texte existant
                        clicked_text = self.get_text_at_pos(event.pos)
                        if clicked_text is not None:
                            self.selected_text_index = clicked_text
                            self.selected_rect_index = None
                            self.is_moving_text = True
                            text_pos = self.texts[clicked_text][0]
                            self.move_offset = (event.pos[0] - text_pos[0], event.pos[1] - text_pos[1])
                        else:
                            # Ajouter un nouveau texte
                            self.add_text_at_position(event.pos)
                        return
                    
                    # Mode RECTANGLE
                    # D'abord vérifier si on clique sur une poignée de redimensionnement
                    if self.selected_rect_index is not None:
                        handle = self.get_handle_at_pos(event.pos, self.selected_rect_index)
                        if handle:
                            self.is_resizing = True
                            self.resize_handle = handle
                            self.original_rect = self.rectangles[self.selected_rect_index][0].copy()
                            self.save_state()
                            return
                    
                    clicked_rect = self.get_rect_at_pos(event.pos)
                    
                    if clicked_rect is not None:
                        # Sélection ou début de déplacement
                        self.selected_rect_index = clicked_rect
                        self.selected_text_index = None
                        self.is_moving = True
                        rect = self.rectangles[clicked_rect][0]
                        self.move_offset = (event.pos[0] - rect.x, event.pos[1] - rect.y)
                    else:
                        # Début du dessin - au pixel près
                        self.selected_rect_index = None
                        self.selected_text_index = None
                        self.is_drawing = True
                        self.start_pos = event.pos  # Position exacte, pas de snap
            
            elif event.type == pygame.MOUSEMOTION:
                # Mise à jour du hover
                self.hovered_rect_index = self.get_rect_at_pos(event.pos)
                
                # Changer le curseur si on survole une poignée
                if self.selected_rect_index is not None:
                    handle = self.get_handle_at_pos(event.pos, self.selected_rect_index)
                    if handle:
                        # Curseur de redimensionnement
                        if handle in ('left', 'right'):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
                        elif handle in ('top', 'bottom'):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
                        elif handle in ('top_left', 'bottom_right'):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENWSE)
                        elif handle in ('top_right', 'bottom_left'):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENESW)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
                if self.is_resizing and self.selected_rect_index is not None:
                    # Redimensionnement du rectangle
                    new_rect = self.resize_rect_with_handle(
                        self.rectangles[self.selected_rect_index][0],
                        self.resize_handle,
                        event.pos,
                        self.original_rect
                    )
                    self.rectangles[self.selected_rect_index][0] = new_rect
                
                elif self.is_moving_text and self.selected_text_index is not None:
                    # Déplacement du texte - au pixel près
                    new_pos = (
                        event.pos[0] - self.move_offset[0],
                        event.pos[1] - self.move_offset[1]
                    )
                    self.texts[self.selected_text_index][0] = new_pos
                
                elif self.is_drawing:
                    # Dessin au pixel près
                    end_pos = event.pos
                    width = end_pos[0] - self.start_pos[0]
                    height = end_pos[1] - self.start_pos[1]
                    self.current_rect = pygame.Rect(
                        self.start_pos[0], self.start_pos[1], width, height
                    )
                    self.current_rect.normalize()
                
                elif self.is_moving and self.selected_rect_index is not None:
                    # Déplacement du rectangle - au pixel près
                    new_pos = (
                        event.pos[0] - self.move_offset[0],
                        event.pos[1] - self.move_offset[1]
                    )
                    self.rectangles[self.selected_rect_index][0].x = new_pos[0]
                    self.rectangles[self.selected_rect_index][0].y = new_pos[1]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.is_moving_text:
                        self.save_state()
                        self.is_moving_text = False
                    
                    elif self.is_resizing:
                        rect = self.rectangles[self.selected_rect_index][0]
                        self.add_notification(
                            f"↔ Redimensionné: {rect.width}x{rect.height}",
                            'success'
                        )
                        self.is_resizing = False
                        self.resize_handle = None
                        self.original_rect = None
                    
                    elif self.is_drawing and self.current_rect:
                        if self.current_rect.width > 5 and self.current_rect.height > 5:
                            self.save_state()
                            color = self.RECT_TYPES.get(self.current_type, self.COLORS['rect_normal'])
                            self.rectangles.append([
                                self.current_rect.copy(),
                                self.current_type,
                                color
                            ])
                            self.add_notification(
                                f"✓ {self.current_type}: ({self.current_rect.x}, {self.current_rect.y}, "
                                f"{self.current_rect.width}, {self.current_rect.height})",
                                'success'
                            )
                        self.current_rect = None
                    
                    elif self.is_moving:
                        self.save_state()
                    
                    self.is_drawing = False
                    self.is_moving = False
            
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
    
    def handle_keydown(self, event):
        """Gère les raccourcis clavier."""
        mods = pygame.key.get_mods()
        # Sur Mac, utiliser Cmd (META), sinon Ctrl
        if USER_OS == 'mac':
            modifier = mods & pygame.KMOD_META  # Cmd sur Mac
        else:
            modifier = mods & pygame.KMOD_CTRL  # Ctrl sur Windows/Linux
        
        if modifier and event.key == pygame.K_z:
            self.undo()
        elif modifier and event.key == pygame.K_y:
            self.redo()
        elif modifier and event.key == pygame.K_c:
            # COPIER
            self.copy_selected()
        elif modifier and event.key == pygame.K_v:
            # COLLER
            self.paste_clipboard()
        elif modifier and event.key == pygame.K_d:
            # DUPLIQUER (copier + coller en décalé)
            self.duplicate_selected()
        elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
            self.delete_selected()
        elif event.key == pygame.K_ESCAPE:
            self.selected_rect_index = None
            self.selected_text_index = None
        elif event.key == pygame.K_g:
            self.show_grid = not self.show_grid
            self.add_notification(f"Grille: {'ON' if self.show_grid else 'OFF'}", 'info')
        elif event.key == pygame.K_s and not modifier:
            self.snap_to_grid = not self.snap_to_grid
            self.add_notification(f"Snap: {'ON' if self.snap_to_grid else 'OFF'}", 'info')
        elif event.key == pygame.K_h:
            self.show_help = not self.show_help
        elif event.key == pygame.K_p:
            self.show_panel = not self.show_panel
        elif event.key == pygame.K_t:
            # Mode TEXTE
            self.mode = 'text'
            self.add_notification("📝 Mode TEXTE - Cliquez pour ajouter du texte", 'warning')
        elif event.key == pygame.K_r:
            # Mode RECTANGLE
            self.mode = 'rect'
            self.add_notification("🔲 Mode RECTANGLE - Dessinez des rectangles", 'info')
        elif event.key == pygame.K_q:
            # Quitter et afficher le code dans le terminal
            if self.rectangles or self.texts:
                self.print_code_to_terminal()
            self.running = False
        elif event.key == pygame.K_l:
            # Ouvrir le sélecteur de fichier
            self.add_notification("📂 Ouverture du sélecteur...", 'info')
            
            # Sur Mac, on utilise AppleScript
            if USER_OS == 'mac':
                try:
                    import subprocess
                    script = '''
                    tell application "System Events"
                        activate
                        set theFile to choose file with prompt "Choisir une image" of type {"png", "jpg", "jpeg", "gif", "bmp"}
                        return POSIX path of theFile
                    end tell
                    '''
                    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
                    if result.returncode == 0 and result.stdout.strip():
                        path = result.stdout.strip()
                        self.load_background(path)
                    else:
                        self.add_notification("Aucune image sélectionnée", 'warning')
                except Exception as e:
                    self.add_notification(f"Erreur: {e}", 'error')
            elif TKINTER_AVAILABLE:
                path = open_file_dialog("Choisir une image de fond")
                if path:
                    self.load_background(path)
                else:
                    self.add_notification("Aucune image sélectionnée", 'warning')
            else:
                # Fallback sur le terminal
                self.add_notification("Entrez le chemin dans le terminal", 'info')
                path = input("Chemin de l'image: ").strip()
                if path:
                    self.load_background(path)
        elif event.key == pygame.K_i:
            # IMPORTER UN FICHIER PYTHON
            self.import_python_file()
        elif event.key == pygame.K_1:
            self.mode = 'rect'
            self.current_type = 'sol'
            self.add_notification("Type: SOL (plateformes)", 'info')
        elif event.key == pygame.K_2:
            self.mode = 'rect'
            self.current_type = 'obstacle'
            self.add_notification("Type: OBSTACLE", 'info')
        elif event.key == pygame.K_3:
            self.mode = 'rect'
            self.current_type = 'zone'
            self.add_notification("Type: ZONE (spéciale)", 'info')
        elif event.key == pygame.K_4:
            self.mode = 'rect'
            self.current_type = 'spawn'
            self.add_notification("Type: SPAWN (point d'apparition)", 'info')
        elif event.key == pygame.K_5:
            self.mode = 'rect'
            self.current_type = 'collectible'
            self.add_notification("Type: COLLECTIBLE", 'info')
        elif event.key == pygame.K_6:
            # Couleurs de texte
            colors = [
                ((255, 255, 255), "BLANC"),
                ((255, 80, 80), "ROUGE"),
                ((0, 255, 100), "VERT"),
                ((100, 200, 255), "BLEU"),
                ((255, 200, 0), "JAUNE"),
            ]
            # Trouver la couleur actuelle et passer à la suivante
            current_idx = 0
            for i, (c, _) in enumerate(colors):
                if c == self.current_text_color:
                    current_idx = i
                    break
            next_idx = (current_idx + 1) % len(colors)
            self.current_text_color = colors[next_idx][0]
            self.add_notification(f"Couleur texte: {colors[next_idx][1]}", 'info')
        elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            # Augmenter la taille du texte
            self.change_text_size(1)
        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            # Diminuer la taille du texte
            self.change_text_size(-1)
        elif event.key == pygame.K_7:
            # Afficher les guides d'alignement
            self.show_alignment_guides = not getattr(self, 'show_alignment_guides', True)
            self.add_notification(f"Guides d'alignement: {'ON' if self.show_alignment_guides else 'OFF'}", 'info')
    
    def change_text_size(self, direction: int):
        """Change la taille du texte (direction: +1 ou -1)."""
        current_idx = 0
        for i, size in enumerate(self.TEXT_SIZES):
            if size == self.current_text_size:
                current_idx = i
                break
        
        new_idx = max(0, min(len(self.TEXT_SIZES) - 1, current_idx + direction))
        self.current_text_size = self.TEXT_SIZES[new_idx]
        
        # Si un texte est sélectionné, changer sa taille aussi
        if self.selected_text_index is not None:
            self.save_state()
            if len(self.texts[self.selected_text_index]) > 3:
                self.texts[self.selected_text_index][3] = self.current_text_size
            else:
                self.texts[self.selected_text_index].append(self.current_text_size)
            self.add_notification(f"📏 Taille texte: {self.current_text_size}px", 'success')
        else:
            self.add_notification(f"📏 Taille texte par défaut: {self.current_text_size}px", 'info')
    
    def draw_center_cross(self):
        """Dessine une croix au centre de l'écran quand on déplace/dessine."""
        # Afficher seulement si on est en train de déplacer ou dessiner
        if not (self.is_drawing or self.is_moving or self.is_resizing or self.is_moving_text):
            return
        
        center_x = self.LARGEUR_ECRAN // 2
        center_y = self.HAUTEUR_ECRAN // 2
        
        # Couleur subtile pour la croix
        cross_color = (100, 100, 100)  # Gris foncé
        
        # Petite croix au centre (20 pixels)
        cross_size = 20
        pygame.draw.line(self.screen, cross_color, 
                        (center_x - cross_size, center_y), 
                        (center_x + cross_size, center_y), 1)
        pygame.draw.line(self.screen, cross_color, 
                        (center_x, center_y - cross_size), 
                        (center_x, center_y + cross_size), 1)
        
        # Petit cercle au centre
        pygame.draw.circle(self.screen, cross_color, (center_x, center_y), 3, 1)
        
        # Afficher les coordonnées du centre
        label = self.font_small.render(f"({center_x}, {center_y})", True, cross_color)
        self.screen.blit(label, (center_x + 5, center_y + 5))
    
    def draw_grid(self):
        """Dessine la grille."""
        if not self.show_grid:
            return
        
        # Lignes verticales
        for x in range(0, self.LARGEUR_ECRAN, self.GRID_SIZE):
            color = self.COLORS['grid_major'] if x % (self.GRID_SIZE * 5) == 0 else self.COLORS['grid']
            pygame.draw.line(self.screen, color, (x, 0), (x, self.HAUTEUR_ECRAN))
        
        # Lignes horizontales
        for y in range(0, self.HAUTEUR_ECRAN, self.GRID_SIZE):
            color = self.COLORS['grid_major'] if y % (self.GRID_SIZE * 5) == 0 else self.COLORS['grid']
            pygame.draw.line(self.screen, color, (0, y), (self.LARGEUR_ECRAN, y))
    
    def draw_alignment_guides(self):
        """Dessine les guides d'alignement quand un rectangle est sélectionné ou en cours de dessin."""
        if not self.show_alignment_guides:
            return
        
        # Couleur des guides
        guide_color = (0, 255, 255)      # Cyan pour alignement avec autres rectangles
        center_color = (255, 100, 255)   # Magenta pour centre de l'écran
        tolerance = 8  # Pixels de tolérance pour l'alignement
        
        # Centre de l'écran
        screen_center_x = self.LARGEUR_ECRAN // 2
        screen_center_y = self.HAUTEUR_ECRAN // 2
        
        # Déterminer l'élément actif (rectangle ou texte)
        active_rect = None
        active_center = None
        
        if self.is_drawing and self.current_rect:
            active_rect = self.current_rect
            active_center = (self.current_rect.centerx, self.current_rect.centery)
        elif self.selected_rect_index is not None and (self.is_moving or self.is_resizing):
            active_rect = self.rectangles[self.selected_rect_index][0]
            active_center = (active_rect.centerx, active_rect.centery)
        elif self.is_moving_text and self.selected_text_index is not None:
            # Pour le texte, calculer le CENTRE réel (pas le coin supérieur gauche)
            text_data = self.texts[self.selected_text_index]
            text_pos = text_data[0]
            text_content = text_data[1]
            text_color = text_data[2]
            text_size = text_data[3] if len(text_data) > 3 else 24
            
            # Calculer la taille du texte pour trouver son centre
            font = pygame.font.Font(None, text_size)
            text_surface = font.render(text_content, True, text_color)
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            
            # Le centre du texte = position + moitié de la taille
            active_center = (text_pos[0] + text_width // 2, text_pos[1] + text_height // 2)
        
        # ═══════════════════════════════════════════════════════════════
        # GUIDES DE CENTRAGE D'ÉCRAN (toujours vérifiés)
        # ═══════════════════════════════════════════════════════════════
        
        if active_center:
            # Vérifier alignement avec le centre horizontal de l'écran
            if abs(active_center[0] - screen_center_x) <= tolerance:
                # Ligne verticale au centre
                pygame.draw.line(self.screen, center_color, 
                               (screen_center_x, 0), (screen_center_x, self.HAUTEUR_ECRAN), 2)
                label = self.font_small.render(f"✓ CENTRÉ X! ({screen_center_x})", True, center_color)
                self.screen.blit(label, (screen_center_x + 5, 20))
                # Indicateur visuel au niveau de l'élément
                pygame.draw.circle(self.screen, center_color, (screen_center_x, active_center[1]), 8, 2)
            
            # Vérifier alignement avec le centre vertical de l'écran
            if abs(active_center[1] - screen_center_y) <= tolerance:
                # Ligne horizontale au centre
                pygame.draw.line(self.screen, center_color, 
                               (0, screen_center_y), (self.LARGEUR_ECRAN, screen_center_y), 2)
                label = self.font_small.render(f"✓ CENTRÉ Y! ({screen_center_y})", True, center_color)
                self.screen.blit(label, (20, screen_center_y + 5))
                # Indicateur visuel au niveau de l'élément
                pygame.draw.circle(self.screen, center_color, (active_center[0], screen_center_y), 8, 2)
            
            # Si centré sur les deux axes = parfaitement centré!
            if abs(active_center[0] - screen_center_x) <= tolerance and abs(active_center[1] - screen_center_y) <= tolerance:
                label = self.font_medium.render("★ PARFAITEMENT CENTRÉ! ★", True, (0, 255, 0))
                self.screen.blit(label, (screen_center_x - label.get_width() // 2, screen_center_y - 40))
        
        # Vérifier aussi les bords du rectangle par rapport au centre
        if active_rect:
            # Bord gauche au centre?
            if abs(active_rect.left - screen_center_x) <= tolerance:
                pygame.draw.line(self.screen, center_color, 
                               (screen_center_x, 0), (screen_center_x, self.HAUTEUR_ECRAN), 1)
                label = self.font_small.render(f"← bord au centre", True, center_color)
                self.screen.blit(label, (screen_center_x + 5, 40))
            
            # Bord droit au centre?
            if abs(active_rect.right - screen_center_x) <= tolerance:
                pygame.draw.line(self.screen, center_color, 
                               (screen_center_x, 0), (screen_center_x, self.HAUTEUR_ECRAN), 1)
                label = self.font_small.render(f"→ bord au centre", True, center_color)
                self.screen.blit(label, (screen_center_x + 5, 60))
            
            # Bord haut au centre vertical?
            if abs(active_rect.top - screen_center_y) <= tolerance:
                pygame.draw.line(self.screen, center_color, 
                               (0, screen_center_y), (self.LARGEUR_ECRAN, screen_center_y), 1)
                label = self.font_small.render(f"↑ bord au centre", True, center_color)
                self.screen.blit(label, (40, screen_center_y + 5))
            
            # Bord bas au centre vertical?
            if abs(active_rect.bottom - screen_center_y) <= tolerance:
                pygame.draw.line(self.screen, center_color, 
                               (0, screen_center_y), (self.LARGEUR_ECRAN, screen_center_y), 1)
                label = self.font_small.render(f"↓ bord au centre", True, center_color)
                self.screen.blit(label, (40, screen_center_y + 25))
        
        # ═══════════════════════════════════════════════════════════════
        # GUIDES D'ALIGNEMENT AVEC LES AUTRES RECTANGLES
        # ═══════════════════════════════════════════════════════════════
        
        if active_rect is None:
            return
        
        # Points clés du rectangle actif
        active_points = {
            'left': active_rect.left,
            'right': active_rect.right,
            'top': active_rect.top,
            'bottom': active_rect.bottom,
            'center_x': active_rect.centerx,
            'center_y': active_rect.centery,
        }
        
        # Vérifier l'alignement avec tous les autres rectangles
        for i, (rect, _, _) in enumerate(self.rectangles):
            if i == self.selected_rect_index:
                continue
            
            # Points clés de ce rectangle
            rect_points = {
                'left': rect.left,
                'right': rect.right,
                'top': rect.top,
                'bottom': rect.bottom,
                'center_x': rect.centerx,
                'center_y': rect.centery,
            }
            
            # Vérifier alignements verticaux (lignes verticales)
            for active_key in ['left', 'right', 'center_x']:
                for rect_key in ['left', 'right', 'center_x']:
                    if abs(active_points[active_key] - rect_points[rect_key]) <= tolerance:
                        x = rect_points[rect_key]
                        pygame.draw.line(self.screen, guide_color, (x, 0), (x, self.HAUTEUR_ECRAN), 1)
                        # Petite étiquette
                        label = self.font_small.render(f"↕ {x}px", True, guide_color)
                        self.screen.blit(label, (x + 3, 5))
            
            # Vérifier alignements horizontaux (lignes horizontales)
            for active_key in ['top', 'bottom', 'center_y']:
                for rect_key in ['top', 'bottom', 'center_y']:
                    if abs(active_points[active_key] - rect_points[rect_key]) <= tolerance:
                        y = rect_points[rect_key]
                        pygame.draw.line(self.screen, guide_color, (0, y), (self.LARGEUR_ECRAN, y), 1)
                        # Petite étiquette
                        label = self.font_small.render(f"↔ {y}px", True, guide_color)
                        self.screen.blit(label, (5, y + 3))
            
            # Vérifier si les rectangles ont la même largeur ou hauteur
            if abs(active_rect.width - rect.width) <= tolerance:
                # Même largeur - afficher un indicateur
                mid_y = min(active_rect.bottom, rect.bottom) + 10
                pygame.draw.line(self.screen, (0, 255, 100), 
                               (active_rect.left, mid_y), (active_rect.right, mid_y), 2)
                pygame.draw.line(self.screen, (0, 255, 100), 
                               (rect.left, mid_y + 15), (rect.right, mid_y + 15), 2)
                label = self.font_small.render(f"= {rect.width}px", True, (0, 255, 100))
                self.screen.blit(label, (max(active_rect.left, rect.left), mid_y + 3))
            
            if abs(active_rect.height - rect.height) <= tolerance:
                # Même hauteur - afficher un indicateur
                mid_x = min(active_rect.right, rect.right) + 10
                pygame.draw.line(self.screen, (0, 255, 100), 
                               (mid_x, active_rect.top), (mid_x, active_rect.bottom), 2)
                pygame.draw.line(self.screen, (0, 255, 100), 
                               (mid_x + 15, rect.top), (mid_x + 15, rect.bottom), 2)
                label = self.font_small.render(f"= {rect.height}px", True, (0, 255, 100))
                self.screen.blit(label, (mid_x + 3, max(active_rect.top, rect.top)))

    def draw_rectangles(self):
        """Dessine tous les rectangles."""
        for i, (rect, type_, color) in enumerate(self.rectangles):
            # Couleur selon l'état
            if i == self.selected_rect_index:
                draw_color = self.COLORS['rect_selected']
                thickness = 3
            elif i == self.hovered_rect_index:
                draw_color = self.COLORS['rect_hover']
                thickness = 2
            else:
                draw_color = color
                thickness = 2
            
            # Rectangle avec bordure
            pygame.draw.rect(self.screen, draw_color, rect, thickness)
            
            # Remplissage semi-transparent
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((*color, 40))
            self.screen.blit(s, rect.topleft)
            
            # Label du type
            label = self.font_small.render(type_, True, draw_color)
            self.screen.blit(label, (rect.x + 2, rect.y + 2))
            
            # Dimensions
            dims = self.font_small.render(f"{rect.width}x{rect.height}", True, self.COLORS['text_dim'])
            self.screen.blit(dims, (rect.x + 2, rect.y + rect.height - 14))
            
            # Dessiner les poignées de redimensionnement si sélectionné
            if i == self.selected_rect_index:
                self.draw_resize_handles(rect)
    
    def draw_texts(self):
        """Dessine tous les textes/annotations."""
        for i, text_data in enumerate(self.texts):
            pos = text_data[0]
            text = text_data[1]
            color = text_data[2]
            size = text_data[3] if len(text_data) > 3 else 24
            
            # Police selon la taille
            font = pygame.font.Font(None, size)
            
            # Couleur selon l'état
            if i == self.selected_text_index:
                draw_color = self.COLORS['rect_selected']
                # Dessiner un contour autour du texte sélectionné
                text_surface = font.render(text, True, color)
                text_rect = text_surface.get_rect(topleft=pos)
                pygame.draw.rect(self.screen, draw_color, text_rect.inflate(6, 6), 2)
                # Afficher la taille
                size_label = self.font_small.render(f"T:{size}", True, self.COLORS['text_dim'])
                self.screen.blit(size_label, (text_rect.right + 5, text_rect.top))
            else:
                draw_color = color
            
            # Dessiner le texte
            text_surface = font.render(text, True, draw_color)
            self.screen.blit(text_surface, pos)
    
    def draw_resize_handles(self, rect: pygame.Rect):
        """Dessine les poignées de redimensionnement sur un rectangle."""
        handles = self.get_handle_rects(rect)
        
        for name, handle_rect in handles.items():
            # Couleur différente si on survole la poignée
            mouse_pos = pygame.mouse.get_pos()
            if handle_rect.collidepoint(mouse_pos):
                color = self.COLORS['handle_active']
            else:
                color = self.COLORS['handle']
            
            # Dessiner le carré de la poignée
            pygame.draw.rect(self.screen, color, handle_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), handle_rect, 1)
    
    def draw_current_rect(self):
        """Dessine le rectangle en cours de création."""
        if self.is_drawing and self.current_rect:
            pygame.draw.rect(self.screen, self.COLORS['rect_drawing'], self.current_rect, 2)
            
            # Remplissage
            s = pygame.Surface((self.current_rect.width, self.current_rect.height), pygame.SRCALPHA)
            s.fill((*self.COLORS['rect_drawing'], 30))
            self.screen.blit(s, self.current_rect.topleft)
            
            # Dimensions
            dims = f"{self.current_rect.width} x {self.current_rect.height}"
            label = self.font_medium.render(dims, True, self.COLORS['rect_drawing'])
            self.screen.blit(label, (self.current_rect.x, self.current_rect.y - 20))
    
    def draw_panel(self):
        """Dessine le panneau d'information."""
        if not self.show_panel:
            return
        
        panel_width = 220
        panel_height = 220
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((*self.COLORS['panel_bg'], 220))
        
        y = 10
        # Titre
        title = self.font_medium.render("📦 Rect Creator Pro", True, self.COLORS['text'])
        panel.blit(title, (10, y))
        y += 25
        
        # Mode actuel
        mode_color = self.COLORS['warning'] if self.mode == 'text' else self.COLORS['success']
        mode_text = self.font_small.render(f"Mode: {'📝 TEXTE' if self.mode == 'text' else '🔲 RECTANGLE'}", True, mode_color)
        panel.blit(mode_text, (10, y))
        y += 20
        
        # Type actuel (si mode rectangle)
        if self.mode == 'rect':
            type_color = self.RECT_TYPES.get(self.current_type, self.COLORS['text'])
            type_text = self.font_small.render(f"Type: {self.current_type.upper()}", True, type_color)
            panel.blit(type_text, (10, y))
        else:
            # Couleur de texte actuelle
            color_text = self.font_small.render(f"Couleur texte:", True, self.current_text_color)
            panel.blit(color_text, (10, y))
        y += 20
        
        # Compteurs
        count = self.font_small.render(f"Rectangles: {len(self.rectangles)}", True, self.COLORS['text'])
        panel.blit(count, (10, y))
        y += 18
        
        text_count = self.font_small.render(f"Textes: {len(self.texts)}", True, self.COLORS['text'])
        panel.blit(text_count, (10, y))
        y += 20
        
        # État des options
        grid_status = "✓" if self.show_grid else "✗"
        snap_status = "✓" if self.snap_to_grid else "✗"
        options = self.font_small.render(f"Grille: {grid_status}  Snap: {snap_status}", True, self.COLORS['text_dim'])
        panel.blit(options, (10, y))
        y += 22
        
        # Position souris
        mouse_pos = pygame.mouse.get_pos()
        pos_text = self.font_small.render(f"Pos: {mouse_pos[0]}, {mouse_pos[1]}", True, self.COLORS['text_dim'])
        panel.blit(pos_text, (10, y))
        y += 20
        
        # Taille écran
        size_text = self.font_small.render(f"Écran: {self.LARGEUR_ECRAN}x{self.HAUTEUR_ECRAN}", True, self.COLORS['text_dim'])
        panel.blit(size_text, (10, y))
        y += 20
        
        # Couleur de fond si personnalisée
        if self.custom_bg_color:
            bg_text = self.font_small.render(f"🎨 Fond: RGB{self.custom_bg_color}", True, self.custom_bg_color)
            panel.blit(bg_text, (10, y))
            y += 20
        
        # Fichier source si chargé
        if self.source_file:
            source_name = os.path.basename(self.source_file)
            if len(source_name) > 20:
                source_name = source_name[:17] + "..."
            source_text = self.font_small.render(f"📂 {source_name}", True, self.COLORS['success'])
            panel.blit(source_text, (10, y))
            y += 20
        
        # Aide
        help_text = self.font_small.render("H=Aide | I=Import | Q=Quit", True, self.COLORS['text_dim'])
        panel.blit(help_text, (10, y))
        
        self.screen.blit(panel, (10, 10))
    
    def draw_help(self):
        """Affiche l'aide."""
        if not self.show_help:
            return
        
        # Touche modificateur selon l'OS
        mod = "⌘" if USER_OS == 'mac' else "Ctrl"
        
        help_lines = [
            "═══ AIDE ═══",
            "",
            "🖱 SOURIS:",
            "  Glisser = Dessiner rect",
            "  Clic    = Sélectionner",
            "  Glisser = Déplacer/Resize",
            "",
            "⌨ CLAVIER:",
            "  T = Mode TEXTE",
            "  R = Mode RECTANGLE",
            "  1-5 = Types de rect",
            "  6 = Couleur texte",
            "  +/- = Taille texte",
            "  7 = Guides align.",
            "  G = Grille ON/OFF",
            "  S = Snap ON/OFF",
            "  Suppr = Effacer",
            f"  {mod}+C = Copier",
            f"  {mod}+V = Coller",
            f"  {mod}+D = Dupliquer",
            f"  {mod}+Z = Annuler",
            "  L = Charger image",
            "  I = 📂 Import .py",
            "  Q = QUITTER",
            "",
            "🎨 TYPES RECT:",
            "  1=Sol  2=Obstacle",
            "  3=Zone 4=Spawn",
            "  5=Collectible",
        ]
        
        panel_width = 185
        panel_height = len(help_lines) * 17 + 20
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((*self.COLORS['panel_bg'], 220))
        
        y = 10
        for line in help_lines:
            color = self.COLORS['text'] if '═' in line or '🖱' in line or '⌨' in line or '🎨' in line else self.COLORS['text_dim']
            text = self.font_small.render(line, True, color)
            panel.blit(text, (10, y))
            y += 18
        
        self.screen.blit(panel, (self.LARGEUR_ECRAN - panel_width - 10, 10))
    
    def draw_notifications(self):
        """Affiche les notifications."""
        current_time = pygame.time.get_ticks()
        y = self.HAUTEUR_ECRAN - 30
        
        # Nettoyer les anciennes notifications
        self.notifications = [
            n for n in self.notifications
            if current_time - n['time'] < n['duration']
        ]
        
        for notif in reversed(self.notifications[-3:]):  # Max 3 visibles
            alpha = min(255, (notif['duration'] - (current_time - notif['time'])) // 3)
            text = self.font_medium.render(notif['message'], True, notif['color'])
            text.set_alpha(alpha)
            self.screen.blit(text, (10, y))
            y -= 25
    
    def draw(self):
        """Dessine tous les éléments."""
        # Fond
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.COLORS['background'])
        
        # Grille
        self.draw_grid()
        
        # Guides d'alignement
        self.draw_alignment_guides()
        
        # Croix de centre (quand on déplace/dessine)
        self.draw_center_cross()
        
        # Rectangles
        self.draw_rectangles()
        self.draw_current_rect()
        
        # Textes
        self.draw_texts()
        
        # Interface
        self.draw_panel()
        self.draw_help()
        self.draw_notifications()
        
        # Indicateur de mode en bas
        mode_indicator = f"Mode: {'📝 TEXTE (clic pour ajouter)' if self.mode == 'text' else '🔲 RECTANGLE (glisser pour dessiner)'}"
        mode_color = self.COLORS['warning'] if self.mode == 'text' else self.COLORS['success']
        mode_surface = self.font_medium.render(mode_indicator, True, mode_color)
        self.screen.blit(mode_surface, (self.LARGEUR_ECRAN // 2 - mode_surface.get_width() // 2, self.HAUTEUR_ECRAN - 25))
        
        pygame.display.flip()
    
    def run(self):
        """Boucle principale."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()


def main():
    """Point d'entrée - Demande la taille de l'écran puis lance l'outil."""
    
    # Demander d'abord le système d'exploitation
    user_os = ask_os()
    
    # NOUVELLE OPTION: Ouvrir un fichier Python existant
    print("\n" + "="*60)
    print("📂 MODE DE DÉMARRAGE")
    print("="*60)
    print("\n  [1] 🆕 Nouveau projet (écran vide)")
    print("  [2] 📂 Ouvrir un fichier Python existant")
    print("      (Analyse automatique des pygame.Rect)")
    print()
    
    mode_choice = input("Votre choix (1-2): ").strip()
    
    parsed_data = None
    width, height = 800, 600
    image_path = None
    bg_color = None
    
    if mode_choice == '2':
        # Ouvrir un fichier Python existant
        print("\n📂 Sélection du fichier Python...")
        py_file = select_python_file()
        
        if py_file and os.path.exists(py_file):
            print(f"\n📖 Analyse du fichier: {os.path.basename(py_file)}")
            parsed_data = parse_python_file(py_file)
            
            if parsed_data and (parsed_data['rectangles'] or parsed_data['texts']):
                print(f"\n✅ Fichier chargé avec succès!")
                print(f"   → {len(parsed_data['rectangles'])} rectangles trouvés")
                print(f"   → {len(parsed_data['texts'])} textes trouvés")
                
                # Récupérer la couleur de fond si détectée
                if parsed_data.get('bg_color'):
                    bg_color = parsed_data['bg_color']
                    print(f"   → Couleur de fond: RGB{bg_color}")
                
                # Afficher un résumé des types de rectangles
                if parsed_data['rectangles']:
                    types_count = {}
                    for rect, type_, color in parsed_data['rectangles']:
                        types_count[type_] = types_count.get(type_, 0) + 1
                    
                    print("   → Types détectés:")
                    for t, c in types_count.items():
                        print(f"      • {t}: {c}")
                
                # Afficher les textes trouvés
                if parsed_data['texts']:
                    print("   → Textes détectés:")
                    for pos, text, color, size in parsed_data['texts'][:5]:  # Max 5
                        print(f"      • \"{text}\" à ({pos[0]}, {pos[1]})")
                    if len(parsed_data['texts']) > 5:
                        print(f"      ... et {len(parsed_data['texts']) - 5} autres")
            else:
                print("  ⚠ Aucun élément trouvé dans ce fichier")
                parsed_data = None
        else:
            print("  ⚠ Aucun fichier sélectionné")
    
    # TOUJOURS demander la taille de l'écran (car les classes n'ont pas les dimensions)
    print("\n" + "="*60)
    print("📐 DIMENSIONS DE L'ÉCRAN")
    print("="*60)
    print("   (Les dimensions ne sont pas dans les fichiers de classe)")
    width, height = ask_screen_size()
    
    # Demander si on veut charger une image
    print("\n📷 Voulez-vous charger une image de fond?")
    
    print("  [O] Oui - Ouvrir le sélecteur de fichier")
    print("  [N] Non - Continuer sans image")
    choice = input("  > ").strip().upper()
    
    if choice == 'O':
        print("  📂 Ouverture du sélecteur de fichier...")
        image_path = open_file_dialog("Choisir une image de fond")
        if image_path:
            print(f"  ✓ Image sélectionnée: {os.path.basename(image_path)}")
        else:
            print("  ⚠ Aucune image sélectionnée")
    
    print("\n🚀 Lancement de Rect Creator Pro...")
    print(f"   Système: {user_os.upper()}")
    if parsed_data:
        print(f"   📂 Fichier source: {os.path.basename(parsed_data['source_file'])}")
    if bg_color:
        print(f"   🎨 Couleur de fond: RGB{bg_color}")
    print("   Appuyez sur L pour charger une image plus tard.")
    print("   Appuyez sur I pour importer un autre fichier Python.")
    print("   Appuyez sur Q pour quitter et voir le code.\n")
    
    # Créer et lancer l'application avec la couleur de fond
    app = RectCreator(
        width=width, 
        height=height, 
        image_path=image_path if image_path else None,
        bg_color=bg_color
    )
    
    # Si on a chargé un fichier, importer les rectangles
    if parsed_data:
        app.load_from_python_file(parsed_data)
    
    app.run()


if __name__ == "__main__":
    main()