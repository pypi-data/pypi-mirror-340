# CG19057UNO

## Descripción

CG19057UNO es una librería en Python diseñada para resolver sistemas de ecuaciones lineales y no lineales utilizando métodos numéricos como:

- Eliminación de Gauss  
- Gauss-Jordan  
- Regla de Cramer  
- Descomposición LU  
- Método de Jacobi  
- Método de Gauss-Seidel  
- Método de Bisección  

_____________________________________________________________________________________________________________

## Requisitos

- Python 3.6 o superior  
- Bibliotecas necesarias:
  - `numpy`
  - `scipy`

Para instalar las dependencias necesarias, ejecuta:

```bash
pip install numpy scipy
```
```bash
pip install pytest
```
_____________________________________________________________________________________________________________

## Instalacion: 

La libreria se puede instalar directamente desde PyPI con el siguiente comando:

```bash
pip install CG19057UNO
```
_____________________________________________________________________________________________________________

## Pruebas:

Para ejecutar las pruebas unitarias incluidas en el proyecto ejecutar: 
```bash
python -m pytest tests/
```

Para ejecutar los ejemplos incluidos en el proyecto ejecutar: 
```bash
python ejemplos_todosMetodos.py
```
_____________________________________________________________________________________________________________

## Uso:

Ejemplos de como usar la libreria:

from CG19057UNO.EcuacionesLineales import elimina_Gauss

from CG19057UNO.EcuacionesNoLineales import biseccion 

#Ejemplo usando eliminacion de Gauss

#Sistema de ecuaciones:

#x + 2y + z = 7

#3x + y + z = 5

#2x + 3y - z = 3

def ejemplo_elimina_Gauss():
    
    A = [
        
        [1, 2, 1],
        
        [3, 1, 1],
        
        [2, 3, -1]
    
    ]
    
    b = [7, 5, 3]
   
    solucion = elimina_Gauss(A, b)
   
    print("Solucion eliminacion de Gauss:", solucion)

#Ejemplo usando Biseccion

def ejemplo_biseccion():
    
    f = lambda x: x**2 - 4
    
    raiz = biseccion(f, 0, 3)
    
    print("Bisección:", raiz)

_____________________________________________________________________________________________________________

## Metodos implementados: 

Para sistemas de ecuaciones lineales
- Eliminacion de Gauss: elimina_Gauss(coeficiente_M, vector_I)
- Gauss-Jordan:gauss_Jordan(coeficiente_M, vector_I)
- Crammer: crammer(coeficiente_M, vector_I)
- Descomposicion LU: descomposicion_LU(coeficiente_M, vector_I)
- Jacobi: jacobi(coeficiente_M, vector_I, estimacion_Ini=None, tolerancia=1e-6, max_Iteraciones=100)
- Gauss-Seidel: gauss_seidel(coeficiente_M, vector_I, estimacion_Ini=None, tolerancia=1e-6 max_iteraciones=100)

Para sistemas de ecuaciones no lineales
- Biseccion: biseccion(funcion_Resolver, extremo_Izquierdo, extremo_derecho, tolerancia=1e-6, max_iteraciones=100) 
_____________________________________________________________________________________________________________

## Licencia:
Este proyecto esta bajo la licencia MIT. Consultar el archivo LICENSE para mas detalles.

