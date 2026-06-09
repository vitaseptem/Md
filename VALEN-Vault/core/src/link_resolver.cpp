#include "link_resolver.hpp"

#include <regex>
#include <algorithm>
#include <unordered_set>

namespace {

// Regex para links no estilo Obsidian: [[alvo]] ou [[alvo|alias]].
// Capturamos o conteudo entre os colchetes e tratamos o alias depois.
const std::regex kWikiLinkRe(R"(\[\[([^\]]+)\]\])");

// Remove espacos das pontas de uma string.
std::string trim(const std::string& s) {
    const auto begin = s.find_first_not_of(" \t\r\n");
    if (begin == std::string::npos) return "";
    const auto end = s.find_last_not_of(" \t\r\n");
    return s.substr(begin, end - begin + 1);
}

// Normaliza o alvo de um link: pega so a parte antes de '|' (alias) e
// antes de '#' (heading) e faz trim. "[[nota|Apelido]]" -> "nota".
std::string normalize_target(const std::string& raw) {
    std::string t = raw;
    if (const auto pipe = t.find('|'); pipe != std::string::npos) t = t.substr(0, pipe);
    if (const auto hash = t.find('#'); hash != std::string::npos) t = t.substr(0, hash);
    return trim(t);
}

}  // namespace

std::vector<LinkHit> LinkResolver::extract_links(const std::string& content) {
    std::vector<LinkHit> hits;

    auto begin = std::sregex_iterator(content.begin(), content.end(), kWikiLinkRe);
    auto end = std::sregex_iterator();

    for (auto it = begin; it != end; ++it) {
        const std::smatch& m = *it;
        const std::string target = normalize_target(m[1].str());
        if (target.empty()) continue;

        // Extrai ~40 chars antes e depois do link como contexto.
        const std::size_t pos = static_cast<std::size_t>(m.position(0));
        const std::size_t len = static_cast<std::size_t>(m.length(0));
        const std::size_t ctx_start = pos >= 40 ? pos - 40 : 0;
        const std::size_t ctx_end = std::min(content.size(), pos + len + 40);
        std::string ctx = content.substr(ctx_start, ctx_end - ctx_start);
        // Achata quebras de linha no contexto para caber em uma linha.
        std::replace(ctx.begin(), ctx.end(), '\n', ' ');

        hits.push_back(LinkHit{target, trim(ctx)});
    }

    return hits;
}

std::vector<std::string> LinkResolver::extract_link_targets(const std::string& content) {
    std::vector<std::string> targets;
    std::unordered_set<std::string> seen;

    for (const auto& hit : extract_links(content)) {
        if (seen.insert(hit.target).second) {
            targets.push_back(hit.target);
        }
    }
    return targets;
}

void LinkResolver::resolve_backlinks(std::unordered_map<std::string, Note>& notes) {
    // Limpa backlinks antigos (idempotente — permite re-rodar apos rescan).
    for (auto& [id, note] : notes) {
        note.backlinks.clear();
    }

    // Para cada nota A -> link B, registra A em B.backlinks (se B existe).
    for (const auto& [source_id, source_note] : notes) {
        for (const auto& target_id : source_note.links) {
            auto it = notes.find(target_id);
            if (it == notes.end()) continue;  // link aponta para nota inexistente: ignora
            it->second.backlinks.push_back(source_id);
        }
    }

    // Ordena backlinks para saida deterministica.
    for (auto& [id, note] : notes) {
        std::sort(note.backlinks.begin(), note.backlinks.end());
    }
}
