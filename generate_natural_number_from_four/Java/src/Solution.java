import java.util.ArrayList;
import java.util.List;

class Solution {

    private static String message(String state, int value) {
        return String.format("%s: %d", state, value);
    }

    public static String START(int n)   { return message("start",   n); }
    public static String APPEND0(int n) { return message("append0", n); }
    public static String APPEND4(int n) { return message("append4", n); }
    public static String DIVIDE2(int n) { return message("divide2", n); }

    public static List<String> solveIterative(int n)
        throws IllegalArgumentException
    {
        if (n < 1)
            throw new IllegalArgumentException("value must be greater than 0");

        List<String> path = new ArrayList<>();

        while (true) {
            if (n == 4) { // solution found
                path.add(0, START(n));
                break;
            }
            
            int prefix = n / 10;
            int digit  = n % 10;

            if (digit == 4) {
                path.add(0, APPEND4(n));
                n = prefix;
            }
            else if (digit == 0) {
                path.add(0, APPEND0(n));
                n = prefix;
            }
            else {
                path.add(0, DIVIDE2(n));
                n *= 2;
            }
        }

        return path;
    }

    public static List<String> solveRecursive(int n)
        throws IllegalArgumentException
    {
        if (n < 1)
            throw new IllegalArgumentException("value must be greater than 0");

        return solveRecursiveBody(n);
    }

    private static List<String> solveRecursiveBody(int n)
    {
        List<String> path;

        if (n == 4) { // solution found
            path = new ArrayList<>();
            path.add(START(n));
            return path;
        }

        int prefix = n / 10;
        int digit  = n % 10;

        if (digit == 4) {
            path = solveRecursiveBody(prefix);
            path.add(APPEND4(n));
            return path;
        }

        if (digit == 0) {
            path = solveRecursiveBody(prefix);
            path.add(APPEND0(n));
            return path;
        }

        path = solveRecursiveBody(n*2);
        path.add(DIVIDE2(n));
        return path;
    }

}
