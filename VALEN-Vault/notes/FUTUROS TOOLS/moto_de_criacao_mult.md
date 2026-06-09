Para levar a **Astraz Studio** e o **Valen** ao nível mais alto possível de automação de engenharia, podemos desenhar **Motores de Compilação e Empacotamento Automatizado (Build & Deployment Engines)** em C++.
A ideia aqui é que você não precise abrir o VS Code, configurar SDKs ou compilar manualmente os projetos. O seu backend ou o Valen apenas envia os arquivos de código-fonte (HTML/JS/CSS, Flutter, C++, etc.) para esses motores nativos na sua VPS de 32 GB, e eles cospem o aplicativo final pronto e empacotado para o cliente.
Aqui estão os prompts ultra detalhados para cada um desses motores de compilação:
### 📱 Motor 1: astraz_apk_compiler (Gerador Automático de APKs Android)
```text
Atue como um Engenheiro de Compilação Mobile Sênior (DevOps Mobile) especialista em C++20, Android NDK/SDK e Automação de Pipelines para Agentes de IA.

Preciso criar um motor utilitário em C++ chamado `astraz-apk-compiler`. O objetivo deste motor é receber um diretório contendo o código-fonte de uma aplicação mobile (seja um projeto Flutter, React Native, Cordova ou uma Web App nativa com WebView) e automatizar todo o pipeline de compilação, assinatura e otimização, gerando um arquivo `.apk` final pronto para instalação. Este binário será uma ferramenta (Tool) para o meu assistente Valen na Astraz Studio.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs, 32 GB de RAM e 200 GB de SSD. O motor C++ deve gerenciar os processos em background de forma assíncrona, capturando os logs do Gradle em tempo real.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--input-dir <CAMINHO>` e `--output-apk <NOME_DO_ARQUIVO>`. O pipeline interno deve executar rigorosamente:
1. **Validação do Ambiente:** Verificar se as variáveis de ambiente do Android SDK, NDK e Java (JDK) estão configuradas corretamente na VPS através de chamadas de sistema eficientes.
2. **Injeção de Assets e Configurações:** Ler um arquivo JSON de configuração enviado pelo Valen contendo o nome do app, a versão, o package name (ex: com.astraz.myapp) e o caminho do ícone gerado. O C++ deve modificar os arquivos `AndroidManifest.xml` e `build.gradle` em memória e salvá-los.
3. **Compilação Assíncrona (Gradle Wrapper):** Chamar o processo `./gradlew assembleRelease` usando pipes assíncronos (`popen` ou `boost::process`) para não bloquear a linha de execução, alocando de forma inteligente a memória RAM para o daemon do Gradle.
4. **Alinhamento e Assinatura Criptográfica:** Invocar as ferramentas `zipalign` para otimização do binário e `apksigner` utilizando uma KeyStore padrão da Astraz Studio armazenada de forma segura, gerando o APK final otimizado.

### 2. Formato de Saída (JSON no stdout)
```json
{
  "status": "sucesso",
  "plataforma": "Android (APK)",
  "package_name": "com.astraz.cliente.app",
  "versao": "1.0.0",
  "tempo_compilacao_segundos": 45.8,
  "arquivo_gerado": "/var/www/downloads/app-release-signed.apk"
}

```
### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto da função JSON para a ferramenta astraz_apk_compiler. Explique ao Valen que ele deve usar esta ferramenta sempre que o usuário pedir para converter um site, landing page ou código mobile em um aplicativo Android (.apk) instalável para o cliente.
```

---

### 🍏 Motor 2: `astraz_macos_packager` (Compilador Híbrido de Apps Mac)

```text
Atue como um Engenheiro de Sistemas Sênior especialista em C++20, Cross-Compilation, Ambientes Apple e Arquitetura de Agentes de IA.

Preciso criar um motor em C++ chamado `astraz-macos-packager`. O objetivo deste motor é receber o código de uma aplicação (como uma Web App HTML/JS ou binário nativo de desktop) e gerar a estrutura de um pacote `.app` executável para macOS, gerando também o instalador `.dmg`. Como o ambiente hospedeiro principal é o Linux (VPS), o motor deve focar em preparar a estrutura de arquivos da Apple e aplicar técnicas de empacotamento cross-platform (como ferramentas baseadas em Electron-Builder headless ou cross-compiler LLVM/Clang direcionado ao target de Darwin).

O ambiente é uma VPS Ubuntu (4 vCPUs, 32 GB de RAM). O motor deve ser ultraveloz no processamento de arquivos.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--source <DIRETORIO>` e `--output-dmg <CAMINHO_DMG>`. O pipeline deve executar:
1. **Construção do Bundle Apple:** Criar de forma programática a árvore de diretórios padrão do macOS: `Contents/`, `Contents/MacOS/` e `Contents/Resources/`.
2. **Compilação do Manifesto PList:** Gerar dinamicamente o arquivo binário ou XML `Info.plist` contendo os metadados do aplicativo (Bundle Identifier, Version, Executable Name).
3. **Conversão de Ícones (ICNS Engine):** Pegar um arquivo PNG mestre enviado pelo usuário e convertê-lo nativamente em um arquivo `.icns` multi-resolução da Apple através de manipulação de buffers.
4. **Criação do DMG (Disk Image):** Invocar utilitários de sistema Linux (como `genisoimage` ou `dmg` tools para Linux) para comprimir a pasta `.app` dentro de um arquivo `.dmg` montável com um background customizado minimalista da Astraz Studio.

### 2. Formato de Saída (JSON no stdout)
```json
{
  "status": "sucesso",
  "plataforma": "macOS",
  "arquitetura": "Universal (Intel/Apple Silicon)",
  "bundle_id": "studio.astraz.desktopapp",
  "arquivo_gerado": "/var/www/downloads/Aplicativo_Mac.dmg"
}

```
### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto JSON da ferramenta astraz_macos_packager. O Valen deve acionar esse motor sempre que um cliente da agência solicitar que sua plataforma web ou software seja empacotado como um aplicativo nativo de desktop para computadores Mac.
```

---

### 🪟 Motor 3: `astraz_windows_compiler` (Compilador Nativo de EXEs e Instaladores Windows)

```text
Atue como um Engenheiro de Software Sênior especialista em C++20, Ferramentas de Cross-Compilation (MinGW-w64) e Automação de Sistemas de Build.

Preciso criar um motor em C++ chamado `astraz-windows-compiler`. O objetivo deste motor é compilar códigos-fonte desktop (C++, Rust ou encapsuladores de Web Apps como NeutralinoJS/Electron) diretamente da minha VPS Linux Ubuntu, gerando um executável nativo do Windows (`.exe`) de 64 bits e um instalador profissional (`.msi` ou `.exe` via NSIS). Este motor será uma ferramenta de backend automatizada para o assistente Valen.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs e 32 GB de RAM.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--src <DIRETORIO>` e `--make-installer`. O pipeline deve executar:
1. **Cross-Compilation Toolchain:** Invocar o compilador `x86_64-w64-mingw32-g++` ou ganchos do CMake configurados para o target do Windows, aplicando otimizações de tamanho de binário e stripping de símbolos (`-s`) para proteção de código.
2. **Embutidor de Recursos (Resource Compiler):** Compilar o arquivo de recursos do Windows (`.rc`) para injetar o ícone da empresa (`.ico`) e as informações de propriedades do arquivo diretamente no cabeçalho do executável PE (Portable Executable).
3. **Automação de Instalador (NSIS/WiX Automation):** Gerar dinamicamente um script de instalação (Nullsoft Scriptable Install System) contendo a tela de termos de uso da Astraz Studio, diretórios de instalação padrão (Program Files) e criação de atalhos na área de trabalho, compilando-o via `makensis`.

### 2. Formato de Saída (JSON no stdout)
```json
{
  "status": "sucesso",
  "plataforma": "Windows (x64)",
  "executavel_puro": "software_cliente.exe",
  "instalador_gerado": "/var/www/downloads/Instalador_Windows.exe",
  "tempo_execucao_ms": 12450
}

```
### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto JSON da ferramenta astraz_windows_compiler. O Valen deve usar esta ferramenta sempre que um projeto exigir uma versão executável para computadores Windows.
```

---

### 🐧 Motor 4: `astraz_linux_distributor` (Gerador de Pacotes DEB, RPM e AppImage para todas as Distros Linux)

```text
Atue como um Engenheiro de Kernel e Empacotamento Linux Sênior especialista em C++20, Padrões Freedesktop e Arquitetura de Agentes de IA.

Preciso criar um motor de distribuição de software em C++ chamado `astraz-linux-distributor`. O objetivo deste motor é receber um aplicativo ou binário compilado para Linux e empacotá-lo simultaneamente em múltiplos formatos de distribuição do ecossistema Linux: um pacote `.deb` (para Debian/Ubuntu/Mint), um pacote `.rpm` (para Fedora/RHEL) e um formato portátil universal `.AppImage` (que roda em qualquer distribuição sem instalação). Este motor alimentará as capacidades de DevOps do assistente Valen.

A execução ocorre em uma VPS Ubuntu com 4 vCPUs e 32 GB de RAM, exigindo o uso de threads em paralelo para criar os pacotes.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--binary <CAMINHO>` e `--output-formats "deb,rpm,appimage"`. O pipeline deve executar:
1. **Motor Debian (.deb):** Criar a árvore de controle `DEBIAN/` na memória, gerar o arquivo de metadados `control` com dependências de pacotes (como `glibc`), copiar os arquivos para os caminhos do sistema (`usr/bin/`, `usr/share/applications/`) e invocar o `dpkg-deb --build`.
2. **Motor Universal (.AppImage):** Configurar a estrutura de uma `AppDir`, gerar o script `AppRun`, injetar o arquivo `.desktop` em conformidade com as regras do Freedesktop.org e invocar a ferramenta `appimagetool` para gerar o binário auto-executável comprimido com `zstd`.
3. **Paralelização:** Processar a geração do DEB, RPM e AppImage usando as 4 vCPUs de forma simultânea via threads C++20.

### 2. Formato de Saída (JSON no stdout)
```json
{
  "status": "sucesso",
  "plataforma": "Linux Multi-Distro",
  "artefatos_gerados": {
    "debian_ubuntu": "/var/www/downloads/app_amd64.deb",
    "fedora_rhel": "/var/www/downloads/app_x86_64.rpm",
    "universal_appimage": "/var/www/downloads/app_Universal.AppImage"
  }
}

```
### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto JSON da ferramenta astraz_linux_distributor. Instrua o Valen a acionar esta ferramenta sempre que o usuário solicitar a publicação ou geração de versões de aplicativos de desktop focados em ambientes Linux e servidores Debian.
```

---

### 🌐 Motor 5: `astraz_web_saas_deployer` (Gerador e Publicador Automático de Sites e SaaS Web)

```text
Atue como um Arquiteto Cloud e Engenheiro de Software Principal especialista em C++20, Integração de APIs Cloud (Supabase/Docker) e Sistemas de IA.

Preciso criar um motor industrial em C++ chamado `astraz-web-saas-deployer`. O objetivo deste motor é receber uma estrutura completa de arquivos web (HTML, CSS, JavaScript, componentes React/Next.js ou configurações de tabelas do Supabase) e realizar o processo completo de build de produção, provisionamento de banco de dados, conteinerização via Docker e deploy em servidores locais ou na nuvem em tempo real. Este motor agirá como o núcleo de publicação da agência Astraz Studio e da agência Astra Growth através do assistente Valen.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs e 32 GB de RAM.

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar os argumentos `--project-dir <CAMINHO>` e `--domain <DOMINIO_DO_CLIENTE>`. O pipeline interno deve executar:
1. **Otimizador de Produção (Minification & Build):** Invocar subprocessos de compilação web (como `npm run build` ou compiladores nativos esbuild/swc via C++), limpando comentários, minificando arquivos JS/CSS e otimizando imagens para WebP automaticamente na memória RAM.
2. **Automação de Banco de Dados (Supabase/PostgreSQL Injection):** Ler os arquivos de migração SQL do projeto e injetá-los programaticamente via `libpqxx` nas tabelas do banco de dados de produção do cliente (criando esquemas, chaves estrangeiras e políticas de RLS automaticamente).
3. **Conteinerização Expressa (Docker API Engine):** Interagir com o socket local do Docker (`/var/run/docker.sock`) para gerar um `Dockerfile` otimizado em tempo real, buildar a imagem do SaaS e levantar o container vinculando-o às portas de rede corretas.
4. **Configuração de Proxy Reverso & SSL:** Modificar arquivos de configuração do servidor web (Nginx ou Caddy) de forma dinâmica para apontar o subdomínio/domínio do cliente para o novo container, disparando a emissão do certificado SSL Let's Encrypt automaticamente.

### 2. Formato de Saída (JSON no stdout)
```json
{
  "status": "sucesso",
  "tipo": "SaaS_Web_Application",
  "url_publicada": "[https://plataforma.clientenexus.com](https://plataforma.clientenexus.com)",
  "container_id": "a8f3d1e92b3c",
  "banco_dados_status": "migracoes_aplicadas_com_sucesso",
  "tempo_total_deploy_ms": 18450
}

```
### 3. Integração com o Valen (Formato Tool)
Escreva o manifesto da função JSON para a ferramenta astraz_web_saas_deployer. Explique detalhadamente ao Valen que ele deve acionar esta ferramenta SEMPRE que o usuário disser que o projeto web, landing page ou sistema SaaS está pronto para ir ao ar (produção), permitindo que a IA faça o deploy completo do negócio do cliente com um único comando no chat.
```

---

