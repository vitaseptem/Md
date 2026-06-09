#include "vault_engine.hpp"

#include "link_resolver.hpp"
#include "indexer.hpp"

#include <filesystem>
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <cctype>
#include <ctime>
#include <stdexcept>

namespace fs = std::filesystem;

namespace {

// --- Helpers de string ------------------------------------------------

std::string trim(const std::string& s) {
    const auto begin = s.find_first_not_of(" \t\r\n");
    if (begin == std::string::npos) return "";
    const auto end = s.find_last_not_of(" \t\r\n");
    return s.substr(begin, end - begin + 1);
}

std::string to_lower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return s;
}

// Faz o parse de uma lista em estilo YAML inline: [a, b, c].
// Tambem aceita "a, b, c" sem colchetes. Remove aspas das pontas.
std::vector<std::string> parse_inline_list(const std::string& raw) {
    std::string s = trim(raw);
    if (!s.empty() && s.front() == '[') s.erase(s.begin());
    if (!s.empty() && s.back() == ']') s.pop_back();

    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, ',')) {
        std::string v = trim(item);
        if (v.size() >= 2 && (v.front() == '"' || v.front() == '\'') && v.back() == v.front()) {
            v = v.substr(1, v.size() - 2);
        }
        if (!v.empty()) out.push_back(v);
    }
    return out;
}

// Conta palavras separadas por espaco em branco.
std::size_t count_words(const std::string& text) {
    std::stringstream ss(text);
    std::string w;
    std::size_t n = 0;
    while (ss >> w) ++n;
    return n;
}

// Timestamp ISO-8601 (data/hora local) a partir do tempo de modificacao do arquivo.
std::string file_mtime_iso(const fs::path& p) {
    std::error_code ec;
    const auto ftime = fs::last_write_time(p, ec);
    if (ec) return "";
    // Converte file_clock -> system_clock -> time_t de forma portavel.
    const auto sctp = std::chrono::time_point_cast<std::chrono::system_clock::duration>(
        ftime - fs::file_time_type::clock::now() + std::chrono::system_clock::now());
    const std::time_t tt = std::chrono::system_clock::to_time_t(sctp);
    std::tm local_tm{};
#if defined(_WIN32)
    localtime_s(&local_tm, &tt);
#else
    localtime_r(&tt, &local_tm);
#endif
    char buf[40];
    std::strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%S%z", &local_tm);
    std::string s(buf);
    if (s.size() >= 5) {
        const std::string off = s.substr(s.size() - 5);
        if (off[0] == '+' || off[0] == '-') {
            s = s.substr(0, s.size() - 5) + off.substr(0, 3) + ":" + off.substr(3);
        }
    }
    return s;
}

// Separa um arquivo .md em (frontmatter, corpo).
// Frontmatter delimitado por "---" na primeira linha e proximo "---".
// Se nao houver frontmatter, retorna frontmatter vazio e tudo como corpo.
void split_frontmatter(const std::string& raw, std::string& frontmatter, std::string& body) {
    frontmatter.clear();
    body = raw;

    std::stringstream ss(raw);
    std::string line;
    if (!std::getline(ss, line)) return;
    if (trim(line) != "---") return;  // sem frontmatter

    std::string fm;
    bool closed = false;
    std::size_t consumed = line.size() + 1;  // +1 do '\n'
    while (std::getline(ss, line)) {
        consumed += line.size() + 1;
        if (trim(line) == "---") { closed = true; break; }
        fm += line + "\n";
    }
    if (!closed) return;  // frontmatter mal formado: trata tudo como corpo

    frontmatter = fm;
    body = consumed <= raw.size() ? raw.substr(consumed) : "";
}

}  // namespace

// =====================================================================
// VaultEngine
// =====================================================================

VaultEngine::VaultEngine(const std::string& vault_root, bool flat)
    : vault_root_(vault_root), flat_(flat) {}

std::string VaultEngine::notes_dir() const {
    // Flat: as notas vivem na propria raiz; senao, em vault_root/notes.
    return flat_ ? vault_root_ : (fs::path(vault_root_) / "notes").string();
}

std::string VaultEngine::index_path() const {
    // Flat: indice oculto em .valen/ p/ nao poluir o diretorio de notas.
    return flat_
        ? (fs::path(vault_root_) / ".valen" / "index.json").string()
        : (fs::path(vault_root_) / "index" / "index.json").string();
}

Note VaultEngine::parse_note_file(const std::string& filepath) const {
    Note note;
    const fs::path p(filepath);

    note.id = p.stem().string();
    note.path = fs::relative(p, vault_root_).generic_string();
    note.last_modified = file_mtime_iso(p);

    // Le arquivo inteiro.
    std::ifstream in(filepath, std::ios::binary);
    std::stringstream buffer;
    buffer << in.rdbuf();
    const std::string raw = buffer.str();

    // Separa frontmatter do corpo.
    std::string frontmatter, body;
    split_frontmatter(raw, frontmatter, body);

    // Parser de frontmatter linha-a-linha (chave: valor). Suficiente p/ v1.
    std::stringstream fss(frontmatter);
    std::string line;
    while (std::getline(fss, line)) {
        const auto colon = line.find(':');
        if (colon == std::string::npos) continue;
        const std::string key = trim(line.substr(0, colon));
        const std::string value = trim(line.substr(colon + 1));

        if (key == "type")          note.type = value;
        else if (key == "tags")     note.tags = parse_inline_list(value);
        else if (key == "created")  note.created = value;
        else if (key == "priority") note.priority = value;
    }

    // Corpo: links, contagem de palavras, conteudo.
    note.links = LinkResolver::extract_link_targets(body);
    note.word_count = count_words(body);
    note.content = body;

    return note;
}

void VaultEngine::scan() {
    notes_.clear();

    const std::string dir = notes_dir();
    if (!fs::exists(dir)) {
        throw std::runtime_error("Pasta de notas nao encontrada: " + dir);
    }

    for (const auto& entry : fs::recursive_directory_iterator(dir)) {
        if (!entry.is_regular_file()) continue;
        if (entry.path().extension() != ".md") continue;

        Note note = parse_note_file(entry.path().string());
        if (note.id.empty()) continue;

        // Colisao de id (mesmo nome de arquivo em subpastas): primeiro vence, avisa.
        if (notes_.count(note.id)) {
            std::cerr << "[aviso] id duplicado ignorado: " << note.id
                      << " (" << note.path << ")\n";
            continue;
        }
        notes_.emplace(note.id, std::move(note));
    }
}

void VaultEngine::resolve_links() {
    LinkResolver::resolve_backlinks(notes_);
}

void VaultEngine::build_index() {
    if (notes_.empty()) {
        scan();
        resolve_links();
    }
    current_index_ = Indexer::build_index_json(notes_);
    Indexer::save_to_file(current_index_, index_path());
}

std::vector<Note> VaultEngine::search(const std::string& query) const {
    const std::string q = to_lower(trim(query));
    std::vector<Note> results;
    if (q.empty()) return results;

    for (const auto& [id, note] : notes_) {
        bool match = to_lower(note.id).find(q) != std::string::npos
                  || to_lower(note.type).find(q) != std::string::npos
                  || to_lower(note.content).find(q) != std::string::npos;

        if (!match) {
            for (const auto& tag : note.tags) {
                if (to_lower(tag).find(q) != std::string::npos) { match = true; break; }
            }
        }
        if (match) results.push_back(note);
    }

    // Ordena por id para saida estavel.
    std::sort(results.begin(), results.end(),
              [](const Note& a, const Note& b) { return a.id < b.id; });
    return results;
}

std::vector<std::string> VaultEngine::get_backlinks(const std::string& note_id) const {
    auto it = notes_.find(note_id);
    if (it == notes_.end()) return {};
    return it->second.backlinks;
}

nlohmann::json VaultEngine::get_graph_json() const {
    return Indexer::build_graph_json(notes_);
}

void VaultEngine::print_stats() const {
    std::size_t total_words = 0;
    std::size_t total_links = 0;
    std::unordered_map<std::string, std::size_t> by_type;
    std::unordered_map<std::string, std::size_t> by_tag;

    for (const auto& [id, note] : notes_) {
        total_words += note.word_count;
        total_links += note.links.size();
        by_type[note.type.empty() ? "(sem type)" : note.type]++;
        for (const auto& t : note.tags) by_tag[t]++;
    }

    std::cout << "VALEN Vault — Estatisticas\n";
    std::cout << "==========================\n";
    std::cout << "Notas:           " << notes_.size() << "\n";
    std::cout << "Palavras totais: " << total_words << "\n";
    std::cout << "Links totais:    " << total_links << "\n";

    std::cout << "\nPor tipo:\n";
    for (const auto& [type, n] : by_type) {
        std::cout << "  " << type << ": " << n << "\n";
    }

    std::cout << "\nTags mais usadas:\n";
    std::vector<std::pair<std::string, std::size_t>> tags(by_tag.begin(), by_tag.end());
    std::sort(tags.begin(), tags.end(),
              [](const auto& a, const auto& b) { return a.second > b.second; });
    std::size_t shown = 0;
    for (const auto& [tag, n] : tags) {
        std::cout << "  #" << tag << ": " << n << "\n";
        if (++shown >= 10) break;
    }
    if (tags.empty()) std::cout << "  (nenhuma)\n";
}

void VaultEngine::print_note_summary(const std::string& note_id) const {
    auto it = notes_.find(note_id);
    if (it == notes_.end()) {
        std::cout << "Nota nao encontrada: " << note_id << "\n";
        return;
    }
    const Note& n = it->second;

    std::cout << "# " << n.id << "\n";
    std::cout << "path:          " << n.path << "\n";
    std::cout << "type:          " << n.type << "\n";
    std::cout << "priority:      " << n.priority << "\n";
    std::cout << "created:       " << n.created << "\n";
    std::cout << "last_modified: " << n.last_modified << "\n";
    std::cout << "word_count:    " << n.word_count << "\n";

    std::cout << "tags:          ";
    for (std::size_t i = 0; i < n.tags.size(); ++i)
        std::cout << "#" << n.tags[i] << (i + 1 < n.tags.size() ? " " : "");
    std::cout << "\n";

    std::cout << "links (" << n.links.size() << "):     ";
    for (std::size_t i = 0; i < n.links.size(); ++i)
        std::cout << n.links[i] << (i + 1 < n.links.size() ? ", " : "");
    std::cout << "\n";

    std::cout << "backlinks (" << n.backlinks.size() << "): ";
    for (std::size_t i = 0; i < n.backlinks.size(); ++i)
        std::cout << n.backlinks[i] << (i + 1 < n.backlinks.size() ? ", " : "");
    std::cout << "\n";
}

void VaultEngine::print_graph(const std::string& note_id) const {
    auto it = notes_.find(note_id);
    if (it == notes_.end()) {
        std::cout << "Nota nao encontrada: " << note_id << "\n";
        return;
    }
    const Note& n = it->second;

    std::cout << "Grafo de conexoes — " << n.id << "\n";
    std::cout << "================================\n";

    std::cout << "Sai (-->):\n";
    if (n.links.empty()) std::cout << "  (nenhum)\n";
    for (const auto& l : n.links) {
        const bool exists = notes_.count(l) > 0;
        std::cout << "  " << n.id << " --> " << l
                  << (exists ? "" : "  [nota inexistente]") << "\n";
    }

    std::cout << "Entra (<--):\n";
    if (n.backlinks.empty()) std::cout << "  (nenhum)\n";
    for (const auto& b : n.backlinks) {
        std::cout << "  " << b << " --> " << n.id << "\n";
    }
}

std::string VaultEngine::create_note(const std::string& name) const {
    // Sanitiza o nome para um id/slug seguro de arquivo.
    std::string slug;
    for (char c : to_lower(trim(name))) {
        if (std::isalnum(static_cast<unsigned char>(c))) slug += c;
        else if (c == ' ' || c == '_' || c == '-') slug += '-';
    }
    while (slug.find("--") != std::string::npos)
        slug.replace(slug.find("--"), 2, "-");
    if (!slug.empty() && slug.front() == '-') slug.erase(slug.begin());
    if (!slug.empty() && slug.back() == '-') slug.pop_back();
    if (slug.empty()) throw std::runtime_error("Nome de nota invalido: " + name);

    const fs::path dir = notes_dir();
    std::error_code ec;
    fs::create_directories(dir, ec);
    const fs::path out = dir / (slug + ".md");

    if (fs::exists(out)) {
        throw std::runtime_error("Nota ja existe: " + out.string());
    }

    // Data atual YYYY-MM-DD para o frontmatter.
    const std::time_t t = std::time(nullptr);
    std::tm local_tm{};
#if defined(_WIN32)
    localtime_s(&local_tm, &t);
#else
    localtime_r(&t, &local_tm);
#endif
    char date_buf[16];
    std::strftime(date_buf, sizeof(date_buf), "%Y-%m-%d", &local_tm);

    std::ofstream f(out);
    if (!f) throw std::runtime_error("Falha ao criar nota: " + out.string());
    f << "---\n"
      << "type: concept\n"
      << "tags: []\n"
      << "created: " << date_buf << "\n"
      << "priority: medium\n"
      << "---\n\n"
      << "# " << name << "\n\n"
      << "Conteudo da nota aqui...\n\n"
      << "Referencia para [[outra-nota]]\n";

    return out.string();
}
