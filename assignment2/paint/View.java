package ca.utoronto.utm.assignment2.paint;

import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

/**
 * View is responsible for setting up the user interface in the Paint application.
 * It connects the PaintModel and multiple selection panels that allows the user
 * to interact with and modify the paint canvas.
 * @author baseetfa
 */
public class View implements EventHandler<ActionEvent> {
        private PaintModel paintModel;
        private PaintPanel paintPanel;
        private ShapeChooserPanel shapeChooserPanel;
        private VisualEditorPanel visualEditorPanel;
        private Command runCommand = new NullCommand();

        /**
         * Constructs View that sets up the user interface for the Paint application.
         * This includes setting up model and the selection panels; ShapeChooserPanel
         * and VisualEditorPanel.
         * @param model - the PaintModel that contains the data for Paint application.
         * @param stage - the primary stage where the user interface is displayed.
         */
        public View(PaintModel model, Stage stage) {
                this.paintModel = model;
                this.paintPanel = new PaintPanel(this.paintModel);
                this.shapeChooserPanel = new ShapeChooserPanel(this);
                this.visualEditorPanel = new VisualEditorPanel(this.paintPanel);

                stage.widthProperty().addListener((observable, oldValue, newValue) -> {
                        if((double)newValue > paintPanel.getWidth()){paintPanel.setPanelWidth((double)newValue);}
                        paintPanel.update(null, null);
                });
                stage.heightProperty().addListener((observable, oldValue, newValue) -> {
                        if((double)newValue > paintPanel.getHeight()){paintPanel.setPanelHeight((double)newValue);}
                        paintPanel.update(null, null);
                });

                BorderPane root = new BorderPane();
                ScrollPane scrollPane = new ScrollPane(root);
                root.setTop(createMenuBar());
                root.setBottom(this.paintPanel);
                HBox topPanel = new HBox();
                topPanel.setStyle("-fx-background-color: #C0C0C0;");
                topPanel.getChildren().addAll(this.shapeChooserPanel, this.visualEditorPanel.getToolBar());
                root.setCenter(topPanel);
                Scene scene = new Scene(scrollPane);
                stage.setScene(scene);
                stage.setTitle("Paint");
                stage.show();
        }

        /**
         * Sets the current command that needs to be executed on PaintPanel which
         * is the command invoker.
         * @param command - Strategy command that is being changed in PaintPanel.
         */
        public void setPanelCommand(DrawCommandStrategy command){
            this.paintPanel.setCommand(command);
        }

        /**
         * Creates a menu bar with various menus and menu items for file operations (New, Open, Save, Exit),
         * editing (Cut, Copy, Paste, Undo, Redo), and shape fill styles (Solid, Outline, Outline & Fill).
         * @return menuBar
         */
        private MenuBar createMenuBar() {

                MenuBar menuBar = new MenuBar();
                Menu menu;
                MenuItem menuItem;

                // A menu for File

                menu = new Menu("File");

                menuItem = new MenuItem("New");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuItem = new MenuItem("Open");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuItem = new MenuItem("Save");//US4.015
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menu.getItems().add(new SeparatorMenuItem());

                menuItem = new MenuItem("Exit");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuBar.getMenus().add(menu);

                // Another menu for Edit

                menu = new Menu("Edit");


                menuItem = new MenuItem("Cut");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuItem = new MenuItem("Clear Canvas");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuItem = new MenuItem("Copy");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuItem = new MenuItem("Paste");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menu.getItems().add(new SeparatorMenuItem());
                menuItem = new MenuItem("Undo"); // ADDED undo functionality
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuItem = new MenuItem("Redo");
                menuItem.setOnAction(this);
                menu.getItems().add(menuItem);

                menuBar.getMenus().add(menu);

                // new menu on the menu bar to choose the type of fill before drawing shape
                menu = new Menu("Fill Style");
                ToggleGroup fillStyle = new ToggleGroup();
                RadioMenuItem solidFill = new RadioMenuItem("Solid");
                RadioMenuItem outline = new RadioMenuItem("Outline");
                RadioMenuItem outlineFill = new RadioMenuItem("Outline & Fill");

                solidFill.setToggleGroup(fillStyle);
                outline.setToggleGroup(fillStyle);
                outlineFill.setToggleGroup(fillStyle);
                solidFill.setSelected(true);

                paintPanel.getModel().setFill("solid");
                solidFill.setOnAction(event -> paintPanel.getModel().setFill("solid"));
                outline.setOnAction(event -> paintPanel.getModel().setFill("outline"));
                outlineFill.setOnAction(event -> paintPanel.getModel().setFill("both"));

                menu.getItems().addAll(solidFill, outline, outlineFill);
                menuBar.getMenus().add(menu);

                return menuBar;
        }

        /**
         * Handles action event in menu bar when user clicks on a menu item.
         * The handle method executes the corresponding commands for each menu item.
         * @param event - the ActionEvent in menu bar triggered by menu item.
         */
        @Override
        public void handle(ActionEvent event) {
                System.out.println(((MenuItem) event.getSource()).getText());
                String command = ((MenuItem) event.getSource()).getText();
                runCommand = new CommandFactory().getCommand(command);
                runCommand.execute(paintPanel);
                if (command.equals("Exit")) {
                        Platform.exit();
                }
        }

}
