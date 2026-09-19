Práctica 1: Configuración del Entorno de Desarrollo y A

1. Descripción del Entorno y Proyectos
Herramientas Instaladas
Java Development Kit: Lo instalé para tener el entorno de ejecución de Java y el compilador que usan Android Studio y Gradle.

Apache Maven: Lo configuré para la gestión de proyectos y dependencias en el sistema.

Git: Lo usé desde la terminal para llevar el control de versiones y subir los cambios a mi repositorio.

Node.js: Lo instalé para contar con el entorno de ejecución de JavaScript y sus herramientas.

Docker: Lo configuré en la computadora para el manejo de contenedores.

Android Studio: Es el IDE principal que usé para crear los proyectos nativos, gestionar las SDKs de Android y correr el emulador Pixel 8.

Flutter: Lo instalé y configuré en las variables de entorno para desarrollar la versión multiplataforma.

Proyectos Desarrollados
xmlviews: Es la primera versión que hice, usando la forma tradicional de Android con archivos XML para el diseño de la pantalla.

compose: La segunda versión, donde usé Jetpack Compose en Kotlin para hacer la interfaz de forma declarativa sin archivos XML.

hola_mundo_flutter: La tercera versión, desarrollada en Dart con Flutter usando su sistema de widgets.

2. Paso a Paso de Creación y Ejecución
Versión 1: Android XML (xmlviews)
Abrí Android Studio y le di en New Project.

Escogí la plantilla Views Activity y le di en Next.

Le puse de nombre xmlviews, en paquete dejé com.example.xmlviews, seleccioné Kotlin como lenguaje y la API 24 como SDK mínimo.

Le di en Finish y esperé a que Gradle terminara de cargar el proyecto.

Me fui al archivo app/src/main/res/layout/activity_main.xml y modifiqué el código para poner los TextViews ordenados hacia abajo con mi nombre (Diego Mendieta González), boleta (2024630077) y grupo (7CV4).

Abrí el Device Manager, encendí el emulador Pixel 8, seleccioné la configuración app arriba y le di al botón de Run para ver la app en el teléfono virtual.

Versión 2: Jetpack Compose (hola_mundo_compose)
En Android Studio fui a File > New > New Project...

Seleccioné la plantilla Empty Activity (la que trae el ícono de Jetpack Compose) y le di en Next.

Le puse de nombre hola_mundo_compose, configuré el paquete como dmendieta2005.gmail.dmendieta2005.compose y dejé la API 24 en Kotlin.

Esperé a que descargara y creara las dependencias iniciales.

Abrí el archivo MainActivity.kt y modifiqué la función @Composable poniendo un Column alineado a la izquierda (Alignment.Start), agregando los Text en color negro con mis datos personales dentro del ComposeTheme.

Seleccioné el emulador Pixel 8 en la barra superior y le di en Run 'app' para comprobar que abriera bien.

Versión 3: Flutter (hola_mundo_flutter)
Abrí la terminal de PowerShell dentro de la carpeta de mi repositorio.

Ejecuté el comando flutter create hola_mundo_flutter para que creara la estructura del proyecto.

Abrí el proyecto en el editor y me fui al archivo lib/main.dart.

Borré el código que viene por defecto y armé la interfaz usando un Scaffold con fondo blanco, un SafeArea y un Column alineado a la izquierda con crossAxisAlignment: CrossAxisAlignment.start.

Agregué los widgets Text en color negro para mostrar "Hola Mundo", mi nombre, mi boleta y mi grupo.

Asegurándome de tener encendido el emulador de Android, ejecuté flutter run desde la terminal dentro de la carpeta del proyecto para desplegar la app.

3. Problemas que Tuve y Cómo los Resolví
Licencias del SDK de Android:

Tuve detalles al intentar aceptar las licencias automáticamente desde la consola, así que mejor me fui directo al SDK Manager en Android Studio y acepté los términos instalando los componentes desde la interfaz gráfica.

Error del NDK en Flutter y Gradle:

Al intentar correr flutter run, la consola me lanzaba un fallo diciendo Package ndk not found o buscando la versión específica 28.2.13676358 mediante sdkmanager.bat. Lo solucioné entrando al SDK Manager > SDK Tools, activando la casilla Show Package Details e instalando esa versión exacta dentro de NDK (Side by side). También comenté la línea ndkVersion en el archivo build.gradle.kts para evitar bloqueos.

El emulador se trabó (Can't find service: package):

En una de las pruebas con Compose, el emulador dejó de responder al intentar instalar el APK y marcaba error de servicio. Lo arreglé yendo al Device Manager, le di a los tres puntos en el emulador Pixel 8 y seleccioné Cold Boot Now para forzar un reinicio limpio del teléfono virtual.

Target de compilación en Flutter:

En un intento le di ejecutar a Flutter y me marcó error de Visual Studio porque intentó compilar para Windows (desktop). Solo tuve que cambiar el dispositivo de destino en la barra superior de Android Studio para seleccionar el emulador sdk gphone64 / Pixel 8.

4. Conclusiones
Al hacer esta práctica me di cuenta de cómo ha ido cambiando la forma de programar aplicaciones móviles en Android:

XML tradicional: Se me hizo un poco más tardado porque hay que estar pasando entre el archivo de diseño XML y la lógica en Kotlin. Funciona bien para estructurar cosas muy específicas, pero requiere escribir más código y mantener más archivos.

Jetpack Compose: Me pareció una forma mucho más rápida y cómoda de trabajar. Al escribir la interfaz directamente en Kotlin con funciones composables me ahorré el uso de XMLs, y el código queda más ordenado y fácil de entender.

Flutter: Es una opción bastante práctica si se quiere hacer una app que funcione en varias plataformas. Me gustó mucho el uso de widgets y la facilidad para alinear las cosas en pantalla, aunque al principio cuesta un poco ajustar la configuración inicial del entorno entre Flutter, Gradle y el NDK de Android.