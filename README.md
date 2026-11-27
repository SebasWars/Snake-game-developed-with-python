# Snake con Python y pygame

Una implementación del clásico Snake, hecha para practicar Python y, sobre todo, para entender la **lógica que hay detrás de un juego**: el bucle principal, el estado, el movimiento por celdas y la separación entre lógica y dibujado.

El juego en sí es sencillo. Lo interesante es cómo está pensado.

<!-- Añade aquí un GIF o captura del juego -->
<!-- ![Demo](docs/demo.gif) -->

## Cómo ejecutarlo

```bash
git clone https://github.com/SebasWars/Snake-game-developed-with-python.git
cd Snake-game-developed-with-python
pip install -r requirements.txt
python app.py
```

**Controles**

| Tecla | Acción |
| --- | --- |
| `Espacio` | Empezar / volver a jugar tras un game over |
| Flechas | Cambiar la dirección de la serpiente |

## Qué demuestra este proyecto

- Un **bucle de juego** que separa eventos, actualización de lógica y dibujado.
- Una **máquina de estados** (`START`, `PLAYING`, `GAME OVER`) que decide qué se actualiza y qué se dibuja en cada momento.
- **Movimiento desacoplado de los FPS**: el juego se dibuja a 60 FPS, pero la serpiente avanza según un intervalo de tiempo propio.
- Un **modelo de datos simple**: el tablero se trabaja en coordenadas de celda y solo se convierte a píxeles al dibujar.
- Uso de **vectores de dirección** para mover la serpiente, validar giros y hacer crecer el cuerpo.

## Flujo general

En cada vuelta del bucle principal ocurre siempre lo mismo, en este orden:

1. **Eventos:** se leen las teclas. Lo que significan depende del estado actual del juego.
2. **Lógica:** solo si el estado es `PLAYING` y ha pasado el tiempo suficiente, se mueve la serpiente, se comprueba si come y se comprueban las colisiones.
3. **Dibujado:** se pinta el fondo, la cuadrícula, la serpiente, la comida y el score. Si no se está jugando, se pinta en su lugar la pantalla de inicio o de game over.

## La lógica, paso a paso

### 1. El tablero son celdas, no píxeles

La ventana se divide en una cuadrícula:

```
COLS = WIDTH  // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
```

Todo lo que importa para el juego (la serpiente, la comida, las colisiones) vive en **coordenadas de celda** `(x, y)`. Los píxeles solo aparecen al dibujar, multiplicando por `CELL_SIZE`.

La regla que mantiene todo coherente: **x se relaciona con columnas y ancho; y con filas y altura**. Así funciona con cualquier tamaño de ventana, no solo con tableros cuadrados.

### 2. La serpiente es una lista de tuplas

```
SNAKE = [(12, 10), (11, 10), (10, 10), (9, 10)]
```

El primer elemento es la cabeza y el último es la cola. No hay objetos ni clases: una lista ordenada de posiciones es suficiente.

### 3. Mover la serpiente

Moverla es un cambio de posiciones en dos pasos:

1. Se calcula la **nueva cabeza** sumando el vector de dirección a la cabeza actual.
2. Cada pieza ocupa la posición de la pieza que tenía delante, recorriendo la lista desde la cola hacia la cabeza.

Las direcciones son vectores: `UP = (0, -1)`, `DOWN = (0, 1)`, `LEFT = (-1, 0)`, `RIGHT = (1, 0)`.

### 4. Evitar el giro de 180°

Una serpiente que va a la derecha no puede girar directamente a la izquierda, porque chocaría con su propio cuello. Se detecta de forma elegante con vectores: dos direcciones son opuestas si **su suma es `(0, 0)`**.

### 5. Movimiento por tiempo, no por frame

El bucle se ejecuta a 60 FPS, pero la serpiente solo avanza cuando ha pasado un intervalo (`MOVEMENT_INTERVAL`, en milisegundos). Para ello se guarda el instante del último movimiento y se compara con `pygame.time.get_ticks()`. Así la velocidad del juego no depende de la potencia del ordenador y se puede ajustar cambiando un solo valor.

### 6. Comer y crecer

Cuando la cabeza llega a la celda de la comida:

- se genera una comida nueva en una celda que no esté ocupada por la serpiente,
- se suma un punto,
- se añade una pieza nueva al final del cuerpo.

La parte delicada es **dónde colocar esa pieza nueva** (ver la siguiente sección).

### 7. Colisiones

- **Con el muro:** la cabeza sale del rango `0 .. COLS-1` en x o `0 .. ROWS-1` en y.
- **Consigo misma:** la cabeza coincide con alguna pieza del cuerpo (`SNAKE[1:]`).

### 8. Dibujado eficiente y separado de la lógica

- La **cuadrícula** se dibuja una sola vez en una superficie aparte, y en cada frame solo se copia a la pantalla.
- El **score** es una imagen de texto que se vuelve a renderizar **solo cuando el valor cambia** (comparando con el último valor dibujado), no 60 veces por segundo.
- Las funciones que **calculan** (mover, comer, colisionar) no dibujan, y las que **dibujan** no modifican el estado.

### 9. Reinicio

Al volver a jugar tras un game over se restablece todo el estado de la partida: la serpiente, la dirección, el score, la comida y el temporizador de movimiento.

## Un bug interesante: la pieza que aparecía en el sitio equivocado

Mi primera versión colocaba la pieza nueva a partir de la cola, en sentido contrario a la **dirección de la cabeza**. Funcionaba solo cuando la serpiente iba recta. Si había girado, la cola apuntaba en otra dirección distinta a la de la cabeza, y la pieza aparecía una celda a la derecha o a la izquierda de donde debía.

La causa era un supuesto incorrecto: la cabeza y la cola **no** se mueven en la misma dirección salvo que la serpiente esté recta.

La solución fue calcular la dirección **de la cola**, no la de la cabeza:

> dirección de la cola = posición de la cola − posición de la penúltima pieza
>
> pieza nueva = cola + dirección de la cola

Después apareció otro error al implementarlo: usé la resta como si fuera una posición, y la pieza salía en la esquina superior izquierda del tablero. Una resta de dos posiciones da un **vector** (una dirección), no una **posición**. Para obtener una posición hay que sumar ese vector a un punto de partida. Esa confusión entre vector y posición es la que más me hizo aprender en el proyecto.

## Estructura del proyecto

```
.
├── app.py             # Todo el juego
├── requirements.txt   # Dependencias (pygame)
└── README.md
```

## Posibles mejoras

- Guardar la puntuación máxima entre partidas.
- Aumentar la velocidad a medida que sube el score.
- Agrupar el estado en una clase `Game` en lugar de variables globales.
- Separar la lógica del dibujado en módulos distintos y añadir tests para la lógica pura (movimiento, colisiones, crecimiento).
- Generar la comida a partir de la lista de celdas libres en lugar de reintentar con recursión.

## Tecnologías

- Python 3
- [pygame](https://www.pygame.org/)
