package ca.utoronto.utm.assignment2.paint;

import javafx.scene.paint.Color;

/**
 * FillBackgroundCommand is responsible for changing the background color of the PaintPanel.
 */
public class FillBackgroundCommand extends DrawCommandStrategy{
    private Color oldBGColor;
    private Color newBGColor;

    /**
     * Executes the command by changing the background color of the PaintPanel to the current default color.
     * The previous background color is stored, and the new background color is fetched from the default color in {
     * ShapeStrategy.
     * @param paintPanel - the PaintPanel on which the background color will be changed.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        oldBGColor = paintPanel.getModel().getbackgroundColor();
        newBGColor = ShapeStrategy.getDefaultColour();
        paintPanel.getModel().setbackgroundColor(newBGColor);
        COMMANDS.add(this);
    }

    /**
     * Undoes the background color change by reverting the background to the previously stored color.
     * @param paintPanel - the PaintPanel where the background color will be reverted.
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
        paintPanel.getModel().setbackgroundColor(oldBGColor);

    }

    /**
     * Redoes the background color change by setting the background to the new color again.
     * @param paintPanel - the PaintPanel where the background color will be set to the new color again.
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
        paintPanel.getModel().setbackgroundColor(newBGColor);

    }

}
