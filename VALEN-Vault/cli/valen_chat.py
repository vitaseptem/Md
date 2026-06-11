#!/usr/bin/env python3
"""
=====================================================================
 VALEN CLI — INTERFACE DE TERMINAL (roda na VPS ORACLE)
=====================================================================
 Chat interativo estilo Claude Code para conversar com o cérebro do
 Valen (FastAPI + Llama 3 70B na Contabo).

 MODOS DE USO:
   valen-chat                       -> abre o chat interativo (REPL)
   valen-chat "crie um login..."    -> modo one-shot (pergunta única)
   valen-chat login                 -> (re)faz a autenticação
   valen-chat logout                -> apaga o token local

 COMANDOS DENTRO DO CHAT:
   /skills   lista as skills disponíveis no servidor
   /login    refaz a autenticação
   /limpar   limpa a tela
   /ajuda    mostra a ajuda
   /sair     encerra o chat (ou Ctrl+D / Ctrl+C)

 AUTENTICAÇÃO:
   No primeiro uso, a CLI pergunta IP/porta do servidor, usuário e
   senha do Admin, troca por um JWT no /auth/login e guarda tudo em
   ~/.config/valen/config.json (permissão 600, só seu usuário lê).

 INSTALAÇÃO NA ORACLE:
   pip install requests rich
   chmod +x valen_chat.py
   sudo ln -sf "$(pwd)/valen_chat.py" /usr/local/bin/valen-chat
=====================================================================
"""

import getpass
import json
import os
import platform
import readline  # noqa: F401 — habilita histórico/edição com setas no input()
import stat
import subprocess
import sys
from pathlib import Path

import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

# ===============================================================
# CONFIGURAÇÃO
#   IP/porta do servidor (Contabo) são pedidos no primeiro login e
#   salvos em ~/.config/valen/config.json. Para trocar depois:
#   rode `valen-chat login` ou edite o arquivo diretamente.
#   Variáveis de ambiente têm prioridade sobre o arquivo salvo.
# ===============================================================
CONFIG_DIR = Path.home() / ".config" / "valen"
CONFIG_FILE = CONFIG_DIR / "config.json"
VALEN_TIMEOUT = int(os.getenv("VALEN_TIMEOUT", "600"))  # Llama 70B pode demorar
PORTA_PADRAO = "8777"

console = Console()

BANNER = r"""
██╗   ██╗ █████╗ ██╗     ███████╗███╗   ██╗
██║   ██║██╔══██╗██║     ██╔════╝████╗  ██║
██║   ██║███████║██║     █████╗  ██╔██╗ ██║
╚██╗ ██╔╝██╔══██║██║     ██╔══╝  ██║╚██╗██║
 ╚████╔╝ ██║  ██║███████╗███████╗██║ ╚████║
  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝
"""


# ---------------------------------------------------------------
# CREDENCIAIS LOCAIS (~/.config/valen/config.json, modo 600)
# ---------------------------------------------------------------
def carregar_config() -> dict:
    """Lê a configuração local. Env vars sobrescrevem o arquivo."""
    cfg = {}
    if CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text())
        except json.JSONDecodeError:
            console.print("[bold yellow]⚠ config.json corrompido — será recriado no login.[/]")
    # Variáveis de ambiente têm prioridade (útil para scripts/CI)
    if os.getenv("VALEN_SERVER_IP"):
        cfg["server_ip"] = os.environ["VALEN_SERVER_IP"]
    if os.getenv("VALEN_SERVER_PORT"):
        cfg["server_port"] = os.environ["VALEN_SERVER_PORT"]
    if os.getenv("VALEN_TOKEN"):
        cfg["token"] = os.environ["VALEN_TOKEN"]
    return cfg


def salvar_config(cfg: dict) -> None:
    """Grava a configuração com permissão 600 (só o dono lê o token)."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))
    CONFIG_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 600


def base_url(cfg: dict) -> str:
    """Porta 443 -> https (domínio com TLS); demais portas -> http."""
    porta = cfg.get("server_port", PORTA_PADRAO)
    esquema = "https" if str(porta) == "443" else "http"
    return f"{esquema}://{cfg['server_ip']}:{porta}"


def headers(cfg: dict) -> dict:
    return {"Authorization": f"Bearer {cfg.get('token', '')}"}


# ---------------------------------------------------------------
# LOGIN — troca usuário/senha do Admin por um JWT de longa duração
# ---------------------------------------------------------------
def fazer_login(cfg: dict | None = None) -> dict | None:
    """Fluxo interativo de autenticação. Salva o JWT localmente."""
    cfg = dict(cfg or {})
    console.print(Panel("🔐 Autenticação no cérebro do Valen (Contabo)", border_style="magenta"))

    ip_atual = cfg.get("server_ip", "")
    porta_atual = cfg.get("server_port", PORTA_PADRAO)
    ip = console.input(f"[bold]IP do servidor[/] [{ip_atual or 'ex: 144.91.x.x'}]: ").strip() or ip_atual
    if not ip:
        console.print("[bold red]✗ IP do servidor é obrigatório.[/]")
        return None
    porta = console.input(f"[bold]Porta[/] [{porta_atual}]: ").strip() or porta_atual
    usuario = console.input("[bold]Usuário (Admin)[/]: ").strip()
    senha = getpass.getpass("Senha: ")

    cfg.update({"server_ip": ip, "server_port": porta})
    try:
        resp = requests.post(
            f"{base_url(cfg)}/auth/login",
            json={"usuario": usuario, "senha": senha},
            timeout=30,
        )
        if resp.status_code == 401:
            console.print("[bold red]✗ Usuário ou senha incorretos.[/]")
            return None
        resp.raise_for_status()
        dados = resp.json()
    except requests.RequestException as exc:
        console.print(f"[bold red]✗ Falha ao falar com o servidor:[/] {exc}")
        return None

    cfg["token"] = dados["access_token"]
    cfg["expira_em"] = dados.get("expira_em", "")
    salvar_config(cfg)
    console.print(f"[bold green]✔ Login OK.[/] Token salvo em {CONFIG_FILE} (expira: {cfg['expira_em']})")
    return cfg


def garantir_login(cfg: dict) -> dict | None:
    """Garante que existe token salvo; dispara o login se necessário."""
    if cfg.get("token") and cfg.get("server_ip"):
        return cfg
    console.print("[bold yellow]⚠ Nenhum token salvo — vamos fazer login primeiro.[/]")
    return fazer_login(cfg)


# ---------------------------------------------------------------
# COMUNICAÇÃO COM O CÉREBRO (Contabo)
# ---------------------------------------------------------------
def montar_contexto() -> str:
    """Contexto da máquina local enviado junto ao pedido (ajuda o Llama)."""
    return (
        f"sistema: {platform.system()} {platform.release()} | "
        f"diretório atual: {os.getcwd()} | usuário: {os.getenv('USER', '?')}"
    )


def perguntar_ao_valen(cfg: dict, mensagem: str) -> dict | None:
    """POST /chat no servidor central. Reloga automaticamente se o JWT expirou."""
    for tentativa in (1, 2):
        try:
            with console.status("[bold magenta]Valen pensando (Llama 3 70B)...", spinner="dots"):
                resp = requests.post(
                    f"{base_url(cfg)}/api/valen/v1/chat",
                    headers=headers(cfg),
                    json={"mensagem": mensagem, "contexto": montar_contexto()},
                    timeout=VALEN_TIMEOUT,
                )
            if resp.status_code == 401 and tentativa == 1:
                console.print("[bold yellow]⚠ Token expirado/rejeitado — refazendo login.[/]")
                novo = fazer_login(cfg)
                if not novo:
                    return None
                cfg.update(novo)
                continue
            if resp.status_code == 429:
                console.print("[bold yellow]⏳ Limite de requisições atingido. Aguarde um pouco.[/]")
                return None
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError:
            console.print(f"[bold red]✗ Não consegui falar com o cérebro em {base_url(cfg)}.[/]")
            console.print("[dim]Confira IP/porta e se o brain está de pé na Contabo.[/]")
            return None
        except requests.exceptions.Timeout:
            console.print("[bold red]✗ O Valen demorou demais para responder (timeout).[/]")
            return None
        except requests.RequestException as exc:
            console.print(f"[bold red]✗ Erro na requisição:[/] {exc}")
            return None
    return None


def listar_skills(cfg: dict) -> None:
    """GET /skills — mostra o catálogo de habilidades carregadas no servidor."""
    try:
        resp = requests.get(f"{base_url(cfg)}/api/valen/v1/skills", headers=headers(cfg), timeout=30)
        resp.raise_for_status()
        dados = resp.json()
        linhas = "\n".join(
            f"[bold cyan]• {s['nome']}[/] — {s['descricao']}" for s in dados["skills"]
        ) or "[dim]Nenhuma skill carregada.[/]"
        console.print(Panel(linhas, title=f"🧠 Skills do Valen ({dados['total']})", border_style="magenta"))
    except requests.RequestException as exc:
        console.print(f"[bold red]✗ Falha ao listar skills:[/] {exc}")


# ---------------------------------------------------------------
# EXECUÇÃO LOCAL DAS AÇÕES (com trava de segurança y/n)
# ---------------------------------------------------------------
def confirmar(pergunta: str) -> bool:
    """Trava de segurança: pergunta y/n antes de qualquer ação local."""
    resposta = console.input(f"[bold yellow]{pergunta} (y/n): [/]").strip().lower()
    return resposta in ("y", "yes", "s", "sim")


def executar_comando(resposta: dict) -> None:
    """tipo_acao == 'comando': mostra, pede autorização e roda via subprocess."""
    skill = resposta["skill_utilizada"]
    modelo = resposta.get("modelo_utilizado", "?")
    comando = resposta["conteudo"]

    console.print(Panel(
        Syntax(comando, "bash", theme="monokai", word_wrap=True),
        title=f"⚡ Valen [Skill: {skill} | Modelo: {modelo}] propõe executar",
        subtitle=resposta.get("explicacao") or "",
        border_style="yellow",
    ))

    if not confirmar(f"Valen [Skill: {skill}] deseja executar este comando. Confirmar?"):
        console.print("[dim]Ação cancelada pelo usuário.[/]")
        return

    # Execução em tempo real, com saída transmitida direto ao terminal
    console.rule("[dim]saída do comando[/]")
    resultado = subprocess.run(comando, shell=True)
    console.rule()
    if resultado.returncode == 0:
        console.print("[bold green]✔ Comando concluído com sucesso.[/]")
    else:
        console.print(f"[bold red]✗ Comando saiu com código {resultado.returncode}.[/]")


def criar_arquivo(resposta: dict) -> None:
    """tipo_acao == 'codigo': mostra o código, pede autorização e grava o arquivo."""
    skill = resposta["skill_utilizada"]
    modelo = resposta.get("modelo_utilizado", "?")
    codigo = resposta["conteudo"]
    nome = resposta.get("arquivo") or console.input(
        "[bold yellow]Nome do arquivo a criar: [/]"
    ).strip() or "valen_output.txt"

    # Realça a sintaxe conforme a extensão do arquivo
    extensao = Path(nome).suffix.lstrip(".") or "text"
    console.print(Panel(
        Syntax(codigo, extensao, theme="monokai", line_numbers=True, word_wrap=True),
        title=f"📄 Valen [Skill: {skill} | Modelo: {modelo}] propõe criar [bold]{nome}[/]",
        subtitle=resposta.get("explicacao") or "",
        border_style="cyan",
    ))

    if not confirmar(f"Valen [Skill: {skill}] deseja criar o arquivo {nome}. Confirmar?"):
        console.print("[dim]Ação cancelada pelo usuário.[/]")
        return

    destino = Path(nome).expanduser()
    if destino.exists() and not confirmar(f"⚠ {destino} já existe. Sobrescrever?"):
        console.print("[dim]Ação cancelada pelo usuário.[/]")
        return

    destino.parent.mkdir(parents=True, exist_ok=True)  # cria pastas intermediárias
    destino.write_text(codigo, encoding="utf-8")
    console.print(f"[bold green]✔ Arquivo criado:[/] {destino.resolve()}")


def exibir_texto(resposta: dict) -> None:
    """tipo_acao == 'texto': renderiza a resposta como Markdown num painel."""
    console.print(Panel(
        Markdown(resposta["conteudo"]),
        title=(
            f"🤖 Valen [Skill: {resposta['skill_utilizada']} | "
            f"Modelo: {resposta.get('modelo_utilizado', '?')}]"
        ),
        border_style="magenta",
    ))


def processar_resposta(resposta: dict) -> None:
    """Roteia a resposta estruturada do cérebro para o handler certo."""
    acoes = {"comando": executar_comando, "codigo": criar_arquivo, "texto": exibir_texto}
    acoes.get(resposta.get("tipo_acao", "texto"), exibir_texto)(resposta)


# ---------------------------------------------------------------
# CHAT INTERATIVO (REPL estilo Claude Code)
# ---------------------------------------------------------------
def mostrar_ajuda() -> None:
    console.print(Panel(
        "[bold cyan]/skills[/]  lista as habilidades do Valen\n"
        "[bold cyan]/login[/]   refaz a autenticação\n"
        "[bold cyan]/limpar[/]  limpa a tela\n"
        "[bold cyan]/ajuda[/]   mostra esta ajuda\n"
        "[bold cyan]/sair[/]    encerra o chat (Ctrl+D também)",
        title="❓ Ajuda", border_style="blue",
    ))


def chat_interativo(cfg: dict) -> None:
    """Loop principal do chat: prompt, comandos de barra e conversa."""
    console.print(Text(BANNER, style="bold magenta"))
    console.print("[bold]Valen[/] — seu assistente pessoal soberano. [dim](/ajuda para comandos)[/]")
    console.print(f"[dim]Cérebro: {base_url(cfg)}[/]\n")

    while True:
        try:
            entrada = console.input("[bold magenta]❯ [/]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Até logo, Davi. Valen desligando.[/]")
            break

        if not entrada:
            continue

        # Comandos de barra (locais, não vão para o servidor)
        if entrada in ("/sair", "/exit", "/quit"):
            console.print("[dim]Até logo, Davi. Valen desligando.[/]")
            break
        if entrada in ("/limpar", "/clear"):
            console.clear()
            continue
        if entrada in ("/ajuda", "/help"):
            mostrar_ajuda()
            continue
        if entrada == "/skills":
            listar_skills(cfg)
            continue
        if entrada == "/login":
            novo = fazer_login(cfg)
            if novo:
                cfg.update(novo)
            continue

        # Conversa normal: envia ao cérebro e processa a ação proposta
        resposta = perguntar_ao_valen(cfg, entrada)
        if resposta:
            processar_resposta(resposta)
        console.print()  # respiro visual entre turnos


# ---------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------
def main() -> None:
    cfg = carregar_config()

    # Subcomandos de gestão de sessão
    if len(sys.argv) > 1 and sys.argv[1] == "login":
        fazer_login(cfg)
        return
    if len(sys.argv) > 1 and sys.argv[1] == "logout":
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
            console.print("[bold green]✔ Token local apagado.[/]")
        else:
            console.print("[dim]Nenhum token salvo.[/]")
        return

    cfg = garantir_login(cfg)
    if not cfg:
        sys.exit(1)

    if len(sys.argv) > 1:
        # Modo one-shot:  valen-chat "crie um sistema de login em flask"
        resposta = perguntar_ao_valen(cfg, " ".join(sys.argv[1:]))
        if resposta:
            processar_resposta(resposta)
    else:
        # Sem argumentos: abre o chat interativo estilo Claude Code
        chat_interativo(cfg)


if __name__ == "__main__":
    main()
