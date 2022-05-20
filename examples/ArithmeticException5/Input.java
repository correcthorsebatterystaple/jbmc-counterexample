public class Input {
  public static void test() {
    try {
      double i = 0;
      double j = 10 / i;
    } catch (ArithmeticException exc) {
      assert false;
    }
  }
}