import cv2
import os

output_dir = 'C:/Users/selectstar/Desktop/pm/로우데이터1_1/vlc-record-2022-05-18-16h17m01s-rtsp___192.168.1.8-'
filepath = 'C:/Users/selectstar/Desktop/pm/로우데이터1_1/vlc-record-2022-05-18-16h17m01s-rtsp___192.168.1.8-.mp4'
vidcap = cv2.VideoCapture(filepath) #'' 사이에 사용할 비디오 파일의 경로 및 이름을 넣어주도록 함

success, image = vidcap.read()

count = 1
success = True

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

while success:
    success, image = vidcap.read()
    #print('success', success)
    #print('image', image)
    if count % 5 == 0:
        cv2.imwrite(output_dir + '/%d.jpg' % (count // 5), image)
        print("saved image %d.jpg" % (count // 5))

    if cv2.waitKey(10) == 27:
        break
    count += 1
