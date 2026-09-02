#!/usr/bin/env python3
"""Give Wook in Sheep's Clothing its own autoplay soundtrack, copying the
hub's mechanism, and add a new section for it plus a companion video.

## The autoplay track ("Free Discernment")

Ports hub/catalogue-redesign.html's #npAudio feature exactly: inlined as
base64 (not hosted -- see below for why that's the right call here, unlike
the Real Ones songs), starts on the first real user gesture (browsers
block unmuted audio autoplay with zero interaction outright, so a
gestureless attempt would just silently fail -- this is why the hub itself
ties its start to "the same click that chooses a door" rather than firing
on load), remembers an explicit mute for the rest of the tab's session,
and never re-attempts playback on a later reload without a fresh gesture.
Wook has no door-choosing gate, so the trigger here is the page's first
pointerdown/touchstart/keydown/scroll instead -- functionally "starts when
you open it" for a visitor arriving via an NFC tap, who is about to touch
the screen anyway.

Why inlined and not hosted like the Real Ones songs: the hub inlines
exactly ONE always-loaded track for the same reason -- it is the single
persistent atmosphere for the whole visit, not one of many optional plays.
Ten separate hosted Real Ones songs would be excessive to inline; one
book-wide theme track, matching the hub's own precedent, is not.

## The new #soundtrack section

Sits between #real-ones and #author. Two songs plus a video:
- Free Discernment: NOT a second <audio> with its own copy of the same
  ~7MB base64 payload (that would double it in the page for nothing) --
  this card is a play/pause control wired to the SAME #wkAudio element
  that's already playing, with a live progress bar.
- Warfare Is Directional: a normal hosted mp3 (library/wook/audio/), same
  pattern as every Real Ones song -- absolute URL, because this book is
  proxied at /wook and a root-relative path would resolve against
  noblefathercreations.com instead (see wook-add-songs.py's docstring).
- The video: hosted the same way, from library/wook/video/.

Run: python3 scripts/wook-add-soundtrack.py
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WOOK = ROOT / "library/wook/index.html"
AUDIO_BASE = "https://wook-in-sheeps-clothing.netlify.app/audio/"
VIDEO_BASE = "https://wook-in-sheeps-clothing.netlify.app/video/"

# Free Discernment lives here as a source file too, alongside the hosted
# tracks, even though the page never links to it directly -- it's what
# this script reads to produce the inline copy, so a future edit (a new
# cut, a re-encode) has something to re-run against instead of only
# existing as bytes already baked into index.html.
FREE_DISCERNMENT_MP3 = ROOT / "library/wook/audio/free-discernment.mp3"
WARFARE_FILE = "warfare-is-directional.mp3"
VIDEO_FILE = "companion.mp4"

MUTE_CSS = """
  /* ---- book soundtrack, autoplay on first touch (scripts/wook-add-soundtrack.py) ----
     Mirrors the hub's #npAudio feature -- same reasoning, same mute
     persistence -- in this book's own zine tokens, on the opposite
     corner from the seal so the two read as a pair without colliding. */
  .wk-mute{position:fixed;left:18px;bottom:18px;z-index:9950;width:50px;height:50px;
    border-radius:50%;border:2.5px solid #000;cursor:pointer;padding:0;
    background:var(--neon);color:var(--ink);display:grid;place-items:center;
    box-shadow:3px 3px 0 rgba(0,0,0,.6);
    opacity:0;transform:scale(.8);pointer-events:none;
    transition:opacity 220ms ease,transform 220ms ease,box-shadow 150ms ease}
  .wk-mute.wk-mute-on{opacity:1;transform:scale(1);pointer-events:auto}
  .wk-mute:active{transform:scale(.92)}
  .wk-mute svg{width:20px;height:20px;stroke:var(--ink);fill:none;stroke-width:2;
    stroke-linecap:round;stroke-linejoin:round}
  .wk-mute .wk-mute-off-icon{display:none}
  .wk-mute[aria-pressed="true"] .wk-mute-on-icon{display:none}
  .wk-mute[aria-pressed="true"] .wk-mute-off-icon{display:block}
"""

SOUNDTRACK_CSS = """
  /* ---- #soundtrack extras: the live-synced card, the video card ---- */
  .mixtape-playbtn{cursor:pointer;border:2.5px solid #000}
  .mixtape-playbtn .mp-pause{display:none}
  .mixtape-playbtn[aria-pressed="true"] .mp-play{display:none}
  .mixtape-playbtn[aria-pressed="true"] .mp-pause{display:block}
  .mixtape-playbtn svg{width:16px;height:16px;fill:var(--ink)}
  .mixtape-bar{height:8px;border-radius:999px;border:2px solid #000;
    background:#fff;overflow:hidden;margin-top:.15rem}
  .mixtape-fill{display:block;height:100%;width:0%;background:var(--neon);
    transition:width 120ms linear}
  .mixtape-time{font-family:var(--mono);font-size:.62rem;font-weight:700;
    color:#6747E8;margin-top:.35rem;letter-spacing:.04em}
  .vidcard{margin-top:.95rem;background:#000;border:2.5px solid #000;
    border-radius:.6rem;box-shadow:3px 3px 0 rgba(0,0,0,.6);overflow:hidden}
  .vidcard video{width:100%;display:block;background:#000}
  .vidcard-label{background:var(--paperA);padding:.6rem .75rem;color:var(--ink)}
"""


def install_css(html):
    marker = ".org-links a.alt{background:var(--teal)}"
    if MUTE_CSS not in html:
        assert html.count(marker) == 1
        html = html.replace(marker, marker + "\n" + MUTE_CSS, 1)
    if SOUNDTRACK_CSS not in html:
        anchor = ".mixtape audio{width:100%;display:block;height:32px}"
        assert html.count(anchor) == 1, "run wook-add-songs.py first"
        html = html.replace(anchor, anchor + "\n" + SOUNDTRACK_CSS, 1)
    return html


def install_player(html):
    """The hidden autoplay element + the mute toggle, first thing in body."""
    if 'id="wkAudio"' in html:
        return html
    assert FREE_DISCERNMENT_MP3.exists(), FREE_DISCERNMENT_MP3
    b64 = base64.b64encode(FREE_DISCERNMENT_MP3.read_bytes()).decode()

    markup = (
        f'<audio id="wkAudio" preload="none" loop '
        f'src="data:audio/mpeg;base64,{b64}"></audio>\n'
        '<button class="wk-mute" type="button" id="wkToggle" '
        'aria-label="Mute the soundtrack" aria-pressed="false">'
        '<svg class="wk-mute-on-icon" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M4 9v6h4l5 5V4L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/>'
        '<path d="M19 6a8.5 8.5 0 0 1 0 12"/></svg>'
        '<svg class="wk-mute-off-icon" viewBox="0 0 24 24" aria-hidden="true">'
        '<path d="M4 9v6h4l5 5V4L8 9H4z"/><path d="M16 9l5 6M21 9l-5 6"/></svg>'
        "</button>\n"
    )
    assert html.count("<body>") == 1
    return html.replace("<body>", "<body>\n" + markup, 1)


PLAYER_JS = """
(function(){
  var audio = document.getElementById('wkAudio');
  var muteBtn = document.getElementById('wkToggle');
  if(!audio || !muteBtn) return;
  var musicMuted = false;
  try { musicMuted = sessionStorage.getItem('wkMusicMuted') === '1'; } catch(_){}

  function setMuteState(muted){
    musicMuted = muted;
    muteBtn.setAttribute('aria-pressed', muted ? 'true' : 'false');
    muteBtn.setAttribute('aria-label', muted ? 'Unmute the soundtrack' : 'Mute the soundtrack');
    try { sessionStorage.setItem('wkMusicMuted', muted ? '1' : '0'); } catch(_){}
    syncCardButtons();
  }

  function showMuteBtn(){ muteBtn.classList.add('wk-mute-on'); }

  function startMusic(){
    showMuteBtn();
    if (musicMuted) return; // an earlier explicit mute this tab is respected, not overridden
    var p = audio.play();
    if (p && typeof p.catch === 'function'){
      p.catch(function(){ setMuteState(true); }); // refused -- button reflects paused
    }
  }

  muteBtn.addEventListener('click', function(){
    if (audio.paused){ audio.play().catch(function(){}); setMuteState(false); }
    else { audio.pause(); setMuteState(true); }
  });

  // ---- the #soundtrack card for this same track: a play/pause control and
  // a progress bar wired to #wkAudio, not a second copy of the audio ----
  var cardBtns = [].slice.call(document.querySelectorAll('[data-wk-playbtn]'));
  var fill = document.getElementById('fdFill');
  var timeEl = document.getElementById('fdTime');
  function syncCardButtons(){
    var playing = !audio.paused && !musicMuted;
    cardBtns.forEach(function(b){
      b.setAttribute('aria-pressed', playing ? 'true' : 'false');
      b.setAttribute('aria-label', playing ? 'Pause Free Discernment' : 'Play Free Discernment');
    });
  }
  function fmt(s){
    if (!isFinite(s)) return '0:00';
    s = Math.floor(s);
    return Math.floor(s/60) + ':' + (s%60 < 10 ? '0' : '') + (s%60);
  }
  cardBtns.forEach(function(b){
    b.addEventListener('click', function(){
      if (audio.paused){ audio.play().catch(function(){}); setMuteState(false); }
      else { audio.pause(); setMuteState(true); }
    });
  });
  audio.addEventListener('play', syncCardButtons);
  audio.addEventListener('pause', syncCardButtons);
  audio.addEventListener('timeupdate', function(){
    if (fill && audio.duration) fill.style.width = (audio.currentTime/audio.duration*100) + '%';
    if (timeEl) timeEl.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration);
  });
  syncCardButtons();

  // ---- starts on the first real gesture on the page. See the module
  // docstring in scripts/wook-add-soundtrack.py for why a gesture, not
  // page load, is the earliest point this can actually work. ----
  var already = false;
  try { already = sessionStorage.getItem('wkMusicStarted') === '1'; } catch(_){}
  if (already) { showMuteBtn(); }
  else {
    var events = ['pointerdown','touchstart','keydown','scroll'];
    var onFirstGesture = function(){
      events.forEach(function(evt){ document.removeEventListener(evt, onFirstGesture); });
      try { sessionStorage.setItem('wkMusicStarted','1'); } catch(_){}
      startMusic();
    };
    events.forEach(function(evt){
      document.addEventListener(evt, onFirstGesture, {passive:true});
    });
  }
})();
"""


def install_js(html):
    if "wkMusicStarted" in html:
        return html
    assert html.count("</body>") == 1
    return html.replace(
        "</body>", f"<script>{PLAYER_JS}</script>\n</body>", 1)


def soundtrack_section_html():
    warfare_src = AUDIO_BASE + WARFARE_FILE
    video_src = VIDEO_BASE + VIDEO_FILE
    return f"""<section class="panel pp-black prose" id="soundtrack"><svg class="doodle st-tl" aria-hidden="true"><use href="#flower"/></svg><svg class="doodle st-br" aria-hidden="true"><use href="#smile"/></svg><h2 class="zine-h light">&#127925; THE SOUNDTRACK</h2><p class="script-note">&mdash; This book has a sound, too.</p><p>Two original songs and a video that go with it &mdash; written and made alongside the book, not after it. Press play, then keep reading; the first one&rsquo;s probably already going.</p><div class="mixtape">\
<div class="mixtape-label"><button class="mixtape-note mixtape-playbtn" type="button" data-wk-playbtn aria-pressed="false" aria-label="Play Free Discernment"><svg class="mp-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4l14 8-14 8V4z"/></svg><svg class="mp-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg></button>\
<div><p class="mixtape-title">Free Discernment</p><p class="mixtape-sub">the soundtrack for this book</p></div></div>\
<div class="mixtape-bar"><span class="mixtape-fill" id="fdFill"></span></div>\
<p class="mixtape-time" id="fdTime">0:00 / 0:00</p></div>\
<div class="mixtape"><div class="mixtape-label"><span class="mixtape-note" aria-hidden="true">&#9834;</span>\
<div><p class="mixtape-title">Warfare Is Directional</p><p class="mixtape-sub">another original song for this book</p></div></div>\
<audio controls preload="none" src="{warfare_src}"><a href="{warfare_src}">Warfare Is Directional (MP3)</a></audio></div>\
<div class="vidcard"><video controls preload="none" playsinline src="{video_src}"><a href="{video_src}">Watch the video</a></video>\
<div class="vidcard-label"><p class="mixtape-title">The book, on video</p></div></div>\
<p class="org-salute">Turn it up. &#128266;</p></section>
"""


def install_section(html):
    if 'id="soundtrack"' in html:
        return html
    anchor = '<section class="panel pp-purple prose" id="author">'
    assert html.count(anchor) == 1
    return html.replace(anchor, soundtrack_section_html() + anchor, 1)


def main():
    html = WOOK.read_text(errors="surrogateescape")
    before = len(html)

    html = install_css(html)
    html = install_player(html)
    html = install_js(html)
    html = install_section(html)

    WOOK.write_text(html, errors="surrogateescape")
    print(f"wook: {before:,} -> {len(html):,} bytes")


if __name__ == "__main__":
    sys.exit(main())
