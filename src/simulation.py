from threading import Barrier
from environnement import *
from agent2 import *
import random
# random.seed(424242) 10
random.seed(424242) 

def randomPosition(height, width, nbAgent):
    """Retourne des coordonnée unique contenu dans une grille
    """
    list = [ (i,j) for j in range(width) for i in range(height)]
    return random.sample(list,nbAgent)

def main():
    agentsMap = dict()
    HEIGHT,WIDTH,NB_AGENT = 5,5,10
    env = Environment(HEIGHT,WIDTH,agentsMap)
    
    ########## Exemple 1
    # ids = ["🔴","🔆","⌛","⭐"]
    # positions = [(0,2),(0,3),(0,1),(2,3)]
    # goals = [(0,0),(0,1),(0,2),(0,3)]
    
    ########## Exemple 2
    ids = ["🔴","🔆","⌛","⭐","🤡","🥔","🔥","🏈","👀","🤝","🎄","🧨","✨","🎉","🧧","🎁","🏀","⚽","🎱","🏉","🏆","📞"] # 22
    ids = ids[:NB_AGENT]
    positions = randomPosition(HEIGHT,WIDTH,NB_AGENT)
    goals = randomPosition(HEIGHT,WIDTH,NB_AGENT)
    
    ########## Creation des agent
    env.setGrid(ids,positions,goals)
    agents = []
    b= Barrier(len(ids))
    for i in range(len(ids)):
        tmp = Agent(b,env,ids[i],positions[i])
        agents.append(tmp)
        agentsMap[ids[i]] = tmp
    env.agents = agentsMap
    
    ########## Affichage de la grille de départ
    print(env)
    
    ########## Lancement des thread d'agent
    for agent in agents:
        agent.start()
    for agent in agents:
        agent.join()
        
    ########## Affichage du résultat
    print("\nLe résultat")
    print(env)
    
    ########## Affichage du goal
    goalss = Environment(5,5,agentsMap)
    goalss.setGrid(ids,goals,goals)
    print("Le goal")
    print(goalss)

if __name__ == '__main__':
    main()