---
type: concept
tags: [futuros-tools]
created: 2026-06-09
priority: medium
---

Atue como um Engenheiro de Software Sênior especialista em Processamento Gráfico, Sistemas de Arquivos em C++20 e Arquitetura de Agentes de IA.

Preciso criar um motor utilitário de processamento de mídia em C++ chamado `astraz-asset-bundler`. O objetivo deste motor é receber o logotipo principal de um novo cliente da Astraz Studio (em formato de imagem de alta resolução como PNG ou um vetor SVG) e, diretamente na memória RAM, redimensionar, remover metadados, aplicar compressão moderna (WebP) e gerar automaticamente todo o pacote padrão de produção (Assets) exigido por desenvolvedores web e mobile, incluindo favicons em múltiplos tamanhos. Este binário será integrado como uma ferramenta (Tool) oficial no backend do meu assistente de IA, o Valen.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs, 32 GB de RAM e 200 GB de SSD. O código deve ser puramente assíncrono, focado em baixo uso de CPU através do reaproveitamento de buffers de memória contíguos em C++20.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--input <CAMINHO_DA_IMAGEM_ORIGINAL>` e `--output-dir <DIRETORIO_DE_SAIDA>`. O pipeline interno deve executar rigorosamente as seguintes etapas:

1. **Ingestão e Validação de Imagem:**
   - Carregar a imagem na memória utilizando uma biblioteca gráfica nativa para C++ de alta performance, como `Magick++` (ImageMagick) ou `Skia`.
   - Validar se o arquivo possui canal alfa (transparência) e se a resolução mínima é aceitável para geração de assets (mínimo de 512x512 pixels).

2. **Geração do Pacote Web & Favicons (Redimensionamento em Memória):**
   - A partir da imagem mestre, o motor deve gerar os seguintes arquivos otimizados usando algoritmos de reamostragem de alta qualidade (como Lanczos):
     - `favicon.ico` (arquivo multi-resolução contendo os ícones de 16x16 e 32x32 pixels).
     - `favicon-16x16.png` e `favicon-32x32.png`.
     - `apple-touch-icon.png` (exatamente 180x180 pixels, sem canal alfa se necessário para conformidade iOS).
     - `android-chrome-192x192.png` e `android-chrome-512x512.png`.
     - `logo-optimized.webp` (conversão da imagem original para o formato WebP com compressão lossy controlada em 85% de qualidade para garantir carregamento sub-milenar em landing pages).

3. **Geração do Manifesto de Configuração (`site.webmanifest`):**
   - O motor C++ deve gerar automaticamente um arquivo JSON estruturado chamado `site.webmanifest` apontando para os ícones recém-criados do Android, estruturando as chaves padrão de Progressive Web Apps (PWA).

4. **Empacotamento Assíncrono (ZIP):**
   - Compactar todos os assets gerados e o arquivo de manifesto em um único arquivo `.zip` chamado `assets_producao.zip` utilizando a biblioteca `miniz.h` ou `libarchive` vinculada nativamente ao binário, salvando-o no diretório de saída de forma assíncrona.

### 2. Formato de Saída (JSON no stdout)
Ao finalizar com sucesso, o binário deve imprimir no `stdout` um JSON de status indicando o caminho absoluto do arquivo ZIP gerado e a lista de mídias processadas para que o Valen possa fornecer o link de download direto no chat:

```json
{
  "status": "sucesso",
  "arquivo_original": "/tmp/upload_logo.png",
  "pacote_zip_gerado": "/var/www/assets/assets_producao.zip",
  "arquivos_incluidos": [
    "favicon.ico",
    "favicon-16x16.png",
    "favicon-32x32.png",
    "apple-touch-icon.png",
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "logo-optimized.webp",
    "site.webmanifest"
  ]
}

3. Integração com o Valen (Formato Tool)
Escreva o manifesto da função (Tool Definition) no formato JSON padrão para agentes de IA. A ferramenta deve se chamar astraz_asset_bundler.
Inclua uma descrição refinada instruindo o Valen a acionar esta ferramenta SEMPRE que o usuário enviar uma nova imagem de logotipo ou identidade visual e pedir para preparar os arquivos finais para a equipe de desenvolvimento de sites, aplicativos ou design da Astraz Studio.
4. Entregáveis esperados:
O código-fonte em C++20 (main.cpp) modular e focado em tratamento de erros (como falta de permissão de escrita em disco ou formatos de imagem corrompidos).
O arquivo CMakeLists.txt configurado para linkar corretamente com a biblioteca gráfica escolhida (ex: Magick++) e otimizado com a flag -O3.
O comando bash completo para instalar no Ubuntu todas as dependências de desenvolvimento necessárias (libmagick++-dev ou similar).
O esquema JSON do Tool para o Valen e um exemplo prático em Node.js ou Python demonstrando como capturar o caminho do ZIP para disponibilizá-lo ao usuário final.
Gere uma solução profissional de engenharia limpa e pronta para rodar na minha infraestrutura.