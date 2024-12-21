package ca.utoronto.utm.assignment2.paint;

import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;

/**
 * AddTextCommand is a Command that creates Text based on user inputs. This command
 * adds textbox to the PaintPanel.
 *
 */
public class AddTextCommand implements Command {
    Text text;
    KeyEvent keyEvent;

    /**
     * Creates an AddTextCommand object.
     * @param keyEvent - the key event that is associated with the AddTextCommand object
     */
    public AddTextCommand(KeyEvent keyEvent) {this.keyEvent = keyEvent;}

    /**
     * Executes appropriate consequence of AddTextCommand based on user input. If user clicked Enter,
     * user inputted textbox gets added to canvas.
     *
     * @param paintPanel - the PaintPanel on which the text will be added
     */
    @Override
    public void execute(PaintPanel paintPanel) {
        PaintModel model = paintPanel.getModel();
        if (keyEvent.getEventType().equals(KeyEvent.KEY_PRESSED)) {
            this.text = new Text(new Point(paintPanel.getWidth()/2, paintPanel.getHeight()/2), model.getTextInput());
            if (keyEvent.getCode().equals(KeyCode.ENTER)) {
                model.addShape(text);
                System.out.println("Added Text");
                COMMANDS.add(this);
            }
            else{model.addInterimShape(text);}

        }

    }

    /**
     * Undoes the AddText operation by removing the added text from the canvas.
     * @param paintPanel - the PaintPanel on which the paste operation will be undone
     */
    @Override
    public void Undo(PaintPanel paintPanel) {
        paintPanel.getModel().removeLastShape();
    }

    /**
     * Redoes the AddText operation by re-adding the removed text to the canvas.
     * @param paintPanel the PaintPanel on which the paste operation will be redone
     */
    @Override
    public void Redo(PaintPanel paintPanel) {
        paintPanel.getModel().Redo();
    }

}

