---
type: concept
tags: [futuros-tools]
created: 2026-06-09
priority: medium
---

Atue como um Engenheiro de Software Sênior especialista em C++20, Sistemas Linux de Alta Performance e Arquitetura de Agentes de IA. 

Preciso criar um motor utilitário em C++ chamado `astraz-media-ingestor`. O objetivo deste motor é receber uma URL de vídeo (Instagram, TikTok ou YouTube), extrair seu conteúdo de forma assíncrona, transcrever o áudio localmente, capturar frames chave e empacotar tudo em um arquivo .ZIP estruturado com prompts em Markdown (.md). Este binário será integrado como uma ferramenta (Tool) oficial no backend do meu assistente de IA, o Valen.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs, 32 GB de RAM e 200 GB de SSD. O fluxo deve ser extremamente performático, sem memory leaks e otimizado para concorrência usando C++ moderno.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--url <LINK>` e `--output <DIRETORIO>`. O pipeline interno deve seguir estritamente estas etapas:
1. **Download:** Invocar o `yt-dlp` via subprocesso seguro de forma não-bloqueante para baixar o vídeo no formato MP4 na maior qualidade disponível (limitar a 1080p).
2. **Processamento de Mídia (FFmpeg):** 
   - Extrair o áudio e convertê-lo para WAV (16kHz, mono, formato exigido pelo Whisper).
   - Extrair frames do vídeo como imagens PNG. Para evitar poluição, implemente uma lógica que extraia exatamente 1 frame a cada 4 segundos de vídeo, salvando-os em uma subpasta `/frames`.
3. **Transcrição Local (whisper.cpp):** Integrar a biblioteca `whisper.cpp` (ou invocar seu binário otimizado) usando o modelo quantizado `ggml-base.bin` ou `ggml-small.bin`. O motor deve passar o arquivo WAV por ele, aproveitando as 4 vCPUs em paralelo (`-t 4`), e gerar o texto da transcrição.
4. **Geração de Artefatos Markdown:** O motor deve criar dois arquivos dentro da pasta do projeto:
   - `transcricao.md`: Contendo o texto bruto gerado pelo Whisper.
   - `analise_e_ideia.md`: Um arquivo mestre contendo um template de prompt altamente estilizado e agressivo para negócios, instruindo a IA que ler este arquivo a atuar como Copywriter/Estrategista da Astraz Studio, analisar o texto injetado e as imagens da pasta `/frames` para criar novos insights de conteúdo.
5. **Empacotamento (ZIP):** Compactar a pasta inteira (contendo `/frames`, `transcricao.md` e `analise_e_ideia.md`) em um arquivo `.zip` final usando uma biblioteca leve como `miniz.h` ou `libarchive`.

### 2. Estrutura do Arquivo de Prompt Gerado (`analise_e_ideia.md`)
O arquivo mestre gerado pelo C++ deve conter rigorosamente a seguinte estrutura em Markdown:
"# 🚀 Solicitação de Insights de Negócio - Astraz Studio
Atue como um Diretor de Criação, Copywriter e Estrategista de Crescimento da Astraz Studio. 
Analise as imagens contidas na pasta `/frames` e a transcrição abaixo para criar um conceito derivado de alto padrão.
## 📝 Transcrição do Vídeo Original:
[INJETAR_AQUI_A_TRANSCRICAO_DO_WHISPER]
## 🎯 Direcional de Execução:
1. Resuma a grande ideia central e o gatilho psicológico (hook) do vídeo.
2. Adapte essa ideia para o ecossistema da Astraz Studio ou nossos clientes SaaS/Agência.
3. Crie um roteiro de vídeo proprietário baseado nesse insight, adaptado para nossa estética premium e futurista (Dark Mode, Neon, minimalista)."

### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto da função (Tool Definition) no formato JSON padrão aceito por APIs de IA (como OpenAI/Anthropic ferramentas) para que o Valen saiba como chamar esse binário. A ferramenta deve se chamar `astraz_media_ingestor`. Inclua uma descrição detalhada explicando à IA que ela deve usar essa ferramenta SEMPRE que o usuário enviar um link de vídeo de redes sociais para obter ideias.

### 4. Entregáveis esperados:
1. O código-fonte em C++20 (`main.cpp`) estruturado de forma limpa, modular e assíncrona usando boas práticas.
2. O arquivo `CMakeLists.txt` configurado para compilar o projeto na VPS, linkando as dependências necessárias.
3. O comando bash completo para instalar as dependências no Ubuntu (`yt-dlp`, `ffmpeg`, e clonar/compilar o `whisper.cpp`).
4. O esquema JSON do Tool para o Valen e um exemplo de como o código de backend (ex: Node.js/Python) que roda o Valen deve executar o binário C++ usando `exec` ou `spawn` de forma segura, capturando o retorno do caminho do arquivo ZIP.

Gere uma solução profissional e pronta para implementação na minha infraestrutura.
