import numpy as np

# Método de Gauss-Seidel
def gauss_seidel(a, b, x0=None, tol=1e-10, max_iter=100):
    """
    Método iterativo de Gauss-Seidel para resolver sistemas lineales.
    """
    n = len(a)
    x = x0 if x0 is not None else np.zeros(n)

    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(a[i][j] * x_new[j] for j in range(i))
            s2 = sum(a[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / a[i][i]
        
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new.tolist()
        
        x = x_new

    return x.tolist()
