package ca.utoronto.utm.assignment2.paint;

import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.scene.control.Slider;
import javafx.scene.control.Tooltip;
import java.text.DecimalFormat;

/**
 * ThicknessSliderHandler handles the ChangeListener that responds to the changes in the slider
 * and adjusts the stroke thickness in the Paint application.
 */
public class ThicknessSelectorHandler implements ChangeListener<Number> {
    private Slider slider;
    private PaintPanel paintPanel;

    /**
     * Constructs the ThicknessSelectorHandler with the given paintPanel and thickness slider.
     * @param paintPanel - the PaintPanel to be edited.
     * @param slider - The thickness slider in the VisualEditorPanel.
     */
    public ThicknessSelectorHandler(PaintPanel paintPanel, Slider slider) {
        this.slider = slider;
        this.paintPanel = paintPanel;
    }

    /**
     * Gets the newValue of the thickness slider and updates the stroke thickness in paintPanel.
     * @param observableValue - the observable value of the slider.
     * @param oldValue - the old thickness value on the slider.
     * @param newValue - the new thickness of the slider after the listener change.
     */
    @Override
    public void changed(ObservableValue<? extends Number> observableValue, Number oldValue, Number newValue) {
        Tooltip tooltip = new Tooltip();
        DecimalFormat df = new DecimalFormat("0.00");
        tooltip.setText(df.format(newValue));
        slider.setTooltip(tooltip);
        double lineThickness = slider.getValue();
        paintPanel.getModel().setLineThickness(lineThickness);
    }
}