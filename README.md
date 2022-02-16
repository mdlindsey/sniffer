# Mobile App Network Inspection

This repo is intended to simplify the process for sniffing network traffic on mobile applications. Current support is limited to Android apps running via emulator on MacOS but this may be extended later.

## Installation

Install [Android Studio](https://developer.android.com/studio)

```
brew install --cask android-studio
```

Install [MITM Proxy](https://mitmproxy.org/) - [CLI Shortcuts](https://www.stut-it.net/blog/2017/mitmproxy-cheatsheet.html)

```
brew install mitmproxy
```

Install [Frida Tools](https://frida.re/docs/installation/)

```
pip3 install frida-tools
```

If you do not already have `pip`/`pip3` installed, installing Python via Homebrew will enable these commands.

```
brew install python
```

Download [Frida Server](https://github.com/frida/frida/releases) for your specific architecture and place it in `scripts/frida/**` if it is not already present at `scripts/frida/frida-server-**`.

### Running Scripts

If you want to enable `yarn` shortcuts you can use the command below. Alternatively, you may run the scripts from `package.json` manually if you do not have or do not wish to use the `npm`/`yarn` ecosystem.

```
npm i -g yarn
```

If you do not already have `node`/`npm` available on your system, you may install it via Homebrew.

```
brew install node
```

## Getting Started

Begin by starting the MITM proxy. Attempting to copy the SSL certificate prior to running the proxy will cause the script to fail. This is only required for the first time running MITM but it's best practice to start the proxy first to ensure it's listening prior to the emulator booting up and redirecting traffic.

This must stay running in the background in a separate terminal.

```
yarn mitm
```

Now start the emulator. You may need/want to change the variables inside `./scripts/emu.sh` depending on your available devices within Android Studio AVD Manager or your screen size preferences. When creating new devices, ensure they do not have Google Play capability or you will be unable to (easily) gain root access.

This must stay running in the background in a separate terminal.

```
yarn emu
```

Once the emulator is fully booted, you must copy the MITM SSL certificate to the device. It is somewhat normal for this script to fail; if that is the case simply retry once or twice until it succeeds.

```
yarn cert
```

Certain applications use SSL pinning (also known as cert pinning) to obfuscate their API interactions within an application. We will use Frida to bypass any SSL pinning for specific packages.

This must stay running in the background in a separate terminal.

```
yarn frida:start
```

Once the Frida server is running we must specify which application(s) we want to unpin. You may need to change the `PACKAGE_NAME` variable in `scripts/frida/frida-unpin.sh` depending on which application you are sniffing. Note that package names can be found in the Google Play URLs.

eg: PlayStation application URL - https://play.google.com/store/apps/details?id=**com.scee.psxandroid**

This must stay running in the background in a separate terminal.

```
yarn frida:unpin
```

For demo purposes, the PlayStation app uses SSL pinning and can be found in `apks/PlayStation_v22.1.0.apk` if you'd like to verify that Frida is working as expected.

## Using MITM Proxy

The `--showhost` flag ensures that domain names are preserved rather than resolving to their respective DNS IPs.

To export a request as cURL:
1. Click into the request you wish to export
2. Press `q` to exit the request details view
3. Press `e` to display the context menu for that request
4. Select the `curl` option and provide a filename to be used for the export

## Using Android Studio

Since we cannot (easily) use AVDs with Google Play Services enabled, we must install applications by dragging/dropping `apk` files directly onto the emulator window.

## Acknowledgements & Contributions

Thanks to [Parker Ballner](https://github.com/parker-ballner) for putting together the original documentation on using MITM Proxy.

Thanks to [Tim Perry](https://twitter.com/pimterry) for [his Frida guide](https://httptoolkit.tech/blog/frida-certificate-pinning/#install-and-start-frida-on-the-device) and creating [frida-script.js](https://github.com/httptoolkit/frida-android-unpinning) to simplify Frida interactions.
