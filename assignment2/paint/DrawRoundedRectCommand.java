package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;

/**
 * DrawRoundedRectCommand draws a rounded rectangle shape feedback based on user input.
 * The shape is drawn dynamically by handling mouse events such as pressing, dragging,
 * and releasing. The rounded rectangle is dynamically updated as the user moves the mouse, and it is finalized
 * when the mouse is released.
 */
public class DrawRoundedRectCommand extends DrawCommandStrategy {
    Rectangle rect;

    /**
     * Executes the command by handling various mouse events to draw a rounded rectangle.
     * -When the mouse is pressed, the top-left corner of the rectangle is recorded.
     * -As the mouse is dragged, the rectangle's dimensions are dynamically updated.
     * -When the mouse is released, the rounded rectangle is finalized and added to the model.
     * @param paintPanel - the PaintPanel where the rounded rectangle will be drawn.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        model.deselectShape();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            this.rect = new RoundedRectangle(new Point(mouseEvent.getX(), mouseEvent.getY()), 0, 0);
            this.rect.setThickness(model.getLineThickness());
            this.rect.setFillStyle(model.getFill());
            this.rect.setOutlineColor(model.getOutlineColor());
            System.out.println("Started Rounded Rectangle");
        } else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) { //US1.002 Complete - Aarav Pradhan
            this.rect.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            model.addInterimShape(rect);
            System.out.println("Adding Rounded Rectangle");
        } else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            this.rect.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            this.rect.setCentre(new Point(this.rect.getTopLeftX(), this.rect.getTopLeftY()));
            model.addShape(this.rect);
            System.out.println("Added Rounded Rectangle");
            COMMANDS.add(this);
            this.rect = null;
        }
    }
    
}
