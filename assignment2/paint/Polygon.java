package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;
import java.util.ArrayList;

/**
 * Polygon is a ShapeStrategy consisting of an arbitrary number of vertices (must be greater than three) in the
 * Paint application.
 * Key functionalities include:
 *  -Adding new points to the Polygon.
 *  -Copying the Polygon shape and its attributes.
 *  -Checking if a point lies within the Polygon's boundaries.
 *  -Repositioning the Polygon by adjusting the centre point.
 *  -Drawing the Polygon on a canvas with customizable outline and fill styles.
 */
public class Polygon extends ShapeStrategy {
    ArrayList<Point> points = new ArrayList<>();
    Point currentPoint;

    /**
     * Constructs Polygon by initializing the first point as centre.
     * @param centre - The first point in each Polygon.
     */
    public Polygon(Point centre) {
        super(centre);
        points.add(getCentre());
        currentPoint = getCentre();
    }

    /**
     * Allows user to copy the Polygon instance.
     * @return copy
     */
    public ShapeStrategy copy(){
        Polygon copy = new Polygon(currentPoint);
        copy.points = points;
        copy.currentPoint = currentPoint;
        copyAttributes(copy);
        return copy;
    }

    /**
     * Checks if the user's mouse is on the Polygon element.
     * @param x - x-coordinate of Mouse Event.
     * @param y - y-coordinate of Mouse Event.
     * @return true or false.
     */
    @Override
    public boolean inBoundary(double x, double y) {
        setMinMax();
        return(minX <= x && x <= maxX && minY <= y && y <= maxY);
    }

    /**
     * Calculates the new position of Polygon by the x and y offset after user
     * moves Polygon.
     * @param x - The offset of x-coordinate
     * @param y - The offset of the y-coordinate
     */
    @Override
    public void reposition(double x, double y) {
        for(Point point : points){
            point.x += x;
            point.y += y;
        }
        setMinMax();
    }

    /**
     * Sets the minimum and maximums of the x and y coordinates of the Polygon.
     */
    public void setMinMax(){
        minX = Math.min(points.get(0).x, points.get(1).x);
        maxX = Math.max(points.get(0).x, points.get(1).x);
        minY = Math.min(points.get(1).y, points.get(2).y);
        maxY = Math.max(points.get(1).y, points.get(2).y);
        for(int i = 1; i<points.size() - 1; i++){
            minX = Math.min(minX, points.get(i).x);
            maxX = Math.max(maxX, points.get(i).x);
            minY = Math.min(minY, points.get(i).y);
            maxY = Math.max(maxY, points.get(i).y);
        }
    }

    /**
     * Adds new points to the Polygon points array.
     */
    public void setDimensions(double x, double y) {
        this.currentPoint = new Point(x, y);
        points.add(this.currentPoint);
    }

    /**
     * Draws the Polygon on the given GraphicsContext g, allowing for customizable outline and fill styles.
     * @param g - the GraphicContext to draw the Polygon.
     */
    @Override
    public void drawShape(GraphicsContext g) {
        g.setFill(this.getColor());
        double upperx = this.getCentre().x + 5;
        double uppery = this.getCentre().y + 5;
        double lowx = this.getCentre().x - 5;
        double lowy = this.getCentre().y - 5;

        double [] x = new double[points.size()];
        double [] y = new double[points.size()];
        for (int i = 0; i < points.size(); i++) {
            x[i] = points.get(i).x;
            y[i] = points.get(i).y;
        }
        if (lowx <= currentPoint.x && lowy <= currentPoint.y && upperx >= currentPoint.x && uppery >= currentPoint.y
                && points.size() > 2) {

            if(this.getFillStyle().equals("both")){
                g.setLineWidth(getThickness());
            }
            if(this.getFillStyle().equals("outline") || this.getFillStyle().equals("both")){
                g.setStroke(this.getOutlineColor());
                g.setLineWidth(getThickness());
                g.strokePolygon(x,y,points.size());
            }
            if (this.getFillStyle().equals("solid") || this.getFillStyle().equals("both")) {
                g.fillPolygon(x,y,points.size());
            }
        }
        else {
            g.setStroke(this.getOutlineColor());
            g.setLineWidth(getThickness());
            g.strokePolyline(x,y,points.size());
        }
    }
}
