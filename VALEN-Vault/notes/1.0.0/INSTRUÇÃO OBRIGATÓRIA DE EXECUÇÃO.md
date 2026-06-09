---
type: concept
tags: [1-0-0]
created: 2026-06-09
priority: medium
---

## INSTRUÇÃO OBRIGATÓRIA DE EXECUÇÃO

Você **NÃO** deve fazer tudo de uma vez.

Siga **exatamente** esta ordem de etapas. Nunca avance para a próxima etapa sem confirmação explícita do usuário.

### Ordem das Etapas (não pule nenhuma):

**Etapa 0 (Análise e Plano)**
- Crie o arquivo `VALEN_v1.0.0_REFACTOR_PLAN.md`
- Faça uma análise honesta do projeto atual
- Defina o que será mantido, removido, movido para Tools e o que será reescrito
- Mostre um plano realista de migração faseado
- **Pare aqui** e peça confirmação antes de continuar.

**Etapa 1 (Sistema de Tools + Sandbox) — PRIORIDADE MÁXIMA**
- Implemente primeiro o sistema de Tools + Sandbox + ACL + Audit Trail
- Crie as classes base (`ToolBase`, `ToolResult`, `ToolContext`, `Sandbox`, etc.)
- Implemente pelo menos estas Tools: `FilesystemTool`, `TerminalTool`, `MemoryTool`
- Escreva testes para o sistema de Tools
- **Só avance depois que esta etapa estiver funcionando e testada**

**Etapa 2 (NeuroValen)**
- Implemente ou refatore o NeuroValen como cérebro central único
- Implemente `MemoryTool` completa
- Garanta que todos os agentes vão ler e escrever apenas através desta tool

**Etapa 3 (Os 4 Agentes)**
- Refatore os 4 agentes (CEO, Forge, Nexus, Analyst) para usarem **exclusivamente** o sistema de Tools
- Comece pelo CEO
- Depois Forge
- Depois Nexus
- Por último Analyst

**Etapa 4 (Providers e Comunicação)**
- Garanta que todos os providers continuam funcionando
- Implemente fallback entre providers
- Defina como os 4 agentes vão se comunicar entre si

**Etapa 5 (Visual + Interface)**
- Melhore o núcleo visual
- Implemente o sistema de caixas dinâmicas
- Ajuste os 2 modos (Chat e Voz)

**Etapa 6 (Testes, Documentação e Versão)**
- Atualize versão para 1.0.0 em todo o projeto
- Atualize documentação
- Rode testes

---

**Regras rígidas que você deve seguir:**

1. Sempre me mostre o que pretende fazer **antes** de executar mudanças grandes (especialmente deletar arquivos ou refatorar partes críticas).
2. Após cada etapa importante, pare e me mostre o resultado + próximos passos.
3. Se em alguma etapa você sentir que está ficando muito complexo ou arriscado, pare e me avise.
4. Priorize **estabilidade e simplicidade** sobre perfeição arquitetural nesta versão 1.0.0.

Comece pela **Etapa 0**.