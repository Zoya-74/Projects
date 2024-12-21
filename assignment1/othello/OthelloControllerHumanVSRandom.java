package ca.utoronto.utm.assignment1.othello;

/**
 * This controller uses the Model classes to allow the Human player P1 to play
 * the computer P2. The computer, P2 uses a random strategy. 
 * 
 * @author arnold
 *
 */
public class OthelloControllerHumanVSRandom extends Controller{

	/**
	 * Constructs a new OthelloController with a new Othello game, ready to play
	 * with one user at the console, with a random moves computer opponent.
	 */
	public OthelloControllerHumanVSRandom() {
		super();
		this.player2 = new PlayerRandom(this.getOthello(), OthelloBoard.P2);
		this.player1 = new PlayerHuman(this.getOthello(), OthelloBoard.P1);

	}


	/**
	 * Run main to play a Human (P1) against the computer P2. 
	 * The computer uses a random strategy, that is, it randomly picks 
	 * one of its possible moves.
	 * The output should be almost identical to that of OthelloControllerHumanVSHuman.

	 * @param args
	 */
	public static void main(String[] args) {
		
		OthelloControllerHumanVSRandom oc = new OthelloControllerHumanVSRandom();
		oc.play(); // this should work
	}
}
