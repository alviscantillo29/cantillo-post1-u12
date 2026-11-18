# Análisis Técnico del Impacto Cuántico en Ciberseguridad y Migración Post-Cuántica (PQC)

- **Autor:** Alvis Cantillo (Código 1152332)
- **Curso:** Arquitectura de Computadores — Unidad 12

---

## 1. Inventario de Vulnerabilidades Criptográficas ante Computación Cuántica

La llegada de computadores cuánticos tolerantes a fallos (*Cryptographically Relevant Quantum Computers*, CRQC) afecta de manera asimétrica a los primitivos criptográficos actuales según su fundamento matemático:

| Algoritmo | Tipo | Uso Principal | Algoritmo Cuántico Amenazante | Impacto Cuántico | Nivel de Seguridad Efectivo Post-Cuántico |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RSA-2048 / RSA-4096** | Asimétrico (Factorización) | Intercambio de claves, firmas digitales, certificados TLS | Algoritmo de Shor | **Roto completamente** (tiempo polinomial $O((\log N)^3)$) | $0$ bits (inseguro) |
| **ECDSA P-256 / P-384** | Asimétrico (Logaritmo discreto en curvas elípticas) | Firmas digitales en TLS, blockchain, identidad | Algoritmo de Shor | **Roto completamente** | $0$ bits (inseguro) |
| **ECDH / X25519** | Asimétrico (Logaritmo discreto en curvas elípticas) | Acuerdos de clave efímeros en TLS 1.3, VPN, SSH | Algoritmo de Shor | **Roto completamente** | $0$ bits (inseguro) |
| **AES-128** | Simétrico (Cifrado por bloques) | Cifrado de datos en tránsito y en reposo | Algoritmo de Grover | **Debilitado** (aceleración cuadrática $O(\sqrt{{2^k}})$) | $\approx 64$ bits (insuficiente; requiere migrar a AES-256) |
| **AES-256** | Simétrico (Cifrado por bloques) | Cifrado simétrico de alta seguridad | Algoritmo de Grover | **Debilitado** (seguridad efectiva reducida a la mitad) | $\approx 128$ bits (aceptable/seguro) |
| **SHA-256** | Hash criptográfico | Integridad, firmas, HMAC, árboles de Merkle | Grover (preimagen) / Brassard-Høyer-Tapp | **Debilitado** (reducción cuadrática en búsqueda de preimagen) | $\approx 128$ bits en preimagen (recomendable SHA-384/512 para márgenes mayores) |
| **SHA-3-256** | Hash criptográfico (Esponja Keccak) | Integridad, derivación de claves, soporte PQC | Grover (preimagen) | **Debilitado** (mantiene margen de seguridad post-cuántico estándar) | $\approx 128$ bits en preimagen |

En síntesis, la criptografía de clave pública basada en factorización entera o logaritmo discreto queda **completamente rota** por el algoritmo de Shor, mientras que los cifrados simétricos y funciones *hash* sufren únicamente un **debilitamiento cuadrático** mediante el algoritmo de Grover, mitigable duplicando la longitud de clave (por ejemplo, de AES-128 a AES-256).

---

## 2. Análisis Comparativo de los Estándares PQC del NIST (2024)

El 13 de agosto de 2024, el Instituto Nacional de Estándares y Tecnología de Estados Unidos (NIST) publicó los primeros tres estándares finales de criptografía post-cuántica:

| Estándar | Algoritmo (Familia) | Función | Problema Matemático Subyacente | Conjuntos de Parámetros | Nivel de Seguridad NIST Recomendado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[NIST FIPS 203](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf)** | **ML-KEM** (*Module-Lattice-Based KEM*, derivado de CRYSTALS-Kyber) | Encapsulación de claves (KEM) | *Module Learning With Errors* (MLWE) sobre retículos | ML-KEM-512, ML-KEM-768, ML-KEM-1024 | **ML-KEM-768** (Nivel 3, equivalente a AES-192) |
| **[NIST FIPS 204](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf)** | **ML-DSA** (*Module-Lattice-Based Digital Signature*, derivado de CRYSTALS-Dilithium) | Firma digital | *Module Learning With Errors / Short Integer Solution* (MLWE/MSIS) | ML-DSA-44, ML-DSA-65, ML-DSA-87 | **ML-DSA-65** (Nivel 3, uso general recomendado) |
| **[NIST FIPS 205](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.205.pdf)** | **SLH-DSA** (*Stateless Hash-Based Digital Signature*, derivado de SPHINCS+) | Firma digital sin estado | Seguridad de funciones *hash* criptográficas (SHA-2 / SHAKE) | 12 conjuntos (variantes `128s/f`, `192s/f`, `256s/f`) | **SLH-DSA-128s / 128f** (Nivel 1, respaldo conservador) |

- **ML-KEM ([FIPS 203](https://csrc.nist.gov/pubs/fips/203/final)):** constituye el reemplazo principal para el intercambio de claves (ECDH/RSA-KEM) en protocolos como TLS 1.3 gracias a su alto rendimiento y tamaños de clave compactos dentro de los esquemas basados en retículos.
- **ML-DSA ([FIPS 204](https://csrc.nist.gov/pubs/fips/204/final)):** es la recomendación primaria del NIST para firmas digitales de propósito general por su equilibrio entre velocidad de generación/verificación y tamaño de firma.
- **SLH-DSA ([FIPS 205](https://csrc.nist.gov/pubs/fips/205/final)):** ofrece diversidad matemática al no depender de retículos sino únicamente de funciones *hash* estudiadas durante décadas, sirviendo como alternativa de respaldo (*backup*) para infraestructuras críticas de larga vida (como raíces de confianza), a costa de firmas más grandes y mayor tiempo de cómputo.

---

## 3. Planes de Migración por Perfil Organizacional

Siguiendo las recomendaciones conjuntas de [CISA, NSA y NIST (2023)](https://www.cisa.gov/resources-tools/resources/quantum-readiness-migration-post-quantum-cryptography), las organizaciones deben priorizar la migración según el horizonte de confidencialidad de sus datos y la exposición al ataque ***Harvest Now, Decrypt Later* (HNDL)**, donde un adversario intercepta y almacena tráfico cifrado hoy para descifrarlo cuando disponga de un CRQC.

### Perfil A: Hospital Universitario (Sensibilidad de Datos: $50\text{–}75$ años)

- **Inventario criptográfico:** Historia clínica electrónica (HCE), pasarelas HL7/FHIR sobre TLS 1.2/1.3 (RSA-2048, ECDHE P-256), almacenamiento DICOM cifrado con AES-128/256, VPN IPsec entre sedes y firma digital de recetas médicas y consentimientos informados.
- **Clasificación de sensibilidad y riesgo HNDL:** **Crítico.** Los datos genómicos, diagnósticos e historiales médicos conservan sensibilidad durante toda la vida del paciente ($50\text{–}75$ años), superando ampliamente el horizonte estimado de llegada de un CRQC. El riesgo HNDL sobre copias de respaldo y enlaces externos es inmediato.
- **Estrategia híbrida:** Implementar intercambio de claves híbrido `X25519+ML-KEM-768` en TLS 1.3 y túneles IPsec, elevar todo el almacenamiento en reposo a **AES-256-GCM** y desplegar **ML-DSA-65** para firma de recetas y documentos clínicos.
- **Cronograma de migración:**
  1. *Hito 1 (Meses 1–6):* Descubrimiento automatizado e inventario criptográfico completo (*CBOM*) en sistemas HCE, PACS y redes.
  2. *Hito 2 (Meses 7–15):* Actualización de cifrado en reposo a AES-256 y despliegue de TLS 1.3 híbrido (`X25519MLKEM768`) en pasarelas externas y VPN.
  3. *Hito 3 (Meses 16–24):* Migración de la PKI interna y sistema de receta electrónica a **ML-DSA-65** con pruebas de interoperabilidad.
- **Riesgos y mitigaciones:** Equipos médicos heredados (*IoMT*) sin soporte de firmware para PQC $\to$ aislar en VLANs dedicadas y terminar TLS híbrido en *proxies* inversos o *gateways* perimetrales.

### Perfil B: Startup de Comercio Electrónico (Sensibilidad de Datos: $5\text{–}7$ años, PCI-DSS)

- **Inventario criptográfico:** APIs REST y portal web sobre TLS 1.3 (ECDSA P-256, X25519), pasarelas de pago tokenizadas bajo PCI-DSS, JWT firmados con RS256/ES256 y bases de datos cifradas con AES-128/256 en la nube.
- **Clasificación de sensibilidad y riesgo HNDL:** **Moderado-Bajo.** Los datos transaccionales y tarjetas de pago poseen una vida útil operativa de $5\text{–}7$ años; el riesgo HNDL es menor que en salud o defensa, aunque la continuidad operativa y el cumplimiento PCI-DSS exigen agilidad criptográfica (*crypto-agility*).
- **Estrategia híbrida:** Activar `X25519+ML-KEM-768` en el CDN/balanceador de carga (Cloudflare/AWS ALB) sin modificar la lógica de negocio interna inicialmente, y migrar de AES-128 a AES-256 en KMS.
- **Cronograma de migración:**
  1. *Hito 1 (Trimestre 1):* Inventario de dependencias TLS, librerías OpenSSL/BoringSSL y auditoría de tokens JWT.
  2. *Hito 2 (Trimestre 2–3):* Habilitación de TLS híbrido en el borde (CDN/Ingress) y actualización de claves KMS a AES-256.
  3. *Hito 3 (Trimestre 4–6):* Adopción de certificados ML-DSA conforme los navegadores y entidades certificadoras públicas completen su soporte, evaluando el retiro del modo híbrido a mediano plazo.
- **Riesgos y mitigaciones:** Latencia en *checkout* o incompatibilidad con clientes móviles antiguos $\to$ negociación TLS con *fallback* controlado a `X25519` clásico mientras se monitorea la telemetría de *handshake*.

### Perfil C: Entidad Gubernamental / Defensa (Sensibilidad de Datos: $25\text{–}50$ años, CNSA 2.0)

- **Inventario criptográfico:** Redes clasificadas, infraestructura PKI nacional, sistemas de mando y control, firma de firmware y actualizaciones de software, archivos diplomáticos y comunicaciones satelitales (RSA-3072/4096, ECDSA P-384, ECDH P-384).
- **Clasificación de sensibilidad y riesgo HNDL:** **Extremo.** Los secretos de Estado y datos estratégicos de $25\text{–}50$ años son el objetivo prioritario de recolección masiva HNDL por actores estatales adversarios.
- **Estrategia híbrida y alineación CNSA 2.0:** Priorizar **ML-KEM-1024** (nivel 5) y **ML-DSA-87** (o **SLH-DSA** para raíces y firma de firmware crítico), utilizando modos híbridos solo como puente transitorio hacia PQC puro según la hoja de ruta de la NSA (*CNSA 2.0*, ventana $2025\text{–}2033$).
- **Cronograma de migración:**
  1. *Hito 1 ($2025$):* Exigir soporte PQC en adquisiciones de software/firmware y completar el inventario de sistemas críticos.
  2. *Hito 2 ($2026\text{–}2029$):* Transición obligatoria de navegadores, servidores web, VPN y equipos de red a suites PQC aprobadas (ML-KEM-1024 / ML-DSA-87).
  3. *Hito 3 ($2030\text{–}2033$):* Eliminación total de algoritmos clásicos vulnerables (RSA/ECC) y transición exclusiva a criptografía post-cuántica en toda la infraestructura.
- **Riesgos y mitigaciones:** Dependencias de hardware criptográfico (HSM) sin soporte para retículos $\to$ planificar renovación temprana de HSM con actualización de firmware certificada FIPS 140-3 y uso de **SLH-DSA** en actualizaciones de arranque seguro (*Secure Boot*).

---

## 4. Comparación de Tamaños de Clave y Firma e Impacto en TLS 1.3

La migración hacia criptografía post-cuántica sustituye claves y firmas de decenas de bytes por estructuras de varios kilobytes, como se detalla en la siguiente tabla comparativa (tamaños especificados en [FIPS 203](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf), [FIPS 204](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf) y [FIPS 205](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.205.pdf)):

| Algoritmo | Tipo | Clave Pública (bytes) | Clave Privada (bytes) | Firma / Texto Cifrado (bytes) |
| :--- | :--- | :---: | :---: | :---: |
| **RSA-3072** | Clásico (Asimétrico) | $384$ | $\approx 1\,728$ | $384$ (firma) |
| **ECDSA P-256** | Clásico (Firma ECC) | $64$ | $32$ | $64$ (firma) |
| **X25519** | Clásico (ECDH) | $32$ | $32$ | $32$ (clave compartida) |
| **ML-KEM-768** ([FIPS 203](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf)) | PQC (KEM, Nivel 3) | $1\,184$ | $2\,400$ | $1\,088$ (texto cifrado) |
| **ML-DSA-65** ([FIPS 204](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf)) | PQC (Firma, Nivel 3) | $1\,952$ | $4\,032$ | $3\,309$ (firma) |
| **SLH-DSA-128s** ([FIPS 205](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.205.pdf)) | PQC (Firma Hash, Nivel 1) | $32$ | $64$ | $7\,856$ (firma) |

### Impacto en el *Handshake* de TLS 1.3 Híbrido (`X25519MLKEM768`)

En una negociación estándar TLS 1.3 con `X25519`, el cliente envía una extensión `key_share` de apenas **$32\text{ bytes}$** dentro del mensaje `ClientHello`, y el servidor responde con otros **$32\text{ bytes}$**. Al habilitar el intercambio híbrido `X25519+ML-KEM-768`:
- El `key_share` del cliente pasa de **$32\text{ bytes}$** a **$1\,216\text{ bytes}$** ($32\text{ B}$ de X25519 + $1\,184\text{ B}$ de la clave pública ML-KEM-768).
- El `key_share` del servidor pasa de **$32\text{ bytes}$** a **$1\,120\text{ bytes}$** ($32\text{ B}$ de X25519 + $1\,088\text{ B}$ del texto cifrado ML-KEM-768).

Desde el punto de vista de red, un `ClientHello` tradicional (~$250\text{–}500\text{ bytes}$) crece hasta aproximadamente $1\,500\text{–}1\,700\text{ bytes}$, superando el MTU típico de Ethernet ($1\,500\text{ bytes}$) y fragmentándose en **2 segmentos TCP**. Sin embargo, dado que la ventana inicial de congestión de TCP moderna es de **10 segmentos (`IW10`, $\approx 14\,600\text{ bytes}$)**, ambos segmentos se transmiten en el mismo vuelo inicial sin introducir *round trips* adicionales, manteniendo un impacto mínimo en la latencia percibida siempre que no existan *middleboxes* o cortafuegos antiguos que bloqueen `ClientHello` fragmentados.

---

## 5. Decisiones Técnicas — Parte 2

### Decisión 1: Selección del algoritmo PQC del NIST para firma digital de recetas médicas (Perfil A)

Para la firma digital de recetas médicas electrónicas del Perfil A (hospital universitario), se selecciona **ML-DSA-65** ([NIST FIPS 204](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf)) y se descartan las otras dos familias por razones estructurales y operativas. En primer lugar, **ML-KEM** ([NIST FIPS 203](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf)) queda descartado de plano porque es un mecanismo de encapsulación de claves (KEM) diseñado exclusivamente para intercambio de claves y confidencialidad, no para firmas digitales ni no repudio clínico. Entre las dos alternativas de firma, **ML-DSA-65** (nivel de seguridad 3) produce firmas de $3\,309\text{ bytes}$ y claves públicas de $1\,952\text{ bytes}$ con verificación y firma muy rápidas, frente a **SLH-DSA-128s** ([NIST FIPS 205](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.205.pdf)), cuyas firmas alcanzan $7\,856\text{ bytes}$ (más del doble) y presentan mayor latencia computacional en entornos de alto volumen transaccional hospitalario. Adicionalmente, conviene distinguir dos riesgos distintos: la confidencialidad del historial clínico está expuesta al ataque *Harvest Now, Decrypt Later* (HNDL) a $50\text{–}75$ años, mientras que la firma de la receta exige autenticidad al momento de la emisión y dispensación; no obstante, si las recetas archivadas deben mantener validez probatoria legal a largo plazo, la transición temprana a ML-DSA-65 evita la falsificación futura cuando existan computadores cuánticos criptográficamente relevantes.

### Decisión 2: Permanencia vs. transitoriedad del modo híbrido en TLS para comercio electrónico (Perfil B)

Para el Perfil B (startup de comercio electrónico), el modo híbrido (clásico + PQC, como `X25519+ML-KEM-768`) debe adoptarse como una **etapa de transición planificada** y no como una arquitectura permanente. En el corto y mediano plazo, el modo híbrido aporta una defensa en profundidad indispensable: protege simultáneamente frente a un eventual computador cuántico capaz de romper ECDH mediante el algoritmo de Shor y frente a posibles debilidades criptoanalíticas clásicas aún no descubiertas en los esquemas basados en retículos relativamente jóvenes como ML-KEM. Operativamente, su sobrecarga en TLS 1.3 es manejable: el incremento del campo `key_share` en `ClientHello` (de $\approx 32\text{ bytes}$ a $\approx 1\,216\text{ bytes}$) cabe dentro de la ventana inicial de congestión TCP (`IW10`) en la mayoría de conexiones web sin añadir viajes de ida y vuelta (*round trips*). Sin embargo, mantener ambos algoritmos de forma indefinida duplica la superficie de implementación, complica auditorías PCI-DSS y conserva dependencias de código legado que incrementan el costo de mantenimiento. Por ello, resulta técnicamente óptimo operar en modo híbrido durante la fase de convivencia y planificar el retiro de la criptografía clásica hacia PQC puro en concordancia con la maduración de los estándares y los plazos de referencia como CNSA 2.0 hacia $2033$.

---

## 6. Referencias (Formato APA)

- Cybersecurity and Infrastructure Security Agency (CISA), National Security Agency (NSA), & National Institute of Standards and Technology (NIST). (2023, 21 de agosto). *Quantum-readiness: Migration to post-quantum cryptography*. Departamento de Seguridad Nacional de los Estados Unidos. https://www.cisa.gov/resources-tools/resources/quantum-readiness-migration-post-quantum-cryptography (PDF: https://media.defense.gov/2023/Aug/21/2003284212/-1/-1/0/CSI-QUANTUM-READINESS.PDF)
- National Institute of Standards and Technology (NIST). (2024a). *Module-lattice-based key-encapsulation mechanism standard* (Federal Information Processing Standards Publication 203). Departamento de Comercio de los Estados Unidos. https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf (https://doi.org/10.6028/NIST.FIPS.203)
- National Institute of Standards and Technology (NIST). (2024b). *Module-lattice-based digital signature standard* (Federal Information Processing Standards Publication 204). Departamento de Comercio de los Estados Unidos. https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf (https://doi.org/10.6028/NIST.FIPS.204)
- National Institute of Standards and Technology (NIST). (2024c). *Stateless hash-based digital signature standard* (Federal Information Processing Standards Publication 205). Departamento de Comercio de los Estados Unidos. https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.205.pdf (https://doi.org/10.6028/NIST.FIPS.205)
