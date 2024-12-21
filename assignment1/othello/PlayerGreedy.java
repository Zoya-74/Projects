package ca.utoronto.utm.assignment1.othello;

import java.util.Objects;

/**
 * PlayerGreedy makes a move by considering all possible moves that the player
 * can make. Each move leaves the player with a total number of tokens.
 * getMove() returns the first move which maximizes the number of
 * tokens owned by this player. In case of a tie, between two moves,
 * (row1,column1) and (row2,column2) the one with the smallest row wins. In case
 * both moves have the same row, then the smaller column wins.
 * 
 * Example: Say moves (2,7) and (3,1) result in the maximum number of tokens for
 * this player. Then (2,7) is returned since 2 is the smaller row.
 * 
 * Example: Say moves (2,7) and (2,4) result in the maximum number of tokens for
 * this player. Then (2,4) is returned, since the rows are tied, but (2,4) has
 * the smaller column.
 * 
 * See the examples supplied in the assignment handout.
 *
 * PlayerGreedy is a Player
 * @author arnold
 *
 */

public class PlayerGreedy extends Player {


	/**
	 * Constructs a PlayerGreedy object with a reference to the Othello game and the player character.
	 *
	 * @param othello the Othello game instance this player is participating in
	 * @param player  the character representing the player (typically P1 or P2)
	 */
	public PlayerGreedy(Othello othello, char player) {
		super(othello, player);
	}


	/**
	 * Returns the first valid move that maximizes the number of tokens
	 * owned by this player. In case of a tie between two moves
	 * the method returns the move with the smaller row. In case
	 * of a tie between moves in the same row, returns the smaller
	 * column
	 * @return the greediest Move possible by PlayerGreedy
	 */
	@Override
	public Move getMove() {
		int maxtokens = this.getOthello().getCount(this.getPlayer());
		int rowd = 0;
		int cold = 0;
		int dim = Othello.DIMENSION;
		for (int row = 0; row < dim; row ++){
			for (int col = 0; col < dim; col++){
				OthelloBoard toCheck = this.getOthello().copyBoard();
				if (toCheck.move(row, col, this.getPlayer())){
				int tokens = toCheck.getCount(this.getPlayer());
					if (tokens > maxtokens){
						maxtokens = tokens;
						rowd = row;
						cold = col;
					}
				}
			}
		}
		return new Move(rowd, cold);
	}

}
