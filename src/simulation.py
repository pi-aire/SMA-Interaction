from environnement import *
from agent2 import *

def main():
    agentsMap = dict()
    env = Environment(5,5,agentsMap)
    ids = ["🔴","🔆","⌛","⭐","🤡","🥔","🔥","🏈"]
    # positions = [(0,2),(0,3),(1,2),(2,3),(4,4)]
    # goals = [(0,0),(0,1),(0,3),(0,2),(0,)]
    positions = [(i,j) for i in range(3) for j in range(3)]
    positions.pop(0)
    goals = [(0,0),(0,1),(0,2),(2,0),(1,1),(2,1),(1,0),(1,2)]
    env.setGrid(ids,positions,goals)
    agents = []
    
    for i in range(len(ids)):
        tmp = Agent(env,ids[i],positions[i])
        agents.append(tmp)
        agentsMap[ids[i]] = tmp
    env.agents = agentsMap
    print(env)
    
    for agent in agents:
        agent.start()
    for agent in agents:
        agent.join()
    print("Le résultat")
    print(env)
    
    # Juste pour le display du goal
    goalss = Environment(5,5,agentsMap)
    goalss.setGrid(ids,goals,goals)
    print("Le goal")
    print(goalss)

if __name__ == '__main__':
    main()