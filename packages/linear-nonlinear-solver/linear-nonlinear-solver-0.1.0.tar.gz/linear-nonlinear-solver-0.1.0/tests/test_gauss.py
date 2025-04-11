from linear_nonlinear_solver.gauss import eliminar_gauss
import numpy as np

def test_eliminar_gauss():
    # Caso de prueba 1: Sistema de ecuaciones 2x2
    A = np.array([[2, 1], [1, -1]])
    b = np.array([1, -1])
    expected = np.array([1, 0])
    result = eliminar_gauss(A, b)
    assert np.allclose(result, expected), f"Expected {expected}, but got {result}"

    # Caso de prueba 2: Sistema de ecuaciones 3x3
    A = np.array([[3, 2, -4], [2, 3, 3], [5, -3, 1]])
    b = np.array([3, 15, 14])
    expected = np.array([1, 2, 3])
    result = eliminar_gauss(A, b)
    assert np.allclose(result, expected), f"Expected {expected}, but got {result}"

    # Caso de prueba 3: Sistema sin solución
    A = np.array([[1, 2], [2, 4]])
    b = np.array([1, 2])
    try:
        eliminar_gauss(A, b)
        assert False, "Expected an exception for a singular matrix"
    except np.linalg.LinAlgError:
        pass  # Se espera una excepción

    # Caso de prueba 4: Sistema con infinitas soluciones
    A = np.array([[1, 2], [2, 4]])
    b = np.array([2, 4])
    try:
        eliminar_gauss(A, b)
        assert False, "Expected an exception for a singular matrix"
    except np.linalg.LinAlgError:
        pass  # Se espera una excepción

    # Caso de prueba 5: Sistema de ecuaciones 2x2 con decimales
    A = np.array([[0.5, 1.5], [1.0, 2.0]])
    b = np.array([2.0, 3.0])
    expected = np.array([1.0, 1.0])
    result = eliminar_gauss(A, b)
    assert np.allclose(result, expected), f"Expected {expected}, but got {result}"