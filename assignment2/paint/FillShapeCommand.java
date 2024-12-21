package ca.utoronto.utm.assignment2.paint;

import javafx.scene.paint.Color;
import java.util.ArrayList;

/**
 * FillShapeCommand is responsible for applying a fill color to selected shapes in the paint application.
 * The command records the original color and selected shapes, allowing for undo and redo actions to restore or reapply
 * the fill color. The color applied is the current default fill color set in the ShapeStrategy.
 */
public class FillShapeCommand extends DrawCommandStrategy{
    private ArrayList<ShapeStrategy> shapes;
    private ArrayList<Color> oldColors;
    private ArrayList<Color> newColor;
    private ArrayList<Integer> selected;
    private ArrayList<Integer> originalSelected;

    /**
     * Executes the fill command by applying the default fill color to the currently selected shapes.
     * This method stores the previous colors of the selected shapes and replaces them with the new fill color.
     * @param paintPanel - the PaintPanel where the shapes are drawn and filled.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        shapes = paintPanel.getModel().getShapes();
        originalSelected = new ArrayList<>(paintPanel.getModel().getSelected());
        newColor = new ArrayList<>();
        oldColors = new ArrayList<>(paintPanel.getModel().getOldColor());
        selected = new ArrayList<>(paintPanel.getModel().getSelected());
        Color tempColor = ShapeStrategy.getDefaultColour();
        for (ShapeStrategy s : shapes) {
            newColor.add(tempColor);
        }
        paintPanel.getModel().setSelectedColors(newColor);
        COMMANDS.add(this);
    }

    /**
     * Undoes the fill action, restoring the original colors to the previously selected shapes.
     * @param paintPanel the PaintPanel where the undo action is performed.
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
        paintPanel.getModel().setSelectedArray(selected);
        paintPanel.getModel().setSelectedColors(oldColors);
    }

    /**
     * Redoes the fill action, reapplying the fill color to the selected shapes.
     * @param paintPanel the PaintPanel where the redo action is performed.
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
        paintPanel.getModel().setSelectedArray(originalSelected);
        paintPanel.getModel().setSelectedColors(newColor);

    }
}