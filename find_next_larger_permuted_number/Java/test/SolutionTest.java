import static org.junit.Assert.*;

import org.junit.Test;

public class SolutionTest {

    @Test(expected = IllegalArgumentException.class)
    public void test_raises_with_negative_input() throws Exception {
        Solution.solve(-1);
    }

    @Test
    public void test_single_digit_has_no_solution() throws Exception {
        assertEquals(Solution.solve(1), -1);
    }

    @Test
    public void test_uniform_digits_have_no_solution() throws Exception {
        assertEquals(Solution.solve(11), -1);
    }

    @Test
    public void test_descending_edge_case_has_no_solution() throws Exception {
        assertEquals(Solution.solve(21), -1);
    }

    @Test
    public void test_solves_ascending_edge_case() throws Exception {
        assertTrue(Solution.solve(12) == 21);
    }

    @Test
    public void test_only_changes_rightmost_transition() throws Exception {
        assertTrue(Solution.solve(1212) == 1221);
    }

    @Test
    public void test_sorts_tail() throws Exception {
        assertTrue(Solution.solve(121221) == 122112);
    }

    // examples

    @Test
    public void test_solve_example_11123() throws Exception {
        assertTrue(Solution.solve(11123) == 11132);
    }

    @Test
    public void test_solve_example_1234321() throws Exception {
        assertTrue(Solution.solve(1234321) == 1241233);
    }

    @Test
    public void test_solve_example_123987() throws Exception {
        assertTrue(Solution.solve(123987) == 127389);
    }

}
