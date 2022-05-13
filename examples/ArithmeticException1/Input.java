public class Input {
  public static void test(int i) {
    try {
      int j = 10 / i;
    } catch (ArithmeticException exc) {
      assert false;
    }
  }
}