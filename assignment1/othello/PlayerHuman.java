package ca.utoronto.utm.assignment1.othello;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * PlayerHuman is a user that can make any valid move
 * by playing in the console. A PlayerHuman is a Player
 * This includes an OthelloBoard, as well as which player
 * is PlayerHuman (either OthelloBoard.P1, or OthelloBoard.P2)
 *
 * @author arnold
 *
 */
public class PlayerHuman extends Player {
	
	private static final String INVALID_INPUT_MESSAGE = "Invalid number, please enter 1-8";
	private static final String IO_ERROR_MESSAGE = "I/O Error";
	private static BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));


	/**
	 * Constructs a PlayerHuman object with a reference to the Othello game and the player character.
	 *
	 * @param othello the Othello game instance this player is participating in
	 * @param player  the character representing the player (typically P1 or P2)
	 */
	public PlayerHuman(Othello othello, char player) {
		super(othello, player);
	}


	/**
	 Prompts the human player to input the row and column for their move.
	 * This method ensures the input is valid and returns the selected move as a {@code Move} object.
	 *
	 * @return the Move object representing the player's selected move
	 */
	@Override
	public Move getMove() {
		
		int row = getMove("row: ");
		int col = getMove("col: ");
		return new Move(row, col);
	}

	/**
	 * Prompts the player with a message to input a number (row or column) within the valid range (0-7).
	 * This method ensures the input is within bounds and handles invalid input by requesting the player to re-enter.
	 *
	 * @param message the prompt message displayed to the player (e.g., "row: " or "col: ")
	 * @return the valid move input by the player, or -1 if an error occurs
	 */
	private int getMove(String message) {
		
		int move, lower = 0, upper = 7;
		while (true) {
			try {
				System.out.print(message);
				String line = PlayerHuman.stdin.readLine();
				move = Integer.parseInt(line);
				if (lower <= move && move <= upper) {
					return move;
				} else {
					System.out.println(INVALID_INPUT_MESSAGE);
				}
			} catch (IOException e) {
				System.out.println(INVALID_INPUT_MESSAGE);
				break;
			} catch (NumberFormatException e) {
				System.out.println(INVALID_INPUT_MESSAGE);
			}
		}
		return -1;
	}
}
