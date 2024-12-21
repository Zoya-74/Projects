package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;

/**
 * Rectangle is a ShapeStrategy consisting of four point and four sides, where the edges are pointed.
 * Key functionalities include:
 * -Setting and getting the Rectangle's centre point, length and height.
 * -Copying the Rectangle shape and its attributes.
 * -Checking if a point lies within the Rectangle's boundaries.
 * -Repositioning the Rectangle by adjusting the centre point.
 * -Drawing the Rectangle on a canvas with customizable outline and fill styles.
 * @author baseetfa
 */
public class Rectangle extends ShapeStrategy {
    private double length;
    private double height;
    protected double topLeftX;
    protected double topLeftY;

    /**
     * Constructs a Rectangle with the specified center, length, and height.
     * @param centre - the top left point of the rectangle
     * @param length - the length of the rectangle
     * @param height - height of the rectangle
     */
    public Rectangle(Point centre, double length, double height) {
        super(centre);
        this.length = length;
        this.height = height;
        this.topLeftX = centre.x;
        this.topLeftY = centre.y;
    }

    /**
     * Gets for topLeftX of the Rectangle.
     * @return topLeftX
     */
    public double getTopLeftX(){return topLeftX;}

    /**
     * Gets for topLeftY of the Rectangle.
     * @return topLeftY
     */
    public double getTopLeftY(){return topLeftY;}

    /**
     * Sets for topLeftX with the given input.
     * @param topLeftX - x-coordinate of the centre
     */
    public void setTopLeftX(double topLeftX){this.topLeftX = topLeftX;}

    /**
     * Sets for topLeftY with the given input.
     * @param topLeftY - y-coordinate of the centre
     */
    public void setTopLeftY(double topLeftY){this.topLeftY = topLeftY;}

    /**
     * Sets the dimensions of the Rectangle given the length and height based on the
     * x and y coordinates.
     * @param x - the furthest x-coordinate from the centre.
     * @param y - the furthest y-coordinate from the centre.
     */
    public void setDimensions(double x, double y) {
            setLength(Math.abs(getCentre().x - x));
            setHeight(Math.abs(getCentre().y - y));
            this.topLeftX = Math.min(x, getCentre().x);
            this.topLeftY = Math.min(y, getCentre().y);
    }

    /**
     * Allows user to copy the Rectangle instance.
     * @return copy
     */
    @Override
    public ShapeStrategy copy() {
        Rectangle copy = new Rectangle(getCentre(), getLength(), getHeight());
        copy.topLeftY = this.topLeftY;
        copy.topLeftX = this.topLeftX;
        copyAttributes(copy);
        return copy;
    }

    /**
     * Checks if the user's mouse is on the Rectangle shape.
     * @param x - x-coordinate of Mouse Event.
     * @param y - y-coordinate of Mouse Event.
     * @return true or false.
     */
    @Override
    public boolean inBoundary(double x, double y) {
        setMaxMin();
        return(minX <= x && x <= maxX && minY <= y && y <= maxY);
    }

    /**
     * Calculates the new position of Rectangle by the x and y offset after user
     * moves Rectangle.
     * @param x - The offset of x-coordinate
     * @param y - The offset of the y-coordinate
     */
    @Override
    public void reposition(double x, double y) {
        this.setCentre(new Point(getCentre().x + x, getCentre().y + y));
        topLeftX = getCentre().x + x;
        topLeftY = getCentre().y + y;
        setMaxMin();
    }

    /**
     * Sets the minimum and maximums of the x and y coordinates of the Rectangle.
     */
    public void setMaxMin(){
        minX = getCentre().x;
        minY = getCentre().y;
        maxX = getCentre().x + getLength();
        maxY = getCentre().y + getHeight();
    }

    /**
     * Draws the Rectangle on the given GraphicsContext g, allowing for customizable outline and fill styles.
     * @param g - the GraphicContext to draw the Rectangle.
     */
    @Override
    public void drawShape(GraphicsContext g) {
        double lengthUse;
        double heightUse;

        g.setFill(this.getColor());
        lengthUse = Math.abs(getLength());
        heightUse = Math.abs(getHeight());

        if (this.getFillStyle().equals("both")){
            g.setLineWidth(getThickness());
        }
        if (this.getFillStyle().equals("outline") || this.getFillStyle().equals("both")){
            g.setStroke(this.getOutlineColor());
            g.setLineWidth(getThickness());
            g.strokeRect(topLeftX, topLeftY, lengthUse, heightUse);
        }

        if (this.getFillStyle().equals("solid") || this.getFillStyle().equals("both")) {
            g.fillRect(topLeftX, topLeftY, lengthUse, heightUse);
        }
    }

    /**
     * Gets the length of the Rectangle.
     * @return length
     */
    public double getLength() {return this.length;}

    /**
     * Sets the length with the given input.
     * @param length - the length of Rectangle.
     */
    public void setLength(double length) {this.length = length;}

    /**
     * Gets the height of the Rectangle.
     * @return height
     */
    public double getHeight() {return this.height;}

    /**
     * Sets the height with the given input
     * @param height - the height of Rectangle.
     */
    public void setHeight(double height) {this.height = height;}

}
