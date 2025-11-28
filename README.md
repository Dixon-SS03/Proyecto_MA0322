PROYECTO FINAL – MA0322 Álgebra Lineal

Profesor: Randy Wynta Banton
Repositorio GitHub: https://github.com/Dixon-SS03/Proyecto_MA0322.git

Fecha: 28/11/2025
Hora: 5:00 pm

Responsables del Proyecto

David Díaz López
GitHub: https://github.com/Daviddl20

Dixon Sánchez Soza
GitHub: https://github.com/Dixon-SS03

Grimaldi Solano Tijerino
GitHub: https://github.com/guriSan25

Descripción General del Proyecto

Este proyecto desarrollado para el curso MA0322 – Álgebra Lineal de la Universidad de Costa Rica consiste en una aplicación web educativa enfocada en resolver problemas matemáticos fundamentales del curso mediante interfaces dinámicas, intuitivas y visuales.

El sistema incluye tres módulos principales completamente interactivos:

Determinantes (Matrices 2×2, 3×3 y 4×4)

Intersección de Planos en R³

Triángulos en el Plano R²

Cada módulo presenta el proceso paso a paso, validaciones estrictas y herramientas visuales diseñadas con fines académicos y explicativos.

Módulos Principales
1. Módulo de Determinantes

Permite calcular determinantes de matrices cuadradas de tamaño 2×2, 3×3 y 4×4, con métodos alternativos para reforzar el aprendizaje.

Métodos disponibles

2×2: Método directo (det = ad − bc)

3×3:

Regla de Sarrus

Método de Cofactores

Eliminación Gaussiana

4×4:

Cofactores con Sarrus (subdeterminantes 3×3)

Cofactores con cofactores

Método de Gauss

Características del módulo

Validación numérica estricta

Visualización progresiva de matrices

Modo entrenamiento (muestra cada paso en orden)

Descarga del procedimiento en archivo .txt

Selección de fila o columna para expansión en 4×4

Ruta:

/determinantes

2. Módulo de Intersección de Planos

Permite ingresar dos planos en formato libre, con términos en cualquier orden y en cualquier lado del signo igual, y determina su relación geométrica.

Casos que analiza

Intersección en una recta:

Muestra reducción Gauss-Jordan completa

Calcula punto y vector dirección

Expresa la recta en forma paramétrica

Planos paralelos:

Determina si no se intersecan

Calcula distancia entre ellos

Planos coincidentes:

Identifica cuando ambos representan el mismo plano

Funciones adicionales

Validación exhaustiva de ecuaciones

Manejo de números en ambos lados del igual

Cuatro ejemplos preestablecidos para práctica inmediata

Ruta:

/planos

3. Módulo de Triángulos – Plano R²

Genera y analiza un triángulo a partir de tres puntos seleccionados en un lienzo interactivo.

Cálculos incluidos

Longitudes de los lados

Ángulos internos mediante ley de cosenos

Clasificación por lados y ángulos

Área (Herón o método determinante)

Perímetro

Representación gráfica sobre un canvas

Pasos matemáticos detallados

Ruta:

/triangulos

Arquitectura del Proyecto
```
MA0322/
├── service.py
├── controllers/
│   └── planos_controller.py
├── models/
│   ├── plano.py
│   ├── triangulos_model.py
│   └── determinantes/
│       ├── calcularDeterminante.py
│       ├── determinante2x2.py
│       ├── determinante3x3Sarrus.py
│       ├── determinante3x3Cofactores.py
│       ├── determinante4x4Cofactores.py
│       ├── determinantesGauss.py
│       └── validaciones.py
├── utils/
│   ├── commonUtils.py
│   ├── matematicas.py
│   ├── triangulos_service.py
│   └── determinantes_service.py
└── static/
    ├── views/
    │   ├── index.html
    │   ├── planos.html
    │   ├── triangulos.html
    │   └── determinantes.html
    ├── css/
    │   ├── styles.css
    │   └── determinantes.css
    └── js/
        ├── app.js
        ├── triangulos.js
        └── determinantes.js
```
Requisitos del Sistema

Python 3.8+

Navegador moderno (Chrome, Firefox, Edge, Safari)

No requiere instalar librerías externas

Cómo Ejecutarlo
1. Iniciar el servidor
python service.py

2. Abrir en el navegador
http://localhost:8000

Rutas Disponibles

Página principal:

http://localhost:8000/


Triángulos:

http://localhost:8000/triangulos


Determinantes:

http://localhost:8000/determinantes


Intersección de planos:

http://localhost:8000/planos

Finalidad Académica

El proyecto sirve como herramienta de apoyo para estudiantes, dando la posibilidad de:

Repasar el contenido del curso mediante ejemplos interactivos

Visualizar matemáticamente los conceptos

Entender los procedimientos paso a paso

Validar resultados de ejercicios

Prepararse para evaluaciones mediante práctica guiada

Conclusión General

Este proyecto integra de manera efectiva los conceptos esenciales del curso MA0322 mediante tres módulos complementarios que ofrecen cálculo, visualización y explicación detallada. La aplicación combina rigor matemático con una interfaz accesible, permitiendo al estudiante reforzar los temas vistos en clase, explorar ejemplos prácticos y comprender a profundidad los procesos detrás de cada resultado.

Se trata de un recurso didáctico completo, preciso y bien estructurado, que facilita el aprendizaje autónomo y mejora la comprensión de la geometría analítica y del álgebra lineal.
