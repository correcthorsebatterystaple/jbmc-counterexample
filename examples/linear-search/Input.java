class Input {
    public static int test(int[] x, int searchedValue) {
        int length = x.length;
        boolean found = false;
        int foundIndex = -1;
        for (int index = 0; index < length; index++)
        {
            if (x[index] == searchedValue) {
                found = true;
                foundIndex = index;
                break;
            }
                
        }

        assert found;
        assert x[foundIndex] == searchedValue;
        return foundIndex;
    }
}
