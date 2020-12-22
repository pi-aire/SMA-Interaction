# SMA -  Interaction multi-agent

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

Dans un premier temps, nous avons réalisé une version simplifié du taquin en multi-threading. Pour cela, nous avons implémenté un agent dans le fichier [`src/agent.py`](https://github.com/pi-aire/SMA-Interaction/blob/main/src/agent.py) qui cherche uniquement à rejoindre son but. Nous avons suivi le modèle décrit ci-dessus afin de voir si le modèle était bon et ce qui devait être amélioré Notre grille était une grille 3x3 avec 8 agents. Il n'y a pas de communication entre les agents. La grille initiale est la suivante :

![Grille initiale](./images/Simple_initial.png)

L'objectif à atteindre est le suivant : 

![Grille objectif](./images/Simple_objectif.png)

Malheureusement, le programme s'arrête ici :

![Grille finale](./images/Simple_final.png) 

Il est aisé de déduire que le programme s'arrête car des agents sont bien placés mais bloquent la circulation pour d'autres agents. Notre modélisation du SMA semble pertinente, nous allons faire communiquer les agents entre eux afin qu'il signale quand un agent bloque le passage.


## Les messages

Afin de résoudre le problème soulevé précédemment, nous avons implémenté un agent 2, qui peut communiquer. L'implémentation est disponible dans le fichier [`src/agent2.py`](https://github.com/pi-aire/SMA-Interaction/blob/main/src/agent2.py).

### Type des messages

Nous avons défini différents types de messages :

- `Request` : Qui demande à l'agent destinataire quelque chose
- `Informative` : Pour informer le destinataire

### Contenu des messages

Dans le fichier `src/agent2.py` nous avons créé une classe `Content` qui décrit le contenu d'un message. Pour l'agent 2, qui communique de façon simplifier, le contenu du message repose sur trois attributs:
- `pSender`: Pour la position de l'envoyeur au moment de l'écriture du message
- `pReceiver`: Pour la position du receveur au moment de la l'écriture du message
- `prioritySender`: Qui fixe la priorité de la personne envoyant le message

Les deux premiers attributs nous permettent de déterminer si la requête est toujours d'actualité ou si elle est obsolète. 
Le dernier attribut permet de lui donner plus ou moins d'importance.

### Expédition des messages 

Notre agent cherchera en premier à se déplacer sur une case libre, si elle améliore sa distance de Manhattan pour atteindre son but. Si aucune case libre ne le lui permet, il envera alors un message à son voisin qui améliore le plus ça distance de Manhattan.

### Lecture des messages

Avant de choisir si notre agent va se déplacer ou non, il regarde si il a des messages lui demandant de se déplacer. Si c'est le cas, il enregistre l'information dans un booléen `needToMove`. Ensuite, l'agent prends la décision de se déplacer, même si cela augmente sa distance de Manhattan. 