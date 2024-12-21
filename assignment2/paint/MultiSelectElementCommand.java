package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;

/**
 * MultiSelectElementCommand allows multiple shapes to be selected and repositioned on the canvas.
 */
public class MultiSelectElementCommand extends DrawCommandStrategy {

    /**
     * Executes the multi-select and move operation based on mouse events.
     * - On a mouse press, it selects one or more shapes at the given mouse position.
     * - On a mouse drag, it repositions the selected shapes based on the mouse's current location.
     * @param paintPanel - the PaintPanel where the drawing and selection occurs.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            model.setSelected(true, mouseEvent.getX(), mouseEvent.getY());
        } else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) {
            model.repositionSelectedShapes(mouseEvent.getX(), mouseEvent.getY());
        }
    }

}
