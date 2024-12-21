package ca.utoronto.utm.assignment2.paint;

import javafx.scene.paint.Color;

import java.util.ArrayList;

/**
 * CutCommand cuts (removing) selected shapes from the paint panel and storing them in a clipboard.
 */
public class CutCommand implements Command {
    ArrayList<ShapeStrategy> clipboard = new ArrayList<>();
    ArrayList<Integer> selectedShapesIndex;
    ArrayList<Color> shapeColors;

    /**
     * Executes the cut operation by removing selected shapes from the paint panel and
     * storing them in the clipboard. The selected shapes are also deselected.
     * @param paintPanel - the PaintPanel where the shapes will be cut from.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        if(!paintPanel.getModel().getSelected().isEmpty()) {
            //Copy the two arrays we need before deselecting shape
            selectedShapesIndex = new ArrayList<>(paintPanel.getModel().getSelected());
            shapeColors = new ArrayList<>(paintPanel.getModel().getOldColor());

            paintPanel.getModel().deselectShape();

            // Copy the array of all shapes and another ArrayList for shapes that is only for
            // index referencing
            ArrayList<ShapeStrategy> allShapes = paintPanel.getModel().getShapes();
            ArrayList<ShapeStrategy> copiedListShapes = new ArrayList<>(allShapes);
            //Refer to each index and add the selected shape on clipboard and remove it from
            //paint panel
            for (int i = 0; i < selectedShapesIndex.size(); i++) {
                ShapeStrategy selectedShape = copiedListShapes.get(selectedShapesIndex.get(i));
                allShapes.remove(selectedShape);
                selectedShape.setColor(shapeColors.get(i));
                clipboard.add(selectedShape);
            }
            paintPanel.getModel().setCopiedShapes(clipboard);
            paintPanel.getModel().setShapesList(allShapes);
            System.out.println("Cut " + clipboard.size() + " element(s)");
            paintPanel.getModel().deselectShape();
            COMMANDS.add(this);
        }
    }

    /**
     * Undoes the cut operation by restoring the shapes from the clipboard back into the paint panel.
     * @param paintPanel - the PaintPanel where the shapes will be restored.
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
        paintPanel.getModel().setShapes(clipboard);
        System.out.println("Undo " + clipboard.size() + " element(s)");
    }

    /**
     * Redoes the cut operation by removing the shapes again and adding them to the clipboard.
     * @param paintPanel - the PaintPanel where the cut operation will be reapplied.
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
        //Copy the two arrays we need before deselecting shape

        // Copy the array of all shapes and another ArrayList for shapes that is only for
        // index referencing
        ArrayList<ShapeStrategy> allShapes = paintPanel.getModel().getShapes();
        ArrayList<ShapeStrategy> copiedListShapes = new ArrayList<>(allShapes);
        //Refer to each index and add the selected shape on clipboard and remove it from
        //paint panel
        for (int i = 0; i < selectedShapesIndex.size(); i++) {
            ShapeStrategy selectedShape = copiedListShapes.get(selectedShapesIndex.get(i));
            allShapes.remove(selectedShape);
            selectedShape.setColor(shapeColors.get(i));
            clipboard.add(selectedShape);
        }
        paintPanel.getModel().setCopiedShapes(clipboard);
        paintPanel.getModel().setShapesList(allShapes);
        System.out.println("Redo " + clipboard.size() + " element(s)");
        paintPanel.getModel().deselectShape();
    }
}
