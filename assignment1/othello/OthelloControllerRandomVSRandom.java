package ca.utoronto.utm.assignment1.othello;

/**
 * Determine whether the first player or second player has the advantage when
 * both are playing a Random Strategy.
 * 
 * Do this by creating two players which use a random strategy and have them
 * play each other for 10000 games. What is your conclusion, does the first or
 * second player have some advantage, at least for a random strategy? 
 * State the null hypothesis H0, the alternate hypothesis Ha and 
 * about which your experimental results support. Place your short report in
 * randomVsRandomReport.txt.
 * 
 * @author arnold
 *
 */
public class OthelloControllerRandomVSRandom extends Controller {

	/**
	 * Constructs a new OthelloController with a new Othello game, ready to play
	 * with two random moves computer players.
	 */
	public OthelloControllerRandomVSRandom() {
		super();
		this.player2 = new PlayerRandom(this.getOthello(), OthelloBoard.P2);
		this.player1 = new PlayerRandom(this.getOthello(), OthelloBoard.P1);

	}

	/**
	 * Run main to execute the simulation and print out the two line results.
	 * Output looks like 
	 * Probability P1 wins=.75 
	 * Probability P2 wins=.20
	 * @param args
	 */
	public static void main(String[] args) {
		int p1wins = 0, p2wins = 0, numGames = 10000;

		for (int i = 0; i < numGames; i++) {
			OthelloControllerRandomVSRandom oc = new OthelloControllerRandomVSRandom();
			oc.play();
			char winner = oc.getOthello().getWinner();
			if(winner == OthelloBoard.P1){
				p1wins++;
			}
			else if (winner == OthelloBoard.P2){
				p2wins++;
			}


		}

		System.out.println("Probability P1 wins=" + (float) p1wins / numGames);
		System.out.println("Probability P2 wins=" + (float) p2wins / numGames);
	}
}
