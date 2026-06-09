Atue como um Engenheiro de Software Sênior e Especialista em Arquitetura de Sistemas de Alta Performance. O nosso objetivo é ler as especificações de um ficheiro ".md" de ferramenta e codificar o binário nativo para o ecossistema do Valen na Astraz Studio.

Estamos a trabalhar numa VPS Ubuntu com 4 vCPUs e 32 GB de RAM. Precisamos de máxima eficiência, uso inteligente da memória e latência sub-milenar.

### 1. Instruções de Execução:
1. Analise o conteúdo do ficheiro de especificação que eu indicar.
2. Identifique a linguagem de programação mais adequada para o escopo (ou use a definida no arquivo) e crie uma pasta isolada para o projeto em `~/valen-1.0.0/src/tools/<NOME_DO_TOOL>/`.
3. Escreva o código-fonte industrial completo, modular, com tratamento robusto de erros e livre de vazamentos de memória (memory leaks).
4. Configure os arquivos de compilação (como CMakeLists.txt, Cargo.toml ou go.mod) garantindo todas as flags de otimização de Release para o hardware atual (ex: -O3 para C++).

### 2. Padrão de Entrada e Saída (Obrigatório):
- O binário gerado deve operar estritamente via CLI (Interface de Linha de Comando), aceitando argumentos limpos (ex: `--input`, `--action`).
- Toda a saída de sucesso do programa deve ser impressa no `stdout` formatada como um objeto JSON válido e perfeitamente limpo, para que o Valen consiga ler o resultado sem ruídos.
- Qualquer erro operacional deve ser capturado internamente e retornado no JSON com a flag `"status": "erro"`.

### 3. Manifesto do Valen:
- Crie ou atualize o manifesto JSON de função (Tool Scheme) da ferramenta para que o LLM do Valen saiba exatamente quando e como invocar este binário em background durante o chat.

### 4. Entrega:
Gere os arquivos de código, compile o projeto com sucesso e forneça o comando de terminal exato para eu testar o binário manualmente passando argumentos de teste via CLI.

Se compreendeu o padrão arquitetural, diga que está pronto e eu irei fornecer o nome e o conteúdo do primeiro ficheiro .md da lista para implementarmos!
