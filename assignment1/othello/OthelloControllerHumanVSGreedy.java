package ca.utoronto.utm.assignment1.othello;

/**
 * This controller uses the Model classes to allow the Human player P1 to play
 * the computer P2. The computer, P2 uses a greedy strategy. 
 * 
 * @author arnold
 *
 */
public class OthelloControllerHumanVSGreedy extends Controller{

	/**
	 * Constructs a new OthelloController with a new Othello game, ready to play
	 * with one user at the console and a greedy moves computer opponent.
	 */
	public OthelloControllerHumanVSGreedy() {
		super();
		this.player2 = new PlayerGreedy(this.getOthello(), OthelloBoard.P2);
		this.player1 = new PlayerHuman(this.getOthello(), OthelloBoard.P1);

	}

	/**
	 * Run main to play a Human (P1) against the computer P2. 
	 * The computer uses a greedy strategy, that is, it picks the first
	 * move which maximizes its number of token on the board.
	 * The output should be almost identical to that of OthelloControllerHumanVSHuman.
	 * @param args
	 */
	public static void main(String[] args) {
		OthelloControllerHumanVSGreedy oc = new OthelloControllerHumanVSGreedy();
		oc.play(); // this should work
	}
}
