# rythm_entropy
calculates rhythm complexity from the entropy of the sub audible spectrum. The basic Idea is that the shannon entropy is a measure for peakyness of a distribution and a simple rhythm would have only one peak and more complex rhythms feature more peaks.

Use the notebook to analyze a YouTube video or better a playlist. Whole albums in one file tend to overestimate the entropy as song length also contributes to higher entropy. Also songs with varying tempos tend to have a very high score despite the rhythm and structure being fairly simple. The value is calculated via Shannon entropy but I wouldn't consider it to be information, as a Fourier spectrum does not satisfy the requirements of a probability distribution.
### Some examples values
* Metronome : 100
* Techno: 400
* Indie Rock: 650
* Funk: 700
* Jazz: 800
* Classical music: >1000 
