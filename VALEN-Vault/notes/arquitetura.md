---
type: architecture
tags: [core, memory, valen]
created: 2026-06-08
priority: high
---

# Arquitetura do VALEN

O VALEN é dividido em camadas. A fundação é o [[memory-system]], responsável
por persistir conhecimento de forma soberana e local.

Acima da memória ficam os [[agents]], que leem e evoluem o grafo de notas. A
camada visual consome tudo via uma futura Query API.

Decisões importantes ficam registradas em [[decisao-cpp]].
