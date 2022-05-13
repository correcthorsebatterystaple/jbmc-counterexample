// Counterexample for: assertion at file Input.java line 3 function java::Input.test:(LA;)V bytecode-index 9
class CounterExample2 {
	public static void main(String[] args) {
		A arg0a = new A();
		B b_arg0a = new B();
		b_arg0a.x = 1;
		arg0a.b = b_arg0a;
		Input.test(arg0a);
	}
}