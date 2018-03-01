BYMD
====

Hai domo! Baacharu YouTuber Mixer Desu.

This program allows you to mix random words from videos in YouTube.
It was initially made to see what would happen when you randomly mix Kizuna Ai and
Kaguya Luna in the same audio.

It first downloads the specified videos, splits them in different chunks according
to the silence thresh and length and randomly mixes them into an audio file.

You can skip any of the steps with the `-o` argument, e.g: To just chunk the videos: `python bymd.py -o chunk`
By default, the videos that has already been downloaded won't be downloaded again, so, when you download a full
channel (e.g.: Kizuna's 300 videos), it won't redownload all of them.

The Silence Thresh is the base dBFS for the silence, by default it's *-26* but you should
experiment with the values to find the proper one.
The Silence Length is the minimum length required to split the audio there.

For a full list of arguments, run `python bydm.py -h h`.

To download videos you need to have [YouTubeDL](https://github.com/rg3/youtube-dl)

This is my first python program, it works for me, if it doesn't for you, fix it yourself :)

Some examples:

 * [Kaguya Luna + Kizuna Ai](https://vocaroo.com/i/s1RhWZO8K0EM)
 * [Kizuna Ai](https://vocaroo.com/i/s0X74cAsicva)