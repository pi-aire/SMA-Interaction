# TP interaction SMA
## Infos
* On ne compte pas le mouvement
* On essaye de minimiser les mouvements (on fait des demandes de déplacement à d'autre pièce pour pouvoir minimiser ses mouvements dans le cas ou la pièce refus, la pièce principale va essayer de la com )
* Le gain est uniquement global se qui force les pièces satisfaites à quand même se déplacer pour que tous le monde soit satisfait.
* La grille n'a pas de comportement intelligent
* Lors de l'envoie d'un message on envoie sa position de départ et celle où l'on souhaite arriver. Vu que nous somme en parallèle, la pièce gênante peut avoir bouger, c'est pour ça que l'on fournit la position de départ.
* On n'impose pas via message le déplacement d'un autre agent
* Fonctionne jusqu'à +-90% de la grille, record avec 25 case contenant un case vide.


### Etape 1
* Faire des action simples
* on met en place des simple demandes pas de négociation

### Etape 2
* minimiser le nombre de déplacement
* augmenter le nombre d'agent dans la grille

### Rendu

* La qualiter est important pour le rendu
![tp](./infotp.png)
![sujet](./TP1SMA2020.jpeg)