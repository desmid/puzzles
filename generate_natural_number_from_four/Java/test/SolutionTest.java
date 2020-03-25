import static org.junit.Assert.*;

import java.util.List;
import java.util.Arrays;

import org.junit.Test;

public class SolutionTest {

    @Test(expected = IllegalArgumentException.class)
    public void test_solve_0_should_raise() {
        Solution.solveIterative(0);
        Solution.solveRecursive(0);
    }

    @Test
    public void test_solve_4_should_pass_immediately() {
        List<String> expect = Arrays.asList
            (
             Solution.START(4)
             );
        assertEquals(Solution.solveIterative(4), expect);
        assertEquals(Solution.solveRecursive(4), expect);
    }

    @Test
    public void test_solve_one_digit() {
        List<String> expect = Arrays.asList
            (
             Solution.START(4),
             Solution.DIVIDE2(2),
             Solution.DIVIDE2(1)
             );
        assertEquals(Solution.solveIterative(1), expect);
        assertEquals(Solution.solveRecursive(1), expect);
    }

    @Test
    public void test_solve_13() {
        List<String> expect = Arrays.asList
            (
             Solution.START(4),
             Solution.DIVIDE2(2),
             Solution.DIVIDE2(1),
             Solution.APPEND0(10),
             Solution.APPEND4(104),
             Solution.DIVIDE2(52),
             Solution.DIVIDE2(26),
             Solution.DIVIDE2(13)
             );
        assertEquals(Solution.solveIterative(13), expect);
        assertEquals(Solution.solveRecursive(13), expect);
    }

    @Test
    public void test_solve_17() {
        List<String> expect = Arrays.asList
            (
             Solution.START(4),
             Solution.DIVIDE2(2),
             Solution.APPEND4(24),
             Solution.DIVIDE2(12),
             Solution.DIVIDE2(6),
             Solution.DIVIDE2(3),
             Solution.APPEND4(34),
             Solution.DIVIDE2(17)
             );
        assertEquals(Solution.solveIterative(17), expect);
        assertEquals(Solution.solveRecursive(17), expect);
    }

}
