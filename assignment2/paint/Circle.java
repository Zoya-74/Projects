package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;

/**
 * Circle is a ShapeStrategy consisting of a centre point and a radius.
 * Key functionalities include:
 * -Setting the Circle's centre point.
 * -Copying the Circle's shape and its attributes.
 * -Drawing the Circle on a canvas with customizable outline and fill styles.
 * @author baseetfa
 */
public class Circle extends Oval{
    /**
     * Constructs a Circle with the specified center and radius.
     * @param centre - the centre point of the circle
     * @param radius - the radius of the circle
     */
    public Circle(Point centre, double radius) {super(centre, radius, radius);}

    /**
     * Sets the dimensions of the Circle given the radius based on the
     * x and y coordinates.
     * @param x - the furthest x-coordinate from the centre.
     * @param y - the furthest y-coordinate from the centre.
     */
    public void setDimensions(double x, double y) {
        setWidth(Math.max(Math.abs(getCentre().x - x),Math.abs(getCentre().y - y)));
        setHeight(getWidth());
        setTopLeftX(getCentre().x);
        setTopLeftY(getCentre().y);
    }

    /**
     * Allows user to copy the Circle instance.
     * @return copy
     */
    @Override
    public ShapeStrategy copy() {
        Circle copy = new Circle(getCentre(), getWidth());
        copy.setTopLeftX(this.getTopLeftX());
        copy.setTopLeftY(this.getTopLeftY());
        copyAttributes(copy);
        return copy;
    }

    /**
     * Sets the minimum and maximums of the x and y coordinates of the Circle.
     */
    public void setMaxMin(){
        double radius = getWidth() / 2;
        minX = getCentre().x - radius;
        minY = getCentre().y - radius;
        maxX = getCentre().x + radius;
        maxY = getCentre().y + radius;
    }

    /**
     * Draws the Circle on the given GraphicsContext g, allowing for customizable outline and fill styles.
     * @param g - the GraphicContext to draw the Circle.
     */
    @Override
    public void drawShape(GraphicsContext g) {

        double x = getCentre().x;
        double y = getCentre().y;

        if(this.getFillStyle().equals("both")){
            g.setLineWidth(getThickness());
        }

        if(this.getFillStyle().equals("outline") || this.getFillStyle().equals("both")) {
            g.setStroke(this.getOutlineColor());
            g.setLineWidth(getThickness());
            g.strokeOval(getTopLeftX()-(getWidth()/2), getTopLeftY()-(getHeight()/2), getWidth(), getHeight());
        }
        if(this.getFillStyle().equals("solid")|| this.getFillStyle().equals("both")) {
            g.setFill(this.getColor());
            g.fillOval(getTopLeftX()-(getWidth()/2), getTopLeftY()-(getHeight()/2), getWidth(), getHeight());
        }
    }

}
