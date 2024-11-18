import re
import sys

def parse_equation(equation):
    """
    Parses a polynomial equation string into a dictionary of terms.

    Args:
        equation (str): The polynomial equation in the form "LHS = RHS".

    Returns:
        dict: A dictionary where keys are exponents, and values are coefficients.
    """
    # remove spaces
    equation = equation.replace(" ", "")
    # Split into left-hand side (LHS) and right-hand side (RHS)
    lhs, rhs = equation.split('=')

    # Regex pattern to match terms in the form of "+/- coefficient * X^exp"
    term_pattern = r'([+-]?\d+(\.\d+)?)\s*\*\s*X\^(\d+)'

    def terms_to_dict(terms):
        """
        Converts a list of terms into a dictionary of exponents and coefficients.

        Args:
            terms (list): List of matched terms from regex.

        Returns:
            dict: Dictionary of exponents and coefficients.
        """
        term_dict = {}
        for coeff, _, exp in terms:
            exp = int(exp)
            coeff = float(coeff)
            term_dict[exp] = term_dict.get(exp, 0) + coeff
        return term_dict

    # Parse terms from both sides
    lhs_terms = re.findall(term_pattern, lhs)
    rhs_terms = re.findall(term_pattern, rhs)

    # Convert to dictionaries
    lhs_dict = terms_to_dict(lhs_terms)
    rhs_dict = terms_to_dict(rhs_terms)

    # Normalize by moving RHS to LHS
    for exp, coeff in rhs_dict.items():
        lhs_dict[exp] = lhs_dict.get(exp, 0) - coeff

    return lhs_dict

def generate_reduced_form(term_dict):
    """
    Generates the reduced form of the polynomial.

    Args:
        term_dict (dict): Dictionary of exponents and coefficients.

    Returns:
        str: The reduced form of the polynomial equation.
    """
    terms = []
    for exp in sorted(term_dict.keys(), reverse=True):
        coeff = term_dict[exp]
        if coeff != 0:
            terms.append(f"{coeff:+} * X^{exp}")
    return " ".join(terms) + " = 0" if terms else "0 = 0"

def calculate_discriminant(a, b, c):
    """
    Calculates the discriminant for a quadratic equation.

    Args:
        a (float): Coefficient of X^2.
        b (float): Coefficient of X^1.
        c (float): Coefficient of X^0.

    Returns:
        float: The discriminant value.
    """
    return b * b - 4 * a * c

def calculate_sqrt(number):
    """
    Approximates the square root using Newton's method.

    Args:
        number (float): The number to find the square root of.

    Returns:
        float or None: The square root if non-negative, None otherwise.
    """
    if number < 0:
        return None
    x = number
    for _ in range(20):  # 20 iterations for precision
        x = 0.5 * (x + number / x)
    return x

def solve_quadratic(a, b, c):
    """
    Solves a quadratic equation using its coefficients.

    Args:
        a (float): Coefficient of X^2.
        b (float): Coefficient of X^1.
        c (float): Coefficient of X^0.

    Returns:
        str: The solution(s) or indication of complex roots.
    """
    discriminant = calculate_discriminant(a, b, c)
    if discriminant < 0:
        real_part = -b / (2 * a)
        imaginary_part = calculate_sqrt(abs(discriminant)) / (2 * a)
        return (f"The equation has two complex roots:\n"
                f"x1 = {real_part} + {imaginary_part}i\n"
                f"x2 = {real_part} - {imaginary_part}i")
    elif discriminant == 0:
        root = -b / (2 * a)
        return f"The discriminant is zero. The solution is:\n{root}"
    else:
        sqrt_disc = calculate_sqrt(discriminant)
        root1 = (-b + sqrt_disc) / (2 * a)
        root2 = (-b - sqrt_disc) / (2 * a)
        return (f"The discriminant is strictly positive: {discriminant}\n"
                f"The two solutions are:\n{root1}\n{root2}")

def solve_linear(b, c):
    """
    Solves a linear equation of the form bX + c = 0.

    Args:
        b (float): Coefficient of X.
        c (float): Constant term.

    Returns:
        str: The solution or indication of no/infinite solutions.
    """
    if b == 0:
        return "Infinite solutions" if c == 0 else "No solution"
    return f"The solution is:\n{-c / b}"

def main():
    """
    Main function to parse the equation, generate its reduced form,
    and solve it based on its degree.
    """
    if len(sys.argv) != 2:
        print("Usage: ./computor \"equation\"")
        sys.exit(1)
    
    equation = sys.argv[1]
    terms = parse_equation(equation)
    reduced_form = generate_reduced_form(terms)
    print(f"Reduced form: {reduced_form}")

    degree = max(terms.keys(), default=0)
    print(f"Polynomial degree: {degree}")

    if degree == 2:
        a, b, c = terms.get(2, 0), terms.get(1, 0), terms.get(0, 0)
        print(solve_quadratic(a, b, c))
    elif degree == 1:
        b, c = terms.get(1, 0), terms.get(0, 0)
        print(solve_linear(b, c))
    elif degree == 0:
        if terms.get(0, 0) == 0:
            print("Every real number is a solution.")
        else:
            print("There is no solution.")
    else:
        print("The polynomial degree is strictly greater than 2, I can't solve.")

if __name__ == "__main__":
    main()
