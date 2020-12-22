Lors d'une demande de l'agent A vers le B, l'agent B s'il accepte peut réaliser un demande déplacement à c'est autre vois in pour faire de la place. Dans ce cas l'agent B envoie le message de move avec le rang de l'agent A. -> Les mouvement en chaine.

Il faut penser également à vérifier que les messages sont toujours à jours.

Il y a également le cas où 1 où plusieurs agent peuvent être bloqué dans ce cas il faut qu'ils augmente leur rangs temporairement.

Attention au déplacement des agents en temps réels

Revoir si deux move peut être fais en même temps ou si il y a une synchro lors des moves

IsWaiting dans "agent2" permet de savoir si l'agent attend une ou plusieurs réponse d'un ou plusieurs de ses voisins.

On réalise les demande par message si le rang est supérieur dans le content du message

La formule pour le rang de l'utilisateur