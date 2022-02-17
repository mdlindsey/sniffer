LOCAL_IP=$(ipconfig getifaddr en0)  # Hardcode this if ipconfig doesn't return the correct IP
DEVICE_ID=Pixel_5                   # This will change depending on Android Studio devices/settings
DEVICE_SIZE="1440x2560"             # You may change this as you please for larger/smaller device window
~/Library/Android/sdk/emulator/emulator \
    -avd $DEVICE_ID                     \
    -writable-system                    \
    -skin ${DEVICE_SIZE}                \
    -http-proxy $LOCAL_IP:8080          \
