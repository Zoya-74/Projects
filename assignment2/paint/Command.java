package ca.utoronto.utm.assignment2.paint;
import java.util.ArrayList;
import java.util.EventObject;

/**
 * An interface the command pattern, with methods to execute, undo, and redo actions.
 */
public interface Command {
    ArrayList<Command> COMMANDS = new ArrayList<>();
    ArrayList<Command> HISTORY = new ArrayList<>();

    /**
     * Executes a Command
     * @param paintPanel The paintPanel to execute the command on.
     */
    void execute(PaintPanel paintPanel);

    /**
     * Undoes a Command
     * @param paintPanel The paintPanel to undo the command on.
     */
    void Undo(PaintPanel paintPanel);

    /**
     * Redoes an undo-ed Command
     * @param paintPanel The paintPanel to redo the command on.
     */
    void Redo(PaintPanel paintPanel);
}

