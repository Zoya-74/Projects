package ca.utoronto.utm.assignment2.paint;


import javafx.application.Application;
import javafx.stage.Stage;

/**
 * Paint is the main entry point for the Paint application where user runs the application
 * to interact with View and Model.
 */
public class Paint extends Application {

        PaintModel model; // Model
        View view; // View + Controller

        /**
         * The main method which launches the JavaFX application.
         * @param args Command-line arguments.
         */
        public static void main(String[] args) {
                launch(args);
        }

        /**
         * Sets up the JavaFX stage and initializes the model and view.
         * @param stage The primary stage for the JavaFX application.
         * @throws Exception If an error occurs during startup.
         */
        @Override
        public void start(Stage stage) throws Exception { //modified
                this.model = new PaintModel();
                // View + Controller
                this.view = new View(model, stage);
        }
}
