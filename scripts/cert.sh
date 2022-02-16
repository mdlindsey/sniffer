alias adb=~/Library/Android/sdk/platform-tools/adb

if ! ls ./scripts/certs; then
    mkdir ./scripts/certs
fi

adb root
adb remount
hashedpem="$(openssl x509 -inform PEM -subject_hash_old -in ~/.mitmproxy/mitmproxy-ca-cert.pem | head -1)"
cp ~/.mitmproxy/mitmproxy-ca-cert.pem ./scripts/certs/$hashedpem.0
adb push ./scripts/certs/$hashedpem.0 /system/etc/security/cacerts
adb shell "chmod 664 /system/etc/security/cacerts/$hashedpem.0"
adb reboot
