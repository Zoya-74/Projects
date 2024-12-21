package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.input.MouseEvent;
import javafx.scene.canvas.GraphicsContext;

/**
 * DrawPolylineCommand draws a polyline shape feedback based on user input.
 * The shape is drawn dynamically by handling mouse events such as pressing, dragging,
 * and releasing. The rounded rectangle is dynamically updated as the user moves the mouse, and it is finalized
 * when the mouse is released.
 */
public class DrawPolylineCommand extends DrawCommandStrategy {
    Squiggle polyline;
    double x, y;
    boolean isDrawing;

    /**
     * Executes the command for drawing a polygon.
     * -When the mouse is pressed, the starting point of the polygon is recorded.
     * -As the mouse is moved or dragged, lines are drawn from the last vertex to the current mouse position.
     * -When the mouse is released, the final vertex is recorded. If the mouse is double-clicked,
     * the polygon is added to the model.
     * @param paintPanel the PaintPanel where the polygon will be drawn.
     */
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        model.deselectShape();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            if (!isDrawing) {
                this.x = mouseEvent.getX();
                this.y = mouseEvent.getY();
                this.polyline = new Squiggle(new Point(this.x, this.y));
                this.polyline.setThickness(model.getLineThickness());
                this.polyline.setFillStyle(model.getFill());
                System.out.println("Started Polyline");
                this.isDrawing = true;
            }
        } else if (mouseEventType.equals(MouseEvent.MOUSE_MOVED) || mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) {
            if (isDrawing) {
                GraphicsContext gc = paintPanel.getGraphicsContext2D();
                gc.clearRect(0, 0, paintPanel.getWidth(), paintPanel.getHeight());
                paintPanel.update(null, null);
                model.addInterimShape(this.polyline);

                gc.strokeLine(this.x, this.y, mouseEvent.getX(), mouseEvent.getY());
            }

        }
        else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            this.polyline.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            this.x = mouseEvent.getX();
            this.y = mouseEvent.getY();
            System.out.println("Adding Polyline");

            if (mouseEvent.getClickCount() == 2) {
                model.addShape(this.polyline);
                System.out.println("Added Polyline");
                COMMANDS.add(this);
                this.polyline = null;
                this.isDrawing = false;
            }
        }
    }

}