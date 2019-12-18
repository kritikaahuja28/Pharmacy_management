package com.mkyong;
import java.util.Arrays;
public class SelectionSort {
    public static void main(String[] args) {
        int[] array = {20,50,70,10,90,80};
        selectionsort(array);
        System.out.println(Arrays.toString(array));
        }
        private static void selectionsort(int[] input) {
        int inputLength = input.length;
        for (int i = 0; i < inputLength - 1; i++) {
            int min = i;
            for (int j = i + 1; j < inputLength; j++) {
                if (input[j] < input[min]) {
                    min = j;
                }
            }
            int temp = input[i];
            input[i] = input[min];
            input[min] = temp;
            }
        }
    }
