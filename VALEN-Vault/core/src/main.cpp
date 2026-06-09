// main.cpp — CLI da VALEN Vault Engine v1.
//
// Comandos:
//   valen scan                 Varre notes/ e mostra resumo
//   valen index                Gera index/index.json
//   valen search "termo"       Busca textual nas notas
//   valen graph "note-id"      Mostra conexoes (links + backlinks) de uma nota
//   valen stats                Estatisticas do vault
//   valen note "note-id"       Resumo detalhado de uma nota
//   valen create "nome"        Cria nova nota com frontmatter padrao
//
// O vault_root e detectado automaticamente, mas pode ser sobrescrito com
// --vault <caminho>. Por padrao usa o diretorio atual.

#include <iostream>
#include <string>
#include <vector>
#include <filesystem>

#include "vault_engine.hpp"

namespace fs = std::filesystem;

namespace {

void print_usage() {
    std::cout <<
        "VALEN Vault Engine v1\n"
        "Uso: valen <comando> [args] [--vault <caminho>]\n\n"
        "Comandos:\n"
        "  scan                 Varre notes/ e mostra resumo\n"
        "  index                Gera/atualiza index/index.json\n"
        "  search \"termo\"       Busca textual nas notas\n"
        "  graph \"note-id\"      Mostra conexoes de uma nota\n"
        "  stats                Estatisticas do vault\n"
        "  note \"note-id\"       Resumo detalhado de uma nota\n"
        "  create \"nome\"        Cria nova nota com frontmatter padrao\n"
        "  help                 Mostra esta ajuda\n\n"
        "Opcoes:\n"
        "  --vault <caminho>    Raiz do vault (padrao: diretorio atual)\n";
}

// Tenta achar a raiz do vault: usa o caminho dado, senao sobe a partir do
// diretorio atual procurando uma pasta "notes/".
std::string detect_vault_root(const std::string& override_path) {
    if (!override_path.empty()) return override_path;

    fs::path cur = fs::current_path();
    for (int depth = 0; depth < 6; ++depth) {
        if (fs::exists(cur / "notes")) return cur.string();
        if (!cur.has_parent_path() || cur.parent_path() == cur) break;
        cur = cur.parent_path();
    }
    return fs::current_path().string();  // fallback: cwd
}

}  // namespace

int main(int argc, char** argv) {
    std::vector<std::string> args(argv + 1, argv + argc);

    // Extrai --vault <path> de qualquer posicao.
    std::string vault_override;
    for (std::size_t i = 0; i < args.size(); ++i) {
        if (args[i] == "--vault" && i + 1 < args.size()) {
            vault_override = args[i + 1];
            args.erase(args.begin() + i, args.begin() + i + 2);
            break;
        }
    }

    if (args.empty() || args[0] == "help" || args[0] == "-h" || args[0] == "--help") {
        print_usage();
        return args.empty() ? 1 : 0;
    }

    const std::string command = args[0];
    const std::string arg1 = args.size() > 1 ? args[1] : "";

    try {
        const std::string vault_root = detect_vault_root(vault_override);
        VaultEngine engine(vault_root);

        if (command == "scan") {
            engine.scan();
            engine.resolve_links();
            std::cout << "Scan completo: " << engine.notes().size()
                      << " nota(s) em " << vault_root << "/notes\n";
            engine.print_stats();

        } else if (command == "index") {
            engine.build_index();
            std::cout << "Indice gerado: " << vault_root << "/index/index.json\n";
            std::cout << "Notas indexadas: " << engine.notes().size() << "\n";

        } else if (command == "search") {
            if (arg1.empty()) { std::cerr << "Erro: forneca um termo de busca.\n"; return 1; }
            engine.scan();
            engine.resolve_links();
            const auto results = engine.search(arg1);
            std::cout << "Resultados para \"" << arg1 << "\": " << results.size() << "\n";
            for (const auto& n : results) {
                std::cout << "  - " << n.id << "  [" << n.type << "]  "
                          << n.word_count << " palavras\n";
            }

        } else if (command == "graph") {
            if (arg1.empty()) { std::cerr << "Erro: forneca um note-id.\n"; return 1; }
            engine.scan();
            engine.resolve_links();
            engine.print_graph(arg1);

        } else if (command == "stats") {
            engine.scan();
            engine.resolve_links();
            engine.print_stats();

        } else if (command == "note") {
            if (arg1.empty()) { std::cerr << "Erro: forneca um note-id.\n"; return 1; }
            engine.scan();
            engine.resolve_links();
            engine.print_note_summary(arg1);

        } else if (command == "create") {
            if (arg1.empty()) { std::cerr << "Erro: forneca um nome para a nota.\n"; return 1; }
            const std::string path = engine.create_note(arg1);
            std::cout << "Nota criada: " << path << "\n";

        } else {
            std::cerr << "Comando desconhecido: " << command << "\n\n";
            print_usage();
            return 1;
        }

    } catch (const std::exception& e) {
        std::cerr << "Erro: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
