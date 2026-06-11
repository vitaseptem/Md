// =====================================================================
//  VALEN ANDROID — app/build.gradle.kts
// =====================================================================
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.astraz.valen"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.astraz.valen"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"

        // ============================================================
        // >>> CONFIGURE AQUI O SERVIDOR <<<
        // Host e porta padrão pré-preenchidos na tela de login —
        // podem ser alterados pelo usuário na própria tela.
        // Aceita IP (ex: 100.69.239.8 via Tailscale) ou domínio.
        // Porta 443 -> o app usa https:// automaticamente.
        // ============================================================
        buildConfigField("String", "DEFAULT_SERVER_IP", "\"valen-chat.astrazstudio.com.br\"")
        buildConfigField("String", "DEFAULT_SERVER_PORT", "\"443\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

dependencies {
    // Compose BOM — versões alinhadas de todo o toolkit
    val composeBom = platform("androidx.compose:compose-bom:2024.09.02")
    implementation(composeBom)
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")

    implementation("androidx.activity:activity-compose:1.9.2")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.6")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.6")

    // Retrofit — comunicação com o servidor da Contabo
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-gson:2.11.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // EncryptedSharedPreferences — armazenamento seguro do JWT
    implementation("androidx.security:security-crypto:1.1.0-alpha06")

    // Markdown no chat (via JitPack)
    implementation("com.github.jeziellago:compose-markdown:0.5.4")
}
