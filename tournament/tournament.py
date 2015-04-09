#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# Template provided by Udacity
# Modified to define required DB API
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB =  psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute(" DELETE FROM Match;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect();
    c = DB.cursor()
    c.execute(" DELETE FROM Players;")
    DB.commit()
    DB.close()

def countPlayers():
   """Returns the number of players currently registered."""
   DB = psycopg2.connect("dbname=tournament")
   c = DB.cursor()
   c.execute("Select * FROM Players;")
   result = c.fetchall();
   print "There are" + str(c.rowcount) + "registered players"
   return c.rowcount

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players (playerName) values (%s)", (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect();
    c = DB.cursor()
    query = "SELECT * FROM p_standing;"
    c.execute(query)
    result = c.fetchall()

    return result

def playerStandingsOld():
    """Returns a list of the players and their win records, sorted by wins.
    Unused function as the functionality is defined better using views in above function
    """
    DB = connect();
    c = DB.cursor()
    query = "SELECT p.playerId, p.playerName, u.wins, u.wins + u.loss \
            FROM Players AS p JOIN (SELECT a.id as id , a.loss as loss , b.wins as wins \
                          FROM (SELECT Players.playerId AS id, COUNT(m.matchid) AS loss \
                                FROM Players LEFT JOIN Match as m ON (Players.playerId = m.loserid) GROUP BY id \
                               ) AS a \
                          JOIN (SELECT Players.playerId AS id, COUNT(m.matchid) AS wins \
                                FROM Players LEFT JOIN Match as m ON (Players.playerId = m.winnerid) GROUP BY id \
                               ) AS b \
                          ON (a.id = b.id)) AS u \
                     ON (p.playerId = u.id)\
                     ORDER BY u.wins  DESC; "

    c.execute(query)
    result = c.fetchall()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect();
    c = DB.cursor()
    c.execute("INSERT INTO Match (WinnerId, LoserId) values (%s, %s)", (winner,loser,))
    DB.commit()
    DB.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    if len(standings) < 2:
        print("Not enough Players.")
        return NULL;
    pair = []
    for i in range(0, len(standings), 2):
        pair.append ((standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]))
    return pair

