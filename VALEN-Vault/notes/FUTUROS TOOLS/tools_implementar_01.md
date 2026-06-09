Aqui tens os prompts de nível de engenharia para cada um dos novos motores da **Astraz Studio**. Eles foram estruturados com rigor técnico em C++20, foco em concorrência, otimização de memória e prontos para serem executados diretamente no **Claude Code** ou no terminal da tua VPS de 32 GB de RAM.
### 🎨 Prompt 1: astraz_bento_grid_generator (Gerador de Interfaces Geométricas)
```text
Atue como um Engenheiro de Software Sênior especialista em Algoritmos Geométricos, Engenharia de UI/UX Front-end e Otimização em C++20.

Preciso criar um motor geométrico em C++ chamado `astraz-bento-grid-generator`. O objetivo principal deste motor é receber um payload JSON contendo uma lista de componentes de interface (cards, gráficos, imagens, blocos de texto) com as suas respetivas proporções ou pesos de importância, e calcular a disposição espacial perfeita seguindo o padrão visual Bento Grid (estética minimalista e futurista da Astraz Studio). O motor deve resolver o problema de empacotamento bidimensional (2D Bin Packing) na memória RAM e cuspir o código HTML5 e CSS Grid puro, responsivo e ultra-otimizado.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs e 32 GB de RAM. O código deve rodar em milissegundos sem alocações desnecessárias de heap.

### 1. Requisitos do Fluxo do Motor (C++)
O binário deve aceitar o argumento `--input-json "<DADOS_DOS_CARDS>"` e retornar o HTML/CSS diretamente no `stdout`.
1. **Algoritmo de Posicionamento (Bin Packing):** Implementar ou adaptar um algoritmo heurístico (como Maximal Rectangles ou Shelf Packing) para organizar retângulos de tamanhos variados (ex: 1x1, 2x1, 2x2, 3x2) dentro de uma grade mestre com número de colunas configurável (ex: 4 ou 12 colunas), minimizando espaços vazios.
2. **Geração Dinâmica de CSS Grid:** Calcular as coordenadas exatas (`grid-column: span X`, `grid-row: span Y`) para cada elemento com base no resultado do algoritmo.
3. **Otimização de Responsividade:** O motor deve prever a quebra da grade para dispositivos móveis (viewport < 768px), convertendo a estrutura complexa do Bento Grid numa pilha vertical linear (1 coluna) automaticamente no CSS gerado.

### 2. Formato de Saída (JSON no stdout)
O retorno para o backend do Valen deve ser um JSON estruturado contendo o código pronto:
{
  "status": "sucesso",
  "eficiencia_preenchimento_porcentagem": 98.5,
  "html_componente": "<div class=\"bento-grid\"><div class=\"bento-item card-1\">...</div></div>",
  "css_estilo": ".bento-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; } .card-1 { grid-column: span 2; grid-row: span 2; }"
}

### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto JSON da ferramenta `astraz_bento_grid_generator`. O Valen deve acioná-la sempre que o usuário solicitar o design estrutural de um novo dashboard, landing page ou secção de portfólio para os clientes da Astraz Studio.

Gere os arquivos mestre (main.cpp e CMakeLists.txt com flag -O3) prontos para compilação.

```
### 👕 Prompt 2: astraz_mockup_renderer (Processador de Estampas e Texturas MMLXX)
```text
Atue como um Engenheiro de Computação Gráfica Sênior especialista em Visão Computacional, Processamento de Imagens em C++20 e Automação de E-commerce.

Preciso criar um motor gráfico nativo em C++ chamado `astraz-mockup-renderer` focado na automação da marca de moda MMLXX da Astraz Studio. O objetivo do motor é receber o arquivo de uma estampa ou logotipo minimalista (PNG com canal alfa) e aplicá-lo matematicamente sobre a imagem base de uma peça de vestuário (ex: um moletom ou camiseta de cor sólida), respeitando as dobras do tecido, sombreamento natural e perspetiva tridimensional do corpo.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs e 32 GB de RAM, utilizando a biblioteca corporativa `OpenCV` (módulos `imgproc` e `core`) vinculada nativamente ao C++.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--pattern <CAMINHO_PNG>` e `--base-apparel <CAMINHO_TEMPLATE>` e `--output <CAMINHO_PRODUTO>`.
1. **Mapeamento de Textura e Distorção (Displacement Mapping):** O motor deve ler o canal de iluminação da imagem base (camada de brilho/sombra) para gerar um mapa de deslocamento. A estampa inserida deve ser distorcida seguindo esse mapa para simular as ondulações do tecido.
2. **Mistura de Camadas (Blend Modes):** Implementar operações matemáticas de matrizes (OpenCV expressions) para multiplicar as sombras da camiseta original sobre a estampa aplicada, preservando o realismo fotográfico sem achatar a imagem.
3. **Transformação Afim/Perspetiva:** Permitir passar parâmetros de inclinação e escala via CLI para ajustar o posicionamento exato da estampa no peito, costas ou mangas.

### 2. Formato de Saída (JSON no stdout)
{
  "status": "sucesso",
  "resolucao_saida": "2048x2048",
  "arquivo_renderizado": "/var/www/mmlxx/store/produto_gerado.webp",
  "tempo_renderizacao_ms": 112.4
}

### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto JSON da ferramenta `astraz_mockup_renderer`. O Valen deve usar esta ferramenta sempre que o usuário enviar uma nova arte vetorial ou logo e der ordens para visualizar o produto aplicado nas roupas da MMLXX.

Entregue o código C++ completo com OpenCV integrado e o script bash de instalação das dependências no Ubuntu.

```
### 📈 Prompt 3: astraz_trends_scout (Rastreador de Tendências Headless)
```text
Atue como um Engenheiro de Mineração de Dados Sênior especialista em Redes, Scrapers Assíncronos em C++20 e Análise Preditiva.

Preciso criar um motor automatizado de inteligência de mercado em C++ chamado `astraz-trends-scout` para a Astraz Studio. O objetivo é varrer de forma paralela e invisível (headless) os feeds e endpoints públicos de plataformas de tendências (como TikTok Creative Center, Google Trends e agregadores de comportamento), minerar palavras-chave, ganchos (hooks) e áudios que estão em ascensão exponencial nas últimas horas no Brasil, filtrando futilidades e focando nos nichos da agência: tecnologia, sofisticação, luxo e negócios digitais.

O ambiente de execução é uma VPS Ubuntu (4 vCPUs, 32 GB de RAM), utilizando `libcurl` de forma assíncrona com `std::jthread` do C++20 para requisições paralelas sem travar a rede.

### 1. Requisitos do Fluxo do Motor (C++)
O binário deve rodar de forma cronometrada ou por gatilho do Valen via argumento `--niche <NOME>`.
1. **Scraping Concorrente com Rotação:** Efetuar requisições HTTP paralelas utilizando buffers em memória. O parseamento de strings e extração de dados brutos deve ser feito via regex otimizadas ou manipulação direta de JSON com `nlohmann/json`.
2. **Algoritmo de Score de Tendência (Velocity Rate):** Implementar uma fórmula matemática simples baseada no volume de buscas dividido pelo delta de tempo (aceleração do termo). Termos com picos abruptos recebem prioridade máxima.
3. **Filtro Semântico Negativo:** O motor deve ignorar termos de baixo valor agregado ou fora do escopo corporativo da Astraz Studio através de uma estrutura de dados `std::unordered_set` (Blacklist).

### 2. Formato de Saída (JSON no stdout)
{
  "status": "sucesso",
  "timestamp": 1786199650,
  "tendencias_detectadas": [
    { "termo": "Interface Bento Grid Minimalista", "score_acelera": 9.4, "canal": "Google/Pinterest", "nicho": "Design/Tech" },
    { "termo": "Automação Local com AI Privada", "score_acelera": 8.7, "canal": "TikTok Tech", "nicho": "Business" }
  ]
}

### 3. Integração com o Valen (Formato Tool)
Crie o manifesto da função JSON para a ferramenta `astraz_trends_scout`. O Valen usará este motor para municiar o usuário com relatórios semanais ou diários de ideias de conteúdos de alta conversão.

Forneça os entregáveis: main.cpp, CMakeLists.txt e dependências do sistema.

```
### 📊 Prompt 4: astraz_funnel_simulator (Simulador Matemático de ROI)
```text
Atue como um Engenheiro de Software Sênior especialista em Análise Numérica, Modelagem Estatística e Simulações Computacionais em C++20.

Preciso criar um mecanismo estatístico de alta fidelidade em C++ chamado `astraz-funnel-simulator` para prever os resultados de lançamentos e campanhas de aquisição da Astraz Studio. O motor deve receber métricas estimadas de um funil de vendas através de um payload JSON, modelar o comportamento de tráfego usando estruturas de Grafos Direcionados, e rodar 10.000 iterações matemáticas usando a Simulação de Monte Carlo para gerar a probabilidade real de ROI, custo por lead (CPL), margem líquida e quebra de estoque.

O ambiente é uma VPS Ubuntu com 4 vCPUs e 32 GB de RAM. O código deve fazer uso intensivo de `<random>` do C++20 com geradores de alta qualidade (Mersenne Twister) e paralelização nativa em todas as vCPUs.

### 1. Requisitos do Fluxo do Motor (C++)
O binário deve aceitar o argumento `--funnel-json "<DADOS>"` e calcular os cenários probabilísticos:
1. **Modelagem Baseada em Grafos:** Cada estágio do funil (Anúncio -> Landing Page -> Checkout -> Upsell -> Conversão Final) é um nó no grafo. O peso das arestas é a taxa de conversão flutuante (aplicando uma distribuição normal/gaussiana de desvio padrão para simular a instabilidade do mercado real).
2. **Simulação Multithreaded (Monte Carlo):** Dividir as 10.000 simulações pelas 4 vCPUs usando `std::async` ou loops paralelos (`std::execution::par`), onde cada thread calcula milhares de jornadas de usuários independentes em microssegundos.
3. **Compilação de Percentis:** Calcular intervalos de confiança estatística de 10% (pior cenário), 50% (cenário realista) e 90% (melhor cenário) de lucro.

### 2. Formato de Saída (JSON no stdout)
{
  "status": "sucesso",
  "iteracoes": 10000,
  "roi_medio": 3.4,
  "probabilidade_prejuizo_porcentagem": 1.2,
  "cenarios": {
    "conservador_p10": { "lucro_liquido": 1200.00, "cpl": 4.50 },
    "realista_p50": { "lucro_liquido": 15000.00, "cpl": 2.10 },
    "otimista_p90": { "lucro_liquido": 42000.00, "cpl": 1.05 }
  }
}

### 3. Integração com o Valen (Formato Tool)
Escreva o esquema JSON do Tool `astraz_funnel_simulator`. O Valen usará esta ferramenta para dar respostas preditivas exatas e embasadas em matemática pura sobre a viabilidade de orçamentos de marketing.

Gere os códigos fontes industriais completos.

```
### 🛠️ Prompt 5: astraz_container_sentinel (Monitor Autónomo do Ecossistema Docker)
```text
Atue como un Engenheiro de Sistemas Linux Sênior, Core Developer de C++20 e Especialista em Infraestrutura de Containers (Docker Enterprise).

Preciso criar um daemon utilitário em C++ chamado `astraz-container-sentinel` focado em manter a resiliência máxima da VPS e do futuro Home Lab da Astraz Studio. O objetivo deste binário é monitorar em tempo real o socket UNIX nativo do Docker (`/var/run/docker.sock`) usando loops de eventos assíncronos do Kernel Linux (`epoll`), extraindo telemetria de CPU, memória RAM e saúde de todas as instâncias (Supabase, painéis de clientes, instâncias de LLM locais e o próprio backend do Valen). Se ocorrer vazamento de memória ou travamento de container, o sentinel deve intervir autonomamente em microssegundos.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs e 32 GB de RAM. O código deve ser livre de vazamentos de memória (leak-free) e rodar com privilégios adequados no Linux.

### 1. Requisitos do Fluxo do Motor (C++)
O motor roda em segundo plano através de comunicação via Socket UNIX nativo (usando `sys/socket.h`).
1. **Loop de Eventos `epoll` não-bloqueante:** Monitorar eventos de ciclo de vida do Docker (die, oom, crash) direto do stream do socket do Docker sem realizar pooling constante (arquitetura orientada a eventos).
2. **Análise de Limite de Recursos (Auto-Healing):** Se o motor detectar que um container de homologação ou banco de dados de um cliente ultrapassou 90% de consumo de RAM ou entrou em loop de CPU em idle por mais de 60 segundos, ele deve enviar programaticamente um comando HTTP POST via socket para reiniciar o container (`/containers/{id}/restart`).
3. **Flushing de Memória:** Executar ganchos do sistema operacional para liberar caches da VPS após interrupções críticas.

### 2. Formato de Saída (JSON no stdout/logs)
{
  "evento_detectado": "OOM_KILLED_OR_HIGH_RAM",
  "container_target": "supabase-db-prod",
  "acao_sentinel": "RESTART_EXECUTED",
  "memoria_recuperada_mb": 4096.0,
  "timestamp": 1786199780
}

### 3. Integração com o Valen (Formato Tool)
Escreva a definição do Tool JSON `astraz_container_sentinel`. O Valen deve usar este tool para consultar o status de infraestrutura e emitir alertas preditivos ao usuário direto no chat.

Gere a solução completa com CMakeLists.txt pronto.

```
### 🧹 Prompt 6: astraz_vps_janitor (Garbage Collector de Infraestrutura)
```text
Atue como um Engenheiro de Confiabilidade de Sites (SRE) Sênior e Especialista em Baixo Nível em C++20 e Sistemas de Arquivos Linux (ext4/XFS).

Preciso criar um utilitário de manutenção industrial em C++ chamado `astraz-vps-janitor`. O objetivo deste motor é realizar uma varredura profunda no SSD de 200 GB da minha VPS Ubuntu da Astraz Studio, localizando e limpando com segurança gigabytes de arquivos inúteis gerados automaticamente por pipelines de desenvolvimento, tais como logs inflados, caches de pacotes npm/pip/cargo antigos, imagens Docker suspensas (dangling) e arquivos temporários de compilações de APKs, otimizando o espaço físico instantaneamente.

O código deve usar a biblioteca puramente nativa `<filesystem>` do C++20 para velocidade máxima de navegação em diretórios.

### 1. Requisitos do Fluxo do Motor (C++)
O binário aceita o comando CLI `--clean-all` ou diretórios específicos `--scan <PASTA>`.
1. **Varredura Recursiva de Disco Sub-milenar:** Utilizar `std::filesystem::recursive_directory_iterator` configurado para pular links simbólicos perigosos, calculando o tamanho acumulado de arquivos temporários (`.log`, `.tmp`, `.cache`, `.o`, `.a`).
2. **Interação com Subsistemas (Docker & Package Managers):** Invocar de forma limpa comandos de purga do sistema (como `docker image prune -f` e `apt-get clean`) capturando a saída para consolidar o relatório final de espaço livre.
3. **Truncagem Segura de Logs:** Para arquivos de logs ativos do sistema que não podem ser deletados diretamente por estarem abertos pelo Linux, o motor deve executar uma operação de truncagem para zerar o arquivo (`std::ofstream::trunc`) em vez de apagá-lo, evitando quebra de descritores de arquivo.

### 2. Formato de Saída (JSON no stdout)
{
  "status": "faxina_concluida",
  "espaco_inicial_livre_gb": 45.2,
  "espaco_final_livre_gb": 82.1,
  "total_recuperado_gb": 36.9,
  "detalhes_limpeza": {
    "logs_truncados_bytes": 12450000000,
    "docker_cache_deletado_bytes": 24450000000
  }
}

### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto JSON do Tool `astraz_vps_janitor`. O Valen acionará esta ferramenta sempre que o espaço em disco cair abaixo de níveis críticos ou quando o usuário pedir explicitamente para otimizar os servidores da Astraz Studio.

Entregue o código completo prontinho para rodar na VPS.

```
### 🤖 Prompt 7: astraz_local_embeddings (Indexador Vetorial Privado)
```text
Atue como um Engenheiro de Aprendizado de Máquina Sênior, Especialista em C++20, Arquiteturas de Busca Vetorial Nativas (RAG) e Soberania Digital.

Preciso criar um motor de vetorização e indexação de dados local de altíssima performance em C++ chamado `astraz-local-embeddings` para a infraestrutura privada da Astraz Studio. O objetivo deste motor é ler arquivos de texto, briefings, códigos e históricos de conversas enviados pelo Valen, gerar os embeddings semânticos localmente usando as 4 vCPUs da VPS (sem depender de APIs externas pagas ou expor dados confidenciais), e estruturar uma base de dados vetorial em memória RAM de baixíssima latência para buscas rápidas por similaridade de cosseno.

O motor deve se vincular a bibliotecas nativas como `llama.cpp` (para inferência de modelos base em formato GGML/GGUF como o BERT-base) ou uma implementação otimizada baseada em matemática de matrizes via BLAS/AVX2.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os comandos `--embed --text "<STRING>"` ou `--search --query "<TERMO>" --top-k 3`.
1. **Tokenização e Inferência Local:** Carregar na memória RAM da VPS um modelo leve de embeddings (como o `all-MiniLM-L6-v2.gguf`), processar o texto de entrada em tensores e executar o forward pass nas vCPUs aproveitando as instruções de hardware para gerar um vetor de tamanho fixo (geralmente 384 ou 768 dimensões).
2. **Motor de Busca por Similaridade (Cosine Similarity):** Implementar o cálculo matemático da similaridade de cosseno de forma ultra-paralelizada (usando threads C++20) para comparar o vetor da consulta contra o array de vetores salvos no arquivo binário de índice.
3. **Persistência Eficiente:** Salvar a matriz de vetores e metadados estruturados num arquivo binário contíguo no disco da VPS para carregamento instantâneo.

### 2. Formato de Saída para o Comando `--search` (stdout)
{
  "status": "sucesso",
  "tempo_busca_ms": 2.1,
  "resultados": [
    { "id_documento": "briefing_cliente_nexus.md", "score_similaridade": 0.92, "trecho": "O cliente Nexus exige um dashboard Bento Grid focado em luxo..." },
    { "id_documento": "contrato_089.md", "score_similaridade": 0.78, "trecho": "Desenvolvimento de ecossistema SaaS integrado ao Supabase..." }
  ]
}

### 3. Integração com o Valen (Formato Tool)
Escreva o esquema JSON do Tool `astraz_local_embeddings`. O Valen usará este motor como o seu sistema central de Memória de Longo Prazo Privada (RAG Local), permitindo recordar briefings antigos e decisões de arquitetura em frações de segundo.

Entregue o código completo em C++20 com tratamento de matrizes e o arquivo CMakeLists.txt otimizado.

