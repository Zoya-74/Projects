package ca.utoronto.utm.assignment2.paint;

import javafx.event.EventHandler;
import javafx.scene.control.TextField;
import javafx.scene.input.KeyEvent;

/**
 * TextInputHandler handles the input of the text in the Paint application.
 */
public class TextInputHandler implements EventHandler<KeyEvent> {
    private TextField tf;
    private PaintPanel paintPanel;

    /**
     * Constructs TextInputHandler with the given paintPanel and tf.
     * @param paintPanel - the PaintPanel to be edited.
     * @param tf - the TextField where the user inputs text.
     */
    public TextInputHandler(PaintPanel paintPanel, TextField tf) {
        this.tf = tf;
        this.paintPanel = paintPanel;
    }

    /**
     * Retrieves the current text from tf and stores it in the PaintModel from the paintPanel.
     * The handle method executes AddTextCommand and handles the placement of the text input on the Paint application.
     * @param keyEvent - the keyboard event where it takes in the character of the keyboard.
     */
    @Override
    public void handle(KeyEvent keyEvent) {
        paintPanel.getModel().setTextInput(tf.getText());
        AddTextCommand txtCmd = new AddTextCommand(keyEvent);
        txtCmd.execute(paintPanel);
        System.out.println("Set input text to: " + tf.getText());
    }
}
