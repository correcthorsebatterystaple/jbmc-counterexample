class Input {
    public static void test(int[] x) {
        int length = x.length;
        for (int index1 = 0; index1 < length - 1; index1++)
            for (int index2 = 0; index2 < length - index1 - 1; index2++)
                if (x[index2] > x[index2 + 1]) {
                    // swap x[j+1] and x[j]
                    int temp = x[index2];
                    x[index2] = x[index2 + 1];
                    x[index2 + 1] = temp;
                }

        assert x[0] <= x[1];
        assert x[1] <= x[2];
        assert x[2] <= x[3];
    }
}
