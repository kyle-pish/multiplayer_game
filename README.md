# cs330-final-project-kyle

Multiplayer python game using pygame and a custom networking protocol

Protocol Description:

  Clients will send a message that consists of a flag and some data. 
  The flags are strings that describe the data such as PLAYER_DATA, 
  RESET_GAME_STATE, READY_ CHECK, and more. These flags are how the 
  server determines what to do with the data that is attached, for 
  example if the server receives a packet that has the RESET_GAME_STATE 
  flag, it will call a function to reset all players back to their 
  default state in order to properly start a new game.

Running game:

  1) Run server.py to start the game server
  2) Open 4 client files
  3) Click play and have fun!
