# Journal de Développement : Gestion des Contrôles (Pygame)

**User :** `pygame.key.name()` fait quoi en fait ?

**AI :** C'est une fonction de traduction. Elle prend l'**identifiant numérique** d'une touche (le code interne de Pygame, comme `107`) et le transforme en une **chaîne de caractères** lisible par un humain (comme `"k"` ou `"espace"`).

C'est utile pour :

1. **L'affichage :** Montrer au joueur quelle touche il a configurée.
2. **Le Debug :** Voir rapidement quelle touche est pressée dans la console.

---

**User :** En fait je fais les touches pour changer les touches de mon jeu mais est ce qu on peut utliser en mode quand je veux bien chnager de prendre une touche unique tu vois ou pas ?

**AI :** Oui, c'est indispensable pour éviter les conflits (qu'une même touche fasse deux actions). La meilleure méthode est de vérifier si la touche choisie est déjà présente dans tes paramètres avant de l'attribuer.

Si la `nouvelle_touche` est déjà dans les valeurs utiliséses, tu refuses le changement ou tu affiches une erreur.

---

**User :** La ce que j ai fait c est bon ?

```python
if event.type == pygame.KEYDOWN:
    if self.rect_z_active:
        config.haut = pygame.key.name(event.key)
        self.rect_z_active = False
    elif self.rect_s_active:
        config.bas = pygame.key.name(event.key)
        self.rect_s_active = False
    # ...
```
