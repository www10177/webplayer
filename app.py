from flask import *
from moviepy.editor import *
from os.path import join,abspath,isfile
from os import remove
from urllib.parse import unquote
from subprocess import call
app=Flask(__name__,static_url_path='/static')
videoPath = join('./','static/','video/')
tempPath= join('./','static/','temp/')
# @app.route('/')
# def index():
    # return("Hello FUCKING World")
#def close_clip(clip):
#    try:
#        clip.reader.close()
#        del clip.reader
#        if clip.audio != None:
 #           clip.audio.reader.close_proc()
  #          del clip.audio
   #     del clip
   # except: 
    #    print('qq')

def mix(basename, overlay):
    basePath = join(videoPath,basename)
    base = VideoFileClip(basePath)
    music = []
    length = base.duration / len(overlay)
    for clip in overlay: 
        video_clip= VideoFileClip(join(videoPath,clip))
        music.append(video_clip.audio.set_duration(length))
    concat = concatenate_audioclips(music)
    clip = CompositeAudioClip([base.audio, concat])
    audioFileName=join(tempPath,basename[:-3]+'wav')
    if isfile(audioFileName):
        remove(audioFileName)
    #audioFileName=(join(tempPath,'temp.wav'))
    print(audioFileName)
    clip.write_audiofile(audioFileName,fps=44100, nbytes=2, buffersize=2000)
   # close_clip(base)
   # for clip in music:
    #    close_clip(clip)
    tempVideoName = join(tempPath,basename)
    if isfile(tempVideoName):
        remove(tempVideoName)
    call(['./ffmpeg', '-i', basePath, '-i', audioFileName, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', '-map', '0:v:0', '-map', '1:a:0', tempVideoName])


@app.route('/')
def video():
    return render_template('index.html')


@app.route('/result/',methods=['GET','POST'])
def result():
    if request.method == 'GET':
        return 'QQ'
    if request.method == 'POST':
        video = unquote(request.values.get('video').split('/')[-1])
        overlay = ['Alan Walker - Alone.mp4','Alan Walker - Faded.mp4']
        mix(video,overlay)
        return render_template('result.html',video=video)
if __name__ == '__main__':

    app.run(host='192.168.2.100',debug=True,threaded=True,port=9487)


