package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;

/**
 * DrawSquiggleCommand draws a squiggle shape feedback based on user input.
 * The squiggle is drawn dynamically by handling mouse events such as pressing, dragging, and releasing. The shape is
 * continuously updated as the user moves the mouse and is finalized when the mouse is released.
 */
public class DrawSquiggleCommand extends DrawCommandStrategy {
    Squiggle squiggle;

    /**
     * Executes the command by handling various mouse events to draw a squiggle.
     * -When the mouse is pressed, the starting point of the squiggle is recorded.
     * -As the mouse is dragged, the squiggle is dynamically drawn and updated.
     * -When the mouse is released, the squiggle is finalized and added to the model.
     * @param paintPanel - the PaintPanel where the squiggle will be drawn.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        model.deselectShape();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            this.squiggle = new Squiggle(new Point(mouseEvent.getX(), mouseEvent.getY()));
            this.squiggle.setThickness(model.getLineThickness());
            this.squiggle.setFillStyle("outline");
            System.out.println("Started Squiggle");
        } else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) {
            this.squiggle.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            model.addInterimShape(squiggle);
            System.out.println("Adding Squiggle");
        } else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            this.squiggle.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            model.addShape(this.squiggle);
            System.out.println("Added Squiggle");
            COMMANDS.add(this);
            this.squiggle = null;
        }
    }
    
}
