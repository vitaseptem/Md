// =====================================================================
//  VALEN ANDROID — Tela de Chat (espelho do terminal da Oracle)
//    - Estilo terminal: fundo escuro, fonte mono, Markdown renderizado
//    - Modal Visual de Confirmação: comandos/códigos vindos do Brain
//      TRAVAM a tela até o usuário decidir:
//        CONFIRMAR EXECUÇÃO -> envia 'y' nos bastidores
//        CANCELAR           -> envia 'n' nos bastidores
// =====================================================================
package com.astraz.valen.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.astraz.valen.ChatViewModel
import com.astraz.valen.data.ChatResponse
import com.astraz.valen.data.MensagemChat
import com.astraz.valen.ui.theme.AmareloAviso
import com.astraz.valen.ui.theme.BordaPainel
import com.astraz.valen.ui.theme.FundoPainel
import com.astraz.valen.ui.theme.MagentaValen
import com.astraz.valen.ui.theme.VerdeOk
import com.astraz.valen.ui.theme.VermelhoErro
import dev.jeziellago.compose.markdowntext.MarkdownText

@Composable
fun ChatScreen(vm: ChatViewModel) {
    var entrada by remember { mutableStateOf("") }
    val listaState = rememberLazyListState()

    // Auto-scroll para a última mensagem
    LaunchedEffect(vm.mensagens.size) {
        if (vm.mensagens.isNotEmpty()) listaState.animateScrollToItem(vm.mensagens.size - 1)
    }

    Column(
        Modifier
            .fillMaxSize()
            .imePadding()
            .padding(12.dp)
    ) {
        // ---------- Cabeçalho estilo prompt ----------
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("valen@contabo:~$", color = VerdeOk, style = MaterialTheme.typography.bodyMedium)
            Spacer(Modifier.weight(1f))
            IconButton(onClick = { vm.logout() }) {
                Text("⏻", color = VermelhoErro)
            }
        }

        // ---------- Histórico da conversa ----------
        LazyColumn(
            state = listaState,
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            items(vm.mensagens) { msg -> BalaoMensagem(msg) }
        }

        vm.erro?.let {
            Text(it, color = VermelhoErro, style = MaterialTheme.typography.bodySmall)
        }
        if (vm.carregando) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                CircularProgressIndicator(
                    Modifier.height(16.dp).width(16.dp),
                    color = MagentaValen, strokeWidth = 2.dp,
                )
                Spacer(Modifier.width(8.dp))
                Text("valen pensando...", style = MaterialTheme.typography.bodySmall)
            }
        }

        // ---------- Entrada ----------
        Row(verticalAlignment = Alignment.CenterVertically) {
            OutlinedTextField(
                value = entrada,
                onValueChange = { entrada = it },
                placeholder = { Text("❯ digite sua ordem...") },
                modifier = Modifier.weight(1f),
                maxLines = 4,
            )
            Spacer(Modifier.width(8.dp))
            Button(
                onClick = { vm.enviar(entrada); entrada = "" },
                enabled = entrada.isNotBlank() && !vm.carregando,
            ) {
                Text("➤")
            }
        }
    }

    // ---------- MODAL DE CONFIRMAÇÃO (trava a tela) ----------
    vm.acaoPendente?.let { acao ->
        ModalConfirmacao(
            acao = acao,
            onConfirmar = { vm.confirmarAcao() },   // envia 'y'
            onCancelar = { vm.cancelarAcao() },     // envia 'n'
        )
    }
}

@Composable
private fun BalaoMensagem(msg: MensagemChat) {
    Surface(
        color = if (msg.deUsuario) FundoPainel else MaterialTheme.colorScheme.background,
        shape = RoundedCornerShape(6.dp),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(Modifier.padding(10.dp)) {
            // Linha de identificação: quem fala + skill + modelo do conselho
            val cabecalho = if (msg.deUsuario) "❯ você"
                else "🤖 valen [${msg.skill ?: "geral"} | ${msg.modelo ?: "?"}]"
            Text(
                cabecalho,
                color = if (msg.deUsuario) VerdeOk else MagentaValen,
                style = MaterialTheme.typography.bodySmall,
            )
            Spacer(Modifier.height(4.dp))
            // Markdown para respostas do Valen; texto cru para o usuário
            if (msg.deUsuario) {
                Text(msg.texto, style = MaterialTheme.typography.bodyMedium)
            } else {
                MarkdownText(
                    markdown = msg.texto,
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
    }
}

@Composable
private fun ModalConfirmacao(
    acao: ChatResponse,
    onConfirmar: () -> Unit,
    onCancelar: () -> Unit,
) {
    val titulo = if (acao.tipoAcao == "comando") "⚡ EXECUTAR COMANDO NA VPS?"
                 else "📄 GRAVAR ARQUIVO NA VPS?"

    AlertDialog(
        onDismissRequest = { /* trava: só sai pelos botões */ },
        containerColor = FundoPainel,
        title = { Text(titulo, color = AmareloAviso, style = MaterialTheme.typography.titleMedium) },
        text = {
            Column(Modifier.verticalScroll(rememberScrollState())) {
                Text(
                    "skill: ${acao.skillUtilizada}  |  modelo: ${acao.modeloUtilizado}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MagentaValen,
                )
                acao.arquivo?.let {
                    Text("arquivo: $it", style = MaterialTheme.typography.bodySmall)
                }
                Spacer(Modifier.height(8.dp))
                // Conteúdo do comando/código em "bloco de terminal"
                Surface(
                    color = MaterialTheme.colorScheme.background,
                    shape = RoundedCornerShape(4.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(BordaPainel),
                ) {
                    Text(
                        acao.conteudo,
                        style = MaterialTheme.typography.bodySmall,
                        modifier = Modifier.padding(8.dp),
                    )
                }
                acao.explicacao?.let {
                    Spacer(Modifier.height(8.dp))
                    Text(it, style = MaterialTheme.typography.bodySmall)
                }
            }
        },
        confirmButton = {
            Button(
                onClick = onConfirmar,
                colors = ButtonDefaults.buttonColors(containerColor = VerdeOk),
            ) {
                Text("CONFIRMAR EXECUÇÃO")
            }
        },
        dismissButton = {
            OutlinedButton(onClick = onCancelar) {
                Text("CANCELAR", color = VermelhoErro)
            }
        },
    )
}
