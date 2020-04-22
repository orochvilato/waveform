prérequis :
python 3.6
ffmpeg


Fichiers nécessaires :
- audio.wav et audio.mp3 la source audio au format mp3 et wav
- fond.png l'image dans laquelle intégrer l'équaliseur

spectrum.py genère à 30 images/sec l'"équaliseur" pour le fichier audio.wav et l'intègre dans l'image fond.png

Pour générer la vidéo finale :

Création d'un mp4 à partir des images générées :
`ffmpeg -framerate 30 -i imgs/test%d.png -c:v libx264 -vf fps=30 -pix_fmt yuv420p out.mp4`

Intégration de la bande son :
`ffmpeg -i out.mp4 -i audio.mp3 -c copy -map 0:v:0 -map 1:a:0 fin.mp4`
