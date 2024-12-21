package ca.utoronto.utm.assignment2.paint;

/**
 * NewFileCommand is a Command that opens a new file onto the canvas, clearing all canvas
 * information and updating the canvas to match.
 *
 */
public class NewFileCommand implements Command {

    /**
     * Clears the canvas and all file information of the canvas.
     *
     * @param paintPanel - the paintPanel where the canvas information will be cleared
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        model.clearCanvas();
        model.clearData();
        COMMANDS.clear();
        HISTORY.clear();
    }

    /**
     * This method does not execute anything since undoing opening a new file is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Undo(PaintPanel paintPanel) {

    }

    /**
     * This method does not execute anything since redoing opening a new file is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Redo(PaintPanel paintPanel) {

    }
}
