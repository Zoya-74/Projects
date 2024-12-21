package ca.utoronto.utm.assignment2.paint;

/**
 * NullCommand is a no-operation (no-op) implementation of the DrawCommandStrategy pattern.
 * This class acts as a placeholder to avoid null checks.
 */
public class NullCommand extends DrawCommandStrategy {

    /**
     * Does nothing when called. Acts as a placeholder when no specific command is active.
     * @param paintPanel - the PaintPanel where the drawing takes place.
     */
    @Override
    public void execute(PaintPanel paintPanel) {}

    /**
     * Does nothing for undo functionality. Used when no specific command needs to be undone.
     * @param paintPanel - the PaintPanel where the drawing takes place.
     */
    @Override
    public void Undo(PaintPanel paintPanel) {}

    /**
     * Does nothing for redo functionality. Used when no specific command needs to be redone.
     * @param paintPanel - the PaintPanel where the drawing takes place.
     */
    @Override
    public void Redo(PaintPanel paintPanel) {}
}
