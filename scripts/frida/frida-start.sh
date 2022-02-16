alias adb=~/Library/Android/sdk/platform-tools/adb

# Frida must have been ran or it will fail
frida-ps -U

# Copy the server to the device
adb push ./scripts/frida/frida-server-15.1.17-android-arm64 /data/local/tmp/frida-server

# Enable root access to the device
adb root

# Make the server binary executable
adb shell "chmod 755 /data/local/tmp/frida-server"

# Start the server on your device
adb shell "/data/local/tmp/frida-server &"
