package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;

/**
 * Triangle is a ShapeStrategy that is defined by three points connecting to one another.
 * Key functionalities include:
 *  -Setting and getting the triangle's vertices (points A, B, and C).
 *  -Copying the triangle shape and its attributes.
 *  -Checking if a point lies within the triangle's boundaries.
 *  -Repositioning the triangle by adjusting all three vertices.
 *  -Drawing the triangle on a canvas with customizable outline and fill styles.
 *
 * @author fatim185
 */
public class Triangle extends ShapeStrategy {
    private Point pointB, pointC;

    /**
     * Constructs a Triangle by three points.
     * @param pointA - the first point the user creates (the centre point).
     * @param pointB - the second point the user creates for the triangle.
     * @param pointC - the last point the user creates for the triangle that completes the triangle.
     */
    public Triangle(Point pointA, Point pointB, Point pointC) {
        super(pointA);
        this.pointB = pointB;
        this.pointC = pointC;
    }

    /**
     * Gets the first point of the Triangle.
     * @return Centre
     */
    public Point getPointA(){return getCentre();} //changed triangle class

    /**
     * Gets the second point of the Triangle.
     * @return pointB
     */
    public Point getPointB(){return pointB;}

    /**
     * Gets the third point of the Triangle.
     * @return pointC
     */
    public Point getPointC(){return pointC;}

    /**
     * Sets the first point of the Triangle with the given input.
     */
    public void setPointA(Point pointA){this.setCentre(pointA);}

    /**
     * Sets the second point of the Triangle with the given input.
     */
    public void setPointB(Point pointB){this.pointB = pointB;}

    /**
     * Sets the third point of the Triangle with the given input.
     */
    public void setPointC(Point pointC){this.pointC = pointC;}

    /**
     * Allows user to copy the Triangle instance.
     * @return copy
     */
    @Override
    public ShapeStrategy copy() {
        Triangle copy = new Triangle(getCentre(), pointB, pointC);
        copyAttributes(copy);
        return copy;
    }

    /**
     * Checks if the user's mouse is on the Triangle shape.
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
     * Calculates the new position of Triangle by the x and y offset after user
     * moves triangle.
     * @param x - The offset of x-coordinate
     * @param y - The offset of the y-coordinate
     */
    @Override
    public void reposition(double x, double y) {
        setPointA(new Point(getPointA().x + x, getPointA().y + y));
        setPointB(new Point(getPointB().x + x, getPointB().y+ y));
        setPointC(new Point(getPointC().x + x, getPointC().y + y));
        setMinMax();
    }

    /**
     * Sets the minimum and maximums of the x and y coordinates of the Triangle.
     */
    public void setMinMax() {
        double temp = Math.min(getPointA().x, getPointB().x);
        minX = Math.min(temp, getPointC().x);
        temp = Math.min(getPointA().y, getPointB().y);
        minY = Math.min(temp, getPointC().y);
        temp = Math.max(getPointA().x, getPointB().x);
        maxX = Math.max(temp, getPointC().x);
        temp = Math.max(getPointA().y, getPointB().y);
        maxY = Math.max(temp, getPointC().y);
    }

    /**
     * Draws the Triangle on the given GraphicsContext g, allowing for customizable outline and fill styles.
     * @param g - the GraphicContext to draw the Triangle.
     */
    @Override
    public void drawShape(GraphicsContext g) {
        g.setFill(this.getColor());
            double [] x = {getCentre().x, getPointB().x, getPointC().x};
            double [] y = {getCentre().y, getPointB().y, getPointC().y};

            if(this.getFillStyle().equals("both")){
                g.setLineWidth(getThickness());
            }

            if(this.getFillStyle().equals("outline") || this.getFillStyle().equals("both")){
                g.setStroke(this.getOutlineColor());
                g.setLineWidth(getThickness());
                g.strokePolygon(x, y, 3);
            }
            if (this.getFillStyle().equals("solid") || this.getFillStyle().equals("both")){
                g.fillPolygon(x, y, 3);
            }
        }
    }
