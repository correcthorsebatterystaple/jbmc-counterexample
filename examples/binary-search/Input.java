class Input {
    public static int test(int[] x, int searchedValue) {
        int left = 0, right = x.length - 1;
        while (true) {
            int middle = left + (right - left) / 2;
            if (x[middle] == searchedValue)
                return middle;
            if (x[middle] < searchedValue)
                left = middle + 1;
            else
                right = middle - 1;
        }

        // return -1;
    }
}
