package ca.utoronto.utm.assignment1.othello;

/**
 * Keep track of all of the tokens on the board. This understands some
 * interesting things about an Othello board, what the board looks like at the
 * start of the game, what the players tokens look like ('X' and 'O'), whether
 * given coordinates are on the board, whether either of the players have a move
 * somewhere on the board, what happens when a player makes a move at a specific
 * location (the opposite players tokens are flipped).
 * 
 * Othello makes use of the OthelloBoard.
 * 
 * @author arnold
 *
 */
public class OthelloBoard {
	
	public static final char EMPTY = ' ', P1 = 'X', P2 = 'O', BOTH = 'B';
	private int dim = 8;
	private char[][] board;
	private static final int[][] DIRECTIONS = {{0, 1}, {0, -1}, {1, 0}, {-1, 0},
			{-1, 1}, {1, -1}, {-1, -1}, {1, 1}};

	public OthelloBoard(int dim) {
		this.dim = dim;
		board = new char[this.dim][this.dim];
		for (int row = 0; row < this.dim; row++) {
			for (int col = 0; col < this.dim; col++) {
				this.board[row][col] = EMPTY;
			}
		}
		int mid = this.dim / 2;
		this.board[mid - 1][mid - 1] = this.board[mid][mid] = P1;
		this.board[mid][mid - 1] = this.board[mid - 1][mid] = P2;
	}

	public int getDimension() {
		return this.dim;
	}

	/**
	 * 
	 * @param player either P1 or P2
	 * @return P2 or P1, the opposite of player
	 */
	public static char otherPlayer(char player) {
		// Simply check what player the user inputed and give the opposite
		if (player == P1) {
			return P2;
		}
		else if (player == P2) {
			return P1;
		}
		// In case the argument passed for this method is not a valid player
		return EMPTY;
	}

	/**
	 * 
	 * @param row starting row, in {0,...,dim-1} (typically {0,...,7})
	 * @param col starting col, in {0,...,dim-1} (typically {0,...,7})
	 * @return P1,P2 or EMPTY, EMPTY is returned for an invalid (row,col)
	 */
	public char get(int row, int col) {
		// Check if either row or col is out of bounds
		if (!validCoordinate(row, col)) {
		return EMPTY;
		}
		// Else return the char that is on the board corresponding to the row and column
		return this.board[row][col];
	}

	/**
	 * 
	 * @param row starting row, in {0,...,dim-1} (typically {0,...,7})
	 * @param col starting col, in {0,...,dim-1} (typically {0,...,7})
	 * @return whether (row,col) is a position on the board. Example: (6,12) is not
	 *         a position on the board.
	 */
	private boolean validCoordinate(int row, int col) {
		// Checks whether row and col are within bounds of the
		// dimension and returns the boolean result
		return row < this.dim && row >= 0 && col < this.dim && col >= 0;
    }

	/**
	 * Check if there is an alternation of P1 next to P2, starting at (row,col) in
	 * direction (drow,dcol). That is, starting at (row,col) and heading in
	 * direction (drow,dcol), you encounter a sequence of at least one P1 followed
	 * by a P2, or at least one P2 followed by a P1. The board is not modified by
	 * this method. Why is this method important? If
	 * alternation(row,col,drow,dcol)==P1, then placing P1 right before (row,col),
	 * assuming that square is EMPTY, is a valid move, resulting in a collection of
	 * P2 being flipped.
	 * 
	 * @param row  starting row, in {0,...,dim-1} (typically {0,...,7})
	 * @param col  starting col, in {0,...,dim-1} (typically {0,...,7})
	 * @param drow the row direction, in {-1,0,1}
	 * @param dcol the col direction, in {-1,0,1}
	 * @return P1, if there is an alternation P2 ...P2 P1, or P2 if there is an
	 *         alternation P1 ... P1 P2 in direction (dx,dy), EMPTY if there is no
	 *         alternation
	 */
	private char alternation(int row, int col, int drow, int dcol) {
		// initialize variables that will move in the direction drow and dcol respectively
		if (!validCoordinate(row, col)) {
			return EMPTY;
		}
		int startr = row;
		int startcol = col;
		// store the first player in this direction in a variable to check with the next
		// spaces on the board in direction drow and dcol
		char player = this.board[row][col];

		// There is no alteration if the first value in the given direction is empty, since
		// no player will be able to make a valid move
		if (player == EMPTY ||  (dcol == 0 && drow ==0)) {
			return EMPTY;
		}
		// run this loop through the direction drow and dcol
		// for all the valid coordinates
		while (validCoordinate(startr, startcol)) {

			// Once a spot on the board in the required direction is the opposite of
			// the initial player we stored, an alternation has happened,
			// return the appropriate player
			if (this.board[startr][startcol] == EMPTY) {
				return EMPTY;
			}
			// when the player is not the same as the player at the
			//beginning of the sequence, then there is an alternation
			if (player != this.board[startr][startcol]
					&& this.board[startr][startcol] != EMPTY) {
				return otherPlayer(player);
			}
			startr = startr + drow;
			startcol = startcol + dcol;
		}
		// finally, if no alternation has happened and we have reached the end of the board
		// in the given direction, return the appropriate value
		return EMPTY;
	}

	/**
	 * flip all other player tokens to player, starting at (row,col) in direction
	 * (drow, dcol). Example: If (drow,dcol)=(0,1) and player==O then XXXO will
	 * result in a flip to OOOO
	 * 
	 * @param row    starting row, in {0,...,dim-1} (typically {0,...,7})
	 * @param col    starting col, in {0,...,dim-1} (typically {0,...,7})
	 * @param drow   the row direction, in {-1,0,1}
	 * @param dcol   the col direction, in {-1,0,1}
	 * @param player Either OthelloBoard.P1 or OthelloBoard.P2, the target token to
	 *               flip to.
	 * @return the number of other player tokens actually flipped, -1 if this is not
	 *         a valid move in this one direction, that is, EMPTY or the end of the
	 *         board is reached before seeing a player token.
	 */
	private int flip(int row, int col, int drow, int dcol, char player) {
		// If there is no alternation for the desired player,
		// then a flip cannot happen according to
		// the game rules
		if (alternation(row, col, drow, dcol) != player) {
			return -1;
		}
		// initialize a counter for how many tokens are flipped,
		// also initialize the variables
		// for row and col as we move in drow and dcol

		int flipped = 0;
		int startr1 = row;
		int startcol1 = col;
		// continue flipping tokens in the valid environment,
		// where we are still on the board,
		// the anternation to our desired player hasn't happened yet and
		// there is a token to be flippped

		while (validCoordinate(startr1, startcol1) && this.board[startr1][startcol1] != player
		&& this.board[startr1][startcol1] != EMPTY) {
			this.board[startr1][startcol1] = player;
			flipped++;
			startr1 = startr1 + drow;
			startcol1 = startcol1 + dcol;
		}
		// In case there are no tokens to be flipped or no flips have happened,
		// and we reached the end
		// of the board, return the appropriate value
		if ((! validCoordinate(startr1, startcol1) && flipped == 0) || this.board[row][col] == EMPTY) {
			return -1;
		}
		return flipped;

	}

	/**
	 * Return which player has a move (row,col) in direction (drow,dcol).
	 * 
	 * @param row  starting row, in {0,...,dim-1} (typically {0,...,7})
	 * @param col  starting col, in {0,...,dim-1} (typically {0,...,7})
	 * @param drow the row direction, in {-1,0,1}
	 * @param dcol the col direction, in {-1,0,1}
	 * @return P1,P2,EMPTY
	 */
	private char hasMove(int row, int col, int drow, int dcol) {
		// As long as there is an alternation for the further
		// spots in direction of drow and
		// dcol and the spot before the alternation is empty, there is a valid move
		if (this.board[row][col] == EMPTY ) {
			return alternation(row + drow, col + dcol, drow, dcol);
		}
		// appropriate value when there is no move
		return EMPTY;
	}

	/**
	 * 
	 * @return whether P1,P2 or BOTH have a move somewhere on the board, EMPTY if
	 *         neither do.
	 */
	public char hasMove() {
		// initialize booleans for which players have a move since both is possible

		boolean player1 = false;
		boolean player2 = false;

		// iterate through each spot on the board and use all
		// possible directions from DIRECTIONS to check
		// whether any direction from that spot has a move
		for (int row = 0; row < this.dim; row++) {
			for (int col = 0; col < this.dim; col++) {
				for (int[] direction : DIRECTIONS) {
					int drow = direction[0];
					int dcol = direction[1];
					if (hasMove(row, col, drow, dcol) != EMPTY) {
						// return which player has a valid move.
						// Only one player can have a move in a certain
						// direction from board[row][col]
						char temp = hasMove(row, col, drow, dcol);
						if (temp == P1){
							player1 = true;
						}
						else if (temp == P2){
							player2 = true;
						}
					}
				}
				}
			}

		// return the appropriate value based on who has the move
		if (player1 && player2){
			return BOTH;
		}
		else if (player1){
			return P1;
		}
		else if (player2){
			return P2;
		}
		return EMPTY;
	}


	/**
	 * Make a move for player at position (row,col) according to Othello rules,
	 * making appropriate modifications to the board. Nothing is changed if this is
	 * not a valid move.
	 * 
	 * @param row    starting row, in {0,...,dim-1} (typically {0,...,7})
	 * @param col    starting col, in {0,...,dim-1} (typically {0,...,7})
	 * @param player P1 or P2
	 * @return true if player moved successfully at (row,col), false otherwise
	 */
	public boolean move(int row, int col, char player) {
		// HINT: Use some of the above helper methods to get this methods
		// job done!!
		int[] dir = {0, -1, 1};
		boolean result = false;
		// ensure that out coordinate is valid and iterate through all possible directions that can be
		// taken from board[row][col]
		if (validCoordinate(row, col) && this.board[row][col] == EMPTY) {
			for (int drow: dir){
				for(int dcol: dir) {
					// eliminate the direction where nothing moves and check if
					// the given player is who has a move
					if (! (drow == 0 && dcol == 0) &&
							alternation(row + drow, col + dcol, drow, dcol) == player) {

						// If our given player has a valid move, perform the move and flip tokens,
						// making the successful move true
						this.board[row][col] = player;
						flip(row + drow, col + dcol, drow, dcol, player);
						result = true;
					}
				}
			}
		}
		// after iterating through all the possible directions and
		// not finding a move, return appropriately
		return result;
	}

	/**
	 * 
	 * @param player P1 or P2
	 * @return the number of tokens on the board for player
	 */
	public int getCount(char player) {
		// tracking how many tokens are on the board
		int count = 0;
		// iterate through row and col and if it has a token for the given player, increment count
		for (int row = 0; row < this.dim; row++) {
			for (int col = 0; col < this.dim; col++) {
				if (this.board[row][col] == player) {
					count++;
				}
			}
		}

		return count;
	}

	/**
	 * Getter method for OthelloBoard that returns a copied board so
	 * original board is unmodifiable
	 * @return a copied version of OthelloBoard
	 */
	public OthelloBoard copyBoard(){
		OthelloBoard newBoard = new OthelloBoard(this.dim);
		for (int row = 0; row < 8; row ++){
			for (int col = 0; col < 8; col ++){
				newBoard.board[row][col] = this.board[row][col];
			}
		}
		return newBoard;
	}
	/**
	 * @return a string representation of this, just the play area, with no
	 *         additional information. DO NOT MODIFY THIS!!
	 */
	public String toString() {
		/**
		 * See assignment web page for sample output.
		 */
		String s = "";
		s += "  ";
		for (int col = 0; col < this.dim; col++) {
			s += col + " ";
		}
		s += '\n';

		s += " +";
		for (int col = 0; col < this.dim; col++) {
			s += "-+";
		}
		s += '\n';

		for (int row = 0; row < this.dim; row++) {
			s += row + "|";
			for (int col = 0; col < this.dim; col++) {
				s += this.board[row][col] + "|";
			}
			s += row + "\n";

			s += " +";
			for (int col = 0; col < this.dim; col++) {
				s += "-+";
			}
			s += '\n';
		}
		s += "  ";
		for (int col = 0; col < this.dim; col++) {
			s += col + " ";
		}
		s += '\n';
		return s;
	}

	/**
	 * A quick test of OthelloBoard. Output is on assignment page.
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		
		OthelloBoard ob = new OthelloBoard(8);
		System.out.println(ob.toString());
		System.out.println("getCount(P1)=" + ob.getCount(P1));
		System.out.println("getCount(P2)=" + ob.getCount(P2));
		for (int row = 0; row < ob.dim; row++) {
			for (int col = 0; col < ob.dim; col++) {
				ob.board[row][col] = P1;
			}
		}
		System.out.println(ob.toString());
		System.out.println("getCount(P1)=" + ob.getCount(P1));
		System.out.println("getCount(P2)=" + ob.getCount(P2));

		// Should all be blank
		for (int drow = -1; drow <= 1; drow++) {
			for (int dcol = -1; dcol <= 1; dcol++) {
				System.out.println("alternation=" + ob.alternation(4, 4, drow, dcol));
			}
		}

		for (int row = 0; row < ob.dim; row++) {
			for (int col = 0; col < ob.dim; col++) {
				if (row == 0 || col == 0) {
					ob.board[row][col] = P2;
				}
			}
		}
		System.out.println(ob.toString());

		// Should all be P2 (O) except drow=0,dcol=0
		for (int drow = -1; drow <= 1; drow++) {
			for (int dcol = -1; dcol <= 1; dcol++) {
				System.out.println("direction=(" + drow + "," + dcol + ")");
				System.out.println("alternation=" + ob.alternation(4, 4, drow, dcol));
			}
		}

		// Can't move to (4,4) since the square is not empty
		System.out.println("Trying to move to (4,4) move=" + ob.move(4, 4, P2));

		ob.board[4][4] = EMPTY;
		ob.board[2][4] = EMPTY;

		System.out.println(ob.toString());

		for (int drow = -1; drow <= 1; drow++) {
			for (int dcol = -1; dcol <= 1; dcol++) {
				System.out.println("direction=(" + drow + "," + dcol + ")");
				System.out.println("hasMove at (4,4) in above direction =" + ob.hasMove(4, 4, drow, dcol));
			}
		}
		System.out.println("who has a move=" + ob.hasMove());
		System.out.println("Trying to move to (4,4) move=" + ob.move(4, 4, P2));
		System.out.println(ob.toString());






	}
}
