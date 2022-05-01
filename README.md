# Brickabrack
Brickabrack est une application web développée dans le cadre du cours Python dispensé par M. Thibault Clérice, en Master 2 Technologies numériques appliquées à l'histoire, à l'École nationale des chartes.
Contrairement à ce que l'on pourrait penser, elle ne contient que des briques et des plans de construction LEGO. Désormais tous les amateurs de LEGO 
ne seront plus jamais en panne d'inspiration. 
# Ses fonctionnalités
L'application Brickabrack donne accès aux index des briques, des plans de construction LEGO et des thèmes. Elle permet également de réaliser des recherches simples et plus avancées.
Le numéro d'élément d'une brique permet d'obtenir le(s) plan(s) de construction LEGO associé(s). Il est possible d'affiner la recherche grâce à la date de sortie et le thème du plan de construction LEGO. 
Quant au numéro d'ensemble d'un plan de construction LEGO, il permet d'obtenir la ou les briques associé(es).
Brickabrack est également collaborative. Un utilisateur muni d'un compte, peut ajouter, modifier, supprimer les données d'une brique, d'un plan de construction et d'un thème. Il peut aussi associer une brique à un plan de construction LEGO.
# Comment installer Brickabrack
L'application n'est utilisable que sous Linux.
Pour l'installer, il faut lancer les commmandes suivantes dans un terminal :
- créer un nouveau dossier : mkdir mondossier
- se déplacer dans ce dossier : cd mondossier
- installer à l'intérieur python dans un environnement virtuel dédié à l'application : python3 -m venv env
- initier un dépôt git : git init
- cloner ce présent répertoire git en faisant "git clone" et l'URL vers le répertoire git sur GitHub. 
- activer l'environnement virtuel : source env/bin/activate
- aller dans le dossier "Brickabrack" : cd Brickabrack
- installer les packetages : pip install -r requirements.txt
- lancer la commande : python run.py
# Les sources de l'application
Par souci de respect des droits d'auteurs, l'application ne peut proposer des images des briques et des plans de construction LEGO. Le nom de brique LEGO et le titre des plans de construction sont ceux du site officiel de la marque.
# Les constributeurs
Ses contributeurs sont Lien Céard et son frère Hugues (pour le choix des briques).
