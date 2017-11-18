cd  C:/Users/arama/Documents/WebStormProjects/nsbapp
ionic build --release
cd platforms/android/build/outputs/apk/
jarsigner -verbose -sigalg SHA1withRSA -tsa http://timestamp.comodoca.com/rfc3161 -digestalg SHA1 -keystore nsbapp.keystore android-x86-release-unsigned.apk NSBApp
jarsigner -verbose -sigalg SHA1withRSA -tsa http://timestamp.comodoca.com/rfc3161 -digestalg SHA1 -keystore nsbapp.keystore android-armv7-release-unsigned.apk NSBApp

zipalign -v 4 android-x86-release-unsigned.apk release-x86-1.2.1.apk
zipalign -v 4 android-armv7-release-unsigned.apk release-armv7-1.2.1.apk

exit

gulp -b &  code-push release-cordova NSBApp android
code-push promote NSBApp Staging Production

gulp -b &  code-push release-cordova NSBApp android & code-push promote NSBApp Staging Production



gulp -b && code-push release-cordova NSBApp ios -t 1.2.0  -m && code-push promote NSBApp Staging Production