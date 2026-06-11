// =====================================================================
//  VALEN ANDROID — Modelos de dados (contrato JSON com o Brain)
//  Espelham exatamente os modelos Pydantic do servidor FastAPI.
// =====================================================================
package com.astraz.valen.data

import com.google.gson.annotations.SerializedName

// ---------- /auth/login ----------
data class LoginRequest(
    @SerializedName("usuario") val usuario: String,
    @SerializedName("senha") val senha: String,
)

data class LoginResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("token_type") val tokenType: String,
    @SerializedName("expira_em") val expiraEm: String,
)

// ---------- /api/valen/v1/chat ----------
data class ChatRequest(
    @SerializedName("mensagem") val mensagem: String,
    @SerializedName("contexto") val contexto: String? = null,
)

data class ChatResponse(
    @SerializedName("skill_utilizada") val skillUtilizada: String,
    @SerializedName("modelo_utilizado") val modeloUtilizado: String,
    @SerializedName("tipo_acao") val tipoAcao: String,     // "texto" | "comando" | "codigo"
    @SerializedName("conteudo") val conteudo: String,
    @SerializedName("arquivo") val arquivo: String?,
    @SerializedName("explicacao") val explicacao: String?,
    // Presente quando comando/codigo aguarda o modal — id da ação na mini-api
    @SerializedName("acao_id") val acaoId: String? = null,
)

// ---------- /api/valen/v1/confirmar (mini-api Oracle) ----------
data class ConfirmarRequest(
    @SerializedName("acao_id") val acaoId: String,
    @SerializedName("decisao") val decisao: String,        // "y" confirma | "n" cancela
)

data class ExecucaoResponse(
    @SerializedName("executado") val executado: Boolean,
    @SerializedName("saida") val saida: String,            // stdout+stderr ou caminho do arquivo
    @SerializedName("codigo_retorno") val codigoRetorno: Int,
)

// ---------- Estado da conversa na UI ----------
data class MensagemChat(
    val deUsuario: Boolean,
    val texto: String,
    val skill: String? = null,
    val modelo: String? = null,
    val tipoAcao: String = "texto",
)
