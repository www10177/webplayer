from flask import *
from moviepy.editor import *
from os.path import join,abspath,isfile
from os import remove
from urllib.parse import unquote
from subprocess import call
from sys import argv
import threading
from random import randint
import time
app=Flask(__name__,static_url_path='/static',root_path='.')
videoPath = join('./','static/','video/')
tempPath= join('./','static/','temp/')
exporting_threads = {}
class ExportingThread(threading.Thread):
    def __init__(self):
        self.progress = 0
        super().__init__()
    def run(self):
        self.progress += 10


def createMixAudio(basename, overlay):
    basePath = join(videoPath,basename)
    base = VideoFileClip(basePath)
    music = []
    length = base.duration / len(overlay)
    for clip in overlay: 
        video_clip= VideoFileClip(join(videoPath,clip))
        music.append(video_clip.audio.set_duration(length))
    concat = concatenate_audioclips(music)
    # clip = CompositeAudioClip([base.audio, concat]) # video + audio
    clip = CompositeAudioClip([ concat]) # audio
    audioFileName=join(tempPath,basename[:-3]+'wav')
    if isfile(audioFileName):
        remove(audioFileName)
    print(audioFileName)
    clip.write_audiofile(audioFileName,fps=44100, nbytes=2, buffersize=2000)
    return (join(tempPath,basename),basePath,audioFileName) # tempVideoName

def mixVideoAudio (path):
    tempVideoName,basePath,audioFileName = path
    if isfile(tempVideoName):
        remove(tempVideoName)
    call(['./ffmpeg', '-i', basePath, '-i', audioFileName, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-map', '0:v:0', '-map', '1:a:0', tempVideoName])# combine video stream and audio


@app.route('/')
def video():
    # global exporting_threads
    # thread_id = randint(0, 10000)
    # exporting_threads[thread_id] = ExportingThread()
    # print ('Progress Task id: #%s' % thread_id)
    return render_template('index.html')
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
        overlay = ['Alan Walker - Alone.mp4','Alan Walker - Faded.mp4']
        path = createMixAudio(video,overlay)
        mixVideoAudio(path)
        return render_template('result.html',video=video)

@app.route('/turing/',methods=['GET','POST'])
def turing():
    if request.method == 'GET':
        return 'QQ'
    if request.method == 'POST':
        video = unquote(request.values.get('video').split('/')[-1])
        overlay = ['Alan Walker - Alone.mp4','Alan Walker - Faded.mp4']
        mix(video,overlay)
        return render_template('turing.html',video=video)
if __name__ == '__main__':
    host = '127.0.0.1'
    if len(argv) ==2:
        host = argv[1]
    
    app.run(host=host,debug=True,threaded=True,port=9487)


