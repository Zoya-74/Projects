package ca.utoronto.utm.assignment2.paint;

import java.util.ArrayList;

/**
 * ClearCanvasCommand is a Command that clears the canvas of all drawn ShapeStrategy.
 */
public class ClearCanvasCommand implements Command {
    public ArrayList<ShapeStrategy> storage = new ArrayList<ShapeStrategy>();
    /**
     * Executes the consequences of clearing the canvas, removing all ShapeStrategy from the canvas.
     * @param paintPanel - the PaintPanel on which all the shapes will be removed
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        storage.clear();
        storage.addAll(paintPanel.getModel().getShapes());
        paintPanel.getModel().clearCanvas();
        System.out.println("Clear Canvas");
        COMMANDS.add(this);
    }

    /**
     * Undoes the ClearCanvas operation by adding all erased ShapeStrategy back to the canvas.
     * @param paintPanel - the PaintPanel on which the paste operation will be undone
     */
    @Override
    public void Undo(PaintPanel paintPanel) {paintPanel.getModel().setShapes(storage);}

    /**
     * Redoes the ClearCanvas operation by removing all ShapeStrategy from the canvas.
     * @param paintPanel the PaintPanel on which the paste operation will be redone
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
        execute(paintPanel);
    }

}
