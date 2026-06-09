Atue como um Engenheiro de Sistemas Sênior, especialista em Concorrência em C++20, Protocolos de Rede e Engenharia de Dados orientada a Agentes de IA.

Preciso criar um motor utilitário de altíssima performance em C++ chamado `astraz-lead-enricher`. O objetivo deste motor é receber uma lista de domínios/sites de empresas (enviada em massa por um arquivo ou string), efetuar uma varredura paralela em microssegundos para extrair e-mails corporativos, links de redes sociais, telefones e, crucialmente, executar uma validação profunda de SMTP (handshake de e-mail) para garantir que os leads são reais. Este binário será integrado como uma ferramenta (Tool) oficial no backend do meu assistente de IA, o Valen, para prospecção ativa da Astra Growth.

O ambiente de execução é uma VPS Ubuntu com 4 vCPUs, 32 GB de RAM e 200 GB de SSD. O código deve ser puramente multithreaded (utilizando o pool de threads do C++20), com gerenciamento estrito de memória para evitar vazamentos (leak-free).

### 1. Requisitos do Fluxo do Motor (C++)
O binário C++ deve aceitar o argumento `--domains "<DOMINIO1>,<DOMINIO2>,<DOMINIO3>"` ou `--file <CAMINHO_DO_ARQUIVO_TXT>`. O pipeline interno deve executar rigorosamente as seguintes etapas por domínio, distribuindo a carga entre as 4 vCPUs:

1. **Web Scraping de Alta Velocidade (Contact Extraction):**
   - Efetuar requisições assíncronas assinaladas à `libcurl` para baixar a Home Page e a página de "Contato" ou "Sobre" de cada domínio em paralelo (com timeout agressivo de 3 segundos por site para evitar travamentos).
   - Utilizar expressões regulares otimizadas (`std::regex`) ou um parser como `Lexbor` na memória RAM para capturar instantaneamente:
     - Endereços de e-mail (padrões corporativos).
     - Números de telefone (formatos brasileiros e internacionais).
     - Links de redes sociais (LinkedIn, Instagram, Facebook, WhatsApp).

2. **Verificação de Entregabilidade de E-mail (Deep SMTP Handshake):**
   - Para cada e-mail encontrado, o motor C++ deve abrir um socket TCP nativo na porta 25 (ou 587 se necessário) apontando para o servidor MX do domínio do lead (usando chamadas POSIX padrão ou `Boost.Asio`).
   - O motor deve simular o início de um envio de e-mail (executando os comandos `HELO/EHLO`, `MAIL FROM:<contato@astragrowth.com>`), e capturar a resposta do servidor ao comando `RCPT TO:<e-mail_do_lead>`.
   - **Regra Crítica:** O motor deve abortar a conexão imediatamente após a resposta do `RCPT TO` (enviando `QUIT`) sem nunca enviar um e-mail de fato. Se o servidor responder com código `250 OK`, o e-mail é marcado como válido (`"smtp_valido": true`). Se responder com erro (como `550 User Unknown`), o lead é descartado ou marcado como inválido.

3. **Orquestração Multithreading (Thread Pool):**
   - Implementar um padrão de Thread Pool nativo do C++20 para garantir que até 20 ou 30 domínios sejam processados simultaneamente, mapeados de forma inteligente sobre as 4 vCPUs físicas para evitar sobrecarga de contexto.

### 2. Formato de Saída (JSON estruturado no stdout)
O motor C++ deve cuspir diretamente no `stdout` um objeto JSON consolidado contendo o array de leads enriquecidos, facilitando a leitura direta pelo Valen:

```json
{
  "total_processado": 2,
  "leads": [
    {
      "dominio": "empresaalpha.com.br",
      "status": "sucesso",
      "telefones": ["(98) 99999-9999"],
      "redes_sociais": {
        "instagram": "[https://instagram.com/empresaalpha](https://instagram.com/empresaalpha)",
        "linkedin": "[https://linkedin.com/company/empresaalpha](https://linkedin.com/company/empresaalpha)"
      },
      "emails_encontrados": [
        {
          "endereco": "contato@empresaalpha.com.br",
          "smtp_valido": true
        },
        {
          "endereco": "vendas@empresaalpha.com.br",
          "smtp_valido": false
        }
      ]
    },
    {
      "dominio": "empresabeta.com",
      "status": "nao_encontrado_ou_timeout"
    }
  ]
}

3. Integração com o Valen (Formato Tool)
Escreva o manifesto da função (Tool Definition) no formato JSON padrão para agentes de IA. A ferramenta deve se chamar astraz_lead_enricher.
Inclua uma descrição detalhada explicando ao Valen que ele deve usar esta ferramenta SEMPRE que o usuário fornecer uma lista de sites de empresas, pedir para coletar contatos de possíveis clientes para a agência ou solicitar a validação de uma lista de e-mails de marketing para garantir que a taxa de rejeição (bounce rate) seja zero.
4. Entregáveis esperados:
O código-fonte em C++20 (main.cpp e módulos anexos de rede) estruturado de forma industrial, robusto contra sites lentos ou fora do ar.
O arquivo CMakeLists.txt configurado com otimizações de compilação completas (-O3, -pthread).
O comando bash com os pacotes do Ubuntu necessários para rodar este motor (incluindo libcurl4-openssl-dev e libjsoncpp-dev ou suporte ao nlohmann/json).
O esquema JSON do Tool e um exemplo prático de execução via código de backend do assistente para capturar a saída limpa.
Gere uma solução de nível de produção pronta para escalar a prospecção da Astraz Studio na minha VPS.