class Input {
    static class A {
        int x;
    }
    static class B {
        A a;
    }
    public static void test(B b) {
        if (b != null && b.a != null) {
            assert b.a.x == 0;
        }
    }
}
