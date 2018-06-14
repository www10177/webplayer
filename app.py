from flask import *
from moviepy.editor import *
import os 
from urllib.parse import unquote
from subprocess import call
from sys import argv
import threading
from random import choices,randint
import time
import json
app=Flask(__name__,static_url_path='/static',root_path='.')
videoPath = os.path.join('./','static/','video/')
tempPath= os.path.join('./','static/','temp/')
thumbPath = os.path.join('./','static/','thumb/')
ffmpegEXE = 'ffmpeg.exe'
exporting_threads = {}
class ExportingThread(threading.Thread):
    def __init__(self):
        self.progress = 0
        super().__init__()
    def run(self):
        self.progress += 10


def createMixAudio(basename, overlay):
    basePath = os.path.join(videoPath,basename)
    base = VideoFileClip(basePath)
    music = []
    length = base.duration / len(overlay)
    for clip in overlay: 
        video_clip= VideoFileClip(os.path.join(videoPath,clip))
        music.append(video_clip.audio.set_duration(length))
    concat = concatenate_audioclips(music)
    # clip = CompositeAudioClip([base.audio, concat]) # video + audio
    clip = CompositeAudioClip([ concat]) # audio
    audioFileName=os.path.join(tempPath,basename[:-3]+'wav')
    if os.path.isfile(audioFileName):
        os.remove(audioFileName)
    print(audioFileName)
    clip.write_audiofile(audioFileName,fps=44100, nbytes=2, buffersize=2000)
    return (os.path.join(tempPath,basename),basePath,audioFileName) # tempVideoName

def mixVideoAudio (pathTuple):
    tempVideoName,basePath,audioFileName = pathTuple
    if os.path.isfile(tempVideoName):
        os.remove(tempVideoName)
    call([ffmpegEXE, '-i', basePath, '-i', audioFileName, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-map', '0:v:0', '-map', '1:a:0', tempVideoName])# combine video stream and audio

def getVideoName():
    return [f for f in os.listdir(videoPath) if os.path.isfile(os.path.join(videoPath,f))] 

def checkAndCreateThumb():
    for file in getVideoName():
        thumbName = os.path.join(thumbPath,os.path.splitext(file)[0]+'.jpg')
        if not os.path.isfile(thumbName):
            call([ffmpegEXE,'-hide_banner','-loglevel', 'panic', '-i',os.path.join(videoPath,file), '-ss', '00:00:05.000', '-vframes', '1', thumbName])
            print('created thumbnail file %s' %thumbName)

@app.route('/')
def video():
    # global exporting_threads
    # thread_id = randint(0, 10000)
    # exporting_threads[thread_id] = ExportingThread()
    # print ('Progress Task id: #%s' % thread_id)
    return render_template('index.html',video=map(lambda x : os.path.splitext(x)[0],getVideoName()))
@app.route('/test/')
def run():
    def generate():
        yield 'waiting 5 seconds\n'
        for i in range(1, 101):
            time.sleep(0.05)
            if i % 10 == 0:
                yield '{}%\n'.format(i)
        yield 'done\n'

    return Response(generate(), mimetype='text/plain')

@app.route('/result/',methods=['GET','POST'])
def result():
    if request.method == 'GET':
        return 'QQ'
    if request.method == 'POST':
        # exporting_threads[thread_id].start()
        video = unquote(request.values.get('video').split('/')[-1])
        overlay = choices(getVideoName(),k=randint(1,len(getVideoName())))
        print(overlay)
        path = createMixAudio(video,overlay)
        mixVideoAudio(path)
        return render_template('result.html',video=video)

@app.route('/turing/',methods=['GET','POST'])
def turing():
    if request.method == 'GET':
        return 'QQ'
    if request.method == 'POST':
        video = unquote(request.values.get('video').split('/')[-1])
        overlay = choices(getVideoName(),k=randint(0,len(getVideoName())))
        mix(video,overlay)
        return render_template('turing.html',video=video)
if __name__ == '__main__':
    host = '127.0.0.1'
    if len(argv) ==2:
        host = argv[1]
    print('Video Path : %s' % videoPath )
    print('Temp Path : %s' % tempPath )
    print('Thumb Path : %s' % thumbPath )
    checkAndCreateThumb()
    app.run(host=host,debug=True,threaded=True,port=9487)


