package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

/**
 * Oval is a ShapeStrategy consisting of width, height and curved edges.
 * Key functionalities include:
 * -Setting and getting the Oval's centre point, length and height.
 * -Copying the Oval shape and its attributes.
 * -Checking if a point lies within the Oval's boundaries.
 * -Repositioning the Oval by adjusting the centre point.
 * -Drawing the Oval on a canvas with customizable outline and fill styles.
 * @author
 */
public class Oval extends ShapeStrategy {
    private double width;
    private double height;
    private boolean isFinished=false;
    private double topLeftX;
    private double topLeftY;

    /**
     * Constructs an Oval with the specified center, length, and height.
     * @param centre - the top left point of the Oval.
     * @param width - the length of the Oval.
     * @param height - height of the Oval.
     */
    public Oval(Point centre, double width, double height) {
        super(centre);
        this.height = height;
        this.width = width;
        this.topLeftX = centre.x;
        this.topLeftY = centre.y;
    }

    /**
     * Gets for topLeftX of the Oval.
     * @return topLeftX
     */
    public double getTopLeftX(){return topLeftX;}

    /**
     * Gets for topLeftY of the Oval.
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
     * Sets the dimensions of the Oval given the length and height based on the
     * x and y coordinates.
     * @param x - the furthest x-coordinate from the centre.
     * @param y - the furthest y-coordinate from the centre.
     */
    public void setDimensions(double x, double y) {
        setWidth(Math.abs(getCentre().x - x));
        setHeight(Math.abs(getCentre().y - y));
        topLeftX = Math.min(getCentre().x, x);
        topLeftY = Math.min(getCentre().y, y);
    }

    /**
     * Allows user to copy the Oval instance.
     * @return copy
     */
    @Override
    public ShapeStrategy copy() {
        Oval copy = new Oval(getCentre(), width, height);
        copy.isFinished=isFinished;
        copy.topLeftX = topLeftX;
        copy.topLeftY = topLeftY;
        copyAttributes(copy);
        return copy;
    }

    /**
     * Checks if the user's mouse is on the Oval shape.
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
     * Calculates the new position of Oval by the x and y offset after user
     * moves Oval.
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
     * Sets the minimum and maximums of the x and y coordinates of the Oval.
     */
    public void setMaxMin(){
        minX = getCentre().x;
        minY = getCentre().y;
        maxX = getCentre().x + getWidth();
        maxY = getCentre().y + getHeight();
    }

    /**
     * Draws the Oval on the given GraphicsContext g, allowing for customizable outline and fill styles.
     * @param g - the GraphicContext to draw the Oval.
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
            g.strokeOval(topLeftX,topLeftY,width,height);
        }
        if(this.getFillStyle().equals("solid")|| this.getFillStyle().equals("both")) {
            g.setFill(this.getColor());
            g.fillOval(topLeftX, topLeftY, width, height);
        }

        if (!isFinished){
            g.setStroke(Color.BLACK);
            g.strokeRect(topLeftX, topLeftY, width, height);
        }

    }

    /**
     * Gets the height of the Oval.
     * @return height
     */
    public double getHeight() {return this.height;}

    /**
     * Sets the height with the given input.
     * @param height - the height of Oval.
     */
    public void setHeight(double height) {this.height = height;}

    /**
     * Gets the width of the Oval.
     * @return width
     */
    public double getWidth() {
        return width;
    }

    /**
     * Sets width with the given input.
     * @param width - the width of Oval
     */
    public void setWidth(double width) {
        this.width = width;
    }

    /**
     * Sets isFinished to true when the Oval is finished drawing.
     */
    public void setFinished() {this.isFinished=true;}

}

