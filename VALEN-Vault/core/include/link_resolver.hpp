#pragma once

#include <string>
#include <vector>
#include <unordered_map>

#include "note.hpp"

// Resultado da extracao de um unico link [[alvo]] do corpo de uma nota.
// O "context" guarda um trecho de texto ao redor do link para uso futuro
// (ex.: mostrar previa da conexao na camada visual do VALEN).
struct LinkHit {
    std::string target;   // id da nota referenciada (ex.: "memory-system")
    std::string context;  // trecho de texto ao redor do link
};

// LinkResolver: responsavel por toda a logica de links [[ ]] do vault.
// Stateless por design — apenas funcoes utilitarias sobre conteudo/notas.
class LinkResolver {
public:
    // Extrai todos os links [[alvo]] de um corpo de texto.
    // Retorna alvo + contexto proximo. Duplicatas sao preservadas aqui;
    // a deduplicacao acontece em quem consome (VaultEngine::scan).
    static std::vector<LinkHit> extract_links(const std::string& content);

    // Versao enxuta: apenas os alvos, ja deduplicados e na ordem de aparicao.
    static std::vector<std::string> extract_link_targets(const std::string& content);

    // Popula o campo `backlinks` de cada nota a partir dos `links` ja extraidos.
    // Para cada nota A que linka para B, adiciona A em B.backlinks.
    // Links que apontam para notas inexistentes sao ignorados silenciosamente
    // (decisao v1: nao poluir o indice com nos fantasmas).
    static void resolve_backlinks(std::unordered_map<std::string, Note>& notes);
};
