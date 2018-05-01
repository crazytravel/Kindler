# Kindler
A software for sending a EBook to Kindle device

## Build for desktop
`pip install pyinstaller`

`pyinstaller --windowed Kindler.py`

### for macOS retina screen resolution should add below text to Info.plist

`<key>NSHighResolutionCapable</key>`

`<string>True</string>`