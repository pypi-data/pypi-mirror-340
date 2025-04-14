# SR23002UNO

**SR23002UNO** es una librería de Python diseñada para resolver sistemas de ecuaciones **lineales y no lineales** de forma eficiente y didáctica.

---

## Métodos disponibles

✅ Bisección  
✅ Crammer  
✅ Descomposición LU  
✅ Eliminación de Gauss  
✅ Gauss-Jordan  
✅ Gauss-Seidel  
✅ Jacobi  

---


## ⚙️ Instalación

Desde **PyPI**:

```bash
pip install SR23002UNO
```

Para actualizar a la última versión:

```bash
pip install SR23002UNO --upgrade
```

---

## 💡 Ejemplos de uso

### Resolver sistemas de ecuaciones lineales con Cramer

```python
from SR23002UNO import cramer
import numpy as np

A = np.array([[2, -1, 1], [0, 2, -1], [1, -1, 0]])
b = np.array([3, 1, 1])
solucion = cramer.cramer_solver(A, b)

print("Solución:", solucion)
```

---

## 🧑‍💻 Desarrollo

### Librerías necesarias para preparar una nueva versión:

```bash
pip install setuptools twine
```

### Crear distribución:

```bash
python setup.py sdist bdist_wheel
```

### Subir a PyPI:
```bash
twine upload dist/*
```
O usa el comando:
```bash
python -m twine upload dist/*
```

---

## 🚀 Repositorio

El código fuente está disponible en:

👉 [https://github.com/sr230002/CDA135-GT02-SR23002UNO](https://github.com/sr230002/CDA135-GT02-SR23002UNO)

---

## 📄 Licencia

MIT License © David Enrique Sixco Ramos

