---
type: concept
tags: [cli]
created: 2026-06-09
priority: medium
---

# VALEN CLI - Master Prompt Ultra Detalhado v3.0

**Objetivo:** Criar uma CLI profissional, robusta e instalável via pip para gerenciar o ciclo de vida do projeto VALEN no Ubuntu VPS.

**Repositório oficial:** https://github.com/vitaseptem/Valen.git

---

## 1. Contexto e Visão

Você deve criar uma ferramenta de linha de comando chamada **`valen-cli`** que permita ao usuário gerenciar a instalação do VALEN de forma profissional e soberana.

Após instalar a CLI com `pip install valen-cli`, o usuário deve poder usar comandos como:

```bash
valen upgrade
valen status
valen update-deps
valen backup
valen install
valen uninstall
```

O comando mais importante é **`valen upgrade`**, que deve:

- Puxar as últimas alterações do GitHub
- Atualizar dependências
- Fazer backup automático
- Reiniciar serviços (systemd)
- Ser seguro e confiável para uso em produção (VPS Ubuntu)

---

## 2. Tech Stack Recomendado

- **Python 3.11+**
- **Typer** (framework de CLI moderno e elegante)
- **Rich** (para output bonito, tabelas, painéis, progresso e cores)
- `subprocess` ou `GitPython` para operações Git
- `uv` como gerenciador de dependências preferencial (rápido e moderno)
- Suporte a configuração via arquivo TOML

---

## 3. Estrutura de Pastas Recomendada

```bash
valen-cli/
├── pyproject.toml
├── README.md
├── valen/
│   ├── __init__.py
│   ├── cli.py                    # Ponto de entrada principal
│   ├── config.py                 # Gerenciamento de configuração
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── upgrade.py
│   │   ├── install.py
│   │   ├── uninstall.py
│   │   ├── update_deps.py
│   │   ├── status.py
│   │   └── backup.py
│   └── utils/
│       ├── __init__.py
│       ├── git.py
│       ├── system.py
│       ├── backup.py
│       └── logging.py
└── tests/
```

---

## 4. Especificação dos Comandos

### 4.1 `valen upgrade` (Comando Principal)

Deve ser o comando mais robusto e seguro.

**Comportamento esperado:**

```bash
$ valen upgrade
[VALEN] Iniciando processo de upgrade...

→ Criando backup automático...
→ Atualizando repositório (git pull origin main)...
→ Atualizando dependências com uv...
→ Reiniciando serviço valen.service...
✅ Upgrade concluído com sucesso!
```

**Flags importantes:**
- `--dry-run` → Simula o upgrade sem executar nada
- `--no-backup` → Pula a criação de backup
- `--branch <nome>` → Permite escolher outra branch
- `--yes` → Pula confirmações

**Requisitos obrigatórios:**
- Backup automático antes de qualquer mudança
- Detecção do caminho do VALEN (via config ou detecção automática)
- Integração com systemd (reiniciar serviço se existir)
- Mostrar últimos commits aplicados
- Tratamento de erros com rollback ou mensagens claras

### 4.2 `valen install`

- Clona o repositório do GitHub
- Pergunta o local de instalação (ou usa padrão)
- Instala dependências
- Cria arquivo de configuração apontando para a instalação
- (Opcional) Configura serviço systemd

### 4.3 `valen status`

Mostra informações úteis:
- Caminho da instalação do VALEN
- Versão / último commit
- Status do Git (dirty ou clean)
- Status do serviço systemd
- Versão da CLI
- Espaço em disco usado

### 4.4 `valen update-deps`

- Apenas atualiza as dependências do projeto VALEN (sem fazer `git pull`)

### 4.5 `valen backup`

- Cria backup manual da instalação atual com timestamp

### 4.6 `valen uninstall`

- Remove o VALEN de forma controlada
- Remove serviço systemd (se existir)
- Mantém ou remove backups (perguntar ao usuário)

### 4.7 `valen doctor` (Bônus)

Comando que verifica a saúde da instalação:
- Verifica se o caminho do VALEN existe
- Verifica se as dependências estão instaladas
- Verifica se o serviço systemd está ativo
- Verifica permissões
- Sugere correções

---

## 5. Requisitos de Empacotamento (pip install)

A CLI deve ser um pacote Python instalável:

- `pyproject.toml` bem configurado
- Entry point para o comando `valen`
- Suporte a `pip install -e .` (desenvolvimento)
- Suporte a `pip install valen-cli` (produção)
- Versão semântica

Exemplo de `pyproject.toml` mínimo:

```toml
[project]
name = "valen-cli"
version = "0.1.0"
dependencies = ["typer[all]", "rich", "tomli"]

[project.scripts]
valen = "valen.cli:app"
```

---

## 6. Sistema de Configuração

A CLI deve usar um arquivo de configuração (recomendado: `~/.config/valen/config.toml`).

Exemplo de configuração:

```toml
[paths]
valen_dir = "/home/ubuntu/valen"

[git]
default_branch = "main"

[systemd]
service_name = "valen"
```

---

## 7. Requisitos de Qualidade e Segurança

- Uso pesado de **Rich** para output profissional
- Confirmações em ações destrutivas
- Backup automático antes de `upgrade` e `uninstall`
- Tratamento de erros claro
- Logs (opcional: salvar em arquivo)
- Suporte a `--yes` para automação
- Código limpo, com type hints e boa organização

---

## 8. Estilo de Output (Rich)

Use Rich para criar uma experiência premium:

- Painéis coloridos
- Tabelas
- Barras de progresso (quando aplicável)
- Ícones e emojis moderados
- Mensagens de sucesso/erro bem formatadas

Exemplo de estilo desejado:

```bash
[bold cyan]VALEN Upgrade[/bold cyan]
────────────────────────────────────
→ Fazendo backup...
→ Git pull concluído
✅ Upgrade finalizado com sucesso
```

---

## 9. Instruções Finais para Geração

Gere o projeto completo com:

1. Todos os arquivos de código necessários
2. `pyproject.toml` funcional
3. `README.md` bem escrito com exemplos de instalação e uso
4. Foco especial na qualidade e segurança do comando `valen upgrade`
5. Código limpo, modular e pronto para produção

O resultado final deve ser uma CLI que o usuário possa instalar com:

```bash
pip install valen-cli
```

E usar imediatamente no seu servidor Ubuntu VPS.

---

**Fim do Prompt**

Copie todo este conteúdo e cole no Claude Code.