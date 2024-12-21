package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;

/**
 * DrawOvalCommand draws oval shape feedback based on user input.
 * The oval is drawn interactively by clicking and dragging the mouse. The user clicks to start the oval,
 * and as the mouse is dragged, the oval shape is updated. When the mouse is released, the oval is finalized and added
 * to the model.
 */
public class DrawOvalCommand extends DrawCommandStrategy {
    Oval oval;

    /**
     * Executes the command for drawing an oval.
     * - When the mouse is pressed, the starting point of the oval is recorded.
     * - As the mouse is dragged, the oval is dynamically updated based on the mouse position.
     * - When the mouse is released, the oval is finalized and added to the model.
     * @param paintPanel - the PaintPanel where the oval will be drawn.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        model.deselectShape();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if(mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            this.oval = new Oval(new Point(mouseEvent.getX(), mouseEvent.getY()), 0, 0);
            this.oval.setThickness(model.getLineThickness());
            this.oval.setFillStyle(model.getFill());
            this.oval.setOutlineColor(model.getOutlineColor());
            System.out.println("Starting Oval");

        } else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) { //US1.002 Complete - Aarav Pradhan
            this.oval.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            model.addInterimShape(oval);
            System.out.println("Adding Oval");
        } else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            this.oval.setFinished();
            this.oval.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            this.oval.setCentre(new Point(this.oval.getTopLeftX(), this.oval.getTopLeftY()));
            model.addShape(this.oval);
            System.out.println("Added Oval");
            COMMANDS.add(this);
            this.oval = null;
        }
    }

}
