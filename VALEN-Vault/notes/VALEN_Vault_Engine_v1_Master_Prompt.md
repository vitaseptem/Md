# VALEN Vault Engine v1 — Master Prompt Ultra Detalhado para Claude Code

**Versão:** 1.0  
**Data:** 2026-06-09  
**Objetivo:** Implementar a **VALEN Vault Engine v1** — o motor de memória persistente e estruturada do VALEN em C++ moderno.

---

## 1. CONTEXTO E VISÃO GERAL

Você está construindo o **cérebro de longo prazo** do VALEN.

O VALEN já possui (ou terá) uma camada visual avançada com orbs, canvases neurais, matrizes de pensamento, reatividade por voz e portais. Essa engine em C++ será a **camada de memória persistente** que alimenta todo o resto.

Diferente de um Obsidian comum:
- O humano escreve notas
- A IA (Claude Code, Ruflo, VALEN visual) **lê, organiza, indexa e evolui** o conhecimento de forma autônoma

Essa é a v1 do motor. Deve ser **sólida, simples, performática e extensível**.

**Princípios da v1:**
- Tudo local e soberano (sem dependência de nuvem)
- Notas em Markdown legíveis por humanos + IAs
- Engine em C++20 nativo (binário único, rápido)
- CLI clara e útil desde o primeiro dia
- Preparado para evolução (backlinks, grafo, embeddings, agentes)

---

## 2. OBJETIVO EXATO DA v1

Entregar um executável `valen` que consiga:

1. Varrer uma pasta de notas Markdown
2. Extrair metadados + links `[[nota]]`
3. Gerar um índice JSON estruturado + grafo de conhecimento
4. Permitir buscas textuais e visualização de conexões via CLI
5. Ser a base confiável para integrações futuras com Ruflo e camada visual do VALEN

**Não é para ser completo.** É para ser **correto, limpo e extensível**.

---

## 3. ESPECIFICAÇÃO TÉCNICA COMPLETA

### 3.1 Estrutura de Pastas (obrigatória)

```
VALEN-Vault/
├── core/
│   ├── include/
│   │   ├── vault_engine.hpp
│   │   ├── note.hpp
│   │   ├── link_resolver.hpp
│   │   └── indexer.hpp
│   ├── src/
│   │   ├── main.cpp
│   │   ├── vault_engine.cpp
│   │   ├── note.cpp
│   │   ├── link_resolver.cpp
│   │   └── indexer.cpp
│   └── CMakeLists.txt
├── notes/                 # ← aqui o usuário/Claude edita as notas
│   └── (arquivos .md)
├── index/
│   └── index.json         # gerado automaticamente
├── cache/                 # reservado para v2+
└── README.md
```

### 3.2 Formato das Notas (Markdown + Frontmatter)

Toda nota deve seguir este padrão:

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

**Campos obrigatórios do frontmatter na v1:**
- `type`
- `tags` (array)
- `created`
- `priority`

### 3.3 Formato do Índice (`index/index.json`)

```json
{
  "version": "1.0.0",
  "last_scan": "2026-06-09T00:10:00-03:00",
  "total_notes": 42,
  "notes": {
    "arquitetura": {
      "id": "arquitetura",
      "path": "notes/arquitetura.md",
      "type": "architecture",
      "tags": ["core", "memory"],
      "links": ["memory-system", "agents"],
      "backlinks": ["memory-system"],
      "word_count": 87,
      "last_modified": "2026-06-08T22:15:00-03:00"
    }
  },
  "graph": {
    "nodes": ["arquitetura", "memory-system"],
    "edges": [
      { "from": "arquitetura", "to": "memory-system" }
    ]
  }
}
```

### 3.4 Classes e Responsabilidades

#### `Note` (struct simples)

```cpp
struct Note {
    std::string id;                    // nome do arquivo sem extensão
    std::string path;                  // caminho completo
    std::string type;
    std::vector<std::string> tags;
    std::vector<std::string> links;    // links [[ ]] encontrados
    std::vector<std::string> backlinks;
    size_t word_count = 0;
    std::string last_modified;
    std::string content;               // opcional (carregar sob demanda na v1)
};
```

#### `LinkResolver`

Responsável por:
- Encontrar todos os `[[nome-da-nota]]` no conteúdo
- Extrair contexto próximo ao link (para uso futuro)
- Popular `backlinks` automaticamente

#### `Indexer`

Responsável por:
- Transformar o `std::unordered_map<std::string, Note>` em JSON estruturado
- Construir o grafo (nodes + edges)
- Salvar em `index/index.json`

#### `VaultEngine` (classe principal)

Métodos públicos obrigatórios na v1:

```cpp
class VaultEngine {
public:
    explicit VaultEngine(const std::string& vault_root);

    void scan();                           // varre notes/ e preenche notes_
    void resolve_links();                  // popula backlinks
    void build_index();                    // gera index.json

    std::vector<Note> search(const std::string& query) const;
    std::vector<std::string> get_backlinks(const std::string& note_id) const;
    nlohmann::json get_graph_json() const;

    void print_stats() const;
    void print_note_summary(const std::string& note_id) const;

private:
    std::string vault_root_;
    std::unordered_map<std::string, Note> notes_;
    nlohmann::json current_index_;
};
```

### 3.5 CLI da v1 (comandos mínimos)

```bash
valen scan
valen index
valen search "termo"
valen graph "note-id"
valen stats
valen create "nome-da-nova-nota"     # bônus (cria com frontmatter padrão)
```

---

## 4. REQUISITOS DE IMPLEMENTAÇÃO (Claude Code deve seguir rigorosamente)

### 4.1 Padrões de Código

- **C++20** obrigatório
- CMake para build
- Código limpo, legível e bem comentado (comentários em português)
- Nomes de variáveis e funções em inglês (padrão C++)
- Separação clara entre header (.hpp) e implementação (.cpp)
- Tratamento de erros decente (evitar crashes silenciosos)
- Sem dependências pesadas na v1 (apenas nlohmann/json header-only)

### 4.2 Dependências

- `nlohmann/json` — incluir como header-only (você pode sugerir `FetchContent` ou copiar o header)
- `std::filesystem` (C++17+)
- Regex da STL para parser de `[[links]]`

### 4.3 O que NÃO implementar na v1

- Busca semântica / embeddings
- Watcher de filesystem (rescan manual é ok)
- Criptografia de notas
- Servidor HTTP / socket
- Integração direta com Ruflo ou VALEN visual (deixar preparado)
- Persistência de cache avançada

### 4.4 Preparação para o Futuro (deixar ganchos)

- Estrutura de classes deve permitir fácil adição de:
  - `semantic_search()`
  - `watch_and_reindex()`
  - Query API (JSON) para outros componentes do VALEN
- Comentar claramente onde as extensões devem entrar

---

## 5. INSTRUÇÕES PASSO A PASSO PARA IMPLEMENTAÇÃO

Siga esta ordem exata:

1. **Criar toda a estrutura de pastas** exatamente como especificado
2. **Criar o `CMakeLists.txt`** mínimo funcional (C++20, executável `valen`)
3. **Implementar `Note`** (struct + construtor a partir de arquivo)
4. **Implementar `LinkResolver`** (função que recebe conteúdo e retorna lista de links + contexto)
5. **Implementar `Indexer`** (função que transforma map de Notes em JSON + grafo)
6. **Implementar `VaultEngine`** com os métodos `scan()`, `resolve_links()`, `build_index()`, `search()`, etc.
7. **Implementar `main.cpp`** com CLI funcional (use `argc/argv` ou uma biblioteca leve)
8. **Adicionar o comando `create`** (bônus)
9. **Escrever `README.md`** completo com:
   - Como compilar
   - Como usar cada comando
   - Exemplo de fluxo completo
   - Como adicionar novas notas
10. **Testar** com pelo menos 5-6 notas de exemplo e mostrar a saída dos comandos

---

## 6. FORMATO DE SAÍDA ESPERADO DO CLAUDE CODE

Você deve entregar:

- **Todos os arquivos de código completos** (não pedaços)
- Explicação curta de cada decisão de design importante
- Comandos exatos de build e execução
- Sugestões de próximos passos após a v1 estar funcionando

---

## 7. VISÃO DE LONGO PRAZO (para contexto)

Depois que a v1 estiver estável, o plano é:

- v1.5 → Protocolo simples de comunicação (JSON via stdin/stdout ou pipe) para Ruflo e VALEN visual consultarem o vault
- v2.0 → Camada de embeddings local + busca semântica
- v2.5 → Resumos automáticos e sugestões de novas conexões
- v3.0 → VALEN Memory System completo integrado ao layer visual (orbs puxando contexto do grafo em tempo real)

A v1 é a **fundação crítica**. Faça ela certa.

---

## 8. TOM E QUALIDADE ESPERADA

- Profissional, preciso e direto
- Código de alta qualidade (você é um engenheiro sênior de sistemas)
- Pensamento em arquitetura e extensibilidade
- Zero código desnecessário ou "placeholder" sem explicação

---

**Agora execute.**

Comece criando a estrutura de pastas e o `CMakeLists.txt`, depois vá implementando classe por classe conforme a ordem acima.

Quando terminar, entregue o projeto completo com instruções de build e uso.

Este é o motor de memória do VALEN. Faça com excelência.