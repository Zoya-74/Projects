package ca.utoronto.utm.assignment2.paint;

import javafx.scene.input.MouseEvent;

/**
 * DrawCommandStrategy provides the base functionality for drawing commands in the paint application.
 * It serves as an abstract class for all drawing commands that can be executed in the paint application.
 */
public abstract class DrawCommandStrategy implements Command{
    MouseEvent mouseEvent;
    /**
     * Executes the drawing command. This method will be implemented by concrete subclasses to define
     * the specific behavior of the drawing action.
     * @param paintPanel - the PaintPanel where the drawing will take place.
     */
    public void execute(PaintPanel paintPanel, MouseEvent event){this.mouseEvent = event; execute(paintPanel);}

    /**
     * Undoes the drawing command by removing the last shape from the model.
     * @param paintPanel - the PaintPanel from which the last shape will be removed.
     */
    public void Undo(PaintPanel paintPanel){
        paintPanel.getModel().removeLastShape();
    }

    /**
     * Redoes the drawing command by reapplying the last undone shape.
     * @param paintPanel - the PaintPanel where the redo action will be applied.
     */
    public void Redo(PaintPanel paintPanel){
        paintPanel.getModel().Redo();
    }
}
