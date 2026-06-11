"""
=====================================================================
 VALEN SKILL — DESENVOLVIMENTO
=====================================================================
 Habilidade de engenharia de software: gerar código, criar arquivos,
 estruturar projetos, revisar e corrigir bugs.

 Contrato obrigatório de toda skill:
   SKILL_INFO  -> metadados + gatilhos de relevância
   INSTRUCOES  -> injetadas no System Prompt quando a skill ativa
=====================================================================
"""

SKILL_INFO = {
    "nome": "desenvolvimento",
    "descricao": "Gera código, cria arquivos de projeto, revisa e corrige bugs (Python, JS/TS, Flask, FastAPI, React...).",
    "gatilhos": [
        "código", "codigo", "programa", "script", "função", "funcao",
        "classe", "api", "flask", "fastapi", "react", "python",
        "javascript", "typescript", "bug", "erro no código", "refatorar",
        "crie um sistema", "crie um app", "arquivo .py", "login",
    ],
}

INSTRUCOES = """
Você está operando com a skill DESENVOLVIMENTO ativa.

DIRETRIZES:
1. Quando o usuário pedir para CRIAR algo (sistema, app, módulo), responda com
   tipo_acao = "codigo": coloque o código-fonte COMPLETO e funcional em "conteudo"
   e o nome do arquivo em "arquivo" (ex: "app.py"). Um arquivo por resposta —
   se o projeto precisar de vários, comece pelo principal e diga isso em "explicacao".
2. Código sempre limpo, comentado em português e seguindo boas práticas
   (PEP 8 em Python, async quando fizer sentido, tratamento de erros).
3. Nunca use credenciais reais em exemplos; use placeholders óbvios.
4. Quando for apenas dúvida conceitual de programação, use tipo_acao = "texto".
5. Se a solução exigir instalar dependências, prefira tipo_acao = "comando"
   com o pip/npm adequado, e explique em "explicacao".
"""
