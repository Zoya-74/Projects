package ca.utoronto.utm.assignment2.paint;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.control.Tooltip;
import javafx.scene.layout.*;
import javafx.scene.image.*;

/**
 * ShapeChooserPanel contains several buttons that allows the user to draw different shapes in the Paint
 * application. Each button corresponds to a specific shape which the user can select by clicking.
 * When the button is selected, the specified shape command is applied to the canvas.
 * @author baseetfa
 */
public class ShapeChooserPanel extends GridPane implements EventHandler<ActionEvent> {
        private View view;
        private Button selectedButton;

        /**
         * Constructs ShapeChooserPanel by creating various buttons for each shape.
         * @param view - the View that the shape chooser panel is part of.
         */
        public ShapeChooserPanel(View view) {

                this.view = view;
                ImageView[] buttonIcons = getImageViews();
                String[] buttonLabels = { "Circle", "Rectangle", "Rounded Rectangle", "Square", "Squiggle",
                        "Polyline","Oval", "Triangle", "Polygon", "Select", "MultiSelect"};

                int col = 0;
                for (int i = 0; i < buttonLabels.length; i++) {
                        Button button = new Button();
                        Tooltip tooltip = new Tooltip();
                        tooltip.setText(buttonLabels[i]);
                        button.setTooltip(tooltip);
                        button.setMinWidth(30);
                        button.setGraphic(buttonIcons[i]);
                        this.add(button, col, 0);
                        col++;
                        button.setOnAction(this);
                }
        }

        /**
         * Generates the images for each shape button.
         * @return buttonIcons
         */
        private static ImageView[] getImageViews(){
                Image circleImage = new Image("https://cdn.icon-icons.com/icons2/906/PNG/512/circle_icon-icons.com_70254.png");
                ImageView viewCircle = new ImageView(circleImage);
                viewCircle.setFitWidth(20);  // Set the width
                viewCircle.setFitHeight(20);

                Image rectangleImage = new Image("https://cdn-icons-png.flaticon.com/512/5895/5895916.png");
                ImageView viewRectangle = new ImageView(rectangleImage);
                viewRectangle.setFitWidth(20);  // Set the width
                viewRectangle.setFitHeight(20);

                Image squareImage = new Image("https://cdn1.iconfinder.com/data/icons/material-design-icons-light/24/shape-square-512.png");
                ImageView viewSquare = new ImageView(squareImage);
                viewSquare.setFitWidth(20);  // Set the width
                viewSquare.setFitHeight(20);

                Image squiggleimg = new Image("https://cdn-icons-png.flaticon.com/512/5141/5141429.png");
                ImageView viewSquiggle = new ImageView(squiggleimg);
                viewSquiggle.setFitWidth(20);  // Set the width
                viewSquiggle.setFitHeight(20);

                Image polylineImage = new Image("https://cdn-icons-png.flaticon.com/512/6407/6407067.png");
                ImageView viewPolyline = new ImageView(polylineImage);
                viewPolyline.setFitWidth(20);  // Set the width
                viewPolyline.setFitHeight(20);

                Image ovalImage = new Image("https://cdn-icons-png.flaticon.com/512/649/649719.png");
                ImageView viewOval = new ImageView(ovalImage);
                viewOval.setFitWidth(20);  // Set the width
                viewOval.setFitHeight(20);

                //New icon for triangle -Zoya Fatima
                Image triangleImage = new Image("https://cdn-icons-png.flaticon.com/512/649/649738.png");
                ImageView viewTriangle = new ImageView(triangleImage);
                viewTriangle.setFitWidth(20);
                viewTriangle.setFitHeight(20);

                Image PolygonImage = new Image("https://cdn-icons-png.flaticon.com/512/274/274383.png");
                ImageView viewPolygon = new ImageView(PolygonImage);
                viewPolygon.setFitWidth(20);
                viewPolygon.setFitHeight(20);

                Image RoundedRectImage = new Image("https://cdn-icons-png.flaticon.com/512/3305/3305374.png");
                ImageView viewRoundedRect = new ImageView(RoundedRectImage);
                viewRoundedRect.setFitWidth(20);
                viewRoundedRect.setFitHeight(20);

                Image SelectImage = new Image("https://cdn-icons-png.flaticon.com/512/1536/1536384.png");
                ImageView viewSelect = new ImageView(SelectImage);
                viewSelect.setFitWidth(20);
                viewSelect.setFitHeight(20);

                Image MultiSelectImage = new Image("https://static.thenounproject.com/png/181386-200.png");
                ImageView viewMultiSelect = new ImageView(MultiSelectImage);
                viewMultiSelect.setFitWidth(20);
                viewMultiSelect.setFitHeight(20);


                ImageView[] buttonIcons = {viewCircle, viewRectangle, viewRoundedRect, viewSquare, viewSquiggle, viewPolyline, viewOval,
                        viewTriangle, viewPolygon, viewSelect, viewMultiSelect};
                return buttonIcons;
        }

        /**
         * Handles the event when the button is clicked by the user in ShapeChooserPanel.
         * When the button is selected, the button is highlighted.
         * @param event - the ActionEvent triggered by the button click
         */
        @Override
        public void handle(ActionEvent event) {
                Button clickedButton = (Button) event.getSource();
                String command = clickedButton.getTooltip().getText();
                view.setPanelCommand((DrawCommandStrategy) ((new CommandFactory()).getCommand(command)));

                if (selectedButton != null) {
                        selectedButton.setStyle("");
                }
                clickedButton.setStyle("-fx-background-color: pink");
                selectedButton = clickedButton;

        }
}


