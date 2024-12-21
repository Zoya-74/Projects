package ca.utoronto.utm.assignment2.paint;

import java.util.ArrayList;
import java.util.Random;

/**
 * PasteCommand is a DrawCommandStrategy that pastes ShapeStrategy onto the PaintPanel.
 * This command duplicates the selected shapes, repositions them slightly, and adds them to the canvas.
 */
public class PasteCommand extends DrawCommandStrategy {
    ArrayList<Integer> copiedShapesIndex = new ArrayList<>();
    ArrayList<ShapeStrategy> removedShapes = new ArrayList<>();

    /**
     * Executes the paste command, duplicating the selected shapes and repositioning them on the canvas.
     * The copied shapes are repositioned by a random offset to avoid overlap.
     * @param paintPanel - the PaintPanel on which the shapes will be pasted
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        ArrayList<ShapeStrategy> currShapes = paintPanel.getModel().getShapes();
        ArrayList<ShapeStrategy> copiedShapes = new ArrayList<>();
        ArrayList<ShapeStrategy> selectedShapesToCopy = paintPanel.getModel().getCopiedShapes();
        // Reposition the shapes slightly by some random offset
        Random rand = new Random();
        int offsetX = rand.nextInt(30) + 5;
        int offsetY = rand.nextInt(30) + 5;
        for(ShapeStrategy s : selectedShapesToCopy) {
            ShapeStrategy copy = s.copy();
            copy.reposition(offsetX, offsetY);
            copiedShapes.add(copy);
            currShapes.add(copy);
            copiedShapesIndex.add(currShapes.size() - 1);
        }
        // Now the copied shapes are part of the canvas of shapes
        paintPanel.getModel().setShapesList(currShapes);


        // Show the copied shapes now!
        System.out.println("Pasted " + copiedShapes.size() + " element(s)");
        COMMANDS.add(this);
    }

    /**
     * Undoes the paste operation by removing the pasted shapes from the canvas.
     * @param paintPanel - the PaintPanel on which the paste operation will be undone
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
        ArrayList<ShapeStrategy> currShapes = paintPanel.getModel().getShapes();
        // Copy the entire shapes array
        ArrayList<ShapeStrategy> originalShapes = new ArrayList<>(currShapes);
        for (int index : copiedShapesIndex) {
            removedShapes.add(originalShapes.get(index));
            currShapes.remove(originalShapes.get(index));
        }
        paintPanel.getModel().setShapesList(currShapes);
        System.out.println("Undo " + removedShapes.size() + " pasted shape(s)");
    }

    /**
     * Redoes the paste operation by re-adding the removed shapes to the canvas.
     * @param paintPanel the PaintPanel on which the paste operation will be redone
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
        ArrayList<ShapeStrategy> currShapes = paintPanel.getModel().getShapes();
        for(int i = 0; i < removedShapes.size(); i++) {
            ShapeStrategy s = removedShapes.get(i);
            int index = copiedShapesIndex.get(i);
            currShapes.add(index, s);
        }
        removedShapes.clear();
        paintPanel.getModel().setShapesList(currShapes);
        System.out.println("Redo " + copiedShapesIndex.size() + " pasted shapes");
        removedShapes.clear();
    }
}