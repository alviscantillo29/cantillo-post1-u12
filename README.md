# cantillo-post1-u12 — Computación Cuántica y Criptografía Post-Cuántica

- **Estudiante:** Alvis Cantillo
- **Código:** 1152332
- **Asignatura:** Arquitectura de Computadores — Unidad 12
- **Repositorio:** `cantillo-post1-u12`

Este repositorio contiene el desarrollo de las dos partes del laboratorio de la Unidad 12: la implementación y simulación de circuitos cuánticos en Python con Qiskit sobre `AerSimulator` (Parte 1) y el análisis técnico del impacto cuántico en la ciberseguridad junto con planes de migración hacia criptografía post-cuántica (Parte 2, en [`docs/analisis-pqc.md`](docs/analisis-pqc.md)).

---

## Estructura del Repositorio

```text
cantillo-post1-u12/
├── README.md
├── docs/
│   └── analisis-pqc.md
├── src/
│   ├── bell_state.py
│   ├── deutsch_jozsa.py
│   ├── grover.py
│   └── grover_noise.py
└── capturas/
    └── .gitkeep
```

---

## Parte 1: Laboratorio de Circuitos Cuánticos con Qiskit

### Requisitos e Instrucciones de Ejecución

Los scripts están escritos para **Python 3.10+**, **Qiskit**, **Qiskit Aer** y **Matplotlib**:

```bash
pip install qiskit qiskit-aer matplotlib
python src/bell_state.py
python src/deutsch_jozsa.py
python src/grover.py
python src/grover_noise.py
```

Cada script imprime el diagrama del circuito en consola, reporta los conteos de $1\,024$ *shots* y guarda automáticamente su histograma en la carpeta `capturas/`. *(Nota: En el entorno de generación sin acceso a Qiskit, la carpeta `capturas/` contiene `.gitkeep` para poblarse al ejecutar los scripts localmente).*

---

### 1. Estado de Bell (`src/bell_state.py`)

El circuito aplica una compuerta Hadamard ($H$) sobre $q_0$ para generar superposición y una compuerta `CNOT` ($CX$) controlada por $q_0$ hacia $q_1$, produciendo el estado máximamente entrelazado $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$.

```text
     ┌───┐     ┌─┐   
q_0: ┤ H ├──■──┤M├───
     └───┘┌─┴─┐└╥┘┌─┐
q_1: ─────┤ X ├─╫─┤M├
          └───┘ ║ └╥┘
c: 2/═══════════╩══╩═
                0  1 
```

### 2. Algoritmo de Deutsch-Jozsa (`src/deutsch_jozsa.py`)

Evalúa si una función booleana $f:\{0,1\}^2 \to \{0,1\}$ es constante o balanceada en una sola consulta al oráculo $U_f$, utilizando $2$ qubits de entrada y $1$ qubit auxiliar (*ancilla*) inicializado en $|1\rangle$:
- **Oráculo balanceado** ($f(x_0, x_1) = x_0 \oplus x_1$): implementado con dos compuertas `CX(0,2)` y `CX(1,2)`. Tras la interferencia final, los qubits de entrada colapsan en $|11\rangle$ (estado distinto de $|00\rangle$).
- **Oráculo constante** ($f(x_0, x_1) = 1$): implementado con una compuerta `X(2)`. Al no introducir cambio de fase relativo dependiente de la entrada, la medición devuelve $|00\rangle$ con $100\%$ de probabilidad.

### 3. Algoritmo de Grover sin Ruido (`src/grover.py`)

Busca el estado marcado $|11\rangle$ en un espacio de $N = 2^2 = 4$ estados mediante una superposición uniforme (`H` en ambos qubits), un oráculo de fase (`CZ(0,1)` que invierte el signo de $|11\rangle$) y el operador de difusión (`H` $\to$ `X` $\to$ `CZ` $\to$ `X` $\to$ `H`).

### 4. Algoritmo de Grover con Ruido Despolarizante (`src/grover_noise.py`)

Reutiliza el circuito de Grover de $n=2$ qubits y lo ejecuta sobre `AerSimulator(noise_model=...)` con un modelo de error despolarizante de $p_{1q} = 0.001$ en compuertas de un qubit (`h`, `x`) y $p_{2q} = 0.01$ en compuertas de dos qubits (`cz`).

---

### Resultados Esperados y Plantilla de Registro ($1\,024$ *shots*)

| Experimento | Estado(s) Esperado(s) | Probabilidad Teórica | Conteo Observado (Local) | Porcentaje Observado |
| :--- | :---: | :---: | :---: | :---: |
| **Estado de Bell** (`bell_state.py`) | $|00\rangle$, $|11\rangle$ | $50\%$ / $50\%$ | `[Pendiente ejecución local]` | `[Pendiente]` |
| **Deutsch-Jozsa Balanceado** (`deutsch_jozsa.py`) | $|11\rangle$ (no-$|00\rangle$) | $100\%$ en $|11\rangle$ | `[Pendiente ejecución local]` | `[Pendiente]` |
| **Deutsch-Jozsa Constante** (`deutsch_jozsa.py`) | $|00\rangle$ | $100\%$ en $|00\rangle$ | `[Pendiente ejecución local]` | `[Pendiente]` |
| **Grover Ideal ($n=2$)** (`grover.py`) | $|11\rangle$ | $100\%$ | `[Pendiente ejecución local]` | `[Pendiente]` |
| **Grover con Ruido** (`grover_noise.py`) | $|11\rangle$ dominante + ruido | $>95\%$ en $|11\rangle$ | `[Pendiente ejecución local]` | `[Pendiente]` |

---

### Interpretación Cuántica

1. **¿Por qué basta una sola iteración de Grover para $n=2$ qubits?**
   En un espacio de búsqueda de $N = 2^2 = 4$ elementos con $M = 1$ solución marcada, el ángulo inicial entre la superposición uniforme y el subespacio ortogonal a la solución es $\theta = \arcsin(\sqrt{M/N}) = \arcsin(1/2) = 30^\circ$. Cada iteración de Grover (oráculo + difusor) rota el vector de estado en un ángulo de $2\theta = 60^\circ$ hacia la solución. Tras $k = 1$ iteración, el ángulo resultante es $3\theta = 90^\circ$, por lo que la probabilidad teórica de medir $|11\rangle$ es exactamente $\sin^2(90^\circ) = 1.0$ ($100\%$). Aplicar una segunda iteración sobre-rotaría el estado a $5\theta = 150^\circ$, reduciendo la probabilidad a $\sin^2(150^\circ) = 25\%$.

2. **Ventaja de consulta en Deutsch-Jozsa ($n=2$):**
   Para $n=2$ bits existen $2^n = 4$ posibles entradas. Un algoritmo clásico determinista necesita evaluar en el peor caso $\frac{2^n}{2} + 1 = 3$ entradas distintas para garantizar si la función es constante o balanceada (si las dos primeras evaluaciones devuelven el mismo valor, podría ser constante o balanceada). Mediante paralelismo cuántico e interferencia constructiva/destructiva, Deutsch-Jozsa determina la propiedad global de $f$ con **una única evaluación** del oráculo cuántico $U_f$.

---

### Decisiones Técnicas — Parte 1

#### Decisión 1: Utilidad del resultado de Grover con ruido y necesidad de corrección de errores cuánticos (QEC)

En el circuito simulado de Grover para $n=2$ qubits con ruido despolarizante ($p_{1q}=0.001$ y $p_{2q}=0.01$), la solución $|11\rangle$ sigue siendo claramente útil sin corrección de errores cuánticos (QEC), ya que la profundidad del circuito es mínima (apenas dos compuertas de dos qubits `cz` y una decena de compuertas de un qubit) y el resultado correcto supera con holgura al resto de estados base en la distribución de muestreo. Sin embargo, al escalar el algoritmo hacia registros de $10$ a $20$ qubits para resolver problemas prácticos, la cantidad de iteraciones crece como $O(\sqrt{2^n})$ (por ejemplo, cerca de $805$ iteraciones para $n=20$) y la descomposición del oráculo y del difusor multi-controlados introduce miles de compuertas de dos qubits. Dado que la fidelidad total decae de forma aproximadamente multiplicativa como $(1 - p_{2q})^{N_{2q}}$, incluso una tasa de error de $1\%$ por compuerta destruye la coherencia mucho antes de completar la búsqueda, convergiendo hacia una distribución uniforme indistinguible del azar. Por ello, los algoritmos de búsqueda a gran escala requieren QEC tolerante a fallos —como códigos de superficie cuyo umbral físico ronda el $1\%$— para reducir la tasa de error lógico por debajo de $10^{-6}$.

#### Decisión 2: Representatividad del modelo de ruido despolarizante frente a hardware NISQ real

El modelo de ruido despolarizante simplificado ($p_{1q}=0.001$, $p_{2q}=0.01$) es valioso desde el punto de vista pedagógico y para estimar cotas iniciales de degradación, pero resulta insuficiente para representar con fidelidad un procesador NISQ real. En primer lugar, el canal despolarizante asume errores isotrópicos e independientes del tiempo, ignorando la asimetría física de la relajación térmica ($T_1$, decaimiento de amplitud de $|1\rangle$ hacia $|0\rangle$) y del desfase ($T_2$), los cuales dependen directamente de la duración de cada pulso. En segundo lugar, omite los errores de lectura o medición (SPAM), que en hardware superconductor real suelen ubicarse entre el $1\%$ y el $5\%$ por qubit y sesgan los conteos hacia el estado fundamental. Además, no modela la diafonía (*crosstalk*) entre qubits adyacentes ni la topología de conectividad limitada del chip, la cual obliga al transpilador a insertar compuertas `SWAP` adicionales que multiplican el error efectivo. Por consiguiente, para validar circuitos previos a su ejecución en hardware real, se requiere utilizar perfiles calibrados como `NoiseModel.from_backend()` que incorporen tiempos $T_1/T_2$, tasas de error por par de qubits y matrices de confusión de lectura.

---

## Parte 2: Impacto Cuántico en Ciberseguridad

El análisis completo de vulnerabilidades criptográficas, estándares post-cuánticos del NIST ([FIPS 203](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf), [FIPS 204](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf), [FIPS 205](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.205.pdf)), planes de migración por perfil organizacional, sobrecarga en TLS 1.3 y decisiones técnicas se encuentra documentado en:

- [`docs/analisis-pqc.md`](docs/analisis-pqc.md)
