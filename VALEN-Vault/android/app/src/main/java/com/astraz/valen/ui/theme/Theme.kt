// =====================================================================
//  VALEN ANDROID — Tema escuro estilo terminal (Claude Code vibes)
// =====================================================================
package com.astraz.valen.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.sp

// Paleta terminal: fundo grafite, acento magenta (identidade do Valen)
val FundoTerminal = Color(0xFF0D1117)
val FundoPainel = Color(0xFF161B22)
val BordaPainel = Color(0xFF30363D)
val TextoTerminal = Color(0xFFE6EDF3)
val MagentaValen = Color(0xFFD2A8FF)
val VerdeOk = Color(0xFF3FB950)
val AmareloAviso = Color(0xFFD29922)
val VermelhoErro = Color(0xFFF85149)

private val EsquemaEscuro = darkColorScheme(
    primary = MagentaValen,
    background = FundoTerminal,
    surface = FundoPainel,
    onPrimary = FundoTerminal,
    onBackground = TextoTerminal,
    onSurface = TextoTerminal,
    error = VermelhoErro,
)

// Tudo monoespaçado — o app é um espelho do terminal da Oracle
private val TipografiaMono = Typography(
    bodyLarge = TextStyle(fontFamily = FontFamily.Monospace, fontSize = 14.sp),
    bodyMedium = TextStyle(fontFamily = FontFamily.Monospace, fontSize = 13.sp),
    bodySmall = TextStyle(fontFamily = FontFamily.Monospace, fontSize = 11.sp),
    titleLarge = TextStyle(fontFamily = FontFamily.Monospace, fontSize = 20.sp),
    titleMedium = TextStyle(fontFamily = FontFamily.Monospace, fontSize = 16.sp),
    labelLarge = TextStyle(fontFamily = FontFamily.Monospace, fontSize = 14.sp),
)

@Composable
fun ValenTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = EsquemaEscuro,   // sempre escuro: terminal não tem modo claro
        typography = TipografiaMono,
        content = content,
    )
}
