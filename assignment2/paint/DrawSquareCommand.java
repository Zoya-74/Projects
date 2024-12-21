package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;

/**
 * DrawSquareCommand draws a square shape feedback based on user input.
 * The square is drawn dynamically by handling mouse events such as pressing, dragging, and releasing. The shape is
 * continuously updated as the user moves the mouse and is finalized when the mouse is released.
 */
public class DrawSquareCommand extends DrawCommandStrategy {
    Rectangle square;

    /**
     * Executes the command by handling various mouse events to draw a square.
     * -When the mouse is pressed, the top-left corner of the square is recorded.
     * -As the mouse is dragged, the square's dimensions are dynamically updated.
     * -When the mouse is released, the square is finalized and added to the model.
     * @param paintPanel - the PaintPanel where the square will be drawn.
     */

    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        model.deselectShape();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            this.square = new Square(new Point(mouseEvent.getX(), mouseEvent.getY()), 0, 0);
            this.square.setThickness(model.getLineThickness());
            this.square.setFillStyle(model.getFill());
            this.square.setOutlineColor(model.getOutlineColor());
            System.out.println("Started Square");
        } else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) { //US1.002 Complete - Aarav Pradhan
            this.square.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            model.addInterimShape(square);
            System.out.println("Adding Square");
        } else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            this.square.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            this.square.setCentre(new Point(this.square.getTopLeftX(), this.square.getTopLeftY()));
            model.addShape(this.square);
            System.out.println("Added Square");
            COMMANDS.add(this);
            this.square = null;
        }
    }
    
}
