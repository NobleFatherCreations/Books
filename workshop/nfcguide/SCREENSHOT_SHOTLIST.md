# Screenshot shot list

**16 of 26 screens are real captures.** The remaining 11 render as hand-drawn SVG
diagrams, which is a perfectly good state to publish in — the site is complete either way.

## How the upgrade works

Every screen renders as:

```html
<img src="assets/screens/NAME.png" alt="…">   <!-- falls back to the SVG drawing -->
```

If the PNG isn't there, the drawing takes its place silently. **Drop a correctly-named
PNG into `assets/screens/` and it takes over. No code change, no rebuild.** Delete it
again and the drawing comes back.

## Capture instructions

- **Portrait.** Phone held upright.
- **Any theme.** Dark or light both work — the site frames them identically.
- **No personal data on screen.** No real phone numbers, addresses, emails, Wi-Fi
  passwords, contact names or account handles. Use obvious dummy values.
- **Full screen, including the status bar.** Don't crop the top — the status bar makes
  it read as a real phone.
- **Trim dead space at the bottom** if the screen is mostly empty, or send the full
  screenshot and it can be cropped on the way in.
- **PNG, around 620px wide.** Anything larger just costs page weight.
- Save as exactly `<name>.png`, all lowercase, from the table below.

## The list

| Screen | What should be on screen | Status |
|---|---|---|
| `nfc-tools-home.png` | The main menu: Read, Write, Other, My saved tags. | **shipped** |
| `write-tab.png` | The Write screen: Add a record, More options, Write. | **shipped** |
| `add-record.png` | The record-type picker, top of the list. | **shipped** |
| `record-type-list.png` | The record-type picker scrolled down, showing the rest of the types. | **shipped** |
| `record-url.png` | The URL / URI entry sheet with a link typed in. | **shipped** |
| `record-text.png` | The Text entry sheet with a short message typed in. | needed |
| `record-contact.png` | The Contact form: name, company, address, phone, mail, website. | **shipped** |
| `record-wifi.png` | The Wi-Fi network form: SSID, password, encryption. | needed |
| `record-social.png` | The Social networks record: provider picker plus username. | **shipped** |
| `record-email.png` | The Mail record: address, subject, message. | needed |
| `record-phone.png` | The Phone number entry sheet. | **shipped** |
| `record-sms.png` | The SMS record: To, plus the message body. | **shipped** |
| `record-location.png` | The Location record: Geo, latitude, longitude, Get a location. | **shipped** |
| `record-app.png` | The Application picker listing installed apps. | needed |
| `more-options.png` | More options: clear, import from tag or QR, save and load record lists. | **shipped** |
| `record-file.png` | The File record: the file path or link field. | **shipped** |
| `record-payment.png` | The Payment link record: provider, account, amount. | **shipped** |
| `record-shortcut.png` | The Shortcut record: shortcut name and optional input. | **shipped** |
| `write-hold.png` | The "Ready to Scan / Approach an NFC Tag" sheet, mid-write. | **shipped** |
| `write-success.png` | The confirmation shown after a successful write. | needed |
| `read-tab.png` | The Read screen waiting for a tag. | needed |
| `read-result.png` | A read result: tag type, chip, serial, size, free space. | needed |
| `other-tab.png` | The Other menu: erase, lock, password, tag info. | needed |
| `lock-tag.png` | The lock-tag warning screen. Do NOT confirm it on a tag you care about. | needed |
| `erase-tag.png` | The erase-tag screen. | needed |
| `ios-scan-sheet.png` | iOS Shortcuts: Automation, New, NFC, Scan. | needed |

## Still needed (11)

- `record-text.png` — The Text entry sheet with a short message typed in.
- `record-wifi.png` — The Wi-Fi network form: SSID, password, encryption.
- `record-email.png` — The Mail record: address, subject, message.
- `record-app.png` — The Application picker listing installed apps.
- `write-success.png` — The confirmation shown after a successful write.
- `read-tab.png` — The Read screen waiting for a tag.
- `read-result.png` — A read result: tag type, chip, serial, size, free space.
- `other-tab.png` — The Other menu: erase, lock, password, tag info.
- `lock-tag.png` — The lock-tag warning screen. Do NOT confirm it on a tag you care about.
- `erase-tag.png` — The erase-tag screen.
- `ios-scan-sheet.png` — iOS Shortcuts: Automation, New, NFC, Scan.

### Worth taking first

1. `write-success.png` — the confirmation. It closes the five-step story and is the one
   screen every reader wants to recognise.
2. `record-text.png` — the second most-used record type on the whole site.
3. `read-result.png` — proves the tag type, capacity and free space, which the
   Troubleshooting and Choose Your Tag sections both send people to.
4. `other-tab.png` — the gateway to everything irreversible.
5. `record-wifi.png` — the most-asked-about record.

## One safety note

`lock-tag.png` requires opening the lock screen in NFC Tools. **Capture the warning
screen, then back out.** Do not confirm it against a tag you want to keep — locking is
permanent and irreversible.
