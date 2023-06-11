# rythm_entropy
calculates rhythm complexity from the entropy of the sub audible spectrum

Use the notebook to analyze a YouTube video or better a playlist. Whole albums in one file tend to overestimate the entropy as it is multiple songs with different tempos analzyed together. Also songs with varying tempos tend to have a very high score despite the rhythm and structure being fairly simple. The Value is calculated via Shannon entropy but I wouldn't consider it to be Information, as a Fourier spectrum does not satisfy the requirements of a probability distribution.
### some examples values
* Metronome : 100
* Techno: 400
* IndieRock: 650
* Funk: 700
* Jazz: 800
* Classical Music: >1000 
