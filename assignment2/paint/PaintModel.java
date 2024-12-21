package ca.utoronto.utm.assignment2.paint;

import javafx.scene.paint.Color;
import java.util.ArrayList;
import java.util.Observable;

/**
 * The PaintModel class is the model component of the paint application. It stores and manages the
 * shapes drawn on the canvas, handles shape selection, and maintains other attributes such as
 * background color, line thickness, and fill style.
 */
public class PaintModel extends Observable {
        private ArrayList<ShapeStrategy> shapes=new ArrayList<ShapeStrategy>();
        private ArrayList<ShapeStrategy> History=new ArrayList<ShapeStrategy>();
        int numInterimShapes = 0;
        private double lineThickness;
        private String fill;
        private String TextInput="";
        private Color outlineColor;
        private Color backgroundColor=Color.WHITE;
        private ArrayList<Integer> selected = new ArrayList<Integer>();
        private ArrayList<Color> oldColor = new ArrayList<Color>();
        private Point offset=new Point(0.0,0.0);
        private ArrayList<ShapeStrategy> copiedShapes = new ArrayList<>();
        private ArrayList<ShapeStrategy> selectedShapes = new ArrayList<>();


        /**
         * Adds a new interim shape (shape feedback) to the model.
         * @param shape - The ShapeStrategy object to be added as an interim shape.
         */
        public void addInterimShape(ShapeStrategy shape) {
                deselectShape();
                shapes.add(shape);
                numInterimShapes++;
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Adds a new shape to the model.
         * @param shape - The ShapeStrategy object to be added as a shape.
         */
        public void addShape(ShapeStrategy shape) {
            deselectShape();
            for (int i = 0; i < numInterimShapes; i++) {
                shapes.removeLast();
            }
            shapes.add(shape);
            numInterimShapes = 0;
            this.setChanged();
            this.notifyObservers();
        }

        /**
         * Redoes the last removed shape from the history and adds it back into shapes.
         */
        public void Redo(){
                 deselectShape();
                if(!History.isEmpty()) {
                        shapes.add(History.removeLast());
                        this.setChanged();
                        this.notifyObservers();
                }
        }

        /**
         * Removes the last shape from the model and adds it to the history for undo command.
         */
        public void removeLastShape() {
                deselectShape();
                if (!shapes.isEmpty()) {
                        History.add(shapes.removeLast());
                        this.setChanged();
                        this.notifyObservers();
                }
        }

        /**
         * Clears all shapes from the canvas.
         */
        public void clearCanvas() {
                deselectShape();
                shapes.clear();
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Sets the shapes in the model to the specified list and notifies observers.
         * @param shapes - The new list of ShapeStrategy objects to set in the model.
         */
        public void setShapes(ArrayList<ShapeStrategy> shapes) {
            this.shapes.addAll(shapes);
            this.setChanged();
            this.notifyObservers();
        }

        /**
         * Directly sets the list of shapes in the model (used for undo/redo) and notifies observers.
         * @param shapes The list of ShapeStrategy objects to set as the current shape list.
         */
        protected void setShapesList(ArrayList<ShapeStrategy> shapes) {
                this.shapes = new ArrayList<>(shapes);
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Gets the background color for the canvas
         * @return backgroundColor
         */
        public Color getbackgroundColor(){return backgroundColor;}

        /**
         * Sets the background color for the canvas and notifies observers.
         * @param backgroundColor - the backgroundColor for the canvas.
         */
        public void setbackgroundColor(Color backgroundColor) {
                this.backgroundColor=backgroundColor;
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Sets the TextInput and notifies observers.
         * @param textInput - The text input from Text class
         */
        public void setTextInput(String textInput){
                this.TextInput = textInput;
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Gets the TextInput from the model.
         * @return TextInput
         */
        public String getTextInput(){return TextInput;}

        /**
         * Sets the stroke lineThickness for drawing shapes and notifies observers.
         * @param thickness - current thickness of the line (stroke)
         */
        public void setLineThickness(double thickness) {
                this.lineThickness = thickness;
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Gets current lineThickness from the model.
         * @return
         */
        public double getLineThickness(){return lineThickness;}

        /**
         * Sets fill color to shapes and notifies observers.
         * @param color
         */
        public void ColorSelector(Color color){
                ShapeStrategy.setDefaultColour(color);
                this.setChanged();
                this.notifyObservers();
        }
        /**
         * Sets outlineColor to shapes and notifies observers.
         * @param color
         */
        public void setOutlineColor(Color color){
                this.outlineColor = color;
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Sets outlineColor to shapes and notifies observers.
         * @return outlineColor
         */
        public Color getOutlineColor(){return outlineColor;}

        /**
         * Sets fill for drawing shapes and notifies observers.
         * @param fill - the current fill setting (fill, outline, both)
         */
        public void setFill(String fill) {
                this.fill = fill;
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Gets fill option from the model.
         * @return fill
         */
        public String getFill(){return fill;}

        /**
         * Gets all the shapes added to model.
         * @return shapes
         */
        public ArrayList<ShapeStrategy> getShapes() {return shapes;}

        /**
         * Sets all the copiedShapes with the given input.
         * @param copiedShapes - shapes that are copied.
         */
        public void setCopiedShapes(ArrayList<ShapeStrategy> copiedShapes) {
            this.copiedShapes = new ArrayList<>(copiedShapes);
            }
        /**
         * Gets the copiedShapes from the model.
         * @return copiedShapes
         */
        public ArrayList<ShapeStrategy> getCopiedShapes() {return copiedShapes;}

        /**
         * Gets the old color of selected shapes from the model.
         * @return oldColor
         */
        public ArrayList<Color> getOldColor() {
                return oldColor;
        }

        /**
         * Sets shapes to selected given the Mouse Event coordinates and notifies observers.
         * To show that a shape is selected, change the color to Color.Lime.
         * @param multi - if the command is single select or multi-select.
         * @param x - x-coordinate of the Mouse Event.
         * @param y - y-coordinate of the Mouse Event.
         */
        public void setSelected(boolean multi, double x, double y) {
                if (!multi) {
                        deselectShape();
                }
                for (int i = 0; i < shapes.size(); i++) {
                        if (shapes.get(shapes.size() - i - 1).inBoundary(x, y)) {
                                if(!selected.contains(shapes.size() - i - 1)) {
                                        selected.add(shapes.size() - i - 1);
                                        oldColor.add(shapes.get(selected.getLast()).getColor());
                                        shapes.get(selected.getLast()).setColor(Color.LIME);
                                }
                                setSelectedShapes();
                                System.out.println("Selected " + selected.size() + " element(s)");
                                this.setChanged();
                                this.notifyObservers();
                                return;
                        }
                }
        }

        /**
         * Sets the change in point after the repositioning of a ShapeStrategy.
         * @param offset - the
         */
        public void setOffset(Point offset){this.offset=new Point(offset.x, offset.y);}

        /**
        * Gets all the shapes indexes that are selected from the model.
         * @return selected
         */
        public ArrayList<Integer> getSelected() {return selected;}

        /**
        * Sets the shapes indexes that are selected with the given input.
        * @param selected - A list of shape indexes.
        */
        public void setSelectedArray(ArrayList<Integer> selected) {
            this.selected = new ArrayList<>(selected);
    }

        /**
        * Sets the selectedShapes by adding shapes with the corresponding the selected indexes.
        */
        public void setSelectedShapes() {
            for (int index : selected) {
                selectedShapes.add(shapes.get(index));
            }
        }

        /**
         * Sets the oldColor with the given input
         * @param color - A list of all the selected shapes colors before being selected.
         */
        public void setSelectedColors(ArrayList<Color> color) {
            oldColor = new ArrayList<>(color);
            deselectShape();
        }

        /**
        * Deselects shapes by clearing selected and reverting shape color to oldColor.
        * Also notifies observers.
        */
        public void deselectShape() {
                if (!selected.isEmpty()) {
                        for (int i = 0; i < selected.size(); i++) {
                                shapes.get(selected.get(i)).setColor(oldColor.get(i));
                        }
                }
                selected.clear();
                oldColor.clear();
                this.setChanged();
                this.notifyObservers();
        }

        /**
         * Calculates the new position of selected shapes by the x and y offset after user
         * moves selected shapes.
         * @param x - The offset of x-coordinate
         * @param y - The offset of the y-coordinate
         */
        public void repositionSelectedShapes(double x, double y) {
                if(selected.isEmpty()) {return;}
                double currMinX=shapes.get(selected.get(0)).getMinX();
                double currMinY = shapes.get(selected.get(0)).getMinY();
                double currMaxX = shapes.get(selected.get(0)).getMaxX();
                double currMaxY = shapes.get(selected.get(0)).getMaxY();
                for(int i = 1; i < selected.size(); i++) {
                        currMinX = Math.min(currMinX, shapes.get(selected.get(i)).getMinX());
                        currMaxX = Math.max(currMaxX, shapes.get(selected.get(i)).getMaxX());
                        currMinY = Math.min(currMinY, shapes.get(selected.get(i)).getMinY());
                        currMaxY = Math.max(currMaxY, shapes.get(selected.get(i)).getMaxY());
                }
                double centreX = (currMaxX+currMinX)/2;
                double centreY = (currMaxY+currMinY)/2;
                offset.x = x - centreX;
                offset.y = y - centreY;

                addOffsets();
                System.out.println("Moved multiple annotations");

        }

        /**
         * Changes position of selected shapes and notifies observer
         */
        public void addOffsets(){
                for(int i = 0; i < selected.size(); i++) {
                        shapes.get(selected.get(i)).reposition(offset.x, offset.y);
                }
                this.setChanged();
                this.notifyObservers();
        }

        /**
        * Resets the model and notifies observer.
        */
        public void clearData(){
            shapes.clear();
            History.clear();
            selected.clear();
            oldColor.clear();
            numInterimShapes = 0;
            setOffset(new Point(0.0, 0.0));
            setTextInput("");
            setLineThickness(1.0);
            setbackgroundColor(Color.WHITE);
            this.setChanged();
            this.notifyObservers();
        }

        /**
         * Notifies Observer for open file.
         */
        public void OpenFile(){
            this.setChanged();
            this.notifyObservers();
        }
}
