Drop assets here.

Required / expected files:
  music.mp3          -> background music (autoplays, loops)
  francesco.jpg      -> Francesco's headshot. Used for BOTH the passport photo
                        (Gate 2) and the face-api.js reference (Gate 1).
                        CSS auto-crops it to frame the face.  *** STILL NEEDED ***
  wrong-buzzer.mp3   -> wrong-answer stinger #1  (installed)
  angry-man.mp3      -> wrong-answer stinger #2  (installed) — both play together
  plane.png          -> optional plane image for the cutscene

sprites/           -> Francesco's pixel walk sprites (installed). Per direction:
                      front/back/side + _left/_right foot frames. "right" reuses
                      the side art mirrored. Used by game.html.

None of these are committed — they're placeholders you swap in.
Until music.mp3 exists the audio element simply stays silent.
