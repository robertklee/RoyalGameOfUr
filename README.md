# ECE 356 Project Proposal
The following document describes the proposed project for the ECE 356 Project
## Client Requirements
The goal of this project is to “design and implement a simple, creative, computer game which can interact with end user/users.” Two options are available:
- Option 1: Standalone Game with Wii Remote: This is a standalone game application on your computer which interacts with a Wii Remote.
- Option 2: Networked Game Application: build a simple server app which responds to requests and messages from multiple clients, and build a simple client application which interacts with users and communicates with the server application.
## Selected Option
Option 2, a Networked Game Application, was chosen for this project. The project will be an implementation of the ancient game of Ur. The game is a two-player board game based on both luck and strategy. 
## Game Logic 
The project goal is to implement a networked web application for users to play the game of Ur.
This requires:
- A method to allow users to create a game 
- A method to allow users to invite a player to play against
- A board screen where the users can play against each other
- A game over screen giving some summary of the game and statistics for the winner and loser of the game, with options to create another new game
- Game state is captured and gives to the users 

When the users are on the board game they will be able to play the turn based game of Ur, following the logic here described:
- The main goal of The Royal Game of Ur is to move all your pieces across the board along the defined path before your opponent.
- There are two players, each commanding one half of the board. The center strip is common area where both players’ paths merge. 
- Each player starts with 5 pieces (“Pieces”). 
- Each turn a player flips 4 coins. The number of heads corresponds to the spaces (“Spaces”) a player can move one of their pieces. A player may not subdivide their Spaces across multiple Pieces.
- The player can choose to move any of their Pieces on the board the number of Spaces along their defined path (either the red or the blue path).
- Alternatively the player can move a new Piece onto the board from the start of their path the number of Spaces they have.
- If a player rolls all tails their turn is skipped. 
- If the player moves their Piece to a space already occupied by an opposing player’s Piece that Piece is removed from the board and must start from the beginning of the path again.
- If a piece lands on a rosette (special tile) the player may perform another roll and move that piece again.
Some things to note are:
- A player must always make a move if one is possible.
If a player has no possible moves for their roll their turn is skipped.
- A player may not move one of their Pieces into a space already occupied by one of their own Pieces.
