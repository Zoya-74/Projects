package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;

/**
 * DrawCircleCommand draws circle shape feedback based on user input.
 * The circle is drawn interactively by clicking and dragging the mouse. The user clicks to start the circle,
 * and as the mouse is dragged, the circle shape is updated. When the mouse is released, the circle is finalized and
 * added to the model.
 */
public class DrawCircleCommand extends DrawCommandStrategy {
    Oval circle;

    /**
     * Executes the command for drawing an oval.
     * - When the mouse is pressed, the starting point of the circle is recorded.
     * - As the mouse is dragged, the circle is dynamically updated based on the mouse position.
     * - When the mouse is released, the oval is finalized and added to the model.
     * @param paintPanel - the PaintPanel where the circle will be drawn.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        model.deselectShape();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if(mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
                this.circle = new Circle(new Point(mouseEvent.getX(), mouseEvent.getY()), 0);
                this.circle.setThickness(model.getLineThickness());
                this.circle.setFillStyle(model.getFill());
                this.circle.setOutlineColor(model.getOutlineColor());
        } else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) { //US1.002 Complete - Aarav Pradhan
            circle.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            model.addInterimShape(circle);
        } else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            this.circle.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            model.addShape(this.circle);
            System.out.println("Added Circle");
            COMMANDS.add(this);
            this.circle = null;
        }
    }

}
