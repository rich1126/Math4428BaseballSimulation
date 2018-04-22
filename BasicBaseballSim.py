## Monte-Carlo Simulation of a Baseball Game
## Base code includes walks, but not any defensive schemes/pitching
## A hit shifts every batter by that position. So, if the current set up is
    ##[0,1,1,3], runner on 2nd, 3rd, and 3 runs have scored
    ##A single would make it [1,0,1,4], a double [0,1,0,5]
## No extra innings games. We allow ties
    
## Simulation results output to a csv called baseballSim.txt    
    
## Statistics used were compiled from Baseball Reference, 2017 Full Season

## Statistics are stored in a dictionary, indexed as follows 
## "LastName" : [OBP, 1B, 2B, 3B, HR, BB]
## where 1B,...,BB are proportions on [0,1] of frequency, and BB includes HBP
    
##Find simulation parameters (number of runs) at bottom
    
playerStats = {"Dozier":[0.31, 0.70,0.10,0.02,0.05,0.13]}
awayLineup = ["Dozier","Dozier","Dozier","Dozier","Dozier","Dozier","Dozier","Dozier","Dozier"]
homeLineup = ["Dozier","Dozier","Dozier","Dozier","Dozier","Dozier","Dozier","Dozier","Dozier"]
    
import random

def singleGame(awayLineup, homeLineup):
    ## Initialize lineups, innings, outs, score, batters, baserunners
    ## The 3rd entry in Baserunner array is the score of the team

    awayBaserunner = [0,0,0,0]
    
    homeBaserunner = [0,0,0,0]
    
    inning = 1
    outs = 0
    currentBatterIndex = 0
    
    ## Away team loop. They are always allowed 9 full innings
    while inning <= 9:
        while outs < 3:
            currentBatter = awayLineup[currentBatterIndex]
            OBP = playerStats[currentBatter][0]
            singles = playerStats[currentBatter][1]
            doubles = playerStats[currentBatter][2]
            triples = playerStats[currentBatter][3]
            HR = playerStats[currentBatter][4]
                        
            r = random.random()   # Uniform [0,1] selection
            if r > OBP:
                outs +=1
            else:
                s = random.random()
                if 0<=s< singles:
                    awayBaserunner = hit(1,awayBaserunner)
                elif singles <= s < doubles:
                    awayBaserunner = hit(2,awayBaserunner)
                elif doubles <= s < triples:
                    awayBaserunner = hit(3,awayBaserunner)
                elif triples <= s < HR:
                    awayBaserunner = homeRun(awayBaserunner)
                else:
                    awayBaserunner = walk(awayBaserunner)
            
            #Select next batter, mod 9.
            currentBatterIndex = (currentBatterIndex + 1)%9
        #Clear bases at end of inning, reset outs
        awayBaserunner = [0,0,0,awayBaserunner[3]]
        outs = 0
        inning += 1
            
    ## Home team loop. They play 8 innings, unless they are behind after 8.
    currentBatterIndex = 0
    inning = 0
    outs = 0
    while inning <= 8:
        while outs < 3:
            currentBatter = homeLineup[currentBatterIndex]
            OBP = playerStats[currentBatter][0]
            singles = playerStats[currentBatter][1]
            doubles = playerStats[currentBatter][2]
            triples = playerStats[currentBatter][3]
            HR = playerStats[currentBatter][4]
            
            r = random.random()   # Uniform [0,1] selection
            if r > OBP:
                outs +=1
            else:
                s = random.random()
                if 0<=s< singles:
                    homeBaserunner = hit(1,homeBaserunner)
                elif singles <= s < doubles:
                    homeBaserunner = hit(2,homeBaserunner)
                elif doubles <= s < triples:
                    homeBaserunner = hit(3,homeBaserunner)
                elif triples <= s < HR:
                    homeBaserunner = homeRun(homeBaserunner)
                else:
                    homeBaserunner = walk(homeBaserunner)
            
            #Select next batter, mod 9.
            currentBatterIndex = (currentBatterIndex + 1)%9
        #Clear bases at end of inning    
        homeBaserunner = [0,0,0,homeBaserunner[3]]
        outs= 0
        inning += 1
    if homeBaserunner[3] <= awayBaserunner[3]:
        while outs < 3:
            currentBatter = homeLineup[currentBatterIndex]
            OBP = playerStats[currentBatter][0]
            singles = playerStats[currentBatter][1]
            doubles = playerStats[currentBatter][2]
            triples = playerStats[currentBatter][3]
            HR = playerStats[currentBatter][4]
            
            r = random.random()   # Uniform [0,1] selection
            if r > OBP:
                outs +=1
            else:
                s = random.random()
                if 0<=s< singles:
                    homeBaserunner = hit(1,homeBaserunner)
                elif singles <= s < doubles:
                    homeBaserunner = hit(2,homeBaserunner)
                elif doubles <= s < triples:
                    homeBaserunner = hit(3,homeBaserunner)
                elif triples <= s < HR:
                    homeBaserunner = homeRun(homeBaserunner)
                else:
                    homeBaserunner = walk(homeBaserunner)
            
            #Select next batter, mod 9.
            currentBatterIndex = (currentBatterIndex + 1)%9
    return awayBaserunner[3], homeBaserunner[3]
    
    
#Adds runners and hitter to score total, clears bases
def homeRun(Baserunner):
    Baserunner[3] += (1+sum(Baserunner[0:3]))
    Baserunner = [0,0,0,Baserunner[3]]
    return Baserunner

#Shifts base runner array according to hit type (n=1,2,3)
def hit(n, Baserunner):
    if n == 1:
        Baserunner[3] += Baserunner[2] #Man from 3rd scores
        Baserunner[2] = Baserunner[1]
        Baserunner[1] = Baserunner[0]
        Baserunner[0] = 1
    elif n == 2:
        Baserunner[3] += Baserunner[2] + Baserunner[1] #3rd, 2nd score
        Baserunner[2] = Baserunner[1]
        Baserunner[1] = 1
        Baserunner[0] = 0
    else:
        Baserunner[3] += sum(Baserunner[0:3])
        Baserunner[2] = 1
        Baserunner[1] = 0
        Baserunner[0] = 0
    return Baserunner

#Shifts base runner array accordingly if a walk occurs
def walk(Baserunner):
    if Baserunner[2] ==1:
        if Baserunner[1] == 1:
            if Baserunner[0] == 1:
                Baserunner[3] += 1
            else:
                Baserunner[0] == 1
        elif Baserunner[0] == 1:
            Baserunner[1] == 1
        else:
            Baserunner[0] == 1
    elif Baserunner[1] == 1:
        if Baserunner[0] == 1:
            Baserunner[2] == 1
        else:
            Baserunner[0] == 1
    elif Baserunner[0] == 1:
        Baserunner[1] == 1
    else:
        Baserunner[0] == 1
    return Baserunner


## Define number of games to run
numGames = 100

## Define file to output stuff

simFile = open("baseballSim.txt", "w")

for i in range(numGames):
    result = singleGame(awayLineup,homeLineup)
    simFile.write(str(result[0]))
    simFile.write(',')
    simFile.write(str(result[1]))
    simFile.write('\n')

simFile.close()
