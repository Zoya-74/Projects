package ca.utoronto.utm.assignment2.paint;
import javafx.scene.canvas.Canvas;
import javafx.event.EventHandler;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.MouseEvent;

import java.util.ArrayList;
import java.util.Observable;
import java.util.Observer;

/**
 * PaintPanel is the drawing canvas in the paint application. PaintPanel
 * handles various mouse events such as press, release, drag,
 * and move to allow the user to draw, select, and interact with shapes.
 */
public class PaintPanel extends Canvas implements EventHandler<MouseEvent>, Observer {
    private PaintModel model;
    private DrawCommandStrategy currentCommand = new NullCommand();
    public ShapeStrategy shape;

    /**
     * Constructs a PaintPanel canvas with the given PaineModel and adds itself as an Observer to the model.
     * @param model
     */
    public PaintPanel(PaintModel model) {
        super(1250, 500);
        this.model=model;
        this.model.addObserver(this);

        this.addEventHandler(MouseEvent.MOUSE_PRESSED, this);
        this.addEventHandler(MouseEvent.MOUSE_RELEASED, this);
        this.addEventHandler(MouseEvent.MOUSE_MOVED, this);
        this.addEventHandler(MouseEvent.MOUSE_CLICKED, this);
        this.addEventHandler(MouseEvent.MOUSE_DRAGGED, this);
    }

    /**
     * Getter for PaintModel model.
     * @return model
     */
    public PaintModel getModel(){return model;}

    /**
     * Sets the current command that needs to be executed.
     * @param command - Strategy command that is being changed in PaintPanel.
     */
    public void setCommand(DrawCommandStrategy command){currentCommand = command;}

    /**
     * Handles mouse events by delegating the action to the current drawing command.
     * This method is invoked for every mouse event that occurs on the canvas.
     * @param mouseEvent - The mouse event that occurred.
     */
    @Override
    public void handle(MouseEvent mouseEvent) {
        currentCommand.execute(this, mouseEvent);
    }

    /**
     * Updates the PaintPanel when the model changes by clearing the canvas and redrawing all the shapes
     * based on the model's current state.
     * @param o     the observable object.
     * @param arg   an argument passed to the {@code notifyObservers}
     *                 method.
     */
    @Override
    public void update(Observable o, Object arg) {
        GraphicsContext g2d = this.getGraphicsContext2D();
        g2d.clearRect(0, 0, this.getWidth(), this.getHeight());
        g2d.setFill(getModel().getbackgroundColor());
        g2d.fillRect(0, 0, this.getWidth(), this.getHeight());

        ArrayList<ShapeStrategy> shapes = this.model.getShapes();
        for (ShapeStrategy s : shapes) {
            if (s != null) {
                s.drawShape(g2d);
            }
        }
    }

    /**
     * Setter for PaintPanel's width.
     * @param x - length of width.
     */
    public void setPanelWidth(double x){this.setWidth(x);update(null, null);}

    /**
     * Setter for PaintPanel's height.
     * @param y - length of height.
     */
    public void setPanelHeight(double y){this.setHeight(y); update(null, null);}

}
