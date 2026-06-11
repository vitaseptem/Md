// =====================================================================
//  VALEN ANDROID — Tela de Login Única (Admin Master)
//  Sem cadastro: apenas o usuário único do .env do servidor loga.
//  IP/porta pré-preenchidos pelo BuildConfig (app/build.gradle.kts).
// =====================================================================
package com.astraz.valen.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.astraz.valen.BuildConfig
import com.astraz.valen.ChatViewModel
import com.astraz.valen.ui.theme.MagentaValen
import com.astraz.valen.ui.theme.VermelhoErro

@Composable
fun LoginScreen(vm: ChatViewModel, ipSalvo: String?, portaSalva: String?) {
    var ip by remember { mutableStateOf(ipSalvo ?: BuildConfig.DEFAULT_SERVER_IP) }
    var porta by remember { mutableStateOf(portaSalva ?: BuildConfig.DEFAULT_SERVER_PORT) }
    var usuario by remember { mutableStateOf("") }
    var senha by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Text("VALEN", style = MaterialTheme.typography.titleLarge, color = MagentaValen)
        Text("// acesso restrito ao Admin Master", style = MaterialTheme.typography.bodySmall)
        Spacer(Modifier.height(32.dp))

        // Endereço do cérebro (Contabo) — editável caso o IP mude
        Row(Modifier.fillMaxWidth()) {
            OutlinedTextField(
                value = ip, onValueChange = { ip = it },
                label = { Text("IP do servidor") },
                singleLine = true,
                modifier = Modifier.weight(2f),
            )
            Spacer(Modifier.width(8.dp))
            OutlinedTextField(
                value = porta, onValueChange = { porta = it },
                label = { Text("Porta") },
                singleLine = true,
                modifier = Modifier.weight(1f),
            )
        }
        Spacer(Modifier.height(8.dp))

        OutlinedTextField(
            value = usuario, onValueChange = { usuario = it },
            label = { Text("Usuário") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
        )
        Spacer(Modifier.height(8.dp))

        OutlinedTextField(
            value = senha, onValueChange = { senha = it },
            label = { Text("Senha") },
            singleLine = true,
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth(),
        )
        Spacer(Modifier.height(24.dp))

        if (vm.carregando) {
            CircularProgressIndicator(color = MagentaValen)
        } else {
            Button(
                onClick = { vm.login(ip.trim(), porta.trim(), usuario.trim(), senha) },
                enabled = ip.isNotBlank() && usuario.isNotBlank() && senha.isNotBlank(),
                modifier = Modifier.fillMaxWidth(),
            ) {
                Text("ENTRAR")
            }
        }

        vm.erro?.let {
            Spacer(Modifier.height(16.dp))
            Text(it, color = VermelhoErro, style = MaterialTheme.typography.bodySmall)
        }
    }
}
