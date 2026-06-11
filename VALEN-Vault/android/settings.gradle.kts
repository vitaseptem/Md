// =====================================================================
//  VALEN ANDROID — settings.gradle.kts
// =====================================================================
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        // JitPack: necessário para a lib compose-markdown (renderização Markdown no chat)
        maven(url = "https://jitpack.io")
    }
}

rootProject.name = "ValenApp"
include(":app")
