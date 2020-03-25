import java.util.ArrayList;
import java.util.List;

class Solution {

    public static int solve(int n) throws IllegalArgumentException
    {
        // assume n is int with unlimited upper bound
        if (n < 0)
            throw new IllegalArgumentException("number must be at least 0");

        List<Integer> digits = splitDigits(n);

        int i = findTransition(digits);

        // System.out.println("start: " + n + " " + i);

        if (i == -1)
            return i;

        reorder(digits, i);

        return joinDigits(digits);
    }

    /*
     * Split an unsigned integer into decimal digits and return the list.
     */
    private static List<Integer> splitDigits(int n) {
        List<Integer> digits = new ArrayList<>();
        while (n > 0) {
            digits.add(0, n % 10);
            n = n / 10;
        }
        return digits;
    }

    /*
     * Join a list of unsigned decimal digits and return the integer value.
     */
    private static int joinDigits(List<Integer> digits) {
        int n = 0;
        for (int d : digits) {
            n = 10 * n + d;
        }
        return n;
    }

    /*
     * Given an ordered list of digits, find the rightmost index in the
     * interval [0, size-1] where adjacent digits increase in magnitude. The
     * returned value is the index of the left item of the pair or -1 if there
     * is no pair.
     */
    private static int findTransition(List<Integer> digits) {
        int size = digits.size();
        if (size > 1) {
            for (int i = size-1; i > 0; i--) {
                if (digits.get(i-1) < digits.get(i))
                    return i-1;  // transition
            }
        }
        return -1;
    }

    /*
     * Given a list of digits and a transition index, find the next highest
     * digit afer the transition and swap these two, then sort the tail of the
     * list ascending.
     */
    private static void reorder(List<Integer> digits, int transition) {
        int end = digits.size();
        Integer pivot = digits.get(transition);

        // find the index of the rightwards smallest element above pivot
        int swap = findLeastAbove(digits, transition+1, end, pivot);

        // exchange
        digits.set(transition, digits.get(swap));
        digits.set(swap, pivot);

        // sort tail; subList is backed by original
        List<Integer> tail = digits.subList(transition+1, end);
        tail.sort(null);
    }

    /*
     * Given a list of digits and range [start, end), find the least element
     * larger than threshold, and return its index, or -1 if no such element
     * exists.
     */
    private static int findLeastAbove(List<Integer> digits, int start, int end,
                                      Integer threshold) {
        int j = start;
        Integer winner = digits.get(start);

        for (int i = start+1; i < end; i++) {
            Integer digit = digits.get(i);
            if (digit < winner && digit > threshold) {
                winner = digit;
                j = i;
            }
        }

        return winner > threshold ? j : -1;
    }

}
