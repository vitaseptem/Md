---
type: concept
tags: [futuros-tools]
created: 2026-06-09
priority: medium
---

Atue como um Engenheiro de Sistemas Sênior especialista em C++20, Arquitetura de Software e Otimização de Contexto para Modelos de Linguagem (LLMs).

Preciso criar um motor utilitário em C++ chamado `astraz-code-packer`. O objetivo principal deste motor é ler recursivamente um diretório de código-fonte local na minha VPS, ignorar automaticamente pastas e ficheiros desnecessários (seguindo regras estilo `.gitignore`), construir uma representação visual em árvore da estrutura do projeto e concatenar o conteúdo de todos os ficheiros de código válidos em um único arquivo Markdown (.md) perfeitamente estruturado. Este binário será integrado como uma ferramenta (Tool) oficial no backend do meu assistente de IA, o Valen, permitindo-me dar contexto imediato de repositórios inteiros ao assistente.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs, 32 GB de RAM e 200 GB de SSD. O código deve fazer uso extensivo da biblioteca padrão `<filesystem>` do C++20, garantindo processamento em milissegundos e consumo de memória RAM negligenciável através de streams eficientes.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--input-dir <CAMINHO_DO_PROJETO>` e `--output-file <CAMINHO_DE_SAIDA_MD>`. O pipeline interno deve executar rigorosamente as seguintes etapas:

1. **Varredura Recursiva e Filtragem Inteligente:**
   - Utilizar `std::filesystem::recursive_directory_iterator` para navegar por todas as subpastas.
   - **Regra de Exclusão Crítica (Blacklist):** O motor deve ignorar obrigatoriamente ficheiros e diretórios contendo os seguintes padrões: `node_modules`, `.git`, `.turbo`, `dist`, `build`, `.next`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, imagens (.png, .jpg, .webp), fontes, e quaisquer binários compilados.
   - O motor também deve ler um ficheiro `.gitignore` local (se presente na raiz) e adicionar as suas regras dinamicamente ao filtro de exclusão.

2. **Geração da Árvore de Diretórios (Visual Tree):**
   - Antes de listar os códigos, o motor deve gerar uma representação textual em árvore (estilo o comando Unix `tree`) mapeando apenas os ficheiros e pastas válidos que passaram pelo filtro, armazenando este output em memória.

3. **Concatenação e Formatação de Código (Stream de Alta Velocidade):**
   - Abrir o arquivo Markdown de saída e escrever um cabeçalho inicial contendo a árvore estrutural gerada no passo anterior dentro de um bloco de código genérico.
   - Iterar sobre cada ficheiro de texto válido, injetar o caminho relativo do ficheiro como um título H2 (ex: `## Ficheiro: src/components/Button.tsx`) e abrir um bloco de código Markdown correspondente à extensão do ficheiro (ex: ````tsx ... ````).
   - Ler o conteúdo do ficheiro linha por linha utilizando streams de buffer otimizados (`std::ifstream`) e despejar diretamente no arquivo mestre.

### 2. Estrutura do Arquivo Gerado (.md)
O arquivo gerado pelo motor C++ deve seguir estritamente o seguinte padrão textual para que o Valen o interprete com máxima precisão:

```markdown
# 📂 Contexto do Repositório - Astraz Studio

Este documento contém a estrutura e todo o código-fonte relevante do projeto para análise e refatoração.

## 🌳 Árvore Estrutural do Projeto
```text
.
├── src/
│   ├── components/
│   │   └── Button.tsx
│   ├── database/
│   │   └── supabase.ts
│   └── main.ts
└── CMakeLists.txt

cmake_minimum_required(VERSION 3.20)
project(AstrazEngine CXX)
...


import { createClient } from '@supabase/supabase-js'
export const supabase = createClient(...)

### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto da função (Tool Definition) no formato JSON padrão para agentes de IA. A ferramenta deve se chamar `astraz_code_packer`. 
Inclua uma descrição detalhada explicando ao Valen que ele deve acionar esta ferramenta SEMPRE que o usuário pedir para analisar um projeto local na VPS, solicitar a refatoração de múltiplos ficheiros interligados, ou quando precisar debugar um erro complexo de arquitetura que exige o entendimento do fluxo completo de pastas do sistema.

### 4. Entregáveis esperados:
1. O código-fonte em C++20 (`main.cpp`) estruturado de forma limpa, modular e ultraotimizada para lidar com projetos de milhares de ficheiros sem estourar a memória.
2. O arquivo `CMakeLists.txt` com as flags de otimização (`-O3`, `-std=c++20`).
3. O comando bash para compilar o binário diretamente no ambiente Linux Ubuntu da VPS.
4. O esquema JSON do Tool e um exemplo de integração com o backend do assistente de IA, demonstrando como capturar o caminho do Markdown consolidado e anexá-lo como contexto/prompt do sistema para a LLM.

Gere uma solução profissional de engenharia robusta e limpa.