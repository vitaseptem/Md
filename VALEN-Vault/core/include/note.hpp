#pragma once

#include <string>
#include <vector>
#include <cstddef>

// Representa uma unica nota Markdown do vault.
// Struct simples e "burra": apenas dados. A logica de extracao vive
// em LinkResolver, VaultEngine e Indexer.
struct Note {
    std::string id;                       // nome do arquivo sem extensao (ex.: "arquitetura")
    std::string path;                     // caminho relativo ao vault (ex.: "notes/arquitetura.md")
    std::string type;                     // frontmatter: architecture | concept | decision | log | agent | visual
    std::vector<std::string> tags;        // frontmatter: tags
    std::string created;                  // frontmatter: created (data)
    std::string priority;                 // frontmatter: low | medium | high
    std::vector<std::string> links;       // links [[ ]] encontrados no corpo
    std::vector<std::string> backlinks;   // notas que apontam para esta (preenchido por resolve_links)
    std::size_t word_count = 0;           // contagem de palavras do corpo (sem frontmatter)
    std::string last_modified;            // timestamp ISO-8601 do arquivo no disco
    std::string content;                  // corpo da nota (carregado sob demanda na v1)

    // -------------------------------------------------------------------
    // GANCHO FUTURO (v2): aqui entrara o vetor de embedding da nota.
    //   std::vector<float> embedding;
    // Mantido fora da v1 para evitar dependencias pesadas.
    // -------------------------------------------------------------------
};
