package ca.utoronto.utm.assignment1.othello;

import java.util.ArrayList;
import java.util.Random;

/**
 * PlayerRandom makes a move by first determining all possible moves that this
 * player can make, putting them in an ArrayList, and then randomly choosing one
 * of them.
 * 
 * @author arnold
 *
 */
public class PlayerRandom extends Player{


	/**
	 * Constructs a PlayerRandom object with a reference to the Othello game and the player character.
	 *
	 * @param othello the Othello game instance this player is participating in
	 * @param player  the character representing the player (typically P1 or P2)
	 */
	public PlayerRandom(Othello othello, char player) {
		super(othello, player);
	}

	private Random rand = new Random();

	/**
	 * Determines a random valid move for the player.
	 * It first generates a list of all valid moves by simulating possible moves on a copy of the game board.
	 * Once all valid moves are collected, a random move is selected from the list and returned.
	 *
	 * @return a randomly selected valid Move, or Null if no valid moves are available
	 */
	@Override
	public Move getMove() {
		ArrayList<Move> moves = new ArrayList<>();
		int dim = Othello.DIMENSION;
		for(int row = 0; row <dim; row++) {
			for(int col = 0; col < dim; col++) {
				OthelloBoard N = this.getOthello().copyBoard();
				if(N.move(row, col, this.getPlayer())){
					moves.add(new Move(row, col));
				}
			}
		}
		if(!moves.isEmpty()){
			return moves.get(rand.nextInt(moves.size()));
		}
		return null;
	}

}
