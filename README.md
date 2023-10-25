# Cat In Cat Out
Projet d'intégration 3T

## Important: methodologie pour mettre a jour/recreer la db lors du pull d'une branche

1: Dans pycharm, entrer ctrl+alt+r pour ouvrir le terminal de manage.py

2: Dans ce terminal, entrer migrate

3: S'il y a un problème->contacter le propriétaire de la branche

4: Dans le terminal, entrer: loaddata db.json

5: S'il y a un problème->contacter le propriétaire de la branche

6: Normalement la DB est à jour

## Si vous avez modifié la db pendant votre travail sur votre branche

1: Assurez-vous d'avoir bien fait le makemigration (ce qui devrais être fait de base pour votre travail, mais on sais jamais)

2: Dans pycharm, aller dans le terminal normal (PAS le terminal manage.py)

3: Dans ce terminal, entrer: python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > db.json

4: Le fichier db.json devrais avoir été modifié

## Le fichier dependencies.txt contiens tout les packages nécessaires au fonctionnement du code.

Pour l'utiliser:
depuis le terminal dans le dossier  du projet-> pip install -r dependencies.txt

Pour le mettre a jour:
Si vous avez installé un nouveau package qui sera requis par la suite->pip freeze > dependencies.txt
cela réecrira le fichier avec tout les packages, y compris le nouveau.


