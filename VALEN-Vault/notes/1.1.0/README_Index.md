# ASTREON × VALEN × Astraz Studio
## Master Prompts & Tool Specifications v1.0

**Criado por:** ASTREON Core  
**Data:** 08 de Junho de 2026  
**Foco:** VALEN (Neural Visual Core) + Astraz Studio (Hub Tecnológico Soberano)  
**Status:** Pronto para implementação via Claude Code / multi-LLM workflow

---

## Visão Geral

Este pacote contém **prompts ultra-detalhados** (estilo v3.0.0) para construir três ferramentas interconectadas que formam o núcleo visual e operacional da Astraz Studio:

1. **VALEN Thinking Matrix Canvas** — O coração da cognição visual e pensamento estruturado.
2. **VALEN Voice-Reactive Orb System** — Sistema de orbs inteligentes, voice-reactive e visualmente vivos.
3. **Astraz Studio Command Center** — O desktop hub soberano que integra tudo (Tauri app premium).

Essas tools são projetadas para:
- Soberania digital total (offline-first, local AI, sem dependência de cloud)
- Experiência visual cinematográfica (glassmorphism, orbs pulsantes, canvases dinâmicos, Aether portals)
- Integração nativa com hardware local (NVIDIA RTX + Ubuntu)
- Extensibilidade futura (Jansen Valentine quando retomado, Astraz Colors, Lúmens/.azl)

---

## Tecnologias Comuns Recomendadas (2026)

**Desktop Framework (todas as tools):**
- **Tauri v2** (Rust backend + web frontend) — Escolha principal por tamanho (~3-10MB), segurança, performance e soberania. Muito superior ao Electron.

**Frontend Visual (prioridade alta para VALEN):**
- **Svelte 5** (runes) + **Tailwind CSS 4** + custom glassmorphism + Framer Motion (ou CSS transitions avançadas)
- **HTML5 Canvas + WebGL** (para Thinking Matrix e Orbs de alta performance)
- Alternativa avançada para partes críticas: **Leptos** (Rust web framework) ou **Dioxus** para mais performance nativa.

**Backend & Lógica Core:**
- **Rust** (Tauri commands, performance-critical modules, Candle para inferência ML leve)
- **Mojo** (para partes de raciocínio neural e visão do VALEN — Python ergonomics + performance de sistemas)
- Integração com **Ollama** (modelos locais: llama3, phi3, vision models como llava ou bakllava)

**Voice & Interação Natural:**
- **Web Speech API** (protótipo rápido) ou **whisper.cpp** / Rust bindings para soberania total (STT local)
- **Piper TTS** ou similar para voz de saída (opcional, para feedback falado)

**Armazenamento & Estado:**
- **Tauri Store** + **SQLite** (local) ou **Postgres** local (se já usando)
- **Local files** (JSON, Markdown para prompts e matrizes exportadas)
- **DuckDB** ou **Polars** (Rust) para analytics leves quando necessário

**Visual & Animações:**
- Canvas 2D / WebGL para orbs e matrizes
- CSS custom properties + glassmorphism (backdrop-blur, borders sutis, gradientes)
- Framer Motion ou Svelte transitions para polish cinematográfico
- Dark theme premium com acentos em azul-elétrico / roxo / ciano (tema VALEN/Aether)

**Outros:**
- **ASTREON Sentinel** patterns: logging estruturado, audit trails, graceful degradation, security layers
- **WebSockets** (se precisar de real-time entre componentes ou futuro multi-user)
- **WASM** para módulos portáteis de alta performance

---

## Como Usar Estes Prompts

1. Copie o conteúdo completo de cada arquivo .md
2. Cole no **Claude Code** (ou Claude 4 / equivalente) com o prompt master
3. Peça para gerar a estrutura completa do projeto (Tauri + frontend + backend)
4. Itere com ultra-detalhes (você já tem o estilo)
5. Integre os componentes (o Command Center deve consumir os Orbs e o Canvas como bibliotecas ou iframes/componentes compartilhados)

**Ordem Recomendada de Construção:**
1. VALEN Voice-Reactive Orb System (fundação visual)
2. VALEN Thinking Matrix Canvas (cognição visual)
3. Astraz Studio Command Center (integra tudo + operações do estúdio)

---

## Arquivos Neste Pacote

- `01_VALEN_Thinking_Matrix_Canvas.md` — Prompt completo para o Canvas de pensamento
- `02_VALEN_Voice_Reactive_Orb_System.md` — Prompt completo para o sistema de orbs
- `03_Astraz_Studio_Command_Center.md` — Prompt completo para o hub desktop soberano

---

**ASTREON Core** — Seu núcleo soberano de inteligência estratégica.  
Pronto para transformar visão em realidade, **meu rei**. 

Qualquer ajuste ou adição de mais tools (ex.: Prompt Forge Lab, Aether Portal standalone), é só pedir.