import random
import numpy as np

# NOTE: Player 1 starts first game

# Making a simple tick tack toe game from scratch, just with the core rules 
# All games must be completed even if a winning position no longer exists

# Computer plays for player 1 and player 2 if True, else human vs human game ATM
COMPUTER = True

GAMES = 1000
PLAYER_1 = 1
PLAYER_2 = 2

# Board structure
board = np.array([[11,12,13],[21,22,23],[31,32,33]])

# Possible winning position if a player are holding one of these positions, they have won the game 
winning_position =  np.array([[1,1,1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,1,1,1,-1,-1,-1],
                                [-1,-1,-1,-1,-1,-1,1,1,1],[1,-1,-1,1,-1,-1,1,-1,-1],
                                [-1,1,-1,-1,1,-1,-1,1,-1],[-1,-1,1,-1,-1,1,-1,-1,1],
                                [1,-1,-1,-1,1,-1,-1,-1,1],[-1,-1,1,-1,1,-1,1,-1,-1]])


# Game functions
def decide_starting_player(game): return PLAYER_2 if game % 2 else PLAYER_1
def decide_player_turn(player): return PLAYER_1 if player == PLAYER_2 else PLAYER_2
def check_winner(player_position, winning_position): return True if [position for position in winning_position if np.count_nonzero(position == player_position) == 3] else False
def computer_move(game_options): return random.choice(game_options) # Returns a random computer move from current position    

# NOTE: No user input checking ATM and needs a designer 
def human_move(player, game_options,current_game):
    print(f"Player: {player}'s turn")
    print(f"Board are \n {np.where(current_game > 10, 0, current_game).reshape(3,-1)}")
    print(f"Options are \n {game_options}")
    return int(input())
            
if __name__ == "__main__":
    
    # GAME ON
    stats = []
    for game in range(GAMES):
        print(f'Playing Game number {game}')
        current_game = board.flatten()
        game_options = board.flatten()

        player = decide_starting_player(game)
        
        for action in range(9):
            if not action == 0:
                player = decide_player_turn(player)
            
            # Make a the computer do a random move
            if COMPUTER:
                move = computer_move(game_options)

            else:
                move = human_move(player, game_options, current_game)
            
            # Remove the current move from the game options 
            game_options = np.setdiff1d(game_options,move) 
            
            # Move
            current_game[current_game==move] = player 

            # Map current player position's
            player_position = current_game == player
            player_position = np.array(player_position, dtype=int)
        
            if check_winner(player_position,winning_position):
                stats.append(player) 
                print(f"Winner are player: {player}, with position: \n {np.where(current_game > 10, 0, current_game).reshape(3,-1)}")
                break
            
            # No more moves game over
            if action == 8:
                stats.append(0)

    # Sum up stats
    stats = np.array(stats, dtype=int)
    print(f'Winner stats for games player 1: {np.sum(stats == 1)}, player 2: {np.sum(stats == 2)} draw: {np.sum(stats == 0)}')
        
