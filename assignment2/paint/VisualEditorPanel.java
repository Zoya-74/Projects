package ca.utoronto.utm.assignment2.paint;

import javafx.geometry.Insets;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;

/**
 * VisualEditorPanel provides a toolbar with various for editing a drawing canvas in the Paint application.
 * This includes changing the colour of shapes, background and their outline, changing the shape thickness and adding
 * text.
 *
 * @author karims14
 */
public class VisualEditorPanel {
    private PaintPanel paintPanel;
    private TextField tf;
    private boolean isDisabled=false;
    private double thickness = 1.0;

    /**
     * Constructs a VisualEditorPanel with the given PaintPanel.
     * @param paintPanel - the PaintPanel to be edited.
     */
    public VisualEditorPanel(PaintPanel paintPanel) {
        this.paintPanel = paintPanel;
    }

    /**
     * Creates a slider that adjusts the thickness of the stroke for each shape.
     * @return toolBar
     */
    private ToolBar createThicknessSelector() {
        Slider thicknessSlider = new Slider();
        thicknessSlider.setMax(20.0);
        thicknessSlider.setMin(1.0);
        thicknessSlider.setShowTickLabels(true);
        thicknessSlider.setMajorTickUnit(5);
        thicknessSlider.setShowTickMarks(true);
        paintPanel.getModel().setLineThickness(this.thickness);
        thicknessSlider.valueProperty().addListener(new ThicknessSelectorHandler(paintPanel, thicknessSlider));
        Label thickness = new Label("Line Thickness");
        thickness.setPadding(new Insets(4.0, 0.0, 0.0, 0.0));
        thickness.setMaxWidth(Double.MAX_VALUE);
        HBox thicknessMode = new HBox(5, thickness, thicknessSlider);
        ToolBar toolBar = new ToolBar(thicknessMode);
        toolBar.setBackground(new Background(new BackgroundFill(Color.SILVER, null, null)));
        return toolBar;
    }

    /**
     * Creates a ColorPicker that changes the color of the shape (Shape Fill).
     * @return toolBar
     */
    private ToolBar createShapeColorSelector() {
        ColorPicker colorPicker = new ColorPicker();
        colorPicker.setValue(Color.BLACK);
        colorPicker.setOnAction(new ShapeColorSelectorHandler(paintPanel, colorPicker));
        Label fillLabel = new Label("Fill");
        fillLabel.setPadding(new Insets(4.0, 0.0, 0.0, 0.0));
        fillLabel.setMaxWidth(Double.MAX_VALUE);
        HBox fillBox = new HBox(5, fillLabel, colorPicker);
        ToolBar toolBar = new ToolBar(fillBox);
        toolBar.setBackground(new Background(new BackgroundFill(Color.SILVER, null, null)));
        return toolBar;    }

    /**
     * Creates a ColorPicker that changes the color of the outline of the shape (stroke).
     * @return toolBar
     */
    private ToolBar createOutlineColorSelector() {
        ColorPicker colorPicker = new ColorPicker();
        colorPicker.setValue(Color.BLACK);
        paintPanel.getModel().setOutlineColor(Color.BLACK);
        colorPicker.setOnAction(new OutlineColorSelectorHandler(paintPanel, colorPicker));
        Label outlineLabel = new Label("Outline");
        outlineLabel.setPadding(new Insets(4.0, 0.0, 0.0, 0.0));
        outlineLabel.setMaxWidth(Double.MAX_VALUE); // You can adjust the width depending on the space needed

        // Wrap the label and the color picker in a HBox to control the layout
        HBox outlineBox = new HBox(5, outlineLabel, colorPicker);

        ToolBar toolBar = new ToolBar(outlineBox);
        toolBar.setBackground(new Background(new BackgroundFill(Color.SILVER, null, null)));
        return toolBar;    }

    /**
     * Creates a TextField to input text onto the canvas.
     * @return toolBar
     */
    private ToolBar createTextInput(){
        tf = new TextField();
        tf.setDisable(true);
        tf.setPromptText("Input Text for Text Box Mode. Press enter to confirm entry");
        tf.setOnKeyPressed(new TextInputHandler(paintPanel, tf));

        ToolBar toolBar = new ToolBar(new Label("Text"),tf);
        toolBar.setBackground(new Background(new BackgroundFill(Color.SILVER, null, null)));
        return toolBar;    }

    /**
     * Adds all the toolBars from methods above into an HBox so that the VisualEditorPanel .
     * This also constructs the buttons for fill background and text.
     * @return toolBar
     */
    public HBox getToolBar() {
        HBox toolbar = new HBox();
        toolbar.setSpacing(10);

        Button fillButton = new Button();
        Image fillBGImage =
                new Image("https://icons.iconarchive.com/icons/icons8/ios7/256/Editing-Background-Color-icon.png");
        ImageView viewFillBG = new ImageView(fillBGImage);
        viewFillBG.setFitWidth(20);
        viewFillBG.setFitHeight(20);
        Tooltip tooltip = new Tooltip();
        tooltip.setText("Fill Background");
        fillButton.setTooltip(tooltip);
        fillButton.setMinWidth(30);
        fillButton.setGraphic(viewFillBG);

        fillButton.setOnAction(new FillBackgroundHandler(paintPanel));

        Button fillShapeButton = new Button();
        Image fillShapeImage = new Image("https://cdn-icons-png.flaticon.com/512/1370/1370713.png");
        ImageView viewFillShape = new ImageView(fillShapeImage);
        viewFillShape.setFitWidth(20);
        viewFillShape.setFitHeight(20);
        Tooltip tooltip2 = new Tooltip();
        tooltip2.setText("Fill Shape");
        fillShapeButton.setTooltip(tooltip2);
        fillShapeButton.setMinWidth(30);
        fillShapeButton.setGraphic(viewFillShape);

        fillShapeButton.setOnAction(new FillShapeHandler(paintPanel));

        Button txtButton = new Button();
        Image textImage =
                new Image("https://icons.veryicon.com/png/o/commerce-shopping/online-retailers/text-38.png");
        ImageView viewText = new ImageView(textImage);
        viewText.setFitWidth(20);
        viewText.setFitHeight(20);
        Tooltip tooltipText = new Tooltip();
        tooltipText.setText("Text");
        txtButton.setTooltip(tooltipText);
        txtButton.setMinWidth(30);
        txtButton.setGraphic(viewText);
        fillButton.setOnAction(new FillBackgroundHandler(paintPanel));

        ToolBar txtToolbar = createTextInput();
        txtButton.setOnAction(event -> enableTextField());

        toolbar.getChildren().addAll(fillShapeButton, fillButton, createThicknessSelector(),
                createShapeColorSelector(), createOutlineColorSelector(), txtToolbar, txtButton);
        return toolbar;
    }

    /**
     * Enables user to input text on text toolbar after clicking the textbox button.
     */
    public void enableTextField(){this.tf.setDisable(isDisabled); this.isDisabled=!isDisabled;}

}