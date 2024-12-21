package ca.utoronto.utm.assignment1.othello;
/**
 * The Move class represents a move in a board game, storing
 * row and column. Includes methods to retrieve row and column values
 * @author arnold
 *
 */
public class Move {


	private int row, col;

	/**
	 * Constructs a Move object with given row and column values
	 * @param row the row position of the board
	 * @param col the column position of the board
	 */
	public Move(int row, int col) {
		this.row = row;
		this.col = col;
	}

	/**
	 *
	 * Gets the row position of the move
	 * @return the row position
	 */
	public int getRow() {
		return row;
	}

	/**
	 * Gets the column position of the move
	 *
	 * @return the column position
	 */
	public int getCol() {
		return col;
	}

	/**
	 * Provides a string representation of the move in format (row, column)
	 * @return string (row, column) of the move
	 */
	public String toString() {
		return "(" + this.row + "," + this.col + ")";
	}
}
