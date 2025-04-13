

**FF23004UNO** es una librería de Python diseñada para resolver 
sistemas de ecuaciones lineales y no lineales
utilizando diversos métodos numéricos clásicos. 
Esta librería está pensada con fines educativos y académicos.

---

##Instalación

Una vez publicada en PyPI, podrás instalar la librería con:

```bash
pip install FF23004UNO
```

---

## 📚 Métodos disponibles

### 📐 Sistemas de ecuaciones lineales:

- `eliminacion_gauss(A, b)`
- `gauss_jordan(A, b)`
- `cramer(A, b)`
- `descomposicion_lu(A, b)`
- `jacobi(A, b, x0=None, tol=1e-10, max_iter=100)`
- `gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=100)`

### 🔁 Ecuaciones no lineales:

- `biseccion(f, a, b, tol=1e-10, max_iter=100)`

---

## 🧪 Ejemplo de uso

```python
import numpy as np
from FF23004UNO import eliminacion_gauss, biseccion

A = np.array([[2.0, 1.0], [5.0, 7.0]])
b = np.array([11.0, 13.0])

sol_gauss = eliminacion_gauss(A.copy(), b.copy())
print("Solución por Gauss:", sol_gauss)

raiz = biseccion(lambda x: x**2 - 4, 0, 3)
print("Raíz por bisección:", raiz)
```

---

## 🔧 Requisitos

- Python 3.7+
- `numpy`
- `scipy`

---

## 🧑‍💻 Autor

- **Jonathan Fuentes**
- Universidad Nacional de EL Salvador
- Ingeniera desarrollo de software

---

## 📝 Licencia

Este proyecto se distribuye únicamente con fines educativos.
