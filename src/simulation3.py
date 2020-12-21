from environnement3 import *
from agent3 import *

def main():
    env = Environment(3,3)
    ids = ["🔴","🔆","⌛","⭐","🤡","🥔","🔥","🏈"]
    # positions = [(0,2),(0,3),(1,2),(2,3),(4,4)]
    # goals = [(0,0),(0,1),(0,3),(0,2),(0,)]
    nb_deplacement_total = 0
    positions = [(i,j) for i in range(3) for j in range(3)]
    positions.pop(0)
    goals = [(0,0),(0,1),(0,2),(2,0),(1,1),(2,1),(1,0),(1,2)]
    env.setGrid(ids,positions,goals)
    agents = []
    for i in range(len(ids)):
        agents.append(Agent(env,ids[i],positions[i]))
    print(env)
    goalss = Environment(3,3)
    goalss.setGrid(ids,goals,goals)
    
    for agent in agents:
        agent.start()
    for agent in agents:
        agent.join()
        nb_deplacement_total += agent.getNbMoves()
    print("Le résultat")
    print(env)
    print("Le goal")
    print(goalss)
    print("Le nombre total de déplacements : ", nb_deplacement_total)

if __name__ == '__main__':
    main()