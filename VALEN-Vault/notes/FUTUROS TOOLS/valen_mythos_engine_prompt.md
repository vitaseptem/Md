# Prompt de Engenharia Ultra Detalhado para Implementação do VALEN Mythos Engine

**Versão:** 1.0 - Nível Militar + Hacker Ético  
**Objetivo:** Criar um motor nativo de alta performance que funcione como **Tool nativa de primeira classe do Valen**, com capacidades de inteligência tática, auditoria defensiva e raciocínio avançado, tudo dentro de limites éticos rígidos e robustez de nível militar.

---

## Instruções Gerais para o Engenheiro de Software Principal

Você deve atuar como um **Engenheiro de Software Principal** especialista em:

- Sistemas distribuídos de alta performance em Rust (C++20 ou Go também aceitáveis, mas Rust é fortemente preferido por safety e performance).
- Web scraping assíncrono de alta velocidade com evasão avançada de anti-bot.
- Cybersecurity defensiva e ethical hacking (auditoria, detecção de anomalias, surface mapping, sem qualquer capacidade ofensiva).
- Integração profunda com sistemas de IA visual e neural (orbs, matrizes de pensamento, canvases, portais reativos, visualização de dados em tempo real).
- Arquitetura de ferramentas nativas para assistentes de IA (Tool calling / manifesto JSON, comunicação via WebSocket ou IPC, outputs estruturados para consumo por núcleo visual).

O motor resultante deve ser chamado de **valen_mythos_engine** (ou nome similar claro) e deve ser compilado como binário único otimizado para rodar em VPS Ubuntu com 32 GB RAM.

Todo o código deve priorizar:
- Segurança de memória (Rust é ideal).
- Robustez militar (auditabilidade completa, logging imutável, sandboxing, circuit breakers, kill-switches).
- Conformidade ética rígida (whitelisting obrigatório, modos de simulação, recusa automática de ações fora de escopo).
- Integração nativa com o núcleo visual e neural do Valen (fornecendo `visual_payload` otimizado para orbs, pulsos, cores dinâmicas, matrizes e canvases).
- Performance extrema com concorrência assíncrona real.
- Soberania total (execução 100% local/offline quando possível, sem dependências de APIs externas não autorizadas).

---

## 1. Requisitos Técnicos do Motor Core

### 1.1 Pipeline de Requisições Assíncronas de Alta Performance
- Implementar motor HTTP não-bloqueante usando Tokio (ou equivalente em outra linguagem).
- Gerenciar pools de conexões reutilizáveis.
- Executar pipelines de scraping e auditoria concorrentes com controle estrito de:
  - Timeouts por domínio e por requisição.
  - Rate limiting inteligente e adaptativo por domínio.
  - Backoff exponencial com jitter.
  - Circuit breaker por alvo.
- Suporte completo a IPv4/IPv6.

### 1.2 Camada de Camuflagem e Evasão Avançada (Nível Mythos)
- Rotação dinâmica e inteligente de User-Agents realistas (lista grande + rotação contextual).
- Ordenação aleatória + variação de headers HTTP (Accept, Accept-Language, Referer, etc.).
- Emulação de comportamento humano (delays variáveis, padrões de navegação, mouse movements simulados em headers quando aplicável).
- Suporte nativo e robusto a proxies SOCKS5 e HTTP (com autenticação, rotação e fallback).
- Detecção e adaptação automática a WAFs, rate limits e bloqueios (usando feedback de respostas e headers).
- Estratégias de evasão adaptativas baseadas em histórico de sucesso/falha por domínio (armazenado localmente).

### 1.3 Mecanismo de Parsing, Diff e Análise Avançada
- Parsing eficiente da árvore DOM em memória (html5ever ou equivalente de alta performance).
- Extração cirúrgica de:
  - Tabelas de preços e serviços.
  - Portfólios e alterações de produtos.
  - Dados de contato públicos (e-mails, telefones, formulários).
  - Metadados de segurança (headers HTTP, TLS configuration, WAF detection, cookies flags).
- Mecanismo de **Diff Estatístico e Semântico** entre execuções anteriores:
  - Armazenamento de estados anteriores (hash + snapshot estruturado).
  - Detecção de alterações em preços, novos serviços, remoção de itens, mudanças em contatos.
  - Geração de relatório de diff com relevância e impacto.
- Análise de superfície de ataque ética (quando em modo audit): headers de segurança, flags de cookies, configuração TLS, exposição de informações.

### 1.4 Módulo de Enforcement Ético e Militar (Obrigatório e Inviolável)
- **Whitelist obrigatória**: Todo alvo deve estar explicitamente autorizado via arquivo de escopo JSON assinado ou com hash verificado.
- Modos de operação ética:
  - `strict`: Apenas ações passivas e dentro de whitelist.
  - `balanced`: Permite algumas técnicas de evasão controladas.
  - `simulation`: Executa tudo em modo dry-run, sem requisições reais (ideal para testes).
- Logging imutável com cadeia de hash (hash chain) de **toda** requisição, decisão e resultado.
- Recusa programada e clara de qualquer operação fora do escopo ético ou potencialmente ofensiva.
- Kill-switch global e por sessão.
- Sandboxing de qualquer execução de comandos externos (landlock/seccomp no Linux).

### 1.5 Integração Profunda com o Núcleo Visual e Neural do Valen
- O motor deve produzir, além do JSON clássico, um **`visual_payload`** estruturado otimizado para consumo direto pelo Valen:
  - Cores dinâmicas por nível de threat/prioridade.
  - Intensidade de pulso para orbs.
  - Estrutura de nós e conexões para matrizes de pensamento.
  - Dados de diff formatados para canvases neurais.
  - Alertas visuais (threat indicators, security_score, ethical_compliance).
- Comunicação bidirecional recomendada via **WebSocket local** ou **Unix Domain Socket** para baixa latência.
- Alternativa: invocação via subprocess com JSON via stdin/stdout.
- O Valen deve conseguir invocar o motor de forma autônoma ou semi-autônoma e receber os dados para atualizar suas orbs de inteligência de mercado, threat matrices e canvases de diff em tempo real.

### 1.6 Persistência e Estado
- Armazenamento local leve e seguro de histórico de execuções (SQLite ou similar com criptografia em repouso quando possível).
- Suporte a backups incrementais e restore de estado.
- Metadados de execução (timestamp, duração, ethical_level usado, proxy utilizado, etc.).

---

## 2. Interface de Linha de Comando (CLI) e Invocação como Tool do Valen

O binário deve aceitar parâmetros via linha de comando de forma clara e validada:

```bash
valen-mythos-engine \
  --mode "intel" | "audit" | "defend" | "mythos" \
  --target "https://exemplo.com" \
  --scope-file "/caminho/para/whitelist.json" \
  --depth 2 \
  --ethical-level "strict" \
  --output-format "both" \
  --proxy-list "/caminho/proxies.txt" \
  --daemon
```

**Parâmetros obrigatórios e validados:**
- `--mode`: Define o tipo de operação.
- `--target`: URL ou identificador do alvo (sempre validado contra escopo).
- `--scope-file`: Arquivo JSON com whitelist, regras éticas e configurações de segurança (obrigatório na maioria dos modos).

**Modos de operação detalhados:**
- `intel`: Inteligência comercial e de mercado (preços, serviços, portfólio, contatos).
- `audit`: Auditoria ética defensiva (headers de segurança, TLS, WAF, surface mapping, dependencies quando aplicável).
- `defend`: Monitoramento passivo e detecção de anomalias na infra do Valen/ecossistema.
- `mythos`: Modo agentic avançado com raciocínio mais profundo para planejamento de estratégias de evasão e análise (sempre dentro de limites éticos rígidos).

**Saída padrão (stdout):**
Todo execução de sucesso deve retornar **estritamente JSON limpo** no stdout, estruturado da seguinte forma (exemplo para modo intel):

```json
{
  "status": "sucesso",
  "modo_executado": "intel",
  "alvo_analisado": "https://concorrenteexemplo.com",
  "ethical_compliance": true,
  "security_score": 92,
  "alteracoes_detectadas": true,
  "dados_extraidos": {
    "servicos_novos": ["Gestão de Tráfego Avançada", "Automação de Processos"],
    "alteracoes_preco": [...],
    "links_contato": ["contato@exemplo.com", "+5598999999999"]
  },
  "diff_estatistico": {
    "alteracoes_totais": 7,
    "relevancia_media": 0.78
  },
  "threat_indicators": [],
  "visual_payload": {
    "orb_color": "#00f0ff",
    "pulse_intensity": 0.85,
    "matrix_nodes": [...],
    "canvas_diff_data": "...",
    "alert_level": "medium"
  },
  "tempo_execucao_ms": 1240.67,
  "audit_log_id": "uuid-v4-aqui"
}
```

O `visual_payload` deve ser projetado especificamente para o Valen conseguir renderizar de forma nativa em orbs, pulsos, matrizes e canvases sem processamento adicional pesado.

---

## 3. Esquema de Tool / Manifesto para o Valen (Tool Schema)

Gere um manifesto JSON completo e bem documentado que o LLM do Valen possa usar para decidir quando e como invocar este motor. O manifesto deve incluir:

- Nome da tool
- Descrição clara e estratégica
- Parâmetros com tipos, enums, descrições e exemplos
- Restrições éticas explícitas
- Notas de integração com o núcleo visual do Valen (como consumir o visual_payload)
- Exemplos de chamadas bem-sucedidas e de erro

O manifesto deve ser auto-contido e pronto para ser registrado no sistema de tools do Valen.

---

## 4. Arquitetura de Código e Organização do Projeto (Rust - Preferencial)

Estrutura de diretórios recomendada:

```
valen-mythos-engine/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── cli.rs
│   ├── core/
│   │   ├── engine.rs
│   │   ├── async_pipeline.rs
│   │   ├── camouflage.rs
│   │   ├── parser.rs
│   │   ├── diff_engine.rs
│   │   └── visual_adapter.rs
│   ├── ethical/
│   │   ├── whitelist.rs
│   │   ├── enforcer.rs
│   │   └── audit_logger.rs
│   ├── network/
│   │   ├── client.rs
│   │   ├── proxy_manager.rs
│   │   └── rate_limiter.rs
│   ├── integration/
│   │   ├── websocket.rs
│   │   └── valen_payload.rs
│   └── utils/
├── config/
│   └── default_scope.json
├── tests/
└── README.md
```

**Requisitos de código:**
- Todo módulo deve ter documentação clara.
- Tratamento de erros robusto com thiserror ou similar.
- Configuração via struct + serde.
- Testes unitários e de integração para partes críticas (especialmente ethical_enforcer e diff_engine).
- Logs estruturados (tracing ou log crate).

---

## 5. Build Corporativo e Otimizações de Release (Cargo.toml)

O `Cargo.toml` deve conter otimizações agressivas para Release:

```toml
[profile.release]
opt-level = 3
lto = "fat"
codegen-units = 1
strip = true
panic = "abort"
overflow-checks = false
debug = false
```

Incluir dependências recomendadas com versões fixas ou ranges controlados (tokio, reqwest com rustls, scraper/html5ever, serde, clap, sqlx ou rusqlite, ring ou aws-lc-rs para crypto, etc.).

Instruções completas de build:
```bash
cargo build --release
```

E como rodar o binário otimizado.

---

## 6. Regras Éticas e de Segurança que Devem ser Hardcoded / Fortemente Enforçadas

- Whitelist é soberana: sem entrada na whitelist → recusa imediata com mensagem clara.
- Nunca realizar ações que possam ser interpretadas como ofensivas ou de ataque ativo sem modo `simulation` explícito + confirmação.
- Todo log de ação deve incluir hash anterior para formar cadeia imutável.
- O motor deve expor endpoint ou flag para verificar integridade do binário e do escopo atual.
- Suporte a modo "read-only" / "passive-only".
- Documentação clara de todas as capacidades éticas no README e no código.

---

## 7. Integração com o Valen (Requisito Principal)

O motor deve ser projetado desde o início para ser uma **Tool nativa do Valen**:
- Facilidade de registro via manifesto JSON.
- Invocação simples via CLI ou socket.
- Outputs que o Valen consiga consumir diretamente para atualizar seu estado neural e visual sem transformação complexa.
- Capacidade de o Valen pedir "faça uma análise intel no concorrente X com nível ético strict e atualize minha orb de mercado".
- O visual_payload deve mapear naturalmente para os componentes visuais do Valen (orbs com cor/intensidade, matrizes com nós e pulsos, canvases com dados de diff, etc.).

---

## 8. Entregáveis Finais Esperados

Ao final da implementação, forneça:

1. Código fonte completo e bem organizado em Rust (ou linguagem escolhida).
2. `Cargo.toml` com todas as dependências e perfil de release otimizado.
3. README.md completo com:
   - Instruções de build e execução.
   - Exemplos de uso da CLI.
   - Exemplo completo do Tool Schema JSON.
   - Como integrar com o Valen.
4. Exemplo de arquivo `scope.json` / whitelist.
5. Testes que demonstrem o funcionamento ético e do diff.
6. Instruções de deploy na VPS Ubuntu (systemd service opcional para modo daemon).

---

## Instruções Finais de Execução deste Prompt

- Comece definindo a arquitetura completa antes de escrever código.
- Implemente primeiro o módulo de enforcement ético e o whitelist — ele é a fundação inviolável.
- Depois construa o pipeline assíncrono + camuflagem.
- Em seguida o parser + diff_engine.
- Depois o visual_adapter e a integração com o Valen.
- Por último a CLI e o daemon mode.
- Teste exaustivamente os limites éticos e os casos de recusa.
- Otimize performance apenas após ter funcionalidade e segurança corretas.
- O resultado final deve ser um binário único, rápido, seguro e pronto para ser registrado como Tool nativa do Valen.

Este prompt deve ser seguido com rigor militar em detalhes técnicos, clareza arquitetural e respeito absoluto às regras éticas definidas.

Gere código limpo, performático, bem documentado e pronto para produção em ambiente soberano.