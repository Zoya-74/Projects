package ca.utoronto.utm.assignment2.paint;


import javafx.scene.canvas.GraphicsContext;
import javafx.scene.text.Font;

/**
 * Text is a text element consisting of characters on the keyboard.
 * Text extends ShapeStrategy and allows text to be positioned, drawn,
 * and manipulated like other shapes on the canvas.
 * Key functionalities include:
 *  -Copying the Text shape and its attributes.
 *  -Checking if a point lies within the text's boundaries.
 *  -Repositioning the Text by adjusting the centre point.
 *  -Drawing the text on a canvas.
 */
public class Text extends ShapeStrategy {
    public String text ="";

    /**
     * Constructs a Text with the given text input.
     * @param centre - centre point of the Text on the canvas.
     * @param text - the string to be displayed as Text.
     */
    public Text(Point centre, String text) {
        super(centre);
        setMinMax();
        this.text=text;
    }

    /**
     * Allows user to copy the Text instance.
     * @return copy
     */
    @Override
    public ShapeStrategy copy() {
        Text copy = new Text(getCentre(), text);
        copyAttributes(copy);
        return copy;
    }

    /**
     * Checks if the user's mouse is on the Text element.
     * @param x - x-coordinate of Mouse Event.
     * @param y - y-coordinate of Mouse Event.
     * @return true or false.
     */
    @Override
    public boolean inBoundary(double x, double y) {
        setMinMax();
        return(minX<= x && x <= maxX  && y >= minY && y <= maxY);
    }

    /**
     * Calculates the new position of Text by the x and y offset after user
     * moves Text.
     * @param x - The offset of x-coordinate
     * @param y - The offset of the y-coordinate
     */
    @Override
    public void reposition(double x, double y) {
        setMinMax();
        setCentre(new Point(getCentre().x + x, getCentre().y + y));
        setMinMax();
    }

    /**
     * Sets the minimum and maximums of the x and y coordinates of the Text.
     */
    public void setMinMax(){
        minX = getCentre().x;
        minY = getCentre().y - 20;
        maxX = getCentre().x + text.length() * 10;
        maxY = getCentre().y + 5;
    }

    /**
     * Draws the Text on the given GraphicsContext g.
     * @param g - the GraphicContext to draw the Text.
     */
    @Override
    public void drawShape(GraphicsContext g) {
        g.setFont(new Font("Arial", 20));
        g.setFill(this.getColor());
        g.fillText(this.text, getCentre().x, getCentre().y);
    }
}
