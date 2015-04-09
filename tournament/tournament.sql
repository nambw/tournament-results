-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Player Information... Name may not be unique.
CREATE TABLE Players
 ( playerId SERIAL primary key , playerName TEXT );

-- Match Results
CREATE TABLE Match
( matchId SERIAL primary key, WinnerId INTEGER references Players (playerId), LoserId INTEGER references Players(playerId));

CREATE VIEW p_loss AS
SELECT Players.playerId AS id, COUNT(m.matchid) AS loss 
                                FROM Players LEFT JOIN Match as m ON (Players.playerId = m.loserid) GROUP BY id;

CREATE VIEW p_wins AS
SELECT Players.playerId AS id, COUNT(m.matchid) AS wins 
                                FROM Players LEFT JOIN Match as m ON (Players.playerId = m.winnerid) GROUP BY id;

CREATE VIEW p_standing AS
SELECT p.playerId, p.playerName, u.wins, u.wins + u.loss 
            FROM Players AS p JOIN (SELECT p_loss.id as id , p_loss.loss as loss , p_wins.wins as wins 
                                    FROM p_loss  JOIN  p_wins  ON (p_loss.id = p_wins.id) 
                                   ) AS u ON (p.playerId = u.id)
            ORDER BY u.wins  DESC;



