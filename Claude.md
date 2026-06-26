Project Specification v1.0
DMGPod
A Game Boy DMG housing a Raspberry Pi Zero 2W running an iPod-inspired music player with cartridge-based playlists and retro game launching via RetroArch. UI inspired by the iPod classic 6th gen layout, adapted for 320×240 landscape.

Target Hardware Pi Zero 2W
Display 2.4″ ILI9341 SPI 320×240
Resolution 320×240 Landscape
UI Reference iPod Classic 6th Gen
Estimated Build Cost ~£61
Project Summary
The DMGPod uses a non-working donor Game Boy DMG shell as its enclosure. The original buttons, speaker, headphone jack, volume potentiometer, and cartridge slot are retained from the donor. Two shoulder buttons (L and R triggers) are added to the top edge of the shell, enabling full GBA and GBA SP emulation. A Raspberry Pi Zero 2W runs a custom Python/pygame application with an iPod-inspired UI, using the iPod classic 6th gen layout language adapted for 320×240 landscape — menu list on the left, content/art on the right. Music is stored locally on a MicroSD card. Game Boy cartridges are fitted with NFC stickers — inserting a music cart queues a playlist; inserting a special Games cart unlocks a RetroArch launcher hidden in the menu. Audio automatically switches between speaker and headphones using the original DMG jack switch contact, and pauses playback when headphones are removed.

Bill of Materials
#	Component	Notes	Cost
1	Raspberry Pi Zero 2W	Main compute. Quad-core 1GHz, 512MB RAM, onboard WiFi + Bluetooth	~£15
2	DMG Shell, buttons, membranesDonor	Full shell retained from non-working donor unit	£0
3	DMG SpeakerDonor	Original 8Ω speaker, assumed working. Test with multimeter before committing	£0
4	DMG 3.5mm Headphone JackDonor	Original jack with switch contact for headphone detection	£0
5	DMG Volume PotentiometerDonor	Original pot, assumed working. Analogue read via MCP3008 ADC	£0
6	DMG Cartridge SlotDonor	Original edge connector retained for cartridge insertion. RFID reader sits behind it	£0
7	2.4″ ILI9341 SPI TFT Display	240×320, portrait panel mounted landscape. Driver: fbcp-ili9341 for smooth framerates	~£6
8	RC522 RFID Module (mini)	Reads NTAG213 NFC stickers inside cartridges. SPI bus, 3.3V	~£2
9	NTAG213 NFC Stickers (×10)	Fitted inside donor cart shells. Invisible from outside. Each stores a playlist ID	~£5
10	Donor Game Boy Cartridges	Cheap common carts from eBay. Custom labels applied. Quantity = number of playlists + 1 games cart	£1–3 ea
11	MAX98357A I2S DAC + Amp Board	Tiny I2S digital audio. Drives speaker directly. Clean audio without Pi's noisy 3.5mm output	~£3
12	MCP3008 ADC	8-channel SPI ADC. Reads analogue volume pot. Shares SPI bus with display and RFID	~£2
13	LiPo Battery (1000–2000mAh flat)	Flat profile to fit modified battery compartment. Higher capacity = longer runtime	~£8
14	Pimoroni LiPo SHIM	Designed for Pi Zero footprint. Handles charging, 5V boost, and safe low-battery shutdown	~£10
15	MicroSD Card (32GB+)	OS + music storage. Class 10 or better recommended	~£6
16	L & R Shoulder Buttons (×2)	Small tactile or soft-click buttons mounted to top edge of DMG shell. Enables full GBA / GBA SP emulation. Minor shell modification required	~£1
17	Miscellaneous	Wire, heatshrink, solder, flux, small screws, kapton tape	~£3
Estimated Total
Excluding cartridges. Donor parts at £0. Triggers added.
~£61
UI & Menu Structure
The UI takes inspiration from the iPod classic 6th gen layout, adapted for 320×240 landscape — menu list on the left side, album art and now playing content on the right. This suits the aspect ratio better than the nano's portrait layout and gives more breathing room at this screen size. The core aesthetic language remains: clean Apple typography, the characteristic highlight bar, minimal chrome.

Without Games Cart
▶
Music
Extras
Settings
With Games Cart Inserted
▶
Music
Games
Unlocked
Extras
Settings
Music submenu
▶
Artists
Albums
Songs
Playlists
Now Playing
Cartridge System
Cart Type	Trigger	Behaviour on Insert	Behaviour on Remove
Music Cart	NFC tag → playlist ID	Queues the linked playlist, jumps to Now Playing	Playback continues unaffected
Games Cart	NFC tag → GAMES_UNLOCK	Toast: "Games Unlocked" — Games appears in menu	Game session continues. Games removed from menu on next return to home
No Cart	—	—	Default state. Music, Extras, Settings only
Audio Behaviour
Event	Detected By	Behaviour
Headphones inserted	DMG jack switch contact → GPIO	Audio routes to headphone jack seamlessly. Playback continues
Headphones removed	DMG jack switch contact → GPIO	Playback pauses. Audio routes back to speaker
Volume wheel turn	DMG pot → MCP3008 ADC → SPI	Controls system volume. Works in both music and RetroArch
Bluetooth pairing	Pi Zero 2W onboard BT	Available via Extras menu. No additional hardware required
GPIO Pin Allocation
Planned allocation to avoid conflicts between SPI display, RFID reader, ADC, I2S audio, buttons, and headphone detect.

GPIO Pin	Function	Bus / Interface
GPIO 10 (MOSI)	SPI MOSI	SPI0 — shared: display, RC522, MCP3008
GPIO 9 (MISO)	SPI MISO	SPI0 — shared
GPIO 11 (SCLK)	SPI Clock	SPI0 — shared
GPIO 8 (CE0)	Display CS	SPI0 chip select
GPIO 7 (CE1)	RC522 CS	SPI0 chip select
GPIO 25	MCP3008 CS	SPI0 chip select (software)
GPIO 24	Display DC	ILI9341 data/command
GPIO 23	Display RST	ILI9341 reset
GPIO 18 (PCM_CLK)	I2S BCLK	I2S — MAX98357A
GPIO 19 (PCM_FS)	I2S LRCLK	I2S — MAX98357A
GPIO 21 (PCM_DOUT)	I2S DATA	I2S — MAX98357A
GPIO 4	D-Pad Up	Button input, pull-up
GPIO 17	D-Pad Down	Button input, pull-up
GPIO 27	D-Pad Left	Button input, pull-up
GPIO 22	D-Pad Right	Button input, pull-up
GPIO 5	A Button (Select)	Button input, pull-up
GPIO 6	B Button (Back)	Button input, pull-up
GPIO 13	Start (Play/Pause)	Button input, pull-up
GPIO 12	Select (Skip)	Button input, pull-up
GPIO 26	Headphone Detect	DMG jack switch contact, pull-up
GPIO 16	L Trigger	Shoulder button input, pull-up
GPIO 20	R Trigger	Shoulder button input, pull-up
Note
GPIO 19 conflict from the original draft has been resolved — Select button is assigned to GPIO 20 and R Trigger to a separate pin. L and R triggers use GPIO 16 and GPIO 20 respectively, leaving the I2S bus intact on GPIOs 18, 19, 21.
Development Phases
Phase 0
Product Definition
Mac
Freeze the spec, create the GitHub repository, set up the folder structure. No code yet.

Product spec
README.md
GitHub repo
BOM finalised
Folder structure
Phase 1
Development Environment
Mac
Install Python, VS Code, Git, pygame, and required libraries on macOS. Push initial commit. No Raspberry Pi required.

Python + pygame
VS Code configured
Git + GitHub Desktop
requirements.txt
Phase 2
Desktop Prototype
Mac
320×240 application window on macOS. Keyboard controls. Implement scene manager and main menu navigation. No functionality yet — just the skeleton.

App window 320×240
Scene manager
Keyboard input
Main menu renders
Phase 3
Full UI Build
Mac
Build every menu screen: Music, Games (hidden), Extras, Settings, all submenus, Now Playing screen. iPod classic 6th gen layout language — list left, content right. Navigation working throughout. No audio, no RFID yet.

All menu screens
Now Playing screen
iPod visual style
Full navigation
Games hidden by default
Phase 4
Music System
Mac
Music library scanning, playback, album art, artists/albums/songs/playlists. Audio plays through Mac speakers. Fully functional music player before touching any hardware.

Library scanner
Playback engine
Album art
Playlists
Now Playing live
Phase 5
Cartridge Simulation
Mac
Simulate cartridge insertion and removal from the keyboard. Number keys trigger different carts. Toast notifications. Games unlock mechanic. Validates the full cart logic before any RFID hardware exists.

Keyboard cart simulation
Toast notifications
Playlist loading from cart
Games unlock / lock
Phase 6
Emulator Integration
Mac
Games menu item launches RetroArch. DMGPod suspends, RetroArch runs fullscreen, returns cleanly to DMGPod on exit. Games menu item hidden if cart not present.

RetroArch launch
Clean return to UI
Games conditional visibility
Phase 7
Raspberry Pi Bring-up
Pi
Move to hardware. Install Raspberry Pi OS, configure display driver (fbcp-ili9341), verify display works. SSH access. Git clone the repo. Confirm the app runs on Pi with keyboard input before touching GPIO.

Pi OS installed
fbcp-ili9341 configured
Display working
SSH access
App running on Pi
Phase 8
Hardware Layer
Pi
Replace simulated inputs with real hardware one subsystem at a time. GPIO buttons replace keyboard. RC522 replaces keyboard cart simulation. I2S DAC replaces Mac audio. Volume pot via MCP3008. Headphone detect via jack switch contact.

GPIO buttons
L & R triggers
RC522 RFID
I2S audio
Volume pot (ADC)
Headphone detect + pause
Phase 9
Bench Prototype
Pi
All hardware connected externally on the bench. Do not modify the DMG shell yet. Every subsystem tested independently and together. Everything must work here before any mechanical work begins.

Full system test
All hardware verified
Battery + charging
RetroArch on Pi
Phase 10
Mechanical Design
Design
Design internal mounts for Pi, display, RFID reader, battery, and cable routing. Plan shoulder button placement and top-edge shell modification for L/R triggers. Prototype with 3D printing or cardboard mockups. Plan all shell modifications before cutting anything.

Pi mount
Display mount
RFID mount
Battery holder
Shoulder button plan
Cable routing plan
Phase 11
Final Assembly
Pi
Modify the DMG shell. Install everything. Full test after assembly. This is the only phase where the shell gets modified — everything must be confirmed working before this point.

Shell modified
All components installed
Full system test in shell
Phase 12
Polish
Both
Apple logo boot splash. UI animations and transitions. Toast notification polish. Volume overlay. Battery indicator. Sleep mode. Final bug fixes.

Boot splash
Animations
Battery indicator
Sleep mode
Volume overlay
Milestones
M1
Desktop UI Complete
App runs on macOS. Full navigation. Keyboard controls. iPod visual style.
M2
Music Player Working
Audio playback, library browsing, playlists, album art. All on Mac.
M3
Cartridge System Working
Keyboard-simulated carts load playlists and unlock Games. Toast notifications working.
M4
Pi UI Running
Same application running on Raspberry Pi. Display working. SSH access confirmed.
M5
Full Hardware Working
GPIO buttons, RFID carts, I2S audio, volume pot, headphone detect. All on bench, outside shell.
M6
Bench Prototype Complete
Every subsystem verified. RetroArch launching. Battery tested. Ready for mechanical work.
M7
Final Assembly
Everything inside the DMG shell. Shell modifications complete. Full system test passed.
M8
V1 Release
Boot splash, polish, sleep mode, battery optimisation. V1 feature-complete.
Version Scope
V1 — Must Have
Boot directly into DMGPod
Navigate using DMG controls
Music playback
Album art
Artists, Albums, Songs, Playlists
RFID music cartridges
Games cartridge unlock
RetroArch launching (GB, GBC, GBA, GBA SP)
L & R shoulder triggers for GBA
Speaker / headphone auto-switch
Pause on headphone removal
Volume wheel
Battery indicator
Apple logo boot splash
Toast notifications
Bluetooth audio (onboard, free)
V2 — Future
Cover Flow
Themes
Wi-Fi music syncing
Spotify Connect
Firmware updater
Cartridge-specific themes
Listening statistics
Customisable home screen
Save states
Guiding Principles
💻
Develop on Mac
All code is written and tested on macOS first. The Mac is the primary development machine. The Pi is the deployment target.

🔌
Validate on Pi
After each major feature, verify it runs identically on the Pi. Catch hardware-specific issues early, not at assembly.

🔧
Assemble Last
The DMG shell is not modified until every subsystem works on the bench. Never cut plastic to fix a software problem.

DMGPod — Development Plan v1.0
Develop on Mac · Validate on Pi · Assemble Last