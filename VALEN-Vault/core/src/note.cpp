// note.cpp
//
// A struct Note e puramente de dados (ver note.hpp), entao nao ha
// implementacao de metodos aqui. Este arquivo existe para:
//   1. Manter o paralelo header/.cpp exigido pela especificacao.
//   2. Reservar espaco para metodos utilitarios futuros da Note
//      (ex.: serializacao isolada, validacao de frontmatter).
//
// Toda a logica de construcao de uma Note a partir de arquivo vive em
// VaultEngine::parse_note_file (vault_engine.cpp), por ter acesso ao
// contexto do vault (caminhos relativos, timestamps, etc.).

#include "note.hpp"
