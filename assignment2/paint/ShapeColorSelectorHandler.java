package ca.utoronto.utm.assignment2.paint;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.ColorPicker;

/**
 * ShapeColorSelectorHandler handles the event of selecting a color for ShapeStrategy fill, outline
 * or background color using a ColorPicker.
 * @author pradha91
 */
public class ShapeColorSelectorHandler implements EventHandler<ActionEvent> {
    private ColorPicker colorPicker;
    private PaintPanel paintPanel;

    /**
     * Constructs ShapeColorSelectorHandler with the given paintPanel and colorPicker.
     * @param paintPanel - PaintPanel that contains the shape whose color will be updated.
     * @param colorPicker - the ColorPicker used to select the color.
     */
    public ShapeColorSelectorHandler(PaintPanel paintPanel, ColorPicker colorPicker) {
        this.colorPicker = colorPicker;
        this.paintPanel = paintPanel;
    }

    /**
     * Handles actionEvent where the user selects the color and updates the color of the shape.
     * @param actionEvent - the ActionEvent triggered by selecting a color on colorPicker.
     */
    @Override
    public void handle(ActionEvent actionEvent) {
        paintPanel.getModel().ColorSelector(colorPicker.getValue());
        System.out.println("Selected color");
    }
}
