# Unpin SSL with Frida
PACKAGE_NAME="com.scee.psxandroid"
frida --no-pause -U -l ./scripts/frida/frida-script.js -f $PACKAGE_NAME
