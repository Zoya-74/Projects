package ca.utoronto.utm.assignment2.paint;

import javafx.scene.paint.Color;
import javafx.stage.FileChooser;

import java.io.*;

/**
 * OpenFileCommand is a Command that opens a .paint file onto the canvas.
 *
 */
public class OpenFileCommand implements Command {
    /**
     * Opens fileChooser to allow users to choose which file to open. Then reads a .paint file
     * and draws the canvas to exactly match the file information.
     * Does nothing if file type is not .paint
     *
     * @param paintPanel - the paintPanel where the canvas information from the file will be drawn
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        FileChooser fileChooser = new FileChooser();
        File selectedfile = fileChooser.showOpenDialog(null);
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Paint files", "*.paint"));
        if (selectedfile != null) {
            String filename = selectedfile.getName();
            if (filename.endsWith(".paint")) {//this can be done cleaner as a extension filter?
                try (ObjectInputStream dis = new ObjectInputStream(new FileInputStream(selectedfile.getAbsolutePath()))) {
                    model.clearCanvas();
                    model.clearData();
                    COMMANDS.clear();
                    HISTORY.clear();

                    double backgroundRed = dis.readDouble();
                    double backgroundGreen = dis.readDouble();
                    double backgroundBlue = dis.readDouble();
                    double backgroundAlpha = dis.readDouble();
                    Color backgroundcolor = new Color(backgroundRed, backgroundGreen, backgroundBlue, backgroundAlpha);
                    model.setbackgroundColor(backgroundcolor);

                    //begin reading from file
                    int arraysize = dis.readInt();
                    for (int i = 0; i < arraysize; i++) {
                        ShapeStrategy elem = (ShapeStrategy) dis.readObject();
                        model.getShapes().add(elem);

                        double red = dis.readDouble();
                        double green = dis.readDouble();
                        double blue = dis.readDouble();
                        double alpha = dis.readDouble();
                        elem.setColor(new Color(red, green, blue, alpha));

                        double outlineRed = dis.readDouble();
                        double outlineGreen = dis.readDouble();
                        double outlineBlue = dis.readDouble();
                        double outlineAlpha = dis.readDouble();
                        elem.setOutlineColor(new Color(outlineRed, outlineGreen, outlineBlue, outlineAlpha));

                    }
                    model.OpenFile();//view updated with file contents
                } catch (FileNotFoundException e) {
                    System.err.println("Error: file not found." + e.getMessage());
                } catch (IOException e) {
                    System.err.println("Error occurred while opening file." +
                            e.getMessage());
                } catch (ClassNotFoundException e) {
                    System.err.println("Object in file is not of correct type." +
                            e.getMessage());
                }
            } else{
                System.out.println("Invalid file type. Please select a .paint file.");
            }
        }
        System.out.println("Open File");
    }

    /**
     * This method does not execute anything since undoing opening a file is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Undo(PaintPanel paintPanel) {

    }

    /**
     * This method does not execute anything since redoing opening a file is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Redo(PaintPanel paintPanel) {

    }
}
