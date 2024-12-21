package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import java.io.Serializable;

/**
 * ShapeStrategy defines common properties and methods for various shapes in a Paint application.
 * Each shape is characterized by a central point, thickness, fill style, and colors.
 * This class implements Serializable to allow objects to be saved and loaded,
 * and supports copying attributes to facilitate undo/redo functionality.
 * @author pradha91
 */
public abstract class ShapeStrategy implements Serializable{
    private static Color defaultColor = Color.BLACK;
    private Point centre;
    private double thickness;
    private String fillStyle;
    private transient Color color;//US4.015 added transient
    private transient Color outlineColor = Color.BLACK;
    protected double minX, minY, maxX, maxY;

    /**
     * Constructs a ShapeStrategy given the centre and sets ShapeStrategy to defaultColor.
     * @param centre
     */
    public ShapeStrategy(Point centre) {
        this.centre = centre;
        this.color = defaultColor;
    }
    /**
     * Allows user to copy the ShapeStrategy.
     */
    public abstract ShapeStrategy copy();

    /**
     * Copy attributes of another ShapeStrategy instance.
     * @param other - Another ShapeStrategy instance.
     */
    public void copyAttributes(ShapeStrategy other){
        other.minX = minX;
        other.minY = minY;
        other.maxX = maxX;
        other.maxY = maxY;
        other.setThickness(getThickness());
        other.setFillStyle(getFillStyle());
        other.setColor(getColor());
        other.setOutlineColor(getOutlineColor());
    }

    /**
     * Gets the centre point.
     * @return centre
     */
    public Point getCentre(){return centre;}

    /**
     * Sets the centre point with the given input.
     * @param centreInput - new centre point.
     */
    public void setCentre(Point centreInput){centre = centreInput;}

    /**
     * Sets the stroke thickness size with the given input.
     * @param thicknessInput - new thickness size.
     */
    public void setThickness(double thicknessInput){thickness = thicknessInput;}

    /**
     * Gets the stroke thickness of the ShapeStrategy.
     * @return thickness
     */
    public double getThickness(){return thickness;}

    /**
     * Sets the fillStyle option with the given input.
     * @param fillStyleInput - current fillStyle option (Fill, Outline or Both).
     */
    public void setFillStyle(String fillStyleInput){fillStyle = fillStyleInput;}

    /**
     * Gets the fillStyle option of the ShapeStrategy.
     * @return fillStyle
     */
    public String getFillStyle(){return fillStyle;}

    /**
     * Sets the color with the given input.
     * @param colorInput - the color selected for the ShapeStrategy.
     */
    public void setColor(Color colorInput){color = colorInput;}

    /**
     * Gets the color of the ShapeStrategy.
     * @return color
     */
    public Color getColor(){return color;}

    /**
     * Sets the defaultColor with the given input.
     * @param defaultColourInput - the default color of the ShapeStrategy.
     */
    public static void setDefaultColour(Color defaultColourInput){defaultColor = defaultColourInput;}

    /**
     * Gets the defaultColor of the ShapeStrategy.
     * @return defaultColor
     */
    public static Color getDefaultColour(){return defaultColor;}

    /**
     * Sets the outlineColor with the given input.
     * @param outlineColorInput - the outline colour of the ShapeStrategy.
     */
    public void setOutlineColor(Color outlineColorInput){outlineColor = outlineColorInput;}

    /**
     * Gets the outlineColor of the ShapeStrategy.
     * @return outlineColor
     */
    public Color getOutlineColor(){return outlineColor;}

    /**
     * Checks if the user's mouse is on the ShapeStrategy.
     * @param x - x-coordinate of Mouse Event.
     * @param y - y-coordinate of Mouse Event.
     */
    public abstract boolean inBoundary(double x, double y);

    /**
     * Calculates the new position of ShapeStrategy by the x and y offset after user
     * moves ShapeStrategy.
     * @param x - The offset of x-coordinate
     * @param y - The offset of the y-coordinate
     */
    public abstract void reposition(double x, double y);

    /**
     * Gets the minX of the ShapeStrategy.
     * @return minX
     */
    public double getMinX(){return minX;}

    /**
     * Gets the minY of the ShapeStrategy.
     * @return minX
     */
    public double getMinY(){return minY;}

    /**
     * Gets the maxX of the ShapeStrategy.
     * @return maxX
     */
    public double getMaxX(){return maxX;}

    /**
     * Gets the maxY of the ShapeStrategy.
     * @return maxY
     */
    public double getMaxY(){return maxY;}

    /**
     * Draws the ShapeStrategy on the given GraphicsContext g, allowing for customizable outline and fill styles.
     * @param g - the GraphicContext to draw the ShapeStrategy.
     */
    public abstract void drawShape(GraphicsContext g);
}
