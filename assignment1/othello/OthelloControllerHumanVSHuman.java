package ca.utoronto.utm.assignment1.othello;

/**
 * Run the main from this class to play two humans against eachother. Only
 * minimal modifications to this class are permitted.
 * 
 * @author arnold
 *
 */
public class OthelloControllerHumanVSHuman extends Controller{


	/**
	 * Constructs a new OthelloController with a new Othello game, ready to play
	 * with two users at the console.
	 */
	public OthelloControllerHumanVSHuman() {
		super();
		this.player1 = new PlayerHuman(this.getOthello(), OthelloBoard.P1);
		this.player2 = new PlayerHuman(this.getOthello(), OthelloBoard.P2);
	}

	/**
	 * Run main to play two Humans against each other at the console.
	 * @param args
	 */
	public static void main(String[] args) {
		
		OthelloControllerHumanVSHuman oc = new OthelloControllerHumanVSHuman();
		oc.play();
	}

}
