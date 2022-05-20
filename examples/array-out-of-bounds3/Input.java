public class Input {
    public static void test(int i) {
        try {
            int[] a = new int[4];
            a[i] = 0;
        } catch (Exception exc) {
            assert false;
        }
    }
}
