#pragma once

#include <string>
#include <vector>
#include <unordered_map>

#include <nlohmann/json.hpp>

#include "note.hpp"

// VaultEngine: classe principal do motor de memoria do VALEN.
// Orquestra varredura do disco, resolucao de links, indexacao e consultas.
//
// Ciclo de vida tipico:
//   VaultEngine engine(vault_root);
//   engine.scan();          // le notes/ do disco -> notes_
//   engine.resolve_links(); // popula backlinks
//   engine.build_index();   // gera index/index.json
class VaultEngine {
public:
    explicit VaultEngine(const std::string& vault_root);

    // --- Pipeline principal -------------------------------------------
    void scan();           // varre notes/ e preenche notes_ (frontmatter, links, word_count...)
    void resolve_links();  // popula backlinks de todas as notas
    void build_index();    // gera e salva index/index.json (chama scan+resolve se vazio)

    // --- Consultas ----------------------------------------------------
    // Busca textual simples (case-insensitive) em id, tags, type e conteudo.
    std::vector<Note> search(const std::string& query) const;

    // Retorna os backlinks de uma nota (vazio se nota nao existe).
    std::vector<std::string> get_backlinks(const std::string& note_id) const;

    // Retorna apenas a secao "graph" do indice.
    nlohmann::json get_graph_json() const;

    // --- Saida para CLI -----------------------------------------------
    void print_stats() const;
    void print_note_summary(const std::string& note_id) const;
    void print_graph(const std::string& note_id) const;  // vizinhanca de um no

    // Acesso de leitura ao mapa interno (util para CLI / testes).
    const std::unordered_map<std::string, Note>& notes() const { return notes_; }

    // Cria uma nova nota com frontmatter padrao em notes/<nome>.md.
    // Retorna o caminho criado. Lanca se o arquivo ja existir.
    std::string create_note(const std::string& name) const;

private:
    std::string vault_root_;
    std::unordered_map<std::string, Note> notes_;
    nlohmann::json current_index_;

    // Helpers internos.
    std::string notes_dir() const;
    std::string index_path() const;
    // Faz o parse de um arquivo .md em uma Note (frontmatter + corpo + links).
    Note parse_note_file(const std::string& filepath) const;

    // -------------------------------------------------------------------
    // GANCHOS FUTUROS — pontos de extensao planejados:
    //   std::vector<Note> semantic_search(const std::string& query) const; // v2
    //   void watch_and_reindex();                                          // v1.5+
    //   nlohmann::json query_api(const nlohmann::json& request) const;     // v1.5
    // -------------------------------------------------------------------
};
