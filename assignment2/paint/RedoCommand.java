package ca.utoronto.utm.assignment2.paint;

/**
 * RedoCommand is a Command that redoes the most recent undo in PaintPanel.
 * @author pradha91
 */
public class RedoCommand implements Command {

    /**
     * Executes the redo operation by popping off the history stack and adding it to the command
     * stack and re-executing the command.
     * @param paintPanel - the PaintPanel that contains the current drawing state
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        if(!HISTORY.isEmpty()) {
            Command redoCommand = HISTORY.removeLast();
            COMMANDS.add(redoCommand);
            redoCommand.Redo(paintPanel);
        }
        System.out.println("Redo");
    }

    /**
     * This method does not execute since redoing a redo is not applicable,
     * only here for the Command implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
    }

    /**
     * This method does not execute since redoing a redo is not applicable,
     * only here for the Command implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
    }

}
