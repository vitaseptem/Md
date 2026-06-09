#pragma once

#include <string>
#include <unordered_map>

#include <nlohmann/json.hpp>

#include "note.hpp"

// Indexer: transforma o mapa de Notes em JSON estruturado + grafo.
// Stateless — recebe os dados e devolve/salva JSON. Nao guarda estado proprio.
class Indexer {
public:
    // Versao do formato do indice. Bump quando o schema mudar.
    static constexpr const char* kIndexVersion = "1.0.0";

    // Constroi o objeto JSON completo do indice a partir das notas.
    // Inclui metadados (version, last_scan, total_notes), o mapa de notas
    // e o grafo (nodes + edges).
    static nlohmann::json build_index_json(
        const std::unordered_map<std::string, Note>& notes);

    // Constroi apenas a secao "graph" (nodes + edges). Reaproveitado por
    // VaultEngine::get_graph_json().
    static nlohmann::json build_graph_json(
        const std::unordered_map<std::string, Note>& notes);

    // Serializa o JSON e grava em disco (cria pastas pai se necessario).
    // Lanca std::runtime_error em falha de I/O.
    static void save_to_file(const nlohmann::json& index, const std::string& path);

    // -------------------------------------------------------------------
    // GANCHO FUTURO (v1.5): expor build_index_json como Query API via
    // stdin/stdout para Ruflo e camada visual consultarem o vault.
    // -------------------------------------------------------------------
};
