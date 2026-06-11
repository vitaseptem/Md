// =====================================================================
//  VALEN ANDROID — ViewModel do Chat (Modo Espelho / Controle Remoto)
//
//  Fluxo do Modal de Confirmação:
//    1. Resposta chega do Brain com tipo_acao "comando" ou "codigo".
//    2. O ViewModel NÃO exibe direto: guarda em `acaoPendente` e a
//       tela trava com o modal CONFIRMAR EXECUÇÃO / CANCELAR.
//    3. Confirmar -> envia 'y' nos bastidores (como faria no terminal
//       da Oracle); Cancelar -> envia 'n'. O ecossistema decide o resto.
// =====================================================================
package com.astraz.valen

import android.os.Build
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateListOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.astraz.valen.data.ChatRequest
import com.astraz.valen.data.ChatResponse
import com.astraz.valen.data.ConfirmarRequest
import com.astraz.valen.data.LoginRequest
import com.astraz.valen.data.MensagemChat
import com.astraz.valen.data.TokenStore
import com.astraz.valen.data.ValenApi
import kotlinx.coroutines.launch
import retrofit2.HttpException

class ChatViewModel(private val store: TokenStore) : ViewModel() {

    // ---------------- Estado observado pelas telas ----------------
    val mensagens = mutableStateListOf<MensagemChat>()
    var carregando by mutableStateOf(false)
        private set
    var erro by mutableStateOf<String?>(null)
        private set
    var logado by mutableStateOf(store.temSessao())
        private set

    /** Ação interceptada aguardando o modal (comando/código do servidor). */
    var acaoPendente by mutableStateOf<ChatResponse?>(null)
        private set

    private var api: ValenApi? = recriarApi()

    private fun recriarApi(): ValenApi? {
        val ip = store.serverIp ?: return null
        return ValenApi.criar(ip, store.serverPort ?: "8777")
    }

    private fun bearer() = "Bearer ${store.token.orEmpty()}"

    /** Contexto enviado ao Brain: identifica que a ordem veio do celular. */
    private fun contexto() =
        "origem: app Android (${Build.MODEL}) | papel: controle remoto do ecossistema Valen | " +
        "execução destinada à VPS Oracle"

    // ---------------- LOGIN (usuário único / Admin Master) ----------------
    fun login(ip: String, porta: String, usuario: String, senha: String) {
        viewModelScope.launch {
            carregando = true
            erro = null
            try {
                val novaApi = ValenApi.criar(ip, porta)
                val resp = novaApi.login(LoginRequest(usuario, senha))
                // Sessão persistida cifrada — próximas aberturas vão direto ao chat
                store.serverIp = ip
                store.serverPort = porta
                store.token = resp.accessToken
                api = novaApi
                logado = true
            } catch (e: HttpException) {
                erro = if (e.code() == 401) "Usuário ou senha incorretos."
                       else "Servidor recusou o login (HTTP ${e.code()})."
            } catch (e: Exception) {
                erro = "Não consegui falar com o servidor: ${e.message}"
            } finally {
                carregando = false
            }
        }
    }

    fun logout() {
        store.limparToken()
        logado = false
        mensagens.clear()
        acaoPendente = null
    }

    // ---------------- CHAT ----------------
    fun enviar(texto: String) {
        val msg = texto.trim()
        if (msg.isEmpty() || carregando) return
        mensagens.add(MensagemChat(deUsuario = true, texto = msg))
        enviarAoBrain(msg)
    }

    /**
     * Botão CONFIRMAR EXECUÇÃO do modal: envia 'y' à mini-api da Oracle,
     * que executa o comando/grava o arquivo NA VPS e devolve a saída.
     */
    fun confirmarAcao() = resolverAcao("y")

    /** Botão CANCELAR do modal: envia 'n' — a mini-api descarta a ação. */
    fun cancelarAcao() = resolverAcao("n")

    private fun resolverAcao(decisao: String) {
        val acao = acaoPendente ?: return
        acaoPendente = null
        val id = acao.acaoId
        if (id == null) {
            // Sem id (resposta antiga/brain direto): nada a executar remotamente
            mensagens.add(
                MensagemChat(
                    deUsuario = false,
                    texto = "⚠ Ação sem id de execução — nada foi enviado.\n\n```\n${acao.conteudo}\n```",
                    skill = acao.skillUtilizada,
                    modelo = acao.modeloUtilizado,
                )
            )
            return
        }
        val apiAtual = api ?: run { erro = "Sessão inválida — faça login."; return }
        viewModelScope.launch {
            carregando = true
            erro = null
            try {
                val res = apiAtual.confirmar(bearer(), ConfirmarRequest(id, decisao))
                val texto = if (!res.executado) {
                    "⛔ Ação cancelada.\n\n```\n${acao.conteudo}\n```"
                } else {
                    val status = if (res.codigoRetorno == 0) "✔ concluído (rc=0)"
                                 else "✗ saiu com rc=${res.codigoRetorno}"
                    "⚡ Executado na VPS — $status\n\n```\n${res.saida}\n```"
                }
                mensagens.add(
                    MensagemChat(
                        deUsuario = false,
                        texto = texto,
                        skill = acao.skillUtilizada,
                        modelo = acao.modeloUtilizado,
                    )
                )
            } catch (e: HttpException) {
                erro = if (e.code() == 401) { logout(); "Sessão expirada — faça login novamente." }
                       else "Erro ao resolver ação (HTTP ${e.code()})."
            } catch (e: Exception) {
                erro = "Falha de rede: ${e.message}"
            } finally {
                carregando = false
            }
        }
    }

    private fun enviarAoBrain(mensagem: String) {
        val apiAtual = api ?: run { erro = "Sessão inválida — faça login."; return }
        viewModelScope.launch {
            carregando = true
            erro = null
            try {
                val resp = apiAtual.chat(bearer(), ChatRequest(mensagem, contexto()))
                when (resp.tipoAcao) {
                    // Comando ou gravação de arquivo na VPS: INTERCEPTA e
                    // trava a tela com o modal — nada executa sem 'y' explícito.
                    "comando", "codigo" -> acaoPendente = resp
                    else -> mensagens.add(
                        MensagemChat(
                            deUsuario = false,
                            texto = resp.conteudo,
                            skill = resp.skillUtilizada,
                            modelo = resp.modeloUtilizado,
                            tipoAcao = resp.tipoAcao,
                        )
                    )
                }
            } catch (e: HttpException) {
                if (e.code() == 401) {
                    // JWT expirou: derruba a sessão e volta para o login
                    erro = "Sessão expirada — faça login novamente."
                    logout()
                } else {
                    erro = "Erro do servidor (HTTP ${e.code()})."
                }
            } catch (e: Exception) {
                erro = "Falha de rede: ${e.message}"
            } finally {
                carregando = false
            }
        }
    }
}
