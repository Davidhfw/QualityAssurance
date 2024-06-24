package org.example;


import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class CalculatorAreaTest {

    private final CalculatorArea calculatorArea = new CalculatorArea();

    @Test
    public void BothLengthAndWidthPositive() {
        assertEquals(15, calculatorArea.calculateArea(3, 5));
    }

    @Test
    public void PositiveLengthAndNegativeWidth() {
        assertEquals(0, calculatorArea.calculateArea(3, -5));
    }

    @Test
    public void NegativeLengthAndPositiveWidth() {
        assertEquals(0, calculatorArea.calculateArea(-3, 5));
    }

    @Test
    public void NegativeLengthAndWidth() {
        assertEquals(0, calculatorArea.calculateArea(-3, -5));
    }
}
