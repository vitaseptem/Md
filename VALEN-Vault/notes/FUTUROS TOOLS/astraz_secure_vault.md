---
type: concept
tags: [futuros-tools]
created: 2026-06-09
priority: medium
---

Atue como um Engenheiro de Segurança de Informação e Especialista em C++20, Criptografia de Baixo Nível e Arquitetura de Agentes de IA.

Preciso criar um micro-serviço e utilitário em C++ chamado `astraz-secure-vault`. O objetivo deste motor é atuar como um cofre de credenciais blindado e de ultra-alta performance para o backend do meu assistente de IA, o Valen. Ele deve armazenar, encriptar e decriptar chaves de API (OpenAI, Anthropic, Supabase) e senhas de clientes em disco utilizando o algoritmo AES-256-GCM (Authenticated Encryption), gerenciando o ciclo de vida dos segredos diretamente na memória RAM de forma segura (limpando buffers após o uso).

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs, 32 GB de RAM e 200 GB de SSD. O código deve ser escrito em C++20, utilizando a biblioteca nativa do OpenSSL (`libcrypto`) para operações criptográficas de hardware-accelerated (AES-NI).

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve operar através de comandos de CLI seguros. Ele deve suportar estritamente as seguintes operações:

1. **Inicialização (`--init --vault <CAMINHO>`):**
   - Cria um novo arquivo de cofre criptografado. O motor deve solicitar uma "Master Password" via terminal de forma segura (ocultando a digitação no stdin) ou aceitar uma variável de ambiente `ASTRAZ_VAULT_KEY`.
   - Utilizar o algoritmo PBKDF2 (com HMAC-SHA256) com pelo menos 100.000 iterações e um salt aleatório de 16 bytes para derivar a chave de encriptação real de 256 bits a partir da Master Password.

2. **Armazenamento de Segredos (`--set --key <NOME_DA_CHAVE> --value <VALOR>`):**
   - Abrir o cofre existente, derivar a chave, gerar um IV (Initialization Vector) aleatório de 12 bytes único para esta operação.
   - Encriptar o valor usando **AES-256-GCM**. O motor deve capturar a tag de autenticação de 16 bytes gerada pelo GCM para garantir a integridade do arquivo.
   - Salvar o registro (Chave, IV, Tag, Texto Criptografado) de forma estruturada (pode ser binário ou JSON encriptado) no disco.

3. **Recuperação de Segredos (`--get --key <NOME_DA_CHAVE>`):**
   - Ler o arquivo do cofre, localizar o registro correspondente à chave solicitada.
   - Decriptar o valor na memória RAM usando a chave derivada, o IV e validando a tag de autenticação GCM.
   - **Regra de Segurança Crítica (Memory Sanitization):** Imprimir o segredo decriptado estritamente no `stdout` para consumo do backend do Valen. Imediatamente após a impressão ou em caso de erro, o motor DEVE preencher os buffers de memória RAM que guardavam a senha com zeros (`std::fill` ou `memset_s`) para evitar ataques de vazamento de memória (Memory Dumping).

### 2. Formato de Saída para o Comando `--get` (stdout)
Para garantir que o Valen ou o backend consigam ler o segredo sem parsing complexo, o motor deve retornar um JSON limpo contendo apenas o dado solicitado ou o status de erro:

```json
{
  "status": "sucesso",
  "chave": "SUPABASE_SERVICE_ROLE_KEY",
  "valor": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Em caso de falha de autenticação (Master Password incorreta ou arquivo corrompido):
{
  "status": "erro",
  "mensagem": "Falha na autenticação do cofre. Tag GCM inválida ou chave incorreta."
}


3. Integração com o Valen (Formato Tool)
Escreva o manifesto da função (Tool Definition) no formato JSON padrão para agentes de IA. A ferramenta deve se chamar astraz_secure_vault.
Inclua uma descrição detalhada e restritiva explicando ao Valen que ele deve acionar esta ferramenta SEMPRE que precisar ler credenciais, tokens de bancos de dados ou chaves de terceiros para executar uma tarefa (como atualizar o banco de um cliente no Supabase). O Valen NUNCA deve expor o valor retornado por esta ferramenta diretamente no chat com o usuário; ele deve usar o token internamente em background e descartá-lo.
4. Entregáveis esperados:
O código-fonte em C++20 (main.cpp e implementação criptográfica) limpo, modular e focado em segurança defensiva contra estouros de buffer.
O arquivo CMakeLists.txt configurado para linkar com a libcrypto do OpenSSL, otimizado com -O3 e proteção de pilha (-fstack-protector-strong).
O comando bash completo para instalar o OpenSSL de desenvolvimento no Ubuntu.
O esquema JSON do Tool e um exemplo prático de como o backend do assistente de IA deve interagir com este binário usando pipes seguros sem deixar rastros de texto limpo nos logs do Linux.
Gere uma solução de engenharia de nível militar pronta para rodar na minha VPS.