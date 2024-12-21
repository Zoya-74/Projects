package ca.utoronto.utm.assignment2.paint;

/**
 * UndoCommand is a Command that undoes the last executed command in PaintPanel.
 * @author pradha91
 */
public class UndoCommand implements Command{

    /**
     * Executes the undo command by popping off the command stack and storing it in
     * the command history stack in the paintPanel.
     * @param paintPanel - where the undo command is executed.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        if(!COMMANDS.isEmpty()) {
            Command undoCommand = COMMANDS.removeLast();
            HISTORY.add(undoCommand);
            undoCommand.Undo(paintPanel);
        }
        System.out.println("Undo");
    }

    /**
     * This method does not execute since doing an undo in undo is not applicable,
     * only here for the Command implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
    }

    /**
     * This method does not execute since doing an undo in undo is not applicable,
     * only here for the Command implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
    }
}
