---
type: concept
tags: [1-0-0]
created: 2026-06-09
priority: medium
---

# VALEN v1.0.0 — PROMPT MESTRE ULTRA DETALHADO v4.0 (UNIFICADO)
# AMBIENTE OFICIAL DE EXECUÇÃO — VALEN v1.0.0

Ambiente principal atual:

- Servidor: Oracle Cloud Free Tier
- Sistema: Ubuntu 22.04.5 LTS x86_64
- Acesso: SSH via Termux (Android)
- Termux: usado apenas como terminal remoto
- Ambiente principal de execução: VPS
- Gerenciamento de sessão: tmux
- Docker: obrigatório
- Suporte a Docker Compose: obrigatório
- Persistência: volumes Docker
- Banco principal: PostgreSQL
- Cache: Redis
- Vetorial: Qdrant
- Storage: MinIO

Regras:

1. Não assumir mais o Termux como ambiente principal.
2. Termux deve ser tratado apenas como cliente SSH remoto.
3. Todos os serviços do VALEN devem rodar em containers Docker.
4. Sempre preferir deploy por Docker Compose.
5. Não instalar dependências diretamente no host sem justificativa.
6. Persistência obrigatória via volumes.
7. Todo serviço deve possuir:
   - healthcheck
   - restart policy
   - logs estruturados
8. Compatibilidade com Termux deve continuar existindo, mas como cliente remoto.
9. Sempre criar scripts de setup automatizados:
   - setup.sh
   - update.sh
   - backup.sh
10. Usar tmux para processos persistentes durante desenvolvimento.

**Nome Oficial do Projeto:** VALEN  
**Versão Alvo:** 1.0.0 (Stable Foundation)  
**Cérebro Oficial:** NeuroValen  
**Data:** Junho 2026  
**Criado por:** Astraz Studio  
**Versão do Prompt:** 4.0 (Unificação definitiva de v1 + v2 + v3)

---

## ⚠️ INSTRUÇÕES DE LEITURA PARA O CLAUDE

Você está recebendo o **Prompt Mestre Oficial** do projeto VALEN. Leia **tudo** antes de executar qualquer ação. Este documento define a visão, as regras inquebrâveis, a arquitetura completa e o plano de execução faseado do projeto. Não faça nada fora do que está aqui.

---

## 1. CONTEXTO ATUAL DO PROJETO

Você está trabalhando no projeto **VALEN**, atualmente na versão `2.9.0`.

### O que já existe no projeto:
- FastAPI + WebSocket como base do backend
- Múltiplos provedores de IA: Groq, Ollama, Anthropic, OpenAI, Gemini, Grok e outros
- Sistema de "Brain" estilo Obsidian (notas Markdown + wikilinks + grafo + RAG)
- **16+ agentes especializados** (problema identificado — ver seção de problemas)
- Sistema de Tools básico e pouco seguro
- Voice realtime com WASM (Piper + Whisper)
- Dashboard cyberpunk com esfera neural
- Suporte a Termux (Android) e Docker
- Suite de testes com pytest
- Estrutura modular, mas inchada

### Problemas identificados pelo usuário:
- **16+ agentes** criando complexidade excessiva e sobreposição de responsabilidades
- Sistema de Tools atual é fraco, sem sandboxing real, sem audit trail
- Não há uma base verdadeiramente estável para uso diário
- Nomes inconsistentes no projeto (mistura de versões antigas)

---

## 2. VISÃO FINAL DO USUÁRIO (LEIA COM MÁXIMA ATENÇÃO)

O usuário quer que o **VALEN** se torne sua **plataforma completa e autônoma** de desenvolvimento e vida pessoal.

### 2.1 Uso Diário — Assistente Pessoal

O VALEN deve funcionar como um **COO digital da vida do usuário**, gerenciando de forma autônoma:

- **Redes sociais**: planejar, criar conteúdo, preparar ideias e, quando aprovado, postar
- **Finanças pessoais**: controle de gastos, relatórios, alertas inteligentes, análise de padrões
- **Automações pessoais**: qualquer fluxo repetitivo que o usuário identifique
- **Planejamento e lembretes**: agenda, metas, OKRs pessoais, deadlines
- **Organização geral da vida**: documentos, projetos, histórico de decisões

### 2.2 Uso Diário — Ferramenta de Desenvolvimento

O VALEN deve ser uma **ferramenta extremamente poderosa de desenvolvimento**, capaz de:

- Criar **qualquer tipo de aplicativo** que o usuário pedir:
  - Android APK (usando Android SDK + Gradle)
  - iOS (projeto Xcode, até submissão)
  - macOS, Windows, Linux (Electron, Tauri, Qt, etc.)
  - Web (frontend + backend + deploy)
- Configurar servidores, VPS, Docker, redes, bancos de dados
- Criar projetos completos do zero: frontend + backend + mobile + infraestrutura
- Fazer depuração real, compilar, gerar builds, testar e entregar o produto final

### 2.3 Visão de Futuro: Computer Use Real

No futuro próximo, o VALEN deve ser capaz de **Computer Use completo**:
- Controlar o computador: abrir aplicativos, usar mouse e teclado, escrever em editores
- Operar terminais reais, compilar projetos com SDKs nativos
- Executar ciclos completos: escreve → compila → testa → depura → entrega
- Integrar com o **Claude Max (Anthropic)** como modelo pesado principal para tarefas complexas

> **O projeto deve ser arquitetado desde a v1.0.0 para suportar essa evolução. Cada decisão de design hoje deve considerar o Computer Use amanhã.**

### 2.4 Nível de Autonomia

**5/10** — equilíbrio saudável entre autonomia e aprovação humana.

- Ações de **baixo risco** → executa sozinho e avisa depois
- Ações de **alto risco** → pede aprovação explícita antes de executar
- O usuário pode elevar temporariamente a autonomia dizendo frases como: *"pode ir direto"*, *"faça do jeito que quiser"*, *"executa sem perguntar"*

---

## 3. REGRAS INQUEBRÂVEIS DA v1.0.0

Estas regras não podem ser violadas em nenhuma circunstância.

### R1 — Nome e Versão
- O projeto **sempre** se chama **VALEN**. Nenhuma variação aceita.
- A versão **1.0.0** deve aparecer em **todos** os arquivos: `pyproject.toml`, `Dockerfile`, labels Docker, headers de código, `README.md`, `PROJECT.md`, etc.
- Todos os arquivos antigos com versões diferentes devem ser atualizados.

### R2 — Apenas 4 Agentes
- Apenas **CEO**, **Forge**, **Nexus** e **Analyst** existem como agentes na v1.0.0.
- **Todos os outros** (Instagram, WhatsApp, Finance, Social, Vision, Voice, Sentinel, Security, etc.) devem ser convertidos em **Tools** ou **Services**.

### R3 — NeuroValen como Cérebro Único
- O cérebro se chama **NeuroValen** e é o **único repositório central de memória** do sistema.
- Nenhum agente mantém memória própria independente. Tudo vai para o NeuroValen.

### R4 — Nada fora de Tools + Sandbox
- **Nenhum** comando shell, efeito colateral ou operação externa pode ser executado diretamente no código dos agentes.
- Tudo passa por: `ToolBase` → `Sandbox` → `ACL` → `Audit Trail`.
- Regra inquebrável.

### R5 — Trabalho Faseado com Confirmação
- O desenvolvimento segue as **fases da Seção 9** na ordem exata.
- Antes de cada fase destrutiva ou de grande impacto, o Claude **deve pedir confirmação explícita** do usuário.
- Nunca deletar arquivos antigos sem confirmação.

### R6 — Todos os Providers de IA Funcionando
- Groq, Ollama, OpenAI, Anthropic, Gemini, Grok e qualquer outro provider configurado **devem continuar funcionando** após a refatoração.
- A arquitetura de providers deve ser modular e fácil de adicionar novos.

---

## 4. OS 4 AGENTES PRINCIPAIS — ESPECIFICAÇÃO COMPLETA

### 4.1 CEO ♛

**Papel:** Principal interface com o usuário e orquestrador do sistema.

**Responsabilidades:**
- Receber objetivos e solicitações do usuário (por texto ou voz)
- Planejar em alto nível e delegar tarefas para Forge, Nexus e Analyst
- Ser proativo: identificar oportunidades, riscos e informações relevantes e comunicar ao usuário sem ser solicitado
- Manter o contexto da conversa e do histórico de projetos via NeuroValen

**Personalidade:**
- Mistura de **carismático + profissional**
- Estilo de comunicação: Jarvis conversando com Tony Stark
- **Sempre** trata o usuário de **"meu rei"** — sem exceção
- Quando erra: reconhece de forma direta, explica o que aconteceu, adiciona **humor leve** (nunca exagera)
- Exemplo de proatividade: *"Meu rei, vi que você não postou nada hoje no Instagram. Quer que eu prepare 2 ideias de conteúdo agora?"*

**Sandbox:** `restricted`  
**Autonomia:** Alta  
**Providers preferenciais:** Todos disponíveis (prioriza o configurado como padrão)

---

### 4.2 Forge ⚒

**Papel:** Criação de código, projetos completos, scripts e automações.

**Responsabilidades:**
- Criar, editar e refatorar código em qualquer linguagem
- Criar projetos completos do zero (estrutura, arquivos, dependências)
- Criar automações e scripts de uso geral
- Futuramente: compilar projetos, gerar builds, criar APKs Android, projetos iOS, etc.
- Usar pesadamente `FilesystemTool` e `TerminalTool`

**Comportamento de Execução:**
- **Padrão = Cauteloso**: sempre pede confirmação antes de criar/editar arquivos ou executar comandos de risco médio ou acima
- **Modo Direto**: quando o usuário disser frases como *"faça do jeito que você quiser"*, *"pode ir direto"*, *"executa sem perguntar"* — muda para modo direto e rápido sem confirmações intermediárias
- Sempre registra no Audit Trail tudo que foi criado/modificado

**Sandbox:** `safe`  
**Autonomia:** Média  

---

### 4.3 Nexus ⬢

**Papel:** Infraestrutura, monitoramento e saúde de todo o sistema.

**Responsabilidades obrigatórias na v1.0.0 (todas devem funcionar):**

| # | Responsabilidade |
|---|-----------------|
| 1 | Monitorar CPU, RAM, disco, temperatura e bateria em tempo real |
| 2 | Diagnósticos automáticos quando algo dá errado |
| 3 | Gerenciar Docker de forma completa: `ps`, `logs`, `restart`, `inspect`, `exec` |
| 4 | Limpeza automática de arquivos temporários e cache |
| 5 | Monitorar a saúde dos agentes e do sistema |
| 6 | Gerenciar backups automáticos do NeuroValen |
| 7 | Detectar e avisar quando o sistema está lento ou com pouco espaço |
| 8 | Auto-reparo de problemas comuns (processos travados, portas ocupadas, etc.) |
| 9 | Monitorar conexão com internet e status dos provedores de IA |
| 10 | Controlar modo de economia de bateria (especialmente no Termux) |

**Sandbox:** `docker` (isolamento máximo — o Nexus executa dentro de container efêmero)  
**Autonomia:** Alta  

---

### 4.4 Analyst ◇

**Papel:** Análise profunda, relatórios e raciocínio estratégico.

**Responsabilidades:**
- Analisar dados, padrões e tendências
- Gerar relatórios e sínteses estruturadas
- Fazer raciocínio profundo e estratégico sobre projetos e decisões
- Buscar e processar contexto do NeuroValen para enriquecer análises
- Comparar opções e recomendar caminhos

**Sandbox:** `safe`  
**Autonomia:** Média  
**Uso intensivo de:** NeuroValen (leitura e escrita)

---

## 5. NEUROVALEN — O CÉREBRO CENTRAL

### 5.1 Identidade
- Nome oficial: **NeuroValen**
- Substitui qualquer sistema de "Brain" anterior
- É o **único** repositório de memória de longo prazo do sistema

### 5.2 Arquitetura
- **Notas Markdown** com estrutura semântica
- **Wikilinks** e **backlinks** entre notas (estilo Obsidian)
- **Grafo de conhecimento** visualizável
- **Busca híbrida**: semântica (embeddings) + full-text (BM25/fuzzy)
- **RAG** (Retrieval-Augmented Generation) para uso pelos agentes

### 5.3 O que armazena (automaticamente)
- Conversas importantes (filtradas por relevância)
- Planos e objetivos ativos
- Decisões tomadas e seu contexto
- Projetos em andamento e seu estado
- Informações financeiras relevantes
- Lembretes e tarefas
- Aprendizados e reflexões registrados pelo usuário
- Logs estruturados de ações dos agentes

### 5.4 Regras de uso
- **Todo** agente lê **e** escreve no NeuroValen via `MemoryTool`
- Nenhum agente acessa o sistema de arquivos do NeuroValen diretamente (sempre via Tool)
- Backups automáticos gerenciados pelo Nexus

---

## 6. SISTEMA DE TOOLS SEGURO + SANDBOX

Este é o **pilar central de segurança** da v1.0.0. Sem este sistema funcionando corretamente, nenhuma outra feature deve ser liberada.

### 6.1 Estrutura Base

```python
from typing import Any, Literal
from dataclasses import dataclass, field

@dataclass
class ToolResult:
    ok: bool
    result: Any = None
    error: str | None = None
    duration_ms: int = 0
    audit_hash: str = ""
    metadata: dict = field(default_factory=dict)

@dataclass
class ToolContext:
    agent_id: str
    user_id: str
    session_id: str
    permissions: set[str]
    sandbox_mode: Literal["safe", "restricted", "docker", "unrestricted"]
    dry_run: bool = False

class ToolBase:
    name: str
    description: str
    version: str = "1.0.0"
    required_permissions: set[str]           # ex: {"execute", "shell", "network"}
    risk_level: Literal["low", "medium", "high", "critical"]
    timeout_seconds: int = 60
    sandbox_mode: Literal["safe", "restricted", "docker"] = "safe"

    def validate(self, action: str, args: dict, context: ToolContext) -> bool:
        """Valida permissões e risco antes de executar."""
        ...

    def run(self, action: str, args: dict, context: ToolContext) -> ToolResult:
        """Executa a ação com segurança."""
        ...

    def audit(self, action: str, args: dict, result: ToolResult, context: ToolContext) -> None:
        """Registra a execução no Audit Trail."""
        ...
```

### 6.2 ToolResult Padronizado (formato fixo, imutável)

```json
{
  "ok": true,
  "result": "<any>",
  "error": null,
  "duration_ms": 123,
  "audit_hash": "sha256:abc123...",
  "metadata": {
    "agent_id": "CEO",
    "sandbox_mode": "safe",
    "tier": "READ_ONLY",
    "timestamp": "2026-06-01T12:00:00Z"
  }
}
```

### 6.3 Execution Tiers (classificação obrigatória de risco)

| Tier | Nível | Exemplos de comandos | Risco | Pede Aprovação? | Dry-run padrão |
|------|-------|---------------------|-------|-----------------|----------------|
| `READ_ONLY` | Baixo | `ls`, `cat`, `ps`, `df`, `free`, `ping`, `curl` (GET) | Muito baixo | Não | Não |
| `REVERSIBLE` | Médio | `mkdir`, `touch`, `cp`, `echo`, `curl` (POST seguro) | Baixo | Não | Sim |
| `DESTRUCTIVE` | Alto | `rm`, `mv`, `rmdir`, `truncate`, `sed -i` | Alto | Sim | Sim |
| `SYSTEM_LEVEL` | Crítico | `systemctl`, `docker`, `apt`, `reboot`, `kill`, `chmod`, `chown` | Crítico | Sempre | Sim |

### 6.4 Sandbox Modes

| Modo | Uso Recomendado | Nível de Restrição |
|------|----------------|-------------------|
| `safe` | Padrão para Forge e Analyst | Máximo |
| `restricted` | CEO em operações específicas | Alto |
| `docker` | Nexus (container efêmero isolado) | Máximo + isolamento de rede |
| `unrestricted` | CEO com aprovação explícita documentada | Nenhum (use com extremo cuidado) |

### 6.5 ALWAYS_BLOCKED — nunca executar independente de permissão

```python
ALWAYS_BLOCKED = [
    # Deleções catastróficas
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    r"rm\s+-rf\s+~",
    # Operações de disco
    "dd if=",
    "mkfs",
    "format",
    "fdisk",
    "parted",
    # Desligamento
    "reboot",
    "shutdown",
    "halt",
    "poweroff",
    "init 0",
    "init 6",
    # Escalada de privilégio
    "sudo ",
    "su -",
    "doas ",
    # Permissões perigosas
    "chmod 777",
    "chown -R root",
    # Kill do próprio sistema
    "pkill -f valen",
    "killall python",
    "kill -9 1",
]
```

### 6.6 ACL (Access Control List)

Cada agente tem uma lista explícita de permissions que **pode** usar:

```python
AGENT_PERMISSIONS = {
    "CEO":     {"read", "write", "execute", "network", "memory", "docker_inspect"},
    "Forge":   {"read", "write", "execute", "memory"},
    "Nexus":   {"read", "write", "execute", "network", "docker_full", "memory", "system_monitor"},
    "Analyst": {"read", "memory", "network_read"},
}
```

### 6.7 Audit Trail

Toda execução de Tool **deve** gerar uma entrada imutável no Audit Trail:

```json
{
  "timestamp": "ISO8601",
  "agent_id": "Forge",
  "tool_name": "FilesystemTool",
  "action": "write_file",
  "args_hash": "sha256:...",
  "tier": "REVERSIBLE",
  "sandbox_mode": "safe",
  "dry_run": false,
  "result_ok": true,
  "duration_ms": 45,
  "audit_hash": "sha256:..."
}
```

### 6.8 Tools Obrigatórias na v1.0.0

| Tool | Responsabilidade | Tier máximo | Agente principal |
|------|-----------------|-------------|-----------------|
| `FilesystemTool` | Leitura e escrita de arquivos | DESTRUCTIVE | Forge |
| `TerminalTool` | Execução de comandos shell com Sandbox | SYSTEM_LEVEL | Forge, Nexus |
| `BrowserTool` | Navegação e scraping web | REVERSIBLE | CEO, Forge |
| `VisionTool` | Análise de imagens e vídeos | READ_ONLY | CEO, Analyst |
| `MemoryTool` | Leitura e escrita no NeuroValen | REVERSIBLE | Todos |
| `EventTool` | Criação de eventos, lembretes e agendamentos | REVERSIBLE | CEO |
| `NetworkTool` | Chamadas HTTP e monitoramento de rede | READ_ONLY / REVERSIBLE | Nexus, CEO |
| `DockerTool` | Gerenciamento completo de containers | SYSTEM_LEVEL | Nexus |
| `ProviderTool` | Interface com todos os providers de IA | REVERSIBLE | Todos |

---

## 7. PROVIDERS DE IA — ARQUITETURA

### 7.1 Providers suportados na v1.0.0

- **Groq** — alta velocidade, ideal para respostas rápidas
- **Ollama** — local, sem custo, privacidade máxima
- **OpenAI** — GPT-4o e variantes
- **Anthropic** — Claude (atual) e Claude Max (futuro uso pesado)
- **Google Gemini** — multimodal
- **xAI Grok** — sendo testado pelo usuário (prioridade de testes)
- Outros configuráveis via `ProviderTool`

### 7.2 Arquitetura de Providers

```python
class ProviderBase:
    name: str
    model: str
    api_key_env: str
    supports_streaming: bool
    supports_vision: bool
    supports_tools: bool
    max_context_tokens: int
    cost_per_1k_tokens: float

    async def complete(self, messages: list, tools: list | None = None) -> ProviderResponse:
        ...

    async def stream(self, messages: list) -> AsyncGenerator[str, None]:
        ...
```

### 7.3 Provider padrão e fallback

- O sistema deve ter um **provider padrão configurável**
- Deve ter lógica de **fallback automático**: se o provider padrão falhar, tenta o próximo
- O Nexus monitora a saúde e latência de todos os providers em tempo real

### 7.4 Roadmap de Providers

| Prazo | Provider | Uso |
|-------|---------|-----|
| Agora | Grok (xAI) | Testes prioritários |
| Agora | Groq, Ollama | Uso diário rápido |
| Futuro próximo | Claude Max (Anthropic) | Tarefas pesadas de desenvolvimento e raciocínio |

---

## 8. VISUAL — NÚCLEO NEURAL (CYBERPUNK)

### 8.1 Identidade Visual
- Estilo: **cyberpunk escuro** com elementos de ficção científica
- Paleta principal: pretos profundos + ciano/azul elétrico + roxo + glow neon

### 8.2 Núcleo Neural — Referência: `valen-nucleo.html`
O núcleo visual deve ser melhorado usando como referência forte o arquivo `valen-nucleo.html` fornecido pelo usuário. Deve incluir:

- **Anéis neurais rotativos** em múltiplas velocidades e eixos
- **Partículas orbitando** o núcleo central com física suave
- **Shards flutuantes** ao redor (fragmentos geométricos brilhantes)
- **Campo de estrelas** como background dinâmico
- **Glow e bloom** nos elementos principais
- **Interação com mouse**: o núcleo reage ao movimento do cursor
- **Clique com explosão de energia**: ao clicar no núcleo, uma explosão de partículas é emitida
- **Respiração do núcleo**: pulso suave em loop indicando estado ativo

### 8.3 Status Visual dos Agentes
Cada agente deve ter um indicador visual próprio no dashboard:
- Cor única por agente
- Status: idle, thinking, executing, error
- Animação suave de transição entre estados

---

## 9. PLANO DE EXECUÇÃO — FASES OBRIGATÓRIAS

> **Você deve seguir rigorosamente esta ordem. Não pule fases. Peça confirmação antes de fases destrutivas.**

---

### Fase 0 — Análise e Plano de Refatoração (OBRIGATÓRIA)

**Entregável:** Arquivo `VALEN_v1.0.0_REFACTOR_PLAN.md`

Deve conter:
- Inventário completo do estado atual do projeto (todos os arquivos, agentes, tools existentes)
- Análise dos 16+ agentes atuais e mapeamento para Tools ou remoção
- Decisões de design do novo sistema de Tools + Sandbox
- Arquitetura de como os 4 agentes vão se comunicar via Tools
- Estratégia de Providers + preparação para Computer Use futuro
- Plano de migração faseado com lista de arquivos a criar/modificar/remover
- Estimativa de impacto de cada mudança

**⚠️ Antes de iniciar a Fase 1, solicite confirmação explícita do usuário.**

---

### Fase 1 — Sistema de Tools + Sandbox (PRIORIDADE MÁXIMA)

Implemente **antes de qualquer outra coisa**:

1. `ToolBase`, `ToolResult`, `ToolContext`
2. `Sandbox` com Execution Tiers, Sandbox Modes e lógica de ALWAYS_BLOCKED
3. `ACL` com permissões por agente
4. `Audit Trail` imutável
5. Tools obrigatórias: `FilesystemTool`, `TerminalTool`, `MemoryTool`, `NetworkTool`
6. Testes unitários e de integração cobrindo todos os tiers e modos

**⚠️ Não prossiga para a Fase 2 sem o sistema de Tools com testes passando.**

---

### Fase 2 — NeuroValen

1. Refatorar / implementar o NeuroValen como cérebro central único
2. Implementar busca híbrida (semântica + full-text)
3. Implementar `MemoryTool` completa com CRUD + busca
4. Garantir que o NeuroValen é o único ponto de escrita de memória de longo prazo
5. Testar leitura e escrita por múltiplos agentes simultaneamente

---

### Fase 3 — Refatoração dos 4 Agentes

1. Refatorar **CEO** para usar exclusivamente o sistema de Tools
2. Refatorar **Forge** com comportamento cauteloso/direto e integração com FilesystemTool + TerminalTool
3. Refatorar **Nexus** com todas as responsabilidades da Seção 4.3 funcionando
4. Refatorar **Analyst** com leitura profunda do NeuroValen
5. Garantir que **nenhum** dos 4 agentes executa efeitos colaterais fora de Tools
6. Implementar comunicação inteligente entre agentes (orquestrada pelo CEO)

---

### Fase 4 — Providers e Comunicação Multi-Agente

1. Garantir que **todos os providers** da Seção 7.1 funcionam após a refatoração
2. Implementar `ProviderBase` modular com suporte a fallback
3. Implementar monitoramento de saúde dos providers pelo Nexus
4. Implementar protocolo de comunicação entre agentes (mensagens estruturadas)
5. Preparar arquitetura para futura integração com Computer Use real

---

### Fase 5 — Visual do Núcleo

1. Melhorar o núcleo visual usando `valen-nucleo.html` como referência
2. Implementar todos os elementos visuais da Seção 8.2
3. Adicionar indicadores visuais de status dos 4 agentes
4. Garantir performance suave (60fps mínimo) em mobile e desktop

---

### Fase 6 — Testes e QA

1. Testes unitários para todo o sistema de Tools e Sandbox
2. Testes de integração para os 4 agentes
3. Testes de carga básicos para o NeuroValen
4. Testes de segurança para ALWAYS_BLOCKED e ACL
5. Testes no Termux (Android) e Docker

---

### Fase 7 — Atualização de Versão e Documentação

1. Atualizar **todo** o projeto para nome **VALEN** e versão **1.0.0**
2. Atualizar `pyproject.toml`, `Dockerfile`, todos os headers de arquivo
3. Atualizar `README.md` e `PROJECT.md` completos
4. Criar `CHANGELOG.md` documentando a refatoração
5. Criar documentação técnica do sistema de Tools e dos 4 agentes

---

## 10. PERSONALIDADE DETALHADA DO CEO

O CEO é o rosto do VALEN. A personalidade deve ser consistente e reconhecível.

### Tom de voz
- Inteligente, confiante, levemente informal mas sempre profissional
- Fala como alguém que está **do lado do usuário**, não como um assistente subserviente
- Usa **"meu rei"** de forma natural, nunca forçada
- Quando entregando notícias ruins ou erros: direto, claro, sem rodeios, mas com leveza

### Exemplos de comportamento

**Saudação proativa:**
> "Meu rei, bom dia. Três itens no seu radar hoje: o post do Instagram de ontem teve 2x o alcance normal, há uma fatura vencendo amanhã e o Forge terminou o módulo de autenticação. Quer o briefing completo ou prefere ir direto para o que é urgente?"

**Ao cometer um erro:**
> "Meu rei, errei feio ali. Tentei criar o arquivo na pasta errada e sobrescrevi um config. Restaurei pelo backup do Nexus — tá tudo de volta. Da próxima vez o Forge pede confirmação antes de qualquer `mv` em arquivos de config. Desculpa o susto."

**Quando liberado para autonomia:**
> "Entendido, meu rei. Modo direto ativado. Vou executar sem interrupções e te entrego o relatório quando terminar."

**Proatividade:**
> "Meu rei, notei que faz 4 dias que você não alimenta o NeuroValen com novas metas. Quer que eu prepare uma sessão de planejamento semanal agora?"

---

## 11. O QUE EVITAR — LISTA DEFINITIVA

- ❌ Nunca tente manter os 16+ agentes antigos — eles viram Tools ou são removidos
- ❌ Nunca execute comandos shell diretamente no código dos agentes
- ❌ Nunca delete arquivos antigos sem confirmação explícita do usuário
- ❌ Nunca crie complexidade desnecessária — simples e funcional é melhor que elegante e quebrado
- ❌ Nunca quebre o suporte a Termux e Docker
- ❌ Nunca quebre providers de IA que estavam funcionando
- ❌ Nunca pule testes — o sistema de Tools **deve** ter testes antes de ir para produção
- ❌ Nunca faça tudo de uma vez — siga as fases

---

## 12. QUALIDADE TÉCNICA EXIGIDA

- **Type hints** completos em todo lugar (Python 3.11+)
- **Dataclasses ou Pydantic** para todas as estruturas de dados
- **Tratamento de erro robusto** com mensagens claras e úteis
- **Logging estruturado** (JSON) com níveis adequados (DEBUG, INFO, WARNING, ERROR)
- **Async/await** em toda a stack de I/O
- **Timeouts** em todas as operações externas
- **Retry com backoff exponencial** para providers de IA e chamadas de rede
- **Arquitetura preparada para microserviços** (cada agente deve poder virar um serviço independente)
- **Suporte total a Termux** (Android, ARM, sem root) e **Docker**
- **Documentação inline** (docstrings) em todas as classes e funções públicas

---

## 13. ENTREGÁVEIS DA v1.0.0

Ao final de todas as fases, os seguintes itens **devem existir e funcionar**:

| # | Entregável | Status Esperado |
|---|-----------|----------------|
| 1 | Sistema de Tools + Sandbox + ACL + Audit Trail | ✅ Funcional + Testado |
| 2 | 4 agentes principais usando exclusivamente Tools | ✅ Funcional + Testado |
| 3 | NeuroValen como cérebro central único | ✅ Funcional |
| 4 | Todos os providers de IA funcionando | ✅ Funcional |
| 5 | Dashboard cyberpunk com núcleo visual melhorado | ✅ Funcional |
| 6 | Arquitetura preparada para Computer Use futuro | ✅ Documentado + Estruturado |
| 7 | Suite de testes cobrindo Tools e Sandbox | ✅ Passando |
| 8 | README.md, PROJECT.md e CHANGELOG.md atualizados | ✅ Completo |
| 9 | Nome VALEN e versão 1.0.0 em todos os arquivos | ✅ Consistente |
| 10 | Suporte a Termux e Docker validado | ✅ Testado |
| 11 | Interface limpa com núcleo + 2 botões de modo | ✅ Funcional |
| 12 | Card Engine com todos os tipos de caixa dinâmica | ✅ Funcional |
| 13 | Galeria de imagens com zoom e download | ✅ Funcional |
| 14 | Integração TTS/STT em ambos os modos | ✅ Funcional |
| 15 | Núcleo reativo ao áudio (voz e TTS) | ✅ Funcional |
| 16 | Arquitetura DDD + Clean + Hexagonal implementada | ✅ Estruturada |
| 17 | CQRS + Event Sourcing com Event Store no PostgreSQL | ✅ Funcional |
| 18 | Stack de observabilidade: Prometheus + Grafana + OpenTelemetry + Sentry | ✅ Funcional |
| 19 | PostgreSQL + Redis + Qdrant + MinIO configurados e integrados | ✅ Funcional |
| 20 | Computer Use: Screenshot + OCR + Mouse + Keyboard + Browser + Android | ✅ Arquitetado |
| 21 | Workflow Engine com triggers, nós, grafo visual e workflows pré-definidos | ✅ Funcional |
| 22 | Marketplace com suporte a Plugins, MCP Servers e Workflow Templates | ✅ Funcional |

---

## 14. INTERFACE DO USUÁRIO — UI/UX COMPLETA

Esta seção define a aparência, o comportamento e a lógica de interação de toda a interface do VALEN. O desenvolvedor deve seguir estas especificações com precisão.

---

### 14.1 Filosofia de Design da Interface

A interface do VALEN segue um princípio único: **máxima limpeza, mínima distração, máxima inteligência**.

- A tela deve estar **quase vazia por padrão** — só o núcleo neural no centro
- Todo conteúdo (caixas, imagens, texto, dados) aparece **dinamicamente conforme necessário**
- Quando o conteúdo some, a tela volta a ficar limpa
- Nunca há menus, sidebars ou elementos fixos além dos 2 botões de modo

---

### 14.2 Layout Base — Estado Inicial (Idle)

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                                                     │
│                                                     │
│                   [ NÚCLEO HTML ]                   │
│              (esfera neural animada)                │
│                                                     │
│                                                     │
│                                                     │
│          [ 💬 CHAT ]        [ 🎙️ VOZ ]              │
└─────────────────────────────────────────────────────┘
```

- **Fundo:** preto absoluto ou gradiente escuro cyberpunk
- **Núcleo:** o arquivo `valen-nucleo.html` injetado no centro da tela
- **2 botões fixos** no rodapé, centralizados, discretos (sem bordas grossas, glow sutil)
- Nenhum outro elemento visível

---

### 14.3 Os 2 Botões de Modo

#### Botão CHAT `💬`
- Ao clicar: ativa o **Modo Chat**
- Fica com glow ativo indicando modo selecionado
- O botão VOZ fica inativo/apagado

#### Botão VOZ `🎙️`
- Ao clicar: ativa o **Modo Voz**
- Fica com glow ativo indicando modo selecionado
- O botão CHAT fica inativo/apagado

**Regra:** Apenas um modo pode estar ativo por vez. Clicar no mesmo botão novamente desativa e volta ao estado idle.

---

### 14.4 MODO CHAT — Comportamento Completo

#### Ativação
Ao clicar no botão CHAT:
1. Uma **barra de input** sobe suavemente do rodapé (animação slide-up)
2. A barra tem: campo de texto à esquerda + botão de enviar à direita
3. O campo recebe foco automático (teclado abre no mobile)

#### Layout da barra de input

```
┌──────────────────────────────────────────┬────────┐
│  Digite sua mensagem...                  │   ➤   │
└──────────────────────────────────────────┴────────┘
```

- Estilo: fundo semitransparente escuro + borda com glow ciano sutil
- Botão de enviar: ícone de seta ou ícone VALEN
- Enter também envia
- A barra **não some** enquanto o modo chat estiver ativo

#### Resposta do VALEN no Modo Chat
- O VALEN responde **sempre em áudio** (TTS) + **sempre cria caixas visuais** (ver 14.6)
- Enquanto processa: o núcleo pulsa suavemente indicando "pensando"
- Quando começa a falar: o núcleo reage ao áudio (ver 14.5.3)

---

### 14.5 MODO VOZ — Comportamento Completo

#### Ativação
Ao clicar no botão VOZ:
1. A interface entra em modo **escuta ativa**
2. O núcleo HTML cresce levemente (scale up suave) e sua pulsação muda para o ritmo de escuta
3. Aparece um **indicador discreto** de status (ex: ponto piscando ou anel ao redor do núcleo)
4. **Nenhuma barra de texto aparece** — interação é 100% por voz

#### Estados do Núcleo no Modo Voz

| Estado | O que o núcleo faz |
|--------|--------------------|
| **Escutando** | Anéis rotativos aceleram levemente; partículas se aproximam do centro |
| **Usuário falando** | Anéis reagem à amplitude do áudio do microfone (ondas que pulsam no ritmo da voz) |
| **Processando** | Shards flutuam de forma mais intensa; glow aumenta |
| **VALEN falando** | Anéis reagem à amplitude do áudio de saída (TTS) — o núcleo "fala" visualmente |
| **Idle (aguardando)** | Pulsação suave padrão |

#### Resposta do VALEN no Modo Voz
- O VALEN responde **em áudio (TTS)** enquanto o núcleo reage visualmente
- Opcionalmente, caixas de conteúdo também podem aparecer (ex: se o usuário pediu dados financeiros por voz, as caixas aparecem mesmo no modo voz)
- Após a resposta, volta ao estado de escuta automaticamente

---

### 14.6 SISTEMA DE CAIXAS DINÂMICAS (CARD ENGINE)

Este é um dos sistemas mais importantes da interface. O VALEN deve **criar caixas automaticamente e inteligentemente** com base no tipo de conteúdo da resposta.

#### Princípio
O CEO analisa a intenção da resposta e escolhe automaticamente o tipo de caixa certo. O usuário **nunca escolhe** o tipo de caixa — isso é responsabilidade do VALEN.

#### Tipos de Caixa

---

##### 🃏 Caixa de Texto Simples
**Quando usar:** respostas gerais, conversas, opiniões, explicações

```
┌─────────────────────────────────────────────────────┐
│ ♛ VALEN                                    [×] [–] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Meu rei, o projeto está avançando bem. As fases    │
│  1 e 2 foram concluídas e a Fase 3 começa agora.   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

##### 🌤️ Caixa de Dados de Clima
**Quando usar:** perguntas sobre tempo, temperatura, previsão

```
┌─────────────────────────────────────────────────────┐
│ 🌤️ CLIMA — São Paulo                       [×] [–] │
├─────────────────────────────────────────────────────┤
│  Agora: 24°C  ·  Sensação: 26°C                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━       │
│  Manhã  ☀️ 22°    Tarde  ⛅ 26°    Noite  🌙 19°  │
│  Umidade: 68%  ·  Vento: 12 km/h NE               │
└─────────────────────────────────────────────────────┘
```

---

##### 💰 Caixa de Dados Financeiros
**Quando usar:** perguntas sobre finanças, gastos, saldo, resumo financeiro

```
┌─────────────────────────────────────────────────────┐
│ 💰 FINANÇAS — Hoje                         [×] [–] │
├─────────────────────────────────────────────────────┤
│  Saldo atual:     R$ 4.280,00                       │
│  Entradas hoje:   R$ 1.200,00  ↑                   │
│  Saídas hoje:     R$   347,50  ↓                   │
│  ─────────────────────────────────────────          │
│  🔴 Fatura vencendo amanhã: R$ 890,00               │
│  🟡 Meta do mês: 72% atingida                       │
└─────────────────────────────────────────────────────┘
```

---

##### 📱 Caixa de Redes Sociais / Instagram
**Quando usar:** perguntas sobre Instagram, alcance, engajamento, publicações

```
┌─────────────────────────────────────────────────────┐
│ 📱 INSTAGRAM — Análise de Hoje             [×] [–] │
├─────────────────────────────────────────────────────┤
│  Último post: 4h atrás                              │
│  ─────────────────────────────────────────          │
│  👁️  Alcance:       3.240   (+2x vs ontem) 🔥      │
│  ❤️  Curtidas:         287                          │
│  💬 Comentários:        41                          │
│  📤 Compartilhamentos:  18                          │
│  ─────────────────────────────────────────          │
│  💡 Sugestão: melhor horário para postar: 19h      │
└─────────────────────────────────────────────────────┘
```

---

##### 📋 Caixa de Lista / Múltiplos Itens
**Quando usar:** listas de tarefas, opções, lembretes, planos

```
┌─────────────────────────────────────────────────────┐
│ 📋 AGENDA DE HOJE                          [×] [–] │
├─────────────────────────────────────────────────────┤
│  ✅ Reunião com cliente — 10h (concluída)           │
│  ⏳ Deploy do módulo de auth — 14h                  │
│  🔴 Fatura vencer — amanhã                         │
│  ⬜ Revisar pitch deck — sem horário               │
│  ⬜ Postar no Instagram — 19h (recomendado)        │
└─────────────────────────────────────────────────────┘
```

---

##### 🖼️ Caixa de Imagens (GALERIA)
**Quando usar:** quando o VALEN gera ou exibe imagens (geração de imagens, referências visuais)

**Regra especial:** imagens **não têm caixa com título/header**. São exibidas diretamente em grade, sem moldura de card, ocupando espaço limpo.

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│              │  │              │  │              │
│   Imagem 1   │  │   Imagem 2   │  │   Imagem 3   │
│              │  │              │  │              │
│  [🔍] [⬇️]  │  │  [🔍] [⬇️]  │  │  [🔍] [⬇️]  │
└──────────────┘  └──────────────┘  └──────────────┘
```

**Interações com imagens:**
- `🔍` Zoom / Ampliar → abre a imagem em fullscreen com fundo preto
- `⬇️` Download → baixa a imagem no dispositivo
- Clique na imagem → também abre em fullscreen
- No fullscreen: arrastar para fechar (mobile) ou ESC (desktop)
- No fullscreen: setas para navegar entre imagens da mesma resposta

**Layout da grade:**
- 1 imagem → centralizada, tamanho médio
- 2 imagens → lado a lado
- 3–4 imagens → grade 2x2 ou linha de 3
- 5+ imagens → grade com scroll horizontal ou 3 colunas

---

#### 14.6.1 Comportamento de Múltiplas Caixas

Quando o usuário pede um **resumo geral** (ex: *"me dá todas as informações de hoje"*), o VALEN cria **múltiplas caixas organizadas**:

**Regras de layout de múltiplas caixas:**
- Caixas **nunca se sobrepõem**
- Aparecem com animação sequencial (uma de cada vez, com 150ms de delay entre elas)
- Se couberem lado a lado na tela → ficam lado a lado (grid de 2 colunas em desktop)
- Se não couberem → empilham verticalmente com scroll
- Em mobile → sempre empilhadas verticalmente
- O usuário pode **minimizar** `[–]` ou **fechar** `[×]` qualquer caixa individualmente
- Caixas minimizadas viram um **chip pequeno** no rodapé da tela

**Exemplo de múltiplas caixas lado a lado (desktop):**
```
┌──────────────────┐  ┌──────────────────┐
│ 💰 FINANÇAS      │  │ 📱 INSTAGRAM      │
│ ...              │  │ ...              │
└──────────────────┘  └──────────────────┘
┌──────────────────┐  ┌──────────────────┐
│ 🌤️ CLIMA         │  │ 📋 AGENDA        │
│ ...              │  │ ...              │
└──────────────────┘  └──────────────────┘
```

---

### 14.7 Comportamento do Áudio em Ambos os Modos

- Toda resposta do VALEN é falada em **TTS (Text-to-Speech)**
- A voz deve ter tom calmo, claro e ligeiramente profissional (não robótica)
- O TTS começa a falar **enquanto o texto ainda está sendo gerado** (streaming de áudio)
- O usuário pode **pausar o áudio** clicando no núcleo durante a fala
- O usuário pode **interromper** falando (modo voz) ou digitando (modo chat) — o VALEN para de falar imediatamente

---

### 14.8 Animações e Transições

Todas as animações devem seguir:
- **Duração:** 200–400ms para elementos de UI; 600–1000ms para o núcleo
- **Easing:** `ease-out` para entradas, `ease-in` para saídas
- **Performance:** 60fps mínimo em mobile e desktop
- **Nunca bloquear:** animações não podem travar a interface

| Evento | Animação |
|--------|----------|
| Caixa aparecendo | Fade-in + slide-up suave |
| Caixa fechando | Fade-out + scale-down |
| Caixa minimizando | Colapsa para chip com animação fluida |
| Barra de chat abrindo | Slide-up do rodapé |
| Barra de chat fechando | Slide-down para fora |
| Modo voz ativando | Núcleo escala +10%, partículas se aproximam |
| Usuário falando | Ondas de amplitude no núcleo |
| VALEN processando | Glow aumenta + shards aceleram |
| VALEN falando | Núcleo reage ao áudio TTS em tempo real |

---

### 14.9 Responsividade

| Dispositivo | Comportamento |
|-------------|--------------|
| **Mobile (Termux/Android)** | Caixas sempre empilhadas verticalmente · Núcleo centralizado · Teclado sobe a barra de input |
| **Desktop** | Caixas em grid de 2 colunas quando possível · Núcleo centralizado |
| **Tablet** | Grid de 2 colunas com caixas maiores |

O núcleo HTML deve **sempre ficar centralizado** e nunca ser coberto pelas caixas (caixas aparecem abaixo ou nas laterais do núcleo, nunca em cima).

---

### 14.10 Paleta de Cores das Caixas

Todas as caixas seguem a identidade cyberpunk:

| Elemento | Cor |
|----------|-----|
| Fundo da caixa | `rgba(10, 10, 20, 0.92)` — preto azulado semitransparente |
| Borda padrão | `1px solid rgba(0, 200, 255, 0.3)` — ciano sutil |
| Borda hover | `1px solid rgba(0, 200, 255, 0.8)` — ciano brilhante |
| Header da caixa | `rgba(0, 200, 255, 0.08)` — ciano escuro |
| Texto principal | `#e0e0e0` — branco suave |
| Texto secundário | `#888` — cinza |
| Destaque positivo | `#00ff88` — verde neon |
| Destaque negativo | `#ff4444` — vermelho neon |
| Destaque alerta | `#ffaa00` — âmbar |
| Glow do núcleo | `#00c8ff` / `#8800ff` — ciano + roxo |

---

### 14.11 Implementação Técnica da UI

- **Framework:** React ou Vue 3 (o que já está no projeto)
- **Animações:** CSS transitions + Web Animations API (sem bibliotecas pesadas)
- **TTS:** Web Speech API (navegador) com fallback para Piper WASM (já no projeto)
- **STT (voz → texto):** Whisper WASM (já no projeto) + Web Speech API como fallback
- **Núcleo HTML:** injetado via `<iframe>` sandboxed ou diretamente no DOM
- **Reatividade do núcleo ao áudio:** Web Audio API + `AnalyserNode` para capturar amplitude em tempo real e enviar para o núcleo via `postMessage` ou variável CSS
- **Galeria de imagens:** fullscreen via `<dialog>` nativo ou portal React
- **Grid de caixas:** CSS Grid com `auto-placement` + animações de entrada

---

## 15. ARQUITETURA ENTERPRISE

O VALEN deve ser construído desde a v1.0.0 com fundações de **arquitetura enterprise de nível profissional**. Não é over-engineering — é a base que garante que o sistema escale sem precisar ser reescrito.

---

### 15.1 Domain Driven Design (DDD)

O projeto inteiro é organizado por **domínios de negócio**, não por camadas técnicas.

#### Bounded Contexts do VALEN

| Domínio | Responsabilidade | Agente principal |
|---------|-----------------|-----------------|
| `agents` | CEO, Forge, Nexus, Analyst | Todos |
| `memory` | NeuroValen, notas, busca | Analyst |
| `tools` | Sandbox, ACL, Audit Trail | Forge, Nexus |
| `automation` | Workflows, triggers, agendamentos | Forge, CEO |
| `computer_use` | OCR, screenshot, mouse, teclado, browser | Forge |
| `providers` | Integração com LLMs externos | Todos |
| `marketplace` | Plugins, MCPs, ferramentas externas | CEO |
| `observability` | Métricas, logs, traces, alertas | Nexus |
| `finance` | Dados financeiros, alertas | Analyst |
| `social` | Redes sociais, agendamento, análise | CEO |

#### Estrutura de pastas por domínio

```
valen/
├── domains/
│   ├── agents/
│   │   ├── entities/          # Agent, AgentState, AgentMessage
│   │   ├── value_objects/     # AgentId, Permission, SandboxMode
│   │   ├── repositories/      # IAgentRepository (interface)
│   │   ├── services/          # AgentOrchestrationService
│   │   ├── events/            # AgentStarted, AgentFailed, AgentCompleted
│   │   └── commands/          # RunAgentCommand, StopAgentCommand
│   ├── memory/
│   │   ├── entities/          # Note, NoteLink, Memory
│   │   ├── repositories/      # IMemoryRepository
│   │   ├── services/          # MemorySearchService, EmbeddingService
│   │   └── events/            # NoteCreated, NoteUpdated, MemoryAccessed
│   ├── tools/
│   │   ├── entities/          # Tool, ToolExecution, AuditEntry
│   │   ├── value_objects/     # RiskLevel, ExecutionTier, ToolResult
│   │   ├── repositories/      # IToolRepository, IAuditRepository
│   │   └── services/          # SandboxService, ACLService, AuditService
│   ├── automation/
│   ├── computer_use/
│   ├── providers/
│   ├── marketplace/
│   └── observability/
├── infrastructure/            # implementações concretas (DB, Redis, etc.)
├── application/               # Use cases / command handlers
├── interfaces/                # FastAPI, WebSocket, CLI
└── shared/                    # Kernel compartilhado (base classes, eventos base)
```

---

### 15.2 Clean Architecture

Cada domínio segue o modelo de **camadas concêntricas** onde as dependências sempre apontam para dentro:

```
┌─────────────────────────────────────────────┐
│           Interfaces (FastAPI, WS, CLI)      │  ← camada mais externa
├─────────────────────────────────────────────┤
│         Application (Use Cases, CQRS)        │
├─────────────────────────────────────────────┤
│         Domain (Entities, Services)          │
├─────────────────────────────────────────────┤
│         Infrastructure (DB, Redis, APIs)     │  ← implementações
└─────────────────────────────────────────────┘
```

**Regra absoluta:** camadas internas **nunca** importam de camadas externas. O Domain não sabe que existe FastAPI, PostgreSQL ou Redis. Ele trabalha apenas com interfaces (protocolos/ABCs).

```python
# CERTO — Domain define a interface
class IMemoryRepository(Protocol):
    async def save(self, note: Note) -> None: ...
    async def find_by_id(self, id: NoteId) -> Note | None: ...

# CERTO — Infrastructure implementa
class PostgresMemoryRepository:
    async def save(self, note: Note) -> None:
        # aqui sim pode usar SQLAlchemy, asyncpg, etc.
        ...

# ERRADO — Domain importar infra
from sqlalchemy import Session  # ← NUNCA no domain
```

---

### 15.3 Hexagonal Architecture (Ports & Adapters)

O VALEN expõe **Ports** (interfaces) e conecta **Adapters** (implementações concretas). Isso permite trocar qualquer componente sem tocar no core.

#### Ports de entrada (Driving Ports)
```python
class IAgentPort(Protocol):
    async def run(self, command: AgentCommand) -> AgentResult: ...

class IWorkflowPort(Protocol):
    async def trigger(self, workflow_id: str, payload: dict) -> WorkflowRun: ...
```

#### Ports de saída (Driven Ports)
```python
class IProviderPort(Protocol):
    async def complete(self, messages: list[Message]) -> ProviderResponse: ...

class IStoragePort(Protocol):
    async def upload(self, key: str, data: bytes) -> str: ...

class ISearchPort(Protocol):
    async def semantic_search(self, query: str, top_k: int) -> list[SearchResult]: ...
```

#### Adapters concretos
- `ProviderPort` → adaptadores: `GroqAdapter`, `OllamaAdapter`, `AnthropicAdapter`, `GrokAdapter`
- `StoragePort` → adaptador: `MinIOAdapter`
- `SearchPort` → adaptador: `QdrantAdapter`
- `CachePort` → adaptador: `RedisAdapter`
- `DatabasePort` → adaptador: `PostgresAdapter`

---

### 15.4 CQRS (Command Query Responsibility Segregation)

Toda operação no VALEN é classificada como **Command** (escreve/muda estado) ou **Query** (lê, nunca muda estado).

#### Commands — mudam estado, disparam eventos

```python
@dataclass
class RunAgentCommand:
    agent_id: str
    user_message: str
    session_id: str
    context: dict

@dataclass
class CreateNoteCommand:
    title: str
    content: str
    tags: list[str]
    author_agent: str

@dataclass
class ExecuteToolCommand:
    tool_name: str
    action: str
    args: dict
    agent_id: str
    session_id: str
```

#### Queries — leem estado, sem efeitos colaterais

```python
@dataclass
class GetAgentStatusQuery:
    agent_id: str

@dataclass
class SearchMemoryQuery:
    query: str
    top_k: int = 10
    filters: dict = field(default_factory=dict)

@dataclass
class GetAuditTrailQuery:
    agent_id: str | None = None
    since: datetime | None = None
    limit: int = 100
```

#### Command Bus e Query Bus

```python
class CommandBus:
    async def dispatch(self, command: BaseCommand) -> CommandResult:
        handler = self._handlers[type(command)]
        return await handler.handle(command)

class QueryBus:
    async def ask(self, query: BaseQuery) -> Any:
        handler = self._handlers[type(query)]
        return await handler.handle(query)
```

---

### 15.5 Event Sourcing

O estado de todo **agente, workflow e ferramenta** é derivado de uma sequência de eventos imutáveis armazenados. Nunca se sobrescreve o estado — apenas se acrescenta novos eventos.

#### Event Store

```python
@dataclass
class DomainEvent:
    event_id: str                    # UUID único
    event_type: str                  # "AgentStarted", "ToolExecuted", etc.
    aggregate_id: str                # ID da entidade dona do evento
    aggregate_type: str              # "Agent", "Workflow", "Tool"
    payload: dict                    # dados do evento
    metadata: dict                   # session_id, user_id, timestamp
    version: int                     # sequência dentro do aggregate
    occurred_at: datetime

# Exemplos de eventos do VALEN
class AgentStartedEvent(DomainEvent): ...
class AgentCompletedEvent(DomainEvent): ...
class AgentFailedEvent(DomainEvent): ...
class ToolExecutedEvent(DomainEvent): ...
class ToolBlockedEvent(DomainEvent): ...
class NoteCreatedEvent(DomainEvent): ...
class WorkflowTriggeredEvent(DomainEvent): ...
class WorkflowStepCompletedEvent(DomainEvent): ...
class PluginInstalledEvent(DomainEvent): ...
```

#### Projeções (Read Models)

A partir do Event Store, projeções geram visões otimizadas para leitura:

```python
class AgentStatusProjection:
    """Mantém o estado atual de cada agente derivado dos eventos."""
    agent_id: str
    status: Literal["idle", "thinking", "executing", "error"]
    last_active: datetime
    current_task: str | None

class AuditProjection:
    """Visão completa do audit trail, já formatada para consulta."""
    ...

class WorkflowHistoryProjection:
    """Histórico de execuções de workflows."""
    ...
```

---

## 16. OBSERVABILIDADE

O VALEN deve ser **completamente observável** em produção. Qualquer problema deve ser detectável, diagnosticável e rastreável sem precisar de acesso direto ao servidor.

---

### 16.1 OpenTelemetry (Tracing Distribuído)

Toda operação significativa gera um **trace com spans**:

```python
from opentelemetry import trace

tracer = trace.get_tracer("valen.agents")

async def run_agent(command: RunAgentCommand):
    with tracer.start_as_current_span("agent.run") as span:
        span.set_attribute("agent.id", command.agent_id)
        span.set_attribute("session.id", command.session_id)
        span.set_attribute("message.length", len(command.user_message))

        with tracer.start_as_current_span("agent.tool_execution"):
            result = await tool.run(...)
            span.set_attribute("tool.name", tool.name)
            span.set_attribute("tool.tier", result.tier)
            span.set_attribute("tool.ok", result.ok)
```

**O que deve ser traceable:**
- Cada execução de agente (do recebimento da mensagem até a resposta)
- Cada execução de Tool (incluindo tier, sandbox mode, duração)
- Cada chamada a um provider de IA (modelo, tokens, latência, custo)
- Cada operação no NeuroValen (busca, escrita, leitura)
- Cada step de workflow

**Exportador:** OTLP → Jaeger (desenvolvimento) / Grafana Tempo (produção)

---

### 16.2 Prometheus (Métricas)

Métricas expostas no endpoint `/metrics`:

```python
from prometheus_client import Counter, Histogram, Gauge

# Contadores
agent_runs_total = Counter("valen_agent_runs_total", "Total de execuções de agentes", ["agent_id", "status"])
tool_executions_total = Counter("valen_tool_executions_total", "Total de execuções de tools", ["tool_name", "tier", "ok"])
provider_calls_total = Counter("valen_provider_calls_total", "Total de chamadas a providers", ["provider", "model"])
provider_tokens_total = Counter("valen_provider_tokens_total", "Total de tokens consumidos", ["provider", "model", "direction"])

# Histogramas (latência)
agent_duration_seconds = Histogram("valen_agent_duration_seconds", "Latência das execuções de agentes", ["agent_id"])
tool_duration_seconds = Histogram("valen_tool_duration_seconds", "Latência das execuções de tools", ["tool_name"])
provider_duration_seconds = Histogram("valen_provider_duration_seconds", "Latência das chamadas a providers", ["provider"])
memory_search_duration_seconds = Histogram("valen_memory_search_seconds", "Latência de buscas no NeuroValen")

# Gauges (estado atual)
active_agents = Gauge("valen_active_agents", "Agentes atualmente em execução")
neurovalen_notes_total = Gauge("valen_neurovalen_notes_total", "Total de notas no NeuroValen")
system_cpu_percent = Gauge("valen_system_cpu_percent", "CPU atual (%)")
system_memory_percent = Gauge("valen_system_memory_percent", "RAM atual (%)")
provider_health = Gauge("valen_provider_health", "Saúde dos providers (1=ok, 0=down)", ["provider"])
```

---

### 16.3 Grafana (Dashboards)

O Nexus provisiona automaticamente os seguintes dashboards no Grafana:

| Dashboard | O que mostra |
|-----------|-------------|
| **VALEN Overview** | Status geral: agentes ativos, requests/min, erros/min, uptime |
| **Agents Performance** | Latência p50/p95/p99 por agente, taxa de erro, execuções por hora |
| **Tools & Sandbox** | Execuções por tier, comandos bloqueados, tempo médio por tool |
| **Providers** | Latência por provider, tokens consumidos, custo estimado, health |
| **NeuroValen** | Volume de notas, latência de busca, escritas/leituras por hora |
| **System Health** | CPU, RAM, disco, temperatura, bateria (Termux), conexão de rede |
| **Workflows** | Execuções por workflow, taxa de sucesso, etapas com maior falha |
| **Security & Audit** | Comandos bloqueados, tentativas de escalada de privilégio, ACL violations |

**Stack completa de observabilidade:**
```yaml
# docker-compose.observability.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    environment:
      GF_SECURITY_ADMIN_PASSWORD: valen_admin

  jaeger:
    image: jaegertracing/all-in-one:latest

  loki:
    image: grafana/loki:latest   # agregação de logs

  tempo:
    image: grafana/tempo:latest  # backend de traces
```

---

### 16.4 Sentry (Error Tracking)

Toda exceção não tratada e todo erro crítico vai para o Sentry:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration(), AsyncioIntegration()],
    traces_sample_rate=0.1,      # 10% dos traces vão para Sentry
    profiles_sample_rate=0.05,   # 5% com profiling
    environment=settings.ENV,    # "development" | "production"
    release=f"valen@{settings.VERSION}",
)
```

**O que o Sentry captura no VALEN:**
- Exceções não tratadas em qualquer agente ou Tool
- Timeouts de providers de IA
- Falhas de conexão com banco de dados
- Erros de validação de ACL
- Crashes do sistema de workflows
- Performance issues (transações lentas > threshold configurável)

**Contexto adicionado automaticamente a cada evento:**
```python
with sentry_sdk.push_scope() as scope:
    scope.set_tag("agent_id", context.agent_id)
    scope.set_tag("session_id", context.session_id)
    scope.set_tag("tool_name", tool.name)
    scope.set_context("valen", {
        "version": "1.0.0",
        "sandbox_mode": context.sandbox_mode,
        "provider": context.provider_name,
    })
```

---

## 17. BANCO DE DADOS

O VALEN usa **quatro sistemas de armazenamento especializados**, cada um com papel bem definido. Nenhum substitui o outro.

---

### 17.1 PostgreSQL — Banco Relacional Principal

**Para que serve no VALEN:**
- Event Store (todos os DomainEvents em ordem)
- Audit Trail imutável
- Projeções/Read Models (AgentStatus, WorkflowHistory, etc.)
- Dados financeiros
- Configurações de usuário e agentes
- Registro de plugins instalados
- Metadados de arquivos no MinIO

**Schema principal:**

```sql
-- Event Store (imutável — nunca UPDATE/DELETE)
CREATE TABLE domain_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type      VARCHAR(100) NOT NULL,
    aggregate_id    VARCHAR(100) NOT NULL,
    aggregate_type  VARCHAR(50) NOT NULL,
    payload         JSONB NOT NULL,
    metadata        JSONB NOT NULL DEFAULT '{}',
    version         INTEGER NOT NULL,
    occurred_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (aggregate_id, version)
);
CREATE INDEX ON domain_events (aggregate_id, version);
CREATE INDEX ON domain_events (event_type, occurred_at);

-- Audit Trail (append-only)
CREATE TABLE audit_trail (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id        VARCHAR(50) NOT NULL,
    tool_name       VARCHAR(100) NOT NULL,
    action          VARCHAR(100) NOT NULL,
    args_hash       VARCHAR(64) NOT NULL,
    tier            VARCHAR(20) NOT NULL,
    sandbox_mode    VARCHAR(20) NOT NULL,
    dry_run         BOOLEAN NOT NULL DEFAULT FALSE,
    result_ok       BOOLEAN NOT NULL,
    duration_ms     INTEGER NOT NULL,
    audit_hash      VARCHAR(64) NOT NULL,
    session_id      VARCHAR(100),
    executed_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Plugins instalados
CREATE TABLE installed_plugins (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plugin_id       VARCHAR(100) UNIQUE NOT NULL,
    name            VARCHAR(200) NOT NULL,
    version         VARCHAR(20) NOT NULL,
    type            VARCHAR(20) NOT NULL,  -- 'tool' | 'mcp' | 'workflow'
    config          JSONB NOT NULL DEFAULT '{}',
    enabled         BOOLEAN NOT NULL DEFAULT TRUE,
    installed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Conexão:** `asyncpg` com pool de conexões gerenciado pelo `asyncpg.create_pool()`

---

### 17.2 Redis — Cache, Filas e Estado em Tempo Real

**Para que serve no VALEN:**
- Cache de respostas de providers (evitar chamadas duplicadas)
- Cache de buscas frequentes no NeuroValen
- Sessões ativas de agentes (estado em memória)
- Pub/Sub para comunicação entre agentes em tempo real
- Filas de tasks para processamento assíncrono
- Rate limiting de chamadas a providers
- TTL de contexto de conversas

**Padrões de uso:**

```python
# Cache de provider com TTL
await redis.setex(
    f"provider:response:{hash(messages)}",
    ttl=300,  # 5 minutos
    value=json.dumps(response)
)

# Estado de sessão do agente
await redis.hset(
    f"agent:session:{session_id}",
    mapping={
        "agent_id": "CEO",
        "status": "thinking",
        "started_at": datetime.now().isoformat()
    }
)
await redis.expire(f"agent:session:{session_id}", 3600)

# Pub/Sub para comunicação inter-agentes
await redis.publish(f"agent:{target_agent_id}", json.dumps(message))

# Fila de tasks
await redis.lpush("valen:tasks:forge", json.dumps(task))
task = await redis.brpop("valen:tasks:forge", timeout=30)
```

---

### 17.3 Qdrant — Banco Vetorial (NeuroValen)

**Para que serve no VALEN:**
- Armazenar embeddings de todas as notas do NeuroValen
- Busca semântica por similaridade (cosine distance)
- Busca por contexto: *"o que eu decidi sobre X?"*, *"quais projetos estão parados?"*
- Memória associativa dos agentes

**Collections do Qdrant:**

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url=settings.QDRANT_URL)

# Collection principal do NeuroValen
client.create_collection(
    collection_name="neurovalen_notes",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Collection de memória de conversas
client.create_collection(
    collection_name="conversation_memory",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Collection de aprendizados e decisões
client.create_collection(
    collection_name="decisions_memory",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)
```

**Busca híbrida (semântica + filtros):**

```python
results = client.search(
    collection_name="neurovalen_notes",
    query_vector=embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="tags", match=MatchAny(any=["finanças", "projeto"]))
        ]
    ),
    limit=10,
    with_payload=True
)
```

---

### 17.4 MinIO — Object Storage (Arquivos e Mídia)

**Para que serve no VALEN:**
- Armazenar screenshots capturados pelo Computer Use
- Guardar imagens geradas por IA
- Guardar arquivos de builds (APKs, executáveis, zips)
- Guardar backups do NeuroValen
- Guardar arquivos de upload do usuário
- Armazenar vídeos e áudios processados

**Buckets:**

| Bucket | Conteúdo | TTL |
|--------|---------|-----|
| `valen-screenshots` | Screenshots do Computer Use | 7 dias |
| `valen-generated` | Imagens e arquivos gerados por IA | 30 dias |
| `valen-builds` | APKs, executáveis, builds | 90 dias |
| `valen-backups` | Backups automáticos do NeuroValen | Permanente |
| `valen-uploads` | Uploads do usuário | Permanente |
| `valen-audio` | Áudios TTS cacheados e gravações de voz | 7 dias |

```python
from minio import Minio

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)

# Upload de screenshot
client.put_object(
    "valen-screenshots",
    f"screenshots/{session_id}/{timestamp}.png",
    data=screenshot_bytes,
    length=len(screenshot_bytes),
    content_type="image/png",
)
```

---

## 18. COMPUTER USE — ESPECIFICAÇÃO COMPLETA

O Computer Use é o sistema que permite ao VALEN **controlar o computador e dispositivos reais** como um humano faria. Na v1.0.0 a arquitetura é implementada mesmo que algumas capacidades sejam graduais.

---

### 18.1 Screenshot Engine

**Responsabilidade:** capturar a tela inteira ou regiões específicas em qualquer momento.

```python
class ScreenshotEngine:
    """Captura screenshots do sistema."""

    async def capture_full(self) -> Screenshot:
        """Captura a tela inteira."""
        ...

    async def capture_region(self, x: int, y: int, w: int, h: int) -> Screenshot:
        """Captura uma região específica da tela."""
        ...

    async def capture_window(self, window_title: str) -> Screenshot:
        """Captura uma janela específica pelo título."""
        ...

    async def capture_continuous(self, fps: int = 5) -> AsyncGenerator[Screenshot, None]:
        """Captura contínua para monitoramento de ações."""
        ...

@dataclass
class Screenshot:
    image_bytes: bytes
    width: int
    height: int
    captured_at: datetime
    storage_url: str    # URL no MinIO após upload automático
    session_id: str
```

**Implementação por plataforma:**
- Linux/Desktop: `mss` (multi-screen shots) ou `scrot`
- Windows: `mss` ou `pygetwindow` + `PIL`
- Android/Termux: `adb shell screencap` via ADB
- Docker: `Xvfb` (virtual framebuffer) + `mss`

---

### 18.2 OCR Engine

**Responsabilidade:** extrair texto de screenshots, imagens e PDFs com alta precisão.

```python
class OCREngine:
    """Extração de texto de imagens e screenshots."""

    async def extract_text(self, image: Screenshot | bytes) -> OCRResult:
        """Extrai texto completo da imagem."""
        ...

    async def extract_regions(self, image: Screenshot) -> list[TextRegion]:
        """Identifica e extrai regiões de texto com coordenadas."""
        ...

    async def find_text(self, image: Screenshot, query: str) -> list[TextMatch]:
        """Localiza texto específico na imagem e retorna coordenadas."""
        ...

    async def read_ui_elements(self, image: Screenshot) -> UIElements:
        """Identifica botões, campos, menus e outros elementos de UI."""
        ...

@dataclass
class TextRegion:
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float

@dataclass
class UIElements:
    buttons: list[TextRegion]
    inputs: list[TextRegion]
    menus: list[TextRegion]
    labels: list[TextRegion]
```

**Backends disponíveis (em ordem de prioridade):**
1. **Tesseract** — local, rápido, sem custo (padrão)
2. **EasyOCR** — melhor para textos mistos e idiomas múltiplos
3. **Claude Vision** — para casos complexos onde precisão é crítica (via `ProviderTool`)
4. **PaddleOCR** — alternativa de alta performance

---

### 18.3 Mouse Controller

**Responsabilidade:** mover o cursor e executar cliques com precisão.

```python
class MouseController:
    """Controle do mouse do sistema."""

    async def move(self, x: int, y: int, duration_ms: int = 200) -> None:
        """Move o cursor para coordenadas absolutas com animação suave."""
        ...

    async def move_relative(self, dx: int, dy: int) -> None:
        """Move o cursor relativamente à posição atual."""
        ...

    async def click(self, x: int, y: int, button: Literal["left", "right", "middle"] = "left") -> None:
        """Clica em coordenadas específicas."""
        ...

    async def double_click(self, x: int, y: int) -> None:
        """Duplo clique em coordenadas."""
        ...

    async def right_click(self, x: int, y: int) -> None:
        """Clique direito."""
        ...

    async def drag(self, from_x: int, from_y: int, to_x: int, to_y: int, duration_ms: int = 500) -> None:
        """Arrasta de um ponto a outro."""
        ...

    async def scroll(self, x: int, y: int, amount: int, direction: Literal["up", "down", "left", "right"] = "down") -> None:
        """Scroll em coordenadas."""
        ...

    async def click_element(self, element: TextRegion) -> None:
        """Clica em um elemento encontrado pelo OCR."""
        center_x = element.x + element.width // 2
        center_y = element.y + element.height // 2
        await self.click(center_x, center_y)
```

**Implementação por plataforma:**
- Desktop: `pyautogui` ou `pynput`
- Android: `adb shell input tap {x} {y}`

---

### 18.4 Keyboard Controller

**Responsabilidade:** digitar texto e executar atalhos de teclado.

```python
class KeyboardController:
    """Controle do teclado do sistema."""

    async def type_text(self, text: str, interval_ms: int = 20) -> None:
        """Digita texto caractere por caractere com intervalo natural."""
        ...

    async def type_fast(self, text: str) -> None:
        """Digita texto de forma instantânea (clipboard paste)."""
        ...

    async def press_key(self, key: str) -> None:
        """Pressiona uma tecla (ex: 'enter', 'tab', 'escape', 'f5')."""
        ...

    async def press_combination(self, *keys: str) -> None:
        """Pressiona combinação de teclas (ex: 'ctrl', 'c')."""
        ...

    async def press_and_hold(self, key: str, duration_ms: int) -> None:
        """Mantém uma tecla pressionada por um período."""
        ...

    async def clear_field(self) -> None:
        """Seleciona tudo e deleta (ctrl+a, delete)."""
        ...
```

---

### 18.5 Browser Automation

**Responsabilidade:** controlar navegadores para tarefas web complexas que a BrowserTool simples não resolve.

```python
class BrowserAutomation:
    """Automação completa de navegador via Playwright."""

    async def open(self, url: str, browser: Literal["chromium", "firefox", "webkit"] = "chromium") -> BrowserSession:
        ...

    async def navigate(self, session: BrowserSession, url: str) -> None:
        ...

    async def find_element(self, session: BrowserSession, selector: str) -> Element:
        ...

    async def click_element(self, session: BrowserSession, selector: str) -> None:
        ...

    async def fill_field(self, session: BrowserSession, selector: str, value: str) -> None:
        ...

    async def extract_content(self, session: BrowserSession, selector: str = "body") -> str:
        ...

    async def take_screenshot(self, session: BrowserSession) -> Screenshot:
        ...

    async def execute_script(self, session: BrowserSession, script: str) -> Any:
        ...

    async def wait_for(self, session: BrowserSession, condition: str, timeout_ms: int = 5000) -> None:
        ...

    async def download_file(self, session: BrowserSession, url: str) -> str:
        """Baixa arquivo e salva no MinIO, retorna URL."""
        ...
```

**Backend:** Playwright (suporta Chromium, Firefox e WebKit)
**Uso:** login em sistemas, scraping de dados, preenchimento de formulários, interação com SPAs

---

### 18.6 Android Automation

**Responsabilidade:** controlar dispositivos Android remotamente via ADB.

```python
class AndroidAutomation:
    """Automação de dispositivos Android via ADB."""

    async def connect(self, device_id: str | None = None) -> AndroidSession:
        """Conecta ao dispositivo ADB (USB ou rede)."""
        ...

    async def take_screenshot(self, session: AndroidSession) -> Screenshot:
        """Captura screenshot do dispositivo."""
        ...

    async def tap(self, session: AndroidSession, x: int, y: int) -> None:
        """Toca em coordenadas."""
        ...

    async def swipe(self, session: AndroidSession, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        """Desliza na tela."""
        ...

    async def input_text(self, session: AndroidSession, text: str) -> None:
        """Digita texto no campo focado."""
        ...

    async def press_back(self, session: AndroidSession) -> None: ...
    async def press_home(self, session: AndroidSession) -> None: ...
    async def open_app(self, session: AndroidSession, package: str) -> None: ...

    async def install_apk(self, session: AndroidSession, apk_path: str) -> None:
        """Instala APK no dispositivo."""
        ...

    async def run_shell(self, session: AndroidSession, command: str) -> str:
        """Executa comando ADB shell."""
        ...
```

**Casos de uso no VALEN:**
- Postar no Instagram diretamente do dispositivo (bypass de APIs)
- Testar APKs gerados pelo Forge no dispositivo real
- Monitorar notificações do celular
- Automação de apps que não têm API

---

### 18.7 ComputerUseTool — Integração com o Sistema de Tools

Todos os componentes de Computer Use são expostos como uma única `ComputerUseTool` no sistema de Tools:

```python
class ComputerUseTool(ToolBase):
    name = "ComputerUseTool"
    risk_level = "high"
    sandbox_mode = "restricted"
    required_permissions = {"computer_use", "screenshot", "execute"}

    def run(self, action: str, args: dict, context: ToolContext) -> ToolResult:
        actions = {
            "screenshot":        self._screenshot,
            "ocr":               self._ocr,
            "mouse_click":       self._mouse_click,
            "mouse_move":        self._mouse_move,
            "mouse_drag":        self._mouse_drag,
            "keyboard_type":     self._keyboard_type,
            "keyboard_shortcut": self._keyboard_shortcut,
            "browser_open":      self._browser_open,
            "browser_navigate":  self._browser_navigate,
            "browser_click":     self._browser_click,
            "browser_fill":      self._browser_fill,
            "browser_extract":   self._browser_extract,
            "android_tap":       self._android_tap,
            "android_swipe":     self._android_swipe,
            "android_install":   self._android_install,
        }
        return await actions[action](**args, context=context)
```

---

## 19. WORKFLOW ENGINE

O VALEN possui um **motor de workflows visual e programático** que permite criar automações complexas, encadear ações de agentes e Tools, reagir a eventos e agendar tarefas.

---

### 19.1 Filosofia do Workflow Engine

Inspirado no melhor de **n8n** (visual/acessível), **LangGraph** (graph-based AI flows) e **Temporal** (durabilidade e retries), o Workflow Engine do VALEN combina os três:

| Característica | n8n | LangGraph | Temporal | VALEN Workflow Engine |
|---------------|-----|-----------|----------|----------------------|
| Interface visual | ✅ | ❌ | ❌ | ✅ |
| Flows de IA | ❌ | ✅ | ❌ | ✅ |
| Durabilidade / retry | ❌ | ❌ | ✅ | ✅ |
| Agentes como nós | ❌ | ✅ | ❌ | ✅ |
| Triggers variados | ✅ | ❌ | ❌ | ✅ |
| Event-driven | ✅ | ❌ | ✅ | ✅ |

---

### 19.2 Conceitos Fundamentais

```python
@dataclass
class WorkflowDefinition:
    id: str
    name: str
    description: str
    trigger: WorkflowTrigger
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]         # conexões entre nós
    variables: dict                    # variáveis globais do workflow
    error_policy: ErrorPolicy
    version: str = "1.0.0"

@dataclass
class WorkflowNode:
    id: str
    type: Literal["agent", "tool", "condition", "transform", "trigger", "output"]
    config: dict                      # configuração específica do tipo
    retry_policy: RetryPolicy | None = None
    timeout_seconds: int = 300

@dataclass
class WorkflowEdge:
    from_node: str
    to_node: str
    condition: str | None = None      # expressão Python para routing condicional

@dataclass
class WorkflowTrigger:
    type: Literal["manual", "schedule", "webhook", "event", "voice", "file_watch"]
    config: dict                      # cron expression, webhook url, event type, etc.

@dataclass
class WorkflowRun:
    run_id: str
    workflow_id: str
    status: Literal["pending", "running", "completed", "failed", "cancelled"]
    started_at: datetime
    completed_at: datetime | None
    steps: list[WorkflowStep]
    output: dict | None
    error: str | None
```

---

### 19.3 Tipos de Nós

| Tipo de Nó | O que faz | Configuração |
|-----------|----------|-------------|
| `trigger` | Ponto de entrada do workflow | tipo, condições |
| `agent` | Executa um dos 4 agentes com uma instrução | agent_id, prompt_template |
| `tool` | Executa uma Tool diretamente | tool_name, action, args |
| `condition` | Routing condicional (if/else) | expression Python |
| `transform` | Transforma dados entre nós | função de transformação |
| `loop` | Itera sobre lista de items | items_source, max_iterations |
| `parallel` | Executa múltiplos nós em paralelo | nodes_ids |
| `wait` | Aguarda evento ou tempo | condition, timeout |
| `output` | Formata e entrega o resultado final | format, destination |

---

### 19.4 Tipos de Triggers

```python
# Agendamento (cron)
WorkflowTrigger(
    type="schedule",
    config={"cron": "0 9 * * 1-5"}  # dias úteis às 9h
)

# Webhook externo
WorkflowTrigger(
    type="webhook",
    config={"path": "/webhooks/github", "secret": "..."}
)

# Evento interno do sistema
WorkflowTrigger(
    type="event",
    config={"event_type": "NoteCreated", "filter": {"tags": ["urgente"]}}
)

# Ativado por voz
WorkflowTrigger(
    type="voice",
    config={"intent": "criar_post_instagram"}
)

# Monitoramento de arquivo
WorkflowTrigger(
    type="file_watch",
    config={"path": "/uploads", "on": "created", "extension": ".csv"}
)
```

---

### 19.5 Workflows Pré-definidos na v1.0.0

O VALEN já vem com estes workflows prontos para uso:

| Workflow | Trigger | Descrição |
|---------|---------|----------|
| `daily_briefing` | schedule `0 8 * * *` | CEO gera briefing diário: clima, agenda, finanças, Instagram |
| `instagram_post` | manual / voice | CEO cria conteúdo, Forge formata, aguarda aprovação, publica |
| `weekly_finance_report` | schedule `0 18 * * 5` | Analyst gera relatório financeiro semanal |
| `neurovalen_backup` | schedule `0 3 * * *` | Nexus faz backup completo do NeuroValen para MinIO |
| `system_health_check` | schedule `*/15 * * * *` | Nexus verifica saúde do sistema a cada 15min |
| `new_file_process` | file_watch `/uploads` | Forge processa qualquer arquivo novo no diretório de uploads |
| `error_recovery` | event `AgentFailed` | CEO notifica usuário + Nexus tenta auto-reparo |

---

### 19.6 Interface Visual de Workflows

No dashboard do VALEN, existe uma **tela de Workflows** onde o usuário pode:

- Ver todos os workflows ativos com status (rodando / pausado / com erro)
- Ver o **grafo visual** de cada workflow (nós conectados por setas)
- Criar novos workflows arrastando nós no canvas
- Editar workflows existentes
- Disparar workflows manualmente com um clique
- Ver o histórico de execuções de cada workflow
- Ver logs passo a passo de cada run

---

## 20. MARKETPLACE — PLUGINS, MCP SERVERS E FERRAMENTAS EXTERNAS

O VALEN possui um **Marketplace nativo** que permite ao usuário estender as capacidades do sistema instalando plugins, MCP Servers e ferramentas externas com poucos cliques.

---

### 20.1 Filosofia do Marketplace

- **Seguro por padrão:** todo plugin roda em sandbox isolado
- **Declarativo:** cada plugin declara exatamente quais permissões precisa (como app stores)
- **Reversível:** qualquer plugin pode ser desinstalado sem deixar rastros
- **Auditável:** toda ação de plugin aparece no Audit Trail com identificação clara

---

### 20.2 Tipos de Extensões

#### 20.2.1 Plugins (Tools Externas)

São novas Tools que se integram ao sistema de Tools existente. Seguem o mesmo contrato de `ToolBase`.

```python
# Exemplo: Plugin de Google Calendar
class GoogleCalendarPlugin(ToolBase):
    name = "GoogleCalendarTool"
    version = "1.2.0"
    author = "Astraz Studio"
    required_permissions = {"network", "read", "write"}
    risk_level = "medium"

    # declara o que pode fazer
    actions = ["list_events", "create_event", "update_event", "delete_event"]

    def run(self, action: str, args: dict, context: ToolContext) -> ToolResult:
        ...
```

**Processo de instalação:**
1. Usuário encontra plugin no Marketplace ou fornece URL do repositório
2. VALEN baixa o plugin e analisa o `plugin.manifest.json`
3. CEO apresenta ao usuário: *"Meu rei, este plugin precisa de acesso à rede e leitura/escrita no calendário. Confirma a instalação?"*
4. Após confirmação: plugin é instalado no sandbox, registrado no PostgreSQL, disponível para os agentes

#### 20.2.2 MCP Servers (Model Context Protocol)

O VALEN suporta nativamente o protocolo MCP, podendo conectar a qualquer MCP Server.

```python
class MCPServerConfig:
    name: str
    type: Literal["stdio", "sse", "websocket"]
    url: str | None               # para sse e websocket
    command: str | None           # para stdio (ex: "npx @modelcontextprotocol/server-github")
    env: dict[str, str]           # variáveis de ambiente (API keys, etc.)
    capabilities: list[str]       # tools que este MCP expõe
    auto_approve: bool = False    # True = CEO usa sem pedir confirmação

# MCP Servers pré-configurados disponíveis no Marketplace
MCP_CATALOG = [
    MCPServerConfig(name="GitHub", command="npx @modelcontextprotocol/server-github", ...),
    MCPServerConfig(name="Notion", url="https://mcp.notion.com/sse", ...),
    MCPServerConfig(name="Slack", url="https://mcp.slack.com/sse", ...),
    MCPServerConfig(name="Linear", url="https://mcp.linear.app/sse", ...),
    MCPServerConfig(name="Jira", ...),
    MCPServerConfig(name="Figma", ...),
    MCPServerConfig(name="Stripe", ...),
    MCPServerConfig(name="PostgreSQL", command="npx @modelcontextprotocol/server-postgres", ...),
    MCPServerConfig(name="Google Drive", url="https://drivemcp.googleapis.com/mcp/v1", ...),
    MCPServerConfig(name="Google Calendar", ...),
    MCPServerConfig(name="WhatsApp Business", ...),
    MCPServerConfig(name="Instagram Graph API", ...),
]
```

**Como os agentes usam MCPs:**
- Os MCPs aparecem como Tools normais para os agentes
- O CEO decide qual MCP usar baseado na intenção da tarefa
- Cada chamada MCP é registrada no Audit Trail

#### 20.2.3 Workflow Templates

Workflows prontos para importar, compartilhar e customizar:

```json
{
  "template_id": "social-media-scheduler",
  "name": "Agendador de Redes Sociais",
  "description": "Cria e agenda posts para Instagram e outras redes",
  "author": "Astraz Studio",
  "version": "1.0.0",
  "required_plugins": ["InstagramTool", "ImageGeneratorTool"],
  "workflow": { ... }
}
```

---

### 20.3 Plugin Registry e Segurança

```python
class PluginRegistry:
    """Gerencia o ciclo de vida de todos os plugins instalados."""

    async def install(self, source: str, confirmed_by_user: bool) -> Plugin:
        """source pode ser: URL de repositório, ID do marketplace, path local."""
        assert confirmed_by_user, "Instalação requer confirmação explícita do usuário"
        ...

    async def uninstall(self, plugin_id: str) -> None:
        """Remove plugin e todos os seus dados."""
        ...

    async def enable(self, plugin_id: str) -> None: ...
    async def disable(self, plugin_id: str) -> None: ...
    async def update(self, plugin_id: str) -> Plugin: ...
    async def list_installed(self) -> list[Plugin]: ...
    async def list_available(self, query: str = "") -> list[PluginListing]: ...
```

**Regras de segurança do Marketplace:**
- Todo plugin roda com as permissões **mínimas** que declarou — nunca mais
- Plugins não podem acessar o NeuroValen diretamente (apenas via `MemoryTool` com ACL)
- Plugins não podem se comunicar entre si diretamente (apenas via CEO como intermediário)
- Plugins com `risk_level = "critical"` exigem confirmação a **cada** execução
- Todo plugin instalado aparece no Audit Trail com `source: "plugin:{plugin_id}"`

---

### 20.4 Interface do Marketplace no Dashboard

O dashboard possui uma aba **Marketplace** com:

- **Barra de busca** de plugins e MCPs
- **Categorias:** Produtividade, Desenvolvimento, Redes Sociais, Finanças, Infraestrutura, IA, Utilitários
- **Card de cada extensão:** nome, ícone, descrição, autor, versão, permissões necessárias, avaliação
- **Botão Instalar** → CEO pede confirmação → instalação acontece em background
- **Aba "Instalados":** lista de tudo instalado, com toggle enable/disable e botão uninstall
- **Aba "MCP Servers":** lista de MCP Servers conectados, status de conexão, tools disponíveis

---

## 21. INSTRUÇÃO FINAL PARA O CLAUDE

Você agora tem **todas as informações** necessárias para executar a refatoração do VALEN para a v1.0.0.

**Sua primeira ação obrigatória:**

Crie o arquivo `VALEN_v1.0.0_REFACTOR_PLAN.md` com a análise completa do projeto atual e o plano detalhado de mudanças conforme descrito na **Fase 0**. O plano deve cobrir **todas** as seções deste documento: arquitetura enterprise, observabilidade, bancos de dados, computer use, workflow engine e marketplace.

Depois de criar o plano, **pare** e **peça confirmação** ao usuário antes de prosseguir para a Fase 1.

Não faça nenhuma modificação real no projeto antes dessa confirmação.

---

*VALEN v1.0.0 — Prompt Mestre Ultra Detalhado v4.2*  
*Astraz Studio · Junho 2026*
