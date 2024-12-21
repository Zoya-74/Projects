package ca.utoronto.utm.assignment1.othello;

/**
 * The goal here is to print out the probability that Random wins and Greedy
 * wins as a result of playing 10000 games against each other with P1=Random and
 * P2=Greedy. What is your conclusion, which is the better strategy?
 * @author arnold
 *
 */
public class OthelloControllerRandomVSGreedy extends Controller{

	/**
	 * Constructs a new OthelloController with a new Othello game, ready to play
	 * with two computer players with a random and greedy moves strategy.
	 */
	public OthelloControllerRandomVSGreedy() {
		super();
		this.player2 = new PlayerGreedy(this.getOthello(), OthelloBoard.P2);
		this.player1 = new PlayerRandom(this.getOthello(), OthelloBoard.P1);

	}


	/**
	 * Run main to execute the simulation and print out the two line results.
	 * Output looks like: 
	 * Probability P1 wins=.75 
	 * Probability P2 wins=.20
	 * @param args
	 */
	public static void main(String[] args) {
		
		int p1wins = 0, p2wins = 0, numGames = 10000;

		for (int i = 0; i < numGames; i++) {
			OthelloControllerRandomVSGreedy oc = new OthelloControllerRandomVSGreedy();
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
