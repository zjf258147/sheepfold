# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# Capacitor WebView JavaScript interface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Capacitor plugins
-keep class com.getcapacitor.** { *; }
-dontwarn com.getcapacitor.**

# Camera plugins
-keep class io.ionic.libs.ioncameralib.** { *; }

# Barcode scanner (ML Kit)
-keep class com.google.mlkit.** { *; }
-dontwarn com.google.mlkit.**

# Preserve line numbers for stack traces
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile