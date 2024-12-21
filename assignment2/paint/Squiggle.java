package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;
import java.util.ArrayList;

/**
 * Squiggle is a freeform, continuous line ShapeStrategy that consists of a series of points.
 * Squiggle extends the ShapeStrategy class, allowing the user to draw squiggly lines on the canvas.
 * Key functionalities include:
 *  -Adding new points to the Squiggle line.
 *  -Copying the Squiggle shape and its attributes.
 *  -Checking if a point lies within the Squiggle's boundaries.
 *  -Repositioning the Squiggle by adjusting the centre point.
 *  -Drawing the Squiggle on a canvas with customizable outline and fill styles.
 *
 * @author
 */
public class Squiggle extends ShapeStrategy {
    ArrayList<Point> points = new ArrayList<>();

    /**
     * Constructs Squiggle by initializing the first point as centre.
     * @param centre - The first point in each Squiggle.
     */
    public Squiggle(Point centre) {
        super(centre);
        points.add(getCentre());
        minX = points.get(0).x;
        minY = points.get(0).y;
        maxX = points.get(0).x;
        maxY = points.get(0).y;
    }

    /**
     * Allows user to copy the Squiggle instance.
     * @return copy
     */
    @Override
    public ShapeStrategy copy() {
        Squiggle copy = new Squiggle(points.getFirst());
        copy.points = points;
        copyAttributes(copy);
        return copy;
    }

    /**
     * Checks if the user's mouse is on the Squiggle element.
     * @param x - x-coordinate of Mouse Event.
     * @param y - y-coordinate of Mouse Event.
     * @return true or false.
     */
    @Override
    public boolean inBoundary(double x, double y) {
            for (Point point : points) {
                if (x <= point.x + 15 && x >= point.x - 15 && y <= point.y + 15 && y >= point.y - 15) {
                    return true;
                }
            }

            return false;
    }

    /**
     * Calculates the new position of Squiggle by the x and y offset after user
     * moves Squiggle.
     * @param x - The offset of x-coordinate
     * @param y - The offset of the y-coordinate
     */
    @Override
    public void reposition(double x, double y) {
        for(Point p : points) {
            p.x += x;
            p.y += y;
        }
        setMinMax();
    }

    /**
     * Sets the minimum and maximums of the x and y coordinates of the Squiggle.
     */
    public void setMinMax(){
        minX = points.get(0).x;
        minY = points.get(0).y;
        maxX = points.get(0).x;
        maxY = points.get(0).y;
        for(Point p : points) {
            minX = Math.min(p.x, minX);
            minY = Math.min(p.y, minY);
            maxX = Math.max(p.x, maxX);
            maxY = Math.max(p.y, maxY);
        }
    }

    /**
     * Adds new points to the Squiggle points array.
     */
    public void setDimensions(double x, double y) {
            if(!points.isEmpty()){
                minX = Math.min(x, minX);
                maxX = Math.max(x, maxX);
                minY = Math.min(y, minY);
                maxY = Math.max(y, maxY);
            }
            points.add(new Point(x, y));
    }
        /**
        * Draws the Squiggle on the given GraphicsContext g, allowing for customizable outline and fill styles.
        * @param g - the GraphicContext to draw the Squiggle.
        */
        @Override
        public void drawShape(GraphicsContext g) {
            g.setStroke(this.getColor());
            g.setLineWidth(getThickness());
            for (int i = 0; i < points.size() - 1; i++) {
                Point p1 = points.get(i);
                Point p2 = points.get(i + 1);
                g.strokeLine(p1.x, p1.y, p2.x, p2.y);

            }

        }
    }
