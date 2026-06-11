# 📱 Deploy do App — Android (Kotlin/Jetpack Compose)

Controle remoto / espelho do terminal. Projeto em `android/`.

## 1. Configurar o servidor (IP e porta)

Edite **`android/app/build.gradle.kts`**:

```kotlin
// >>> CONFIGURE AQUI O SERVIDOR <<<
buildConfigField("String", "DEFAULT_SERVER_IP", "\"valen-chat.astrazstudio.com.br\"")
buildConfigField("String", "DEFAULT_SERVER_PORT", "\"443\"")
```

São só os valores **pré-preenchidos** — a tela de login permite trocar
host/porta sem recompilar. Regra de esquema: porta `443` → `https://`
(Nginx/TLS na frente); qualquer outra porta → `http://`.

Alternativas de conexão:
- **Domínio + TLS** (produção): `valen-chat.astrazstudio.com.br` porta `443`
- **Tailscale** (sem expor porta pública): IP da tailnet da VPS, porta `8777`
- **IP direto** (teste): IP público, porta `8777` (exige liberar firewall)

## 2. Compilar

Opção A — Android Studio: abra a pasta `android/`, aguarde o Gradle sync,
`Run ▶` num device/emulador (minSdk 26).

Opção B — linha de comando:

```bash
cd android
# gere o wrapper uma vez (precisa de Gradle 8.7+ instalado):
gradle wrapper --gradle-version 8.7
./gradlew assembleDebug
# APK em: app/build/outputs/apk/debug/app-debug.apk
adb install app/build/outputs/apk/debug/app-debug.apk
```

## 3. Fluxo do app

1. **Login único** (Admin Master): usuário + senha → `POST /auth/login` →
   JWT salvo via `EncryptedSharedPreferences` (cifrado pelo Android Keystore).
   Nas próximas aberturas o app vai **direto ao chat**.
2. **Chat estilo terminal**: tema escuro, fonte monoespaçada, Markdown
   renderizado, cabeçalho mostra `skill | modelo` do conselho que respondeu.
3. **Modal de Confirmação**: se a resposta for `tipo_acao: "comando"` ou
   `"codigo"`, a tela **trava** com o modal:
   - **CONFIRMAR EXECUÇÃO** → envia `y` nos bastidores
   - **CANCELAR** → envia `n` nos bastidores
4. Token expirado (HTTP 401) → app volta sozinho para a tela de login.

## 4. Rede e segurança

- O manifest usa `usesCleartextTraffic=true` porque o Brain expõe HTTP puro
  na 8777. **Em produção**: coloque Nginx/Traefik com TLS na frente,
  aponte o app para `https://` e remova a flag.
- Celular fora da rede liberada no firewall da Contabo? Use VPN
  (WireGuard/Tailscale) — não abra a 8777 para o mundo.

## 5. Estrutura do código

```
android/app/src/main/java/com/astraz/valen/
├── MainActivity.kt          # roteia: sessão salva? chat : login
├── ChatViewModel.kt         # estado, login, chat, interceptação de ações
├── data/
│   ├── Models.kt            # contrato JSON (espelha o Pydantic do Brain)
│   ├── ValenApi.kt          # Retrofit (timeout 600s p/ o 70B)
│   └── TokenStore.kt        # EncryptedSharedPreferences (JWT cifrado)
└── ui/
    ├── LoginScreen.kt       # tela única do Admin Master
    ├── ChatScreen.kt        # terminal + modal de confirmação
    └── theme/Theme.kt       # tema escuro mono (Claude Code vibes)
```
