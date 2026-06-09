---
type: decision
tags: [core, cpp, performance]
created: 2026-06-09
priority: high
---

# Decisão: Engine em C++20

A engine de memória é escrita em C++20 nativo para gerar um binário único,
rápido e sem dependência de runtime pesado.

Única dependência externa na v1: `nlohmann/json` (header-only). Isso mantém o
[[memory-system]] leve e soberano, alinhado à [[arquitetura]].
