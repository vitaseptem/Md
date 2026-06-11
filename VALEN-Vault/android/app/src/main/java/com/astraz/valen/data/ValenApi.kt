// =====================================================================
//  VALEN ANDROID — Cliente Retrofit (fala com o Brain na Contabo)
//
//  >>> O IP/porta do servidor são definidos na tela de login <<<
//  (pré-preenchidos pelo BuildConfig.DEFAULT_SERVER_IP / _PORT,
//   configurados em app/build.gradle.kts)
// =====================================================================
package com.astraz.valen.data

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.POST
import java.util.concurrent.TimeUnit

interface ValenApi {

    @POST("auth/login")
    suspend fun login(@Body req: LoginRequest): LoginResponse

    @POST("api/valen/v1/chat")
    suspend fun chat(
        @Header("Authorization") bearer: String,   // "Bearer <jwt>"
        @Body req: ChatRequest,
    ): ChatResponse

    companion object {
        /**
         * Cria o cliente apontando para o servidor (IP ou domínio).
         * Porta 443 -> https:// (Nginx/TLS na frente do Brain);
         * qualquer outra porta -> http:// (rede interna/Tailscale).
         * Timeout generoso: o Llama 3 70B pode levar minutos em CPU.
         */
        fun criar(serverIp: String, serverPort: String): ValenApi {
            val esquema = if (serverPort == "443") "https" else "http"
            val http = OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(600, TimeUnit.SECONDS)    // espera o Especialista Supremo
                .writeTimeout(60, TimeUnit.SECONDS)
                .addInterceptor(
                    HttpLoggingInterceptor().apply {
                        level = HttpLoggingInterceptor.Level.BASIC
                    }
                )
                .build()

            return Retrofit.Builder()
                .baseUrl("$esquema://$serverIp:$serverPort/")
                .client(http)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(ValenApi::class.java)
        }
    }
}
