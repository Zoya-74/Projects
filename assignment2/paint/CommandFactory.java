package ca.utoronto.utm.assignment2.paint;

/**
 * CommandFactory is responsible all creating instances of Command objects.
 *
 */
public class CommandFactory {
    /**
     * Creates the appropriate Command objects based on a provided mode string.
     * @param mode - dictates the type of Command object that will be created
     */
    public Command getCommand(String mode){
        return switch (mode) {
            case "Circle" -> new DrawCircleCommand();
            case "Rectangle" -> new DrawRectangleCommand();
            case "Square" -> new DrawSquareCommand();
            case "Oval" -> new DrawOvalCommand();
            case "Triangle" -> new DrawTriangleCommand();
            case "Squiggle" -> new DrawSquiggleCommand();
            case "Polyline" -> new DrawPolylineCommand();
            case "Rounded Rectangle" -> new DrawRoundedRectCommand();
            case "Polygon" -> new DrawPolygonCommand();
            case "Undo" -> new UndoCommand();
            case "Redo" -> new RedoCommand();
            case "Clear Canvas" -> new ClearCanvasCommand();
            case "Select" -> new SelectElementCommand();
            case "MultiSelect" -> new MultiSelectElementCommand();
            case "Paste" -> new PasteCommand();
            case "Copy" -> new CopyCommand();
            case "Cut" -> new CutCommand();
            case "Save" -> new SaveFileCommand();
            case "Open" -> new OpenFileCommand();
            case "New" -> new NewFileCommand();
            default -> new NullCommand();
        };
    }
}
