# VALEN Vault Engine v1

Motor de memória persistente e estruturada do **VALEN**, escrito em **C++20**.

Varre uma pasta de notas Markdown, extrai metadados e links `[[nota]]`, gera um
índice JSON + grafo de conhecimento e oferece busca textual e visualização de
conexões via CLI.

Tudo **local e soberano** — sem nuvem. Notas legíveis por humanos e IAs. Binário
único e rápido. Pensado para evoluir (backlinks, grafo, embeddings, agentes).

---

## Estrutura

```
VALEN-Vault/
├── core/                   # engine C++
│   ├── include/            # headers (.hpp) + nlohmann/json.hpp vendorizado
│   ├── src/                # implementação (.cpp)
│   ├── CMakeLists.txt      # build principal (C++20)
│   └── Makefile            # build fallback sem CMake
├── notes/                  # ← suas notas .md ficam aqui
├── index/index.json        # gerado automaticamente
├── cache/                  # reservado para v2+
└── README.md
```

---

## Como compilar

### Opção A — CMake (recomendado)

```bash
cd core
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
# binário em: core/build/valen
```

O `nlohmann/json` já vem vendorizado em `core/include/nlohmann/json.hpp`. Se o
header estiver ausente, o CMake faz fallback automático via `FetchContent`.

### Opção B — Makefile (sem CMake)

```bash
cd core
make
# binário em: core/valen
```

### Opção C — g++ direto

```bash
cd core
g++ -std=c++20 -O2 -Iinclude src/*.cpp -o valen
```

> Requer g++ 11+ ou clang 13+ (suporte a C++20 e `std::filesystem`).

---

## Como usar

Rode os comandos a partir da raiz do vault (`VALEN-Vault/`). O `valen` detecta a
raiz automaticamente procurando a pasta `notes/`; use `--vault <caminho>` para
apontar para outro vault.

| Comando | O que faz |
|---|---|
| `valen scan` | Varre `notes/` e mostra um resumo. |
| `valen index` | Gera/atualiza `index/index.json`. |
| `valen search "termo"` | Busca textual em id, tipo, tags e conteúdo. |
| `valen graph "note-id"` | Mostra conexões (links e backlinks) de uma nota. |
| `valen stats` | Estatísticas do vault (totais, tipos, tags). |
| `valen note "note-id"` | Resumo detalhado de uma nota. |
| `valen create "nome"` | Cria nota nova com frontmatter padrão. |
| `valen help` | Ajuda. |

Exemplos (assumindo o binário em `core/valen`):

```bash
core/valen index
core/valen stats
core/valen search "memory"
core/valen graph "memory-system"
core/valen note "arquitetura"
core/valen create "Nova Ideia"
```

### Modo flat (`--flat`)

Por padrão o vault tem a estrutura `vault/notes/` + `vault/index/`. Com `--flat`,
o caminho passado em `--vault` é tratado como a **própria pasta de notas** (sem
subpasta `notes/`) e o índice é gravado em `<vault>/.valen/index.json`. Útil para
indexar diretórios externos de `.md` — por exemplo, a pasta de memória do
Claude Code, que usa o mesmo formato (frontmatter + links `[[nota]]`).

```bash
valen index  --flat --vault ~/.claude/projects/<projeto>/memory
valen stats  --flat --vault ~/.claude/projects/<projeto>/memory
valen graph "alguma-memoria" --flat --vault ~/.claude/projects/<projeto>/memory
```

---

## Formato das notas

Toda nota é Markdown com frontmatter YAML:

```markdown
---
type: architecture | concept | decision | log | agent | visual
tags: [tag1, tag2, tag3]
created: 2026-06-09
priority: low | medium | high
---

Conteúdo da nota aqui...

Referência para [[outra-nota]]
```

Campos obrigatórios na v1: `type`, `tags`, `created`, `priority`.

Links no estilo Obsidian: `[[note-id]]`. Aliases e headings são aceitos e
normalizados (`[[nota|Apelido]]` e `[[nota#secao]]` viram `nota`). O `note-id` é
o nome do arquivo sem `.md`.

---

## Formato do índice (`index/index.json`)

```json
{
  "version": "1.0.0",
  "last_scan": "2026-06-09T00:10:00-03:00",
  "total_notes": 6,
  "notes": {
    "arquitetura": {
      "id": "arquitetura",
      "path": "notes/arquitetura.md",
      "type": "architecture",
      "tags": ["core", "memory", "valen"],
      "links": ["memory-system", "agents", "decisao-cpp"],
      "backlinks": ["agents", "decisao-cpp", "memory-system", "roadmap"],
      "word_count": 54,
      "last_modified": "2026-06-09T04:09:38+00:00"
    }
  },
  "graph": {
    "nodes": ["agents", "arquitetura", "..."],
    "edges": [{ "from": "arquitetura", "to": "memory-system" }]
  }
}
```

Apenas links cujo alvo existe no vault viram arestas do grafo. Backlinks são
preenchidos automaticamente.

---

## Fluxo completo (exemplo)

```bash
# 1. Crie uma nota
core/valen create "Sistema de Plugins"

# 2. Edite notes/sistema-de-plugins.md, adicione links [[arquitetura]] etc.

# 3. Reindexe
core/valen index

# 4. Explore
core/valen stats
core/valen graph "sistema-de-plugins"
core/valen search "plugin"
```

---

## Arquitetura do código

| Componente | Responsabilidade |
|---|---|
| `Note` (struct) | Dados puros de uma nota (metadados + links + conteúdo). |
| `LinkResolver` | Extrai `[[links]]` (regex), contexto e popula backlinks. |
| `Indexer` | Converte o mapa de notas em JSON + grafo; salva em disco. |
| `VaultEngine` | Classe principal: `scan` → `resolve_links` → `build_index` + consultas. |
| `main.cpp` | CLI (parsing de `argc/argv`, despacho de comandos). |

**Decisões de design:**

- **Header-only para a única dependência** (`nlohmann/json`): mantém o binário
  soberano e o build trivial.
- **`Note` é struct burra**; a construção a partir de arquivo vive em
  `VaultEngine::parse_note_file`, que tem acesso ao contexto do vault.
- **`LinkResolver` e `Indexer` são stateless** (métodos estáticos): fáceis de
  testar e reusar.
- **Saída determinística** (listas ordenadas): diffs limpos no `index.json`.
- **Links órfãos são ignorados** no grafo, mas marcados em `valen graph`.

---

## Não incluído na v1 (por design)

Busca semântica/embeddings, watcher de filesystem, criptografia, servidor
HTTP/socket, integração direta com Ruflo/visual. Os ganchos já estão comentados
no código (`semantic_search`, `watch_and_reindex`, `query_api`).

---

## Próximos passos

- **v1.5** — Query API via stdin/stdout (JSON) para Ruflo e camada visual.
- **v2.0** — Embeddings locais + busca semântica.
- **v2.5** — Resumos automáticos e sugestões de novas conexões.
- **v3.0** — Memory System integrado ao layer visual (orbs + grafo em tempo real).
