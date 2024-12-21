package ca.utoronto.utm.assignment2.paint;

import java.util.ArrayList;

/**
 * A CopyCommand is a Command that copies a selected ShapeStrategy.
 *
 */
public class CopyCommand implements Command {
    ArrayList<ShapeStrategy> clipboard = new ArrayList<>();

    /**
     * Copies a selected shape to the clipboard.
     *
     * @param paintPanel - the paint panel that the ShapeStrategy will get copied from.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        if(!paintPanel.getModel().getSelected().isEmpty()) {
            ArrayList<Integer> selectedShapeIndex = paintPanel.getModel().getSelected();
            ArrayList<ShapeStrategy> allShapes = paintPanel.getModel().getShapes();
            for (int i = 0; i < selectedShapeIndex.size(); i++) {
                ShapeStrategy selectedShape = allShapes.get(selectedShapeIndex.get(i));
                selectedShape.setColor(paintPanel.getModel().getOldColor().get(i));
                clipboard.add(selectedShape);
            }
            paintPanel.getModel().setCopiedShapes(clipboard);
            System.out.println("Copied " + clipboard.size() + " element(s)");
            paintPanel.getModel().deselectShape();
        }
    }

    /**
     * This method does not execute anything since undoing a copy command is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
    }

    /**
     * This method does not execute anything since redoing a copy command is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
    }
}
