"""PW2 Lab B Part 2: compare gradient descent, Newton, and SLSQP.

Run: python warmup.py
"""

from scipy.optimize import minimize, newton


# Part 2A: a convex function with one global minimum.
def f(x):
    return (x - 3)**2 + 1


def df(x):
    return 2 * (x - 3)


def d2f(x):
    return 2.0


# Part 2B: a function with two minima and one maximum.
def g(x):
    return x**4 - 3 * x**2 + x + 5


def dg(x):
    return 4 * x**3 - 6 * x + 1


def d2g(x):
    return 12 * x**2 - 6


def gradient_descent(derivative, x0, lr=0.05, tol=1e-10, max_iter=10000):
    """Take downhill steps until consecutive x values are very close."""
    x = float(x0)
    for iteration in range(1, max_iter + 1):
        x_next = x - lr * derivative(x)
        if abs(x_next - x) < tol:
            return x_next, iteration
        x = x_next
    raise RuntimeError("Gradient descent did not converge.")


def stationary_type(curvature):
    if curvature > 0:
        return "minimum"
    if curvature < 0:
        return "maximum"
    return "inconclusive (zero second derivative)"


def compare_methods(name, objective, derivative, second_derivative, x0):
    print(f"\n{name}, starting at x0 = {x0:g}")

    x_gd, iterations = gradient_descent(derivative, x0)
    print(
        f"Gradient descent: x = {x_gd:.9f}, value = {objective(x_gd):.9f}"
        f" ({iterations} steps, lr = 0.05)"
    )

    # Newton solves the derivative = 0; it is not itself a minimizer.
    x_newton = newton(derivative, x0, fprime=second_derivative, tol=1e-12)
    curvature = second_derivative(x_newton)
    print(
        f"Newton:           x = {x_newton:.9f}, value = {objective(x_newton):.9f}"
        f", second derivative = {curvature:.9f}"
        f" -> {stationary_type(curvature)}"
    )

    # minimize passes a one-element array to the objective.
    result = minimize(
        lambda x: objective(x[0]),
        x0=[x0],
        method="SLSQP",
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    if not result.success:
        raise RuntimeError(f"SLSQP failed: {result.message}")
    x_slsqp = float(result.x[0])
    print(f"SLSQP:            x = {x_slsqp:.9f}, value = {objective(x_slsqp):.9f}")


def main():
    compare_methods("Part 2A: f(x) = (x - 3)^2 + 1", f, df, d2f, x0=0.0)
    for x0 in (0.0, 2.0):
        compare_methods("Part 2B: g(x) = x^4 - 3x^2 + x + 5", g, dg, d2g, x0)


if __name__ == "__main__":
    main()
