package ca.utoronto.utm.assignment1.othello;

/**
 * The controller class manages the gameplay of Othello. It handles
 * the flow of the game, including player moves, reporting game state
 * and reporting when the game is over
 * Has an Othello game and two players (player1 and player2)
 *
 * @author Zoya
 *
 */

public class Controller {
    private Othello othello;
    protected Player player1, player2;

    /**
     * Constructs a controller object, initializing a new Othello game
     */
    public Controller() {
        this.othello = new Othello();
    }

    /**
     * gets the Othello game instance that this controller is managing
     * @return the Othello game instance
     */
    protected Othello getOthello() {
        return othello;
    }

    /**
     * Starts and manages the game loop. this game continues until it has a winner or
     * tie. Checks who's turn it is, performs the appropriate move and updates current board
     * and informs the player of the move if there is a human player
     */
    public void play(){
        while (!othello.isGameOver()) {
            if (player1 instanceof PlayerHuman){this.report();}

            Move move = null;
            char whosTurn = othello.getWhosTurn();

            if (whosTurn == OthelloBoard.P1)
                move = player1.getMove();
            if (whosTurn == OthelloBoard.P2)
                move = player2.getMove();

            if (player1 instanceof PlayerHuman){this.reportMove(whosTurn, move);}
            othello.move(move.getRow(), move.getCol());
        }
        if (player1 instanceof PlayerHuman) {
            this.reportFinal();
        }
    }

    /**
     * Reports the move made by player, displaying the player's character and move coordinates
     * @param whosTurn either OthelloBoard.P1 or OthelloBoard.P2
     * @param move the move made by player
     */
    private void reportMove(char whosTurn, Move move) {
        System.out.println(whosTurn + " makes move " + move + "\n");
    }

    /**
     *
     * Reports the current game state, including the board, the count of tokens for each player,
     * and who will move next.
     *
     */
    private void report() {

        String s = othello.getBoardString() + OthelloBoard.P1 + ":"
                + othello.getCount(OthelloBoard.P1) + " "
                + OthelloBoard.P2 + ":" + othello.getCount(OthelloBoard.P2) + "  "
                + othello.getWhosTurn() + " moves next";
        System.out.println(s);
    }

    /**
     *  Reports the final game state when the game is over, including the board and the winner.
     */
    private void reportFinal() {

        String s = othello.getBoardString() + OthelloBoard.P1 + ":"
                + othello.getCount(OthelloBoard.P1) + " "
                + OthelloBoard.P2 + ":" + othello.getCount(OthelloBoard.P2)
                + "  " + othello.getWinner() + " won\n";
        System.out.println(s);
    }


}