package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.MouseEvent;

/**
 * DrawPolygonCommand draws a polygon shape feedback based on user input.
 * A polygon is a shape with an arbitrary number of sides, and the user can click to add vertices to it.
 * The drawing is finalized when the user double-clicks the mouse.
 */
public class DrawPolygonCommand extends DrawCommandStrategy {
    Polygon polygon;
    double x, y;
    boolean isDrawing;
    Point startingPoint;

    /**
     * Executes the command for drawing a polygon.
     * -When the mouse is pressed, the starting point of the polygon is recorded.
     * -As the mouse is moved or dragged, lines are drawn from the last vertex to the current mouse position.
     * -When the mouse is released, the final vertex is recorded. If the mouse is double-clicked,
     * the polygon is added to the model.
     * @param paintPanel - the PaintPanel where the polygon will be drawn.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        GraphicsContext gc = paintPanel.getGraphicsContext2D();
        gc.setStroke(model.getOutlineColor());
        model.deselectShape();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            if (!isDrawing) {
                this.x = mouseEvent.getX();
                this.y = mouseEvent.getY();
                this.startingPoint = new Point(this.x, this.y);
                this.polygon = new Polygon(this.startingPoint);
                this.polygon.setThickness(model.getLineThickness());
                this.polygon.setFillStyle(model.getFill());
                this.polygon.setOutlineColor(model.getOutlineColor());
                System.out.println("Started Polygon");
                this.isDrawing = true;
            }
        } else if (mouseEventType.equals(MouseEvent.MOUSE_MOVED) || mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) {
            if (isDrawing) {
                gc.clearRect(0, 0, paintPanel.getWidth(), paintPanel.getHeight());
                paintPanel.update(null, null);
                model.addInterimShape(this.polygon);
                gc.setStroke(model.getOutlineColor());
                gc.fillOval(this.startingPoint.x-(5), this.startingPoint.y-(5), 10, 10);
                gc.strokeLine(this.x, this.y, mouseEvent.getX(), mouseEvent.getY());

            }
        }
        else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            this.polygon.setDimensions(mouseEvent.getX(), mouseEvent.getY());
            this.x = mouseEvent.getX();
            this.y = mouseEvent.getY();
            System.out.println("Adding Polygon");

            if (mouseEvent.getClickCount() == 2) {
                model.addShape(this.polygon);
                System.out.println("Added Polygon");
                COMMANDS.add(this);
                this.polygon = null;
                this.isDrawing = false;
            }
        }
    }

}


