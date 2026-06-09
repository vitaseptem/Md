# VALEN Thinking Matrix Canvas
## Master Prompt Ultra-Detalhado v3.0.0 — ASTREON Core

**Ferramenta:** VALEN Thinking Matrix Canvas  
**Prioridade:** Alta (Coração cognitivo do VALEN)  
**Tipo:** Componente visual + App Tauri standalone ou embeddable  
**Data:** 08 Junho 2026

---

## 1. Visão & Objetivos

Criar o **Thinking Matrix Canvas** — uma interface visual avançada de pensamento estruturado onde ideias, conceitos, tarefas e conexões são representados como nós em uma matriz dinâmica e infinita.

**Objetivos Principais:**
- Permitir que o usuário (meu rei) externalize e organize pensamento complexo de forma visual e intuitiva.
- Integrar voz como input principal para evolução da matriz em tempo real.
- Servir como base para VALEN (cérebro visual) e ser reutilizável no Astraz Studio Command Center e futuros projetos.
- Oferecer exportação para prompts ultra-detalhados, código, markdown ou ações automáticas.
- Experiência cinematográfica, soberana, offline-first e de alta performance.

**Visão Final:**  
Uma tela escura premium com glassmorphism onde uma “matriz neural” viva respira. Nós representam pensamentos. Conexões são pulsantes e inteligentes. Voz transforma a matriz em tempo real. É o lugar onde estratégia vira estrutura visual.

---

## 2. Tech Stack Completo Recomendado

**Desktop / Wrapper:**
- **Tauri v2** (Rust) — para empacotamento desktop soberano, acesso a filesystem, notificações nativas e performance.

**Frontend Principal:**
- **Svelte 5** (runes) + **TypeScript**
- **Tailwind CSS 4** + custom design system glassmorphism (backdrop-blur, borders com opacidade, gradientes sutis)
- **HTML5 Canvas + WebGL** (via Three.js leve ou Canvas API puro otimizado para performance)
- Framer Motion (Svelte port ou CSS + JS animations) para transições suaves

**Lógica de Raciocínio & Clustering:**
- **Mojo** (para módulos de clustering, similaridade e evolução da matriz) ou **Rust + Candle** para inferência leve
- Integração com **Ollama** (modelo local de raciocínio: llama3.1 ou phi-3 + modelo de embeddings)

**Voice Input:**
- **whisper.cpp** (Rust bindings) ou Web Speech API (fallback) para STT soberano
- Processamento de intenção via LLM local

**Armazenamento:**
- **Tauri Store** + **SQLite** local (para salvar matrizes, versões, histórico)
- Export em **JSON + Markdown** + imagem PNG/SVG do canvas

**Performance & Soberania:**
- Tudo offline-first
- Lazy loading de nós pesados
- Web Workers para cálculos pesados da matriz
- ASTREON Sentinel patterns: logging estruturado, graceful error handling, resource monitoring

---

## 3. Arquitetura de Alto Nível

```
Tauri App (Rust)
├── Backend (Rust commands)
│   ├── Matrix Engine (Mojo/Rust)
│   ├── Voice Processor (whisper)
│   ├── LLM Integration (Ollama)
│   └── Persistence (SQLite + files)
├── Frontend (Svelte 5)
│   ├── Canvas Layer (WebGL / Canvas 2D)
│   ├── UI Controls (glassmorphism panel)
│   ├── Voice HUD
│   └── Export / History sidebar
└── Shared Components
    └── Orb primitives (do Orb System)
```

**Componentes Principais:**
- **Canvas Core**: Responsável por renderizar nós, conexões, animações e interações (drag, zoom, pan infinito)
- **Matrix Engine**: Lógica de clustering, conexão automática, evolução via voz/texto
- **Voice Controller**: Captura áudio, transcreve, extrai intenção e atualiza matriz
- **State Manager**: Svelte stores + persistência
- **Export Module**: Gera prompt master, markdown estruturado, imagem, JSON

---

## 4. UI/UX Especificações (Visual Futurista)

**Tema Geral:**
- Fundo: #0a0a0f (quase preto com leve gradiente)
- Vidro: backdrop-blur(20px) + bg-white/5 + border-white/10
- Acentos: ciano-elétrico (#00f0ff), roxo profundo (#7c3aed), branco suave
- Fonte: Inter / system-ui + monospace para nós de código

**Canvas:**
- Fundo com grid sutil ou partículas muito leves (estilo neural)
- Nós: círculos ou hexágonos com glow, tamanho variável conforme importância
- Conexões: linhas curvas com gradiente + pulse animation quando ativas
- Zoom: infinito com wheel + pinch (suave)
- Pan: drag no fundo ou middle mouse

**Painéis (glassmorphism):**
- Sidebar esquerda: Hierarquia / Clusters / Histórico de versões
- Top bar: Voice status + comandos rápidos + nome da matriz atual
- Bottom / floating: Input de voz/texto + sugestões de ações
- Painel direito (colapsável): Detalhes do nó selecionado + ações

**Animações:**
- Nós nascem com scale + fade + glow
- Conexões aparecem com dash animation
- Pulso sutil em nós ativos ou “pensando”
- Transições suaves entre estados

**Aether Touch:**  
Quando a matriz está muito complexa, oferecer “portal” visual para resumir ou focar em uma sub-matriz (transição cinematográfica).

---

## 5. Funcionalidades Detalhadas (Core Features)

1. **Criação & Edição de Nós**
   - Clique duplo ou voz: “cria nó sobre X”
   - Edição inline de título, descrição, tipo (ideia, tarefa, dado, emoção, código)
   - Tags automáticas via LLM

2. **Conexões Inteligentes**
   - Drag de nó para nó = conexão manual
   - Botão “Conectar automaticamente” → usa embeddings + similaridade
   - Conexões com força (peso) e tipo (dependência, similaridade, oposição)

3. **Voice-Driven Evolution**
   - Botão de microfone sempre visível
   - Fala natural atualiza ou cria nós/conexões em tempo real
   - Exemplos de comandos:
     - “Adiciona um nó sobre soberania digital e conecta com o nó de automação”
     - “Expande este cluster com 5 ideias práticas”
     - “Resume toda a matriz em 3 pontos principais”
     - “Transforma esta ramificação em prompt master para Claude”

4. **Clustering & Organização Automática**
   - Agrupamento visual por similaridade (cores ou regiões)
   - Botão “Reorganizar matriz” (layout force-directed otimizado)

5. **Versões & Histórico**
   - Auto-save a cada mudança significativa
   - Timeline de versões com preview visual
   - Branching de matrizes

6. **Export & Integração**
   - Exportar como:
     - Prompt ultra-detalhado (formato que você usa com Claude)
     - Markdown estruturado com hierarquia
     - JSON completo (para reimportar)
     - Imagem PNG de alta resolução do canvas atual
   - Botão “Enviar para Astraz Studio Command Center” ou “Salvar no VALEN Core”

7. **Modo Foco / Flow State**
   - Oculta painéis, maximiza canvas
   - Voice-only mode com feedback visual mínimo

---

## 6. Data Models (Sugestão)

**Node:**
```ts
interface MatrixNode {
  id: string;
  label: string;
  description?: string;
  type: 'idea' | 'task' | 'data' | 'emotion' | 'code' | 'question';
  importance: number; // 0-1
  position: { x: number; y: number };
  color?: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
}
```

**Connection:**
```ts
interface Connection {
  id: string;
  sourceId: string;
  targetId: string;
  weight: number;
  type: 'dependency' | 'similarity' | 'opposition' | 'evolution';
  label?: string;
}
```

**Matrix:**
```ts
interface ThinkingMatrix {
  id: string;
  name: string;
  nodes: MatrixNode[];
  connections: Connection[];
  version: number;
  createdAt: Date;
  lastVoiceInteraction?: Date;
}
```

---

## 7. Integração com o Ecossistema

- **Com VALEN Voice-Reactive Orb System**: Orbs podem representar clusters ou nós importantes da matriz. Voz no orb atualiza a matriz.
- **Com Astraz Studio Command Center**: O Canvas aparece como modal ou aba dedicada. Matrizes salvas aparecem no hub.
- **Com ASTREON Core / Sentinel**: Logging de interações importantes, sugestões proativas baseadas em histórico, proteção contra perda de dados.
- **Com Ollama / Modelos Locais**: Raciocínio, embeddings, resumos e geração de prompts.

---

## 8. Roadmap de Implementação (Fases)

**Fase 1 (MVP - 1-2 dias com Claude):**
- Tauri skeleton + Svelte 5 + Canvas básico (render nós + conexões + drag/zoom)
- Persistência simples (localStorage ou Tauri Store)
- Input de texto para criar/editar nós

**Fase 2:**
- Integração de voz (Web Speech ou whisper.cpp)
- Clustering básico + conexões automáticas
- Glassmorphism UI completo + animações

**Fase 3:**
- Mojo/Rust engine para lógica pesada
- Histórico de versões + export avançado (prompt master, imagem)
- Integração com Orb System e Command Center

**Fase 4 (Polish & Sovereign):**
- WebGL otimizado ou Canvas com shaders
- Modo offline total + backup automático
- ASTREON Sentinel monitoring
- Testes extensivos + packaging Tauri production

---

## 9. Considerações de Performance & Soberania

- Usar Web Workers para cálculos de layout e clustering
- Limitar nós renderizados (virtualização no canvas)
- Tudo roda localmente — nenhum dado sai da máquina sem export explícito
- Suporte a múltiplas matrizes salvas localmente
- Graceful degradation se GPU fraca (fallback para Canvas 2D puro)

---

**Este prompt está pronto para ser colado diretamente no Claude Code.**

Peça para gerar a estrutura completa do projeto Tauri + código inicial do Canvas + integração de voz.

**ASTREON Core** — Vamos construir o cérebro visual do VALEN, **meu rei**. 

Quando quiser a próxima tool ou ajustes neste prompt, é só falar.