package ca.utoronto.utm.assignment2.paint;

import javafx.scene.canvas.GraphicsContext;

/**
 * RoundedRectangle is a ShapeStrategy consisting of four point and four sides, where the edges are rounded.
 * @author pradha91
 */
public class RoundedRectangle extends Rectangle {
    public RoundedRectangle(Point centre, double length, double height) {super(centre, length, height);}
    @Override
    public ShapeStrategy copy(){
        RoundedRectangle copy = new RoundedRectangle(getCentre(), getLength(), getHeight());
        copy.topLeftY = this.topLeftY;
        copy.topLeftX = this.topLeftX;
        copyAttributes(copy);
        return copy;
    }

    /**
     * Draws the RoundedRectangle on the given GraphicsContext g, allowing for customizable outline and fill styles.
     * @param g - the GraphicContext to draw the RoundedRectangle.
     */
    @Override
    public void drawShape(GraphicsContext g) {
        double lengthUse;
        double heightUse;

        g.setFill(this.getColor());

        lengthUse = Math.abs(getLength());
        heightUse = Math.abs(getHeight());
        if(this.getFillStyle().equals("both")){
            g.setLineWidth(getThickness());
        }
        if(this.getFillStyle().equals("outline") || this.getFillStyle().equals("both")){
            g.setStroke(this.getOutlineColor());
            g.setLineWidth(getThickness());
            g.strokeRoundRect(topLeftX, topLeftY, lengthUse, heightUse, 40, 40);
        }
        if (this.getFillStyle().equals("solid") || this.getFillStyle().equals("both")) {
            g.fillRoundRect(topLeftX, topLeftY, lengthUse, heightUse, 40, 40);

        }
    }
}
