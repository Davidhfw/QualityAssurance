package org.example;

public class CalculatorArea {


    public int calculateArea(int length, int width) {
        int area;
        if (length < 0 || width < 0) {
            area = 0;
        } else {
            area = length * width;
        }
        return area;
    }

}
