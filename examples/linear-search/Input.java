class Input {
    public static int test(int[] x, int searchedValue) {
        int length = x.length;
        for (int index = 0; index < length; index++)
        {
            if (x[index] == searchedValue)
                return index;
        }
        return -1;
    }
}
