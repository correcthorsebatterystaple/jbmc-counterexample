// Counterexample for: Null pointer check
class CounterExample1 {
	public static void main(String[] args) {
		A arg0a = new A();
		arg0a.b = null;
		Input.test(arg0a);
	}
}