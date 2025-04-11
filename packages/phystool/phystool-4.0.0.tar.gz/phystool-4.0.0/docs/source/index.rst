Phystool
========

Ce projet propose différents outils pour la gestion d'une base de donnée de
documents LaTeX. La motivation initiale vient de la difficulté de gérer de gros
documents LaTeX en exploitant le fait qu'il est simple de séparer un tel
document en plusieurs fichiers. Cette séparation offre de nombreux avantages au
détriment d'une prolifération de fichiers individuels. L'objectif initial de ce
projet est de remédier à ce problème dans le contexte de la gestion de
document destinés à l'enseignement en physique (exercices, figures, notices de
laboratoire, notions théorique, questions à choix multiple).

`phystool` simplifie la gestion d'une base de donnée de fichiers
LaTeX et permet notamment de:

* tagger les documents afin de les retrouver rapidement
* gérer l'historique des modifications de fichiers au travers de `git`
* compiler les documents LaTeX en évitant la multiplication des fichiers
  auxiliaires de compilation
* parser les logs liés à la compilation LaTeX afin de les rendre plus lisibles
* automatiquement déclencher une seconde compilation LaTeX en cas de besoin
  (par exemple si certaines références ont changé)




.. toctree::
    :caption: Table des matière
    :hidden:
    :maxdepth: 2

    installation
    usage
    api
