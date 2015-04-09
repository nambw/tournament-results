#!/usr/bin/env python
#
# CLI based program to enter player info, get swiss pair for each round and report match results and player standings after each round.
# Accepts Even number of players only
# Supports single tournament only
#  

from tournament import *

if __name__ == '__main__':

    deleteMatches()
    deletePlayers()
    names = [ ]
    nump = input("Enter even number of players: ")
    if (nump == 0):
       print "No Players"
       exit()

    if (nump %2 != 0):
       print "Number of Players Must be Even"
       exit()

    for i in range(nump):
         player = raw_input("Player Name: ")
         registerPlayer(player)

    ######Begin matches
    matchon = "yes" 
    round = 0 
    while (matchon == "yes"):
      round = round + 1
      print "===== Round ", round, "Begins ===="
      pairs = swissPairings()
      for pair in pairs:
        print pair[0], "vs", pair[2]

      print "Enter Results"
      for pair in pairs:
         pid1  = pair[0]
         pid2  = pair[2]
         print "Player", pid1, "vs Player", pid2	
         getwinner = 1 
         while (getwinner):
            winner = input(" Enter Winner Id: ")
	    if (winner == pid1) :
		getwinner = 0 
		loser = pid2
            elif (winner == pid2):
		getwinner =  0 
		loser = pid1
            else :
	       print "Invalid Winner: Choose from ", pid1, pid2, "only"

         reportMatch(winner, loser)         
      
      print "Player Standing After Round ",round
      print "ID  Name   Wins Matches"
      ps = playerStandings()
      for player in ps:
      	    print player[0], player[1], player[2], player[3]

      matchon = raw_input("Enter yes to continue next round of matches :")

    print "========End of Tournament =========" 


