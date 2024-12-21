package ca.utoronto.utm.assignment2.paint;

/**
 * Square is a Rectangle consisting of four point and four sides in equal length.
 * @author pradha91
 */
public class Square extends Rectangle{
    /**
     * Constructs a Square with specified centre, length and height.
     * @param centre - the top left corner point of the Square.
     * @param length - the side length of the square.
     * @param height - the height of the square.
     */
    public Square(Point centre, double length, double height) {
        super(centre, length, height);
    }

    /**
     * Sets the dimensions of the Square given the length and height based on the
     * x and y coordinates. SetDimensions ensures that the Square length and height
     * are equal by setting both attributes to the largest value of length or height.
     * @param x - the furthest x-coordinate from the centre.
     * @param y - the furthest y-coordinate from the centre.
     */
    public void setDimensions(double x, double y) {
        double size = Math.max(Math.abs(getCentre().x - x), Math.abs(getCentre().y - y));
        setLength(size);
        setHeight(getLength());
        setTopLeftX((x < getCentre().x) ? getCentre().x - size: getCentre().x);
        setTopLeftY((y < getCentre().y) ? getCentre().y - size: getCentre().y);
    }

    /**
     * Allows user to copy the Square instance.
     * @return copy
     */
    @Override
    public ShapeStrategy copy() {
        Square copy = new Square(getCentre(), getHeight(), getLength());
        copy.topLeftX = topLeftX;
        copy.topLeftY = topLeftY;
        copyAttributes(copy);
        return copy;
    }

}
