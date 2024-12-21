package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventType;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.MouseEvent;

import java.util.ArrayList;

/**
 * DrawTriangleCommand draws the triangle shape feedback based on user input.
 * This command allows the triangle to be dynamically drawn by handling mouse events, which include pressing, dragging,
 * and releasing the mouse. The user can specify three points to form the triangle, and the shape will be drawn on the
 * PaintPanel.
 */
public class DrawTriangleCommand extends DrawCommandStrategy {
    Triangle triangle;
    ArrayList<Point> trianglePoints = new ArrayList<>();

    /**
     * Executes the command by handling various mouse events to draw a triangle.
     * -When the mouse is pressed, the mouse is pressed, the first point of the triangle is recorded.
     * -As the mouse is dragged, interim lines are drawn to represent two sides of the triangle.
     * -When the mouse releases, the third point is finalized, and the triangle is added to the model.
     * @param paintPanel the {@link PaintPanel} where the triangle will be drawn.
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        EventType<MouseEvent> mouseEventType = (EventType<MouseEvent>) mouseEvent.getEventType();
        if (mouseEventType.equals(MouseEvent.MOUSE_PRESSED)) {
            if (trianglePoints.size() < 1) {
                System.out.println("Started Triangle");
                Point pointA = new Point(mouseEvent.getX(), mouseEvent.getY());
                this.triangle = new Triangle(pointA, new Point(0, 0), new Point(0, 0));
                this.triangle.setThickness(model.getLineThickness());
                this.triangle.setFillStyle(model.getFill());
                this.triangle.setOutlineColor(model.getOutlineColor());
                trianglePoints.add(pointA);
            }

        } else if (mouseEventType.equals(MouseEvent.MOUSE_DRAGGED)) { //Added US2.018 -Zoya Fatima
            //Get current mouse positions,
            double mouseX = mouseEvent.getX();
            double mouseY = mouseEvent.getY();
            GraphicsContext gc = paintPanel.getGraphicsContext2D();
            gc.clearRect(0, 0, paintPanel.getWidth(), paintPanel.getHeight());
            paintPanel.update(null, null);
            if (trianglePoints.size() == 1) {
                Point pointB = new Point(mouseX, mouseY);
                gc.setLineWidth(model.getLineThickness());
                model.deselectShape();
                gc.strokeLine(trianglePoints.get(0).x, trianglePoints.get(0).y, pointB.x, pointB.y);
                System.out.println("added my line");
            } else if (trianglePoints.size() == 2) {
                Point pointC = new Point(mouseX, mouseY);
                gc.strokeLine(trianglePoints.get(0).x, trianglePoints.get(0).y, trianglePoints.get(1).x,
                        trianglePoints.get(1).y);
                gc.strokeLine(trianglePoints.get(1).x, trianglePoints.get(1).y, pointC.x, pointC.y);
                gc.strokeLine(pointC.x, pointC.y, trianglePoints.get(0).x, trianglePoints.get(0).y);
                this.triangle.setPointA(trianglePoints.get(0));
                this.triangle.setPointB(trianglePoints.get(1));
                this.triangle.setPointC(pointC);
                model.addInterimShape(this.triangle);
                System.out.println("Adding Triangle");
            }
        } else if (mouseEventType.equals(MouseEvent.MOUSE_RELEASED)) {
            GraphicsContext gc = paintPanel.getGraphicsContext2D();
            double mouseX = mouseEvent.getX();
            double mouseY = mouseEvent.getY();
            if(trianglePoints.size() == 2) {
                Point pointC = new Point(mouseX, mouseY);
                trianglePoints.add(pointC);
                this.triangle.setPointA(trianglePoints.get(0));
                this.triangle.setPointB(trianglePoints.get(1));
                this.triangle.setPointC(trianglePoints.get(2));
                model.addShape(this.triangle);
                // Progress of triangle is shown to user
                System.out.println("Added Triangle");
                COMMANDS.add(this);
                this.triangle = null;
                trianglePoints.clear();

            }

            else if (trianglePoints.size() == 1) {
                Point pointB = new Point(mouseX, mouseY);
                trianglePoints.add(pointB);
                gc.strokeLine(trianglePoints.get(0).x, trianglePoints.get(0).y, pointB.x, pointB.y);
            }
        }

    }

}
