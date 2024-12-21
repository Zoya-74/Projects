package ca.utoronto.utm.assignment2.paint;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;

/**
 * FillBackgroundHandler handles the action of filling the background of the with a selected color.
 */
public class FillBackgroundHandler implements EventHandler<ActionEvent> {
    private PaintPanel paintPanel;

    /**
     * Constructs a FillBackgroundHandler with the given paintPanel.
     * @param paintPanel - the PaintPanel on which to apply the background fill.
     */
    public FillBackgroundHandler(PaintPanel paintPanel) {this.paintPanel = paintPanel;}

    /**
     * Handles the action event to fill the background color.
     * When an action occurs, such as a button press, this method creates and executes a FillBackgroundCommand
     * on the associated PaintPanel.
     * @param actionEvent the event that triggers the background fill action.
     */
    @Override
    public void handle(ActionEvent actionEvent) {
        FillBackgroundCommand fillBG = new FillBackgroundCommand();
        fillBG.execute(paintPanel);
    }
}
