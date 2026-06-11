// =====================================================================
//  VALEN ANDROID — Cofre local do JWT (EncryptedSharedPreferences)
//  O token e o endereço do servidor ficam cifrados com chave do
//  Android Keystore — nem backup nem outros apps conseguem ler.
// =====================================================================
package com.astraz.valen.data

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class TokenStore(context: Context) {

    private val prefs: SharedPreferences

    init {
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()

        prefs = EncryptedSharedPreferences.create(
            context,
            "valen_secure_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
        )
    }

    var token: String?
        get() = prefs.getString(KEY_TOKEN, null)
        set(value) = prefs.edit().putString(KEY_TOKEN, value).apply()

    var serverIp: String?
        get() = prefs.getString(KEY_SERVER_IP, null)
        set(value) = prefs.edit().putString(KEY_SERVER_IP, value).apply()

    var serverPort: String?
        get() = prefs.getString(KEY_SERVER_PORT, null)
        set(value) = prefs.edit().putString(KEY_SERVER_PORT, value).apply()

    /** true quando já existe sessão salva — o app abre direto no chat. */
    fun temSessao(): Boolean = !token.isNullOrBlank() && !serverIp.isNullOrBlank()

    /** Logout: apaga token e mantém IP/porta para facilitar o relogin. */
    fun limparToken() = prefs.edit().remove(KEY_TOKEN).apply()

    private companion object {
        const val KEY_TOKEN = "jwt_token"
        const val KEY_SERVER_IP = "server_ip"
        const val KEY_SERVER_PORT = "server_port"
    }
}
