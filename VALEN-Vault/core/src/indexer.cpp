#include "indexer.hpp"

#include <fstream>
#include <filesystem>
#include <ctime>
#include <algorithm>
#include <vector>
#include <stdexcept>

namespace fs = std::filesystem;

namespace {

// Retorna o timestamp atual em ISO-8601 com offset local (ex.: 2026-06-09T00:10:00-03:00).
std::string now_iso8601() {
    const std::time_t t = std::time(nullptr);
    std::tm local_tm{};
#if defined(_WIN32)
    localtime_s(&local_tm, &t);
#else
    localtime_r(&t, &local_tm);
#endif
    char buf[40];
    std::strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%S%z", &local_tm);
    // strftime gera offset "-0300"; convertemos para "-03:00".
    std::string s(buf);
    if (s.size() >= 5) {
        const std::string off = s.substr(s.size() - 5);  // ex.: "-0300"
        if ((off[0] == '+' || off[0] == '-')) {
            s = s.substr(0, s.size() - 5) + off.substr(0, 3) + ":" + off.substr(3);
        }
    }
    return s;
}

}  // namespace

nlohmann::json Indexer::build_graph_json(
    const std::unordered_map<std::string, Note>& notes) {
    nlohmann::json graph;
    graph["nodes"] = nlohmann::json::array();
    graph["edges"] = nlohmann::json::array();

    // Nos: ordenados para saida deterministica.
    std::vector<std::string> ids;
    ids.reserve(notes.size());
    for (const auto& [id, note] : notes) ids.push_back(id);
    std::sort(ids.begin(), ids.end());

    for (const auto& id : ids) graph["nodes"].push_back(id);

    // Arestas: uma por link cujo alvo existe no vault.
    for (const auto& id : ids) {
        const Note& note = notes.at(id);
        for (const auto& target : note.links) {
            if (notes.count(target)) {
                graph["edges"].push_back({{"from", id}, {"to", target}});
            }
        }
    }

    return graph;
}

nlohmann::json Indexer::build_index_json(
    const std::unordered_map<std::string, Note>& notes) {
    nlohmann::json index;
    index["version"] = kIndexVersion;
    index["last_scan"] = now_iso8601();
    index["total_notes"] = notes.size();

    // Mapa de notas (objeto id -> metadados).
    nlohmann::json notes_obj = nlohmann::json::object();
    for (const auto& [id, note] : notes) {
        notes_obj[id] = {
            {"id", note.id},
            {"path", note.path},
            {"type", note.type},
            {"tags", note.tags},
            {"created", note.created},
            {"priority", note.priority},
            {"links", note.links},
            {"backlinks", note.backlinks},
            {"word_count", note.word_count},
            {"last_modified", note.last_modified},
        };
    }
    index["notes"] = std::move(notes_obj);

    // Grafo.
    index["graph"] = build_graph_json(notes);

    return index;
}

void Indexer::save_to_file(const nlohmann::json& index, const std::string& path) {
    // Garante que a pasta pai exista.
    const fs::path p(path);
    if (p.has_parent_path()) {
        std::error_code ec;
        fs::create_directories(p.parent_path(), ec);
        if (ec) {
            throw std::runtime_error("Falha ao criar pasta do indice: " + ec.message());
        }
    }

    std::ofstream out(path, std::ios::trunc);
    if (!out) {
        throw std::runtime_error("Falha ao abrir arquivo de indice para escrita: " + path);
    }
    out << index.dump(2) << '\n';  // pretty-print com 2 espacos
    if (!out) {
        throw std::runtime_error("Falha ao escrever o indice em: " + path);
    }
}
