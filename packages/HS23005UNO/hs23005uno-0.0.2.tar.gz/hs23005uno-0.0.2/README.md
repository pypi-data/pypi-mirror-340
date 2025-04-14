# HS23005UNO

**Librería para resolver sistemas de ecuaciones lineales y no lineales**  
Este proyecto incluye implementaciones de diferentes métodos numéricos como:  
- Gauss  
- Gauss-Jordan  
- Cramer  
- Descomposición LU  
- Jacobi  
- Gauss-Seidel  
- Bisección (para ecuaciones no lineales)

---

## Instalación

1. Clona el repositorio o descarga los archivos.

2. Navega a la carpeta del proyecto y ejecuta:

```bash
pip install HS23005UNO

# como ejecutarlo
con el comando python hs23005uno

## Ejemplo de uso
## con metodo Biseccion

Ejemplo para f(x) = x**3 + 4*x**2 - 10
Ingrese el límite inferior a: 1
Ingrese el límite superior b: 2
Ingrese la tolerancia (ej: 1e-5): 1e-5
Ingrese el numero maximo sw interacciones: 100
Resultado: Raíz aproximada = 1.365234375

##Ejemplo de uso para lo demas metodos

2x + y = 11
5x + 7y = 13

## en la terminal
Ingrese el numero de incognitas: 2
fila 1: 2 1
Fila 2: 5 7
Vector b: 11 13