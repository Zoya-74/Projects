package ca.utoronto.utm.assignment2.paint;

import javafx.scene.paint.Color;
import javafx.stage.FileChooser;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.ArrayList;

/**
 * SaveFileCommand is a Command that saves a .paint file with information about the user's canvas
 * onto their device.
 *
 */
public class SaveFileCommand implements Command{

    /**
     * Writes a .paint file with all information about the user's canvas.  Then opens fileChooser to allow
     * users to choose where to save their file on their device.
     *
     * @param paintPanel - the paintPanel with the canvas information that will be saved
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        FileChooser fileChooser = new FileChooser();
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Paint file", "*.paint"));
        File savedfile = fileChooser.showSaveDialog(null);
        if (savedfile != null) {
            try (ObjectOutputStream dos = new ObjectOutputStream(new FileOutputStream(savedfile.getAbsolutePath()))) {
                Color backgroundColor = model.getbackgroundColor();
                dos.writeDouble(backgroundColor.getRed());
                dos.writeDouble(backgroundColor.getGreen());
                dos.writeDouble(backgroundColor.getBlue());
                dos.writeDouble(backgroundColor.getOpacity());

                ArrayList<ShapeStrategy> canvasArray = model.getShapes();
                dos.writeInt(canvasArray.size());
                for (ShapeStrategy elem : canvasArray) {
                    dos.writeObject(elem);

                    Color color = elem.getColor();
                    dos.writeDouble(color.getRed());
                    dos.writeDouble(color.getGreen());
                    dos.writeDouble(color.getBlue());
                    dos.writeDouble(color.getOpacity());

                    Color outlineColor = elem.getOutlineColor();
                    dos.writeDouble(outlineColor.getRed());
                    dos.writeDouble(outlineColor.getGreen());
                    dos.writeDouble(outlineColor.getBlue());
                    dos.writeDouble(outlineColor.getOpacity());
                }
                System.out.println("Save File");

            } catch (IOException e) {
                System.err.println("Error occurred while saving file." + e.getMessage());
            }

        }
    }

    /**
     * This method does not execute anything since undoing a file save is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Undo(PaintPanel paintPanel) {

    }

    /**
     * This method does not execute anything since redoing an undo-ed file save is not applicable,
     * only here for the Command interface implementation.
     * @param paintPanel - where this method would be applied (if needed)
     */
    @Override
    public void Redo(PaintPanel paintPanel) {

    }
}
