package ca.utoronto.utm.assignment2.paint;

import java.io.Serializable;

/**
 * Point represents a point in a 2D space with x and y coordinates.
 */
public class Point implements Serializable {
        double x, y;

        /**
         * Constructs a Point with the specified x and y coordinates.
         * @param x - the x-coordinate of the point.
         * @param y - the y-coordinate of the point.
         */
        Point(double x, double y){
                this.x=x; this.y=y;
        }
}
