#!/usr/bin/python

from __future__ import unicode_literals
from youtube_dl import YoutubeDL
from pydub import AudioSegment
from pydub.silence import split_on_silence
from glob import glob
from sys import argv
from random import choice
from time import time

##
# Kizuna class.
# =============
#
# The constructor accepts as parameters
# the playlists to download and the directory
# to save them.
#
# Once instantiated call the method `start`
# to download the videos.
#
# @author Manulaiko <manulaiko@gmail.com>
#
class Kizuna:
    ##
    # Constructor.
    #
    # @param lists Playlists to download.
    # @param path  Path to save the audios.
    #
    def __init__(self, lists, path):
        self.lists = lists
        self.path  = path

    ##
    # Downloads the videos.
    #
    def start(self):
        opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                #'preferredquality': '192',
            }],
            'download_archive': '.download_archive',
            'outtmpl': '{0}/%(title)s-%(id)s.%(ext)s'.format(self.path),
            #'audioformat': 'wav'
        }

        with YoutubeDL(opts) as downloader:
            downloader.download(self.lists)

##
# Kaguya class.
# =============
#
# The constructor accepts as parameter the
# paths to the audio and chunks directories,
# it also accepts the `silence_thresh` and
# ` min_silence_len` values.
#
# Once instantiated call the method `start` to
# scan the directories and split the audios.
#
# @author Manulaiko <manulaiko@gmail.com>
#
class Kaguya:
    ##
    # Constructor
    #
    # @param audioPath     Path to the directory containing the audios.
    # @param chunksPath    Path to the directory to export the chunks.
    # @param silenceLength Length between words.
    # @param silenceThresh dBFS considered as silence.
    #
    def __init__(self, audioPath, chunksPath, silenceLength, silenceThresh):
        self.audioPath     = audioPath
        self.chunksPath    = chunksPath
        self.silenceLength = silenceLength
        self.silenceThresh = silenceThresh

    ##
    # Scans the directories and split the audios.
    #
    def start(self):
        print "Scanning directories..."

        self.audios = glob("{0}/*.wav".format(self.audioPath))
        self.chunks = len(glob("{0}/*.wav".format(self.chunksPath)))

        print "Found", len(self.audios), "audios and", self.chunks, "chunks."

        for i, audio in enumerate(self.audios):
            self._parse(audio)

    ##
    # Parses an audio file
    #
    # @param audio Audio file to parse.
    #
    def _parse(self, audio):
        print "Parsing", audio, "..."

        file = AudioSegment.from_wav(audio)
        chunks = split_on_silence(
            file,
            min_silence_len=self.silenceLength,
            silence_thresh=self.silenceThresh
        )

        for i, chunk in enumerate(chunks):
            self.chunks += 1
            out = "{0}/{1}.wav".format(self.chunksPath, self.chunks)

            print "Exporting {0} -> {1}/{2}.wav...".format(audio, self.chunksPath, self.chunks)
            chunk.export(out, format="wav")

##
# Mirai class.
# ============
#
# Mixes random chunks into a file.
#
# The constructor accepts as parameter the path
# to the chunks and the path to save the mixed audio.
#
# Once instantiated, call the method `start` which
# accepts as parameter the length of the audio.
#
# @author Manulaiko <manulaiko@gmail.com>
#
class Mirai:
    ##
    # Constructor.
    #
    # @param chunks Path to the chunks
    # @param mixed  Path to save the audio.
    #
    def __init__(self, chunks, mixed):
        self.chunks     = chunks
        self.chunksList = glob("{0}/*.wav".format(chunks))
        self.mixed      = mixed

    ##
    # Mixes random chunks
    #
    # @param length Seconds of the audio.
    #
    def start(self, length):
        if len(self.chunks) < 1:
            print "No chunks found!"

            pass

        print "Generating audio file..."
        audio  = AudioSegment.from_wav(choice(self.chunksList))
        while audio.duration_seconds < length:
            audio = audio + AudioSegment.from_wav(choice(self.chunksList))

            print "Generated audio:", audio.duration_seconds, "/", length

        name = "{0}/{1}.mp3".format(self.mixed, time())
        print "Exporting to", name, "..."
        audio.export(name, format="mp3")
        print "Done, file exported to", name


def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]

    return opts

if __name__ == '__main__':
    args = getopts(argv)

    option        = "all"
    audioPath     = "audio"
    chunksPath    = "chunks"
    mixedPath     = "mixed"
    silenceLength = 500
    silenceThresh = -26

    if '-a' in args:
        audioPath = args['-a']
    if '-c' in args:
        chunksPath = args['-c']
    if '-m' in args:
        mixedPath = args['-m']
    if '-l' in args:
        silenceLength = args['-l']
    if '-t' in args:
        silenceThresh = args['-t']
    if '-o' in args:
        option = args['-o']
    if '-h' in args:
        print "Usage: python kaguya.py [Options]"
        print "Options:"
        print "  -a path    Path to save the downloaded audios (default: ./audio)"
        print "  -c path    Path to save the chunked audios (default: ./chunks)"
        print "  -m path    Path to save the mixed audios (default: ./mixed)"
        print "  -l ms      Milliseconds of silence to split audio (default: 500)"
        print "  -t dbfs    Minimum dBFS of silence (default -26)"
        print "  -o option  Option to execute (default: all)"
        print "             'all': Download videos, chunk them, mix them"
        print "             'download': Just download videos"
        print "             'chunk': Chunk downloaded audios"
        print "             'mix': Mix chunked audios"
        quit()

    if option == "all" or option == "download":
        videos = []
        video  = ""
        
        print "Enter videos to download ('exit' to stop): "
        video = raw_input()

        while video != "exit":
            videos.append(video)
            print "Enter videos to download ('exit' to stop): "
            video = raw_input()

        downloader = Kizuna(videos, audioPath)
        downloader.start()

    if option == "all" or option == "chunk":
        parser = Kaguya(audioPath, chunksPath, silenceLength, silenceThresh)
        parser.start()

    if option == "all" or option == "mix":
        mixer =  Mirai(chunksPath, mixedPath)

        print "Enter length of mixed audio in seconds (0 = exit):"
        length = int(raw_input())

        while length > 0:
            mixer.start(length)

            print "Enter length of mixed audio in seconds (0 = exit):"
            length = int(raw_input())