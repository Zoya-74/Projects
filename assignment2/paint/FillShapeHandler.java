package ca.utoronto.utm.assignment2.paint;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;

/**
 * FillShapeHandler handles the action of filling selected shapes with a new color.
 */
public class FillShapeHandler implements EventHandler<ActionEvent> {
    private PaintPanel paintPanel;

    /**
     * Constructs a FillShapeHandler for the given PaintPanel.
     * @param paintPanel - the PaintPanel where shapes are filled.
     */
    public FillShapeHandler(PaintPanel paintPanel) {
        this.paintPanel = paintPanel;
    }
    /**
     * Handles the fill action when triggered by the user.
     * When the fill action is triggered, this method executes the FillShapeCommand,
     * which applies the fill color to selected shapes.
     * @param actionEvent the event triggered by user interaction (such as selecting fill).
     */
    @Override
    public void handle(ActionEvent actionEvent) {
            FillShapeCommand fillShapeCommand = new FillShapeCommand();
            fillShapeCommand.execute(paintPanel);

    }
}


