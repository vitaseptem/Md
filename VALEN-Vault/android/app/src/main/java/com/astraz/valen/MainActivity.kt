// =====================================================================
//  VALEN ANDROID — MainActivity
//  Roteamento simples: com sessão salva (JWT cifrado) abre direto no
//  chat; sem sessão, mostra a Tela de Login Única do Admin Master.
// =====================================================================
package com.astraz.valen

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import com.astraz.valen.data.TokenStore
import com.astraz.valen.ui.ChatScreen
import com.astraz.valen.ui.LoginScreen
import com.astraz.valen.ui.theme.ValenTheme

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val store = TokenStore(applicationContext)

        setContent {
            ValenTheme {
                Surface(Modifier.fillMaxSize()) {
                    val vm: ChatViewModel = viewModel(factory = fabrica(store))
                    if (vm.logado) {
                        ChatScreen(vm)
                    } else {
                        LoginScreen(vm, ipSalvo = store.serverIp, portaSalva = store.serverPort)
                    }
                }
            }
        }
    }

    /** Factory mínima: injeta o TokenStore no ViewModel sem libs de DI. */
    private fun fabrica(store: TokenStore) = object : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T =
            ChatViewModel(store) as T
    }
}
