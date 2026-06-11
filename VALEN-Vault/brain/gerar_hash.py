#!/usr/bin/env python3
"""
=====================================================================
 VALEN — GERADOR DE HASH DE SENHA DO ADMIN
=====================================================================
 USO:
   python gerar_hash.py "minha-senha-forte"

 Cole a saída em VALEN_ADMIN_PASSWORD_HASH no arquivo .env da Contabo.
 A senha em texto puro NUNCA é armazenada em lugar nenhum.
=====================================================================
"""

import getpass
import sys

from auth import gerar_hash_senha

if __name__ == "__main__":
    if len(sys.argv) > 1:
        senha = sys.argv[1]
    else:
        senha = getpass.getpass("Senha do Admin (não aparece na tela): ")
        confirma = getpass.getpass("Repita a senha: ")
        if senha != confirma:
            print("✗ As senhas não conferem.", file=sys.stderr)
            sys.exit(1)

    if len(senha) < 8:
        print("✗ Use uma senha com pelo menos 8 caracteres.", file=sys.stderr)
        sys.exit(1)

    print("\nAdicione esta linha ao seu .env:\n")
    print(f"VALEN_ADMIN_PASSWORD_HASH={gerar_hash_senha(senha)}")
