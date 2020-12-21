# SMA -  Interraction multi-agent

### BRUNEAU Richard - VASLIN Pierre

Brouillon :
- Modélisation du SMA
- Négociation
- Protocole d'envoi des messages
- Argumentation

## Modélisation du système multi-agent

Nous avons choisi de modéliser notre SMA avec deux classes : 

- L'environnement, qui peut s'apparenter au plateau du taquin 
- L'agent, qui doit se déplacer dans le taquin pour atteindre son but, aussi appelé la case dans l'énoncé. 

## Réalisation d'un taquin simplifié

Dans un premier temps, nous avons réalisé une version simplifié du taquin en multi-threading. Nous avons suivi le modèle décrit ci-dessus afin de voir si le modèle était bon et ce qui devait être amélioré Notre grille était une grille 3x3 avec 8 agents. Il n'y a pas de communication entre les agents. La grille initiale est la suivante :

![Grille initiale]()

L'objectif à atteindre est le suivant :

![Grille objectif]()

Malheureusement, le programme s'arrête ici :

![Fin du programme]() 

Il est aisé de déduire que le programme s'arrête car des agents sont bien placés mais bloquent la circulation pour d'autres agents. Notre modélisation du SMA semble pertinente, nous allons faire communiquer les agent entre eux afin de pouvoir résoudre les conflits sur les agents bloquants.=