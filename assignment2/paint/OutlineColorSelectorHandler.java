package ca.utoronto.utm.assignment2.paint;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.ColorPicker;

/**
 * OutlineColorSelectorHandler handles the action of selecting an outline color using a ColorPicker.
 * When a user selects a color, this event handler updates the current outline color in the PaintModel.
 * and logs the selected color to the console.
 */
public class OutlineColorSelectorHandler implements EventHandler<ActionEvent> {
    private ColorPicker colorPicker;
    private PaintPanel paintPanel;

    /**
     * Constructs OutlineColorSelectorHandler with the given paintPanel and colorPicker.
     * @param paintPanel - PaintPanel that contains the shape whose outline color will be updated.
     * @param colorPicker - the ColorPicker used to select the outline color.
     */
    public OutlineColorSelectorHandler(PaintPanel paintPanel, ColorPicker colorPicker) {
        this.colorPicker = colorPicker;
        this.paintPanel = paintPanel;
    }

    /**
     * Handles actionEvent where the user selects the color and updates the outline color of the shape.
     * @param actionEvent - the ActionEvent triggered by selecting an outline color on colorPicker.
     */
    @Override
    public void handle(ActionEvent actionEvent) {
        paintPanel.getModel().setOutlineColor(colorPicker.getValue());
        System.out.println("Selected outline color: " + colorPicker.getValue());
    }
}
