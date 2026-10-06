# Cifras aportadas por el autor (lámina de contrastación estadística)

Texto entregado por el autor para la nueva lámina «Contrastación estadística de
la calidad del matching». Las cifras se verificaron con la prueba binomial exacta
(scipy.stats.binomtest) sobre la tabla de 2×2.

- Prueba: McNemar exacta bilateral sobre 161 pares comunes.
- H₀c: TF-IDF y Transformer tienen la misma probabilidad de acierto.
- H₁c: sus probabilidades de acierto son diferentes.
- TF-IDF correcto y Transformer correcto: 106
- TF-IDF correcto y Transformer incorrecto: 3 (b)
- TF-IDF incorrecto y Transformer correcto: 50 (c)
- TF-IDF incorrecto y Transformer incorrecto: 2
- Estadístico exacto: T = min(b, c) = 3, con 53 discordancias.
- Valor p bilateral: 5,52 × 10⁻¹² < 0,05.
- Exactitud: TF-IDF 67,70 % → Transformer 96,89 %.
- Mejora: 29,19 puntos porcentuales.
- Decisión: se rechaza H₀c; la diferencia favorece al Transformer.
