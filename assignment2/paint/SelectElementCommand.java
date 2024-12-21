package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;

/**
 * SelectElementCommand allows a single shape to be selected and repositioned on the canvas.
 */
public class SelectElementCommand extends DrawCommandStrategy {

    /**
     * Executes the selection command by listening for mouse movements and performs the corresponding action.
     * @param paintPanel - the PaintPanel that holds the model and canvas to interact with.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        // If the mouse is pressed, attempt to select a shape
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            model.setSelected(false, mouseEvent.getX(), mouseEvent.getY());
        }
        // If the mouse is dragged, reposition the selected shape
        else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) {
            model.repositionSelectedShapes(mouseEvent.getX(), mouseEvent.getY());
        }
    }
}
