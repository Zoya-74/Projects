package ca.utoronto.utm.assignment1.othello;

/**
 * The abstract Player class represents a player in the Othello game.
 *  It stores the reference to the Othello game and the player character (P1 or P2).
 * Subclasses of Player are expected to implement the {@code getMove()} method,
 * which will determine how the player selects their move.
 *  This class provides methods to retrieve the Othello game instance and the player's character.
 *
 * @author Zoya
 *
 */

public abstract class Player {
    private Othello othello;
    private char player;


    /**
     * Constructs a Player object with a reference to the Othello game and the player character.
     *
     * @param othello the Othello game instance this player is playing on
     * @param player the character representing the player, either OthelloBoard.P1 or OthelloBoard.P2
     */
    public Player(Othello othello, char player) {
        this.othello = othello;
        this.player = player;
    }

    /**
     Gets the next move for this player. This is an abstract method that needs to be implemented
     * by subclasses, defining how the player selects their move.
     *
     * @return the move selected by the player
     */
    public abstract Move getMove();

    /**
     * Retrieves the Othello game instance associated with this player.
     *
     * @return the Othello game instance
     */
    public Othello getOthello() {
        return this.othello;
    }

    /**
     * Retrieves the character representing this player (P1 or P2).
     *
     * @return the character representing the player, OthelloBoard.P1 or OthelloBoard.P2
     */
    public char getPlayer(){
        return this.player;
    }
}
