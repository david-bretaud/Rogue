
Pour lancer le jeu : aller dans le dossier multi (le dossier solo étant une sauvegarde intérmédiaire).

Ensuite executer app.py en tapant python app.py dans un terminal.

## Connexions

Avec le navigateur, se connecter à localhost:5001/player/1 pour jouer le joueur 1. Adapter pour les joueurs 2,3 si ils existent ...
Ainsi chaque fenêtre contrôle un joueur.

Dans un autre onglet aller à localhost:5001/master pour avoir accès à une fenêtre de controle du jeu. Elle permet de spécifier le nombre de joueurs entre 1 et 10, cette opération est validée en apuyant sur "Récupérer la valeur". On se sert aussi de ce menu pour sauvegarder la partie (bouton "save") ou charger la sauvegarde ("load"), auquel cas il faut actualiser les fenêtres des joueurs.

## Contrôles

Pour ce qui est des contrôles : tous les joueurs ont les mêmes : les flèches servent à se déplacer, les boutons de A à I servent à utiliser l'item correspondant. Ceux de Q à K servent à lâcher l'objet.

On peut aussi lancer la musique en appuyant sur le bouton play.
