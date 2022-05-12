public class Input {
    public static void test(A[] x) {
        if(x != null)
            if(x.length != 0)
                if(x[0] != null)
                    assert x[0].x == 0;
    }
}
