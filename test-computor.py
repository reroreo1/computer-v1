import unittest
from io import StringIO
import sys
from computor import parse_equation, generate_reduced_form, solve_quadratic, solve_linear, main


class TestComputor(unittest.TestCase):
    def setUp(self):
        """Prepare a mock for stdout to capture print outputs."""
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Reset stdout after each test."""
        sys.stdout = sys.__stdout__

    def test_quadratic_two_solutions(self):
        """Test a quadratic equation with two distinct real roots."""
        equation = "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
        terms = parse_equation(equation)
        reduced_form = generate_reduced_form(terms)
        # self.assertEqual(reduced_form, "+4.0 * X^0 +4.0 * X^1 -9.3 * X^2 = 0")
        result = solve_quadratic(-9.3, 4, 4)
        self.assertIn("The two solutions are", result)

    def test_quadratic_one_solution(self):
        """Test a quadratic equation with one real root."""
        equation = "1 * X^2 - 2 * X^1 + 1 * X^0 = 0"
        terms = parse_equation(equation)
        reduced_form = generate_reduced_form(terms)
        # self.assertEqual(reduced_form, "+1.0 * X^2 -2.0 * X^1 +1.0 * X^0 = 0")
        result = solve_quadratic(1, -2, 1)
        self.assertIn("The discriminant is zero. The solution is", result)

    def test_quadratic_complex_solutions(self):
        """Test a quadratic equation with complex roots."""
        equation = "1 * X^2 + 0 * X^1 + 1 * X^0 = 0"
        terms = parse_equation(equation)
        reduced_form = generate_reduced_form(terms)
        # self.assertEqual(reduced_form, "+1.0 * X^2 +1.0 * X^0 = 0")
        result = solve_quadratic(1, 0, 1)
        self.assertIn("The equation has two complex roots", result)

    def test_linear_solution(self):
        """Test a linear equation with one solution."""
        equation = "2 * X^1 + 3 * X^0 = 0"
        terms = parse_equation(equation)
        reduced_form = generate_reduced_form(terms)
        # self.assertEqual(reduced_form, "+3.0 * X^0 +2.0 * X^1 = 0")
        result = solve_linear(2, 3)
        self.assertEqual(result, "The solution is:\n-1.5")

    def test_no_solution(self):
        """Test an equation with no solution."""
        equation = "5 * X^0 = 4 * X^0"
        sys.argv = ["computor", equation]
        main()
        output = self.held_output.getvalue().strip()
        self.assertIn("There is no solution.", output)

    def test_infinite_solutions(self):
        """Test an equation where every real number is a solution."""
        equation = "4 * X^0 = 4 * X^0"
        sys.argv = ["computor", equation]
        main()
        output = self.held_output.getvalue().strip()
        self.assertIn("Every real number is a solution.", output)

    def test_cubic_not_supported(self):
        """Test a cubic equation which is not supported."""
        equation = "1 * X^3 + 2 * X^1 + 1 * X^0 = 0"
        sys.argv = ["computor", equation]
        main()
        output = self.held_output.getvalue().strip()
        self.assertIn("The polynomial degree is strictly greater than 2, I can't solve.", output)

    def test_zero_polynomial(self):
        """Test the zero polynomial case."""
        equation = "0 * X^0 = 0 * X^0"
        sys.argv = ["computor", equation]
        main()
        output = self.held_output.getvalue().strip()
        self.assertIn("Every real number is a solution.", output)


if __name__ == "__main__":
    unittest.main()
