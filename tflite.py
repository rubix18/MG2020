# [USAGE]: python3 tflite.py --modeldir=model

# NOTES: 
# Press S to save replay 
# Press Q to quit 


# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
import threading
import importlib.util
import ffmpeg
import queue
import cameraCapture as cc
import requests
import tracemalloc
import socketio
import socket
from datetime import datetime


sio = socketio.Client()
sio.connect('http://10.3.141.1:5002', namespaces=['/test'])

# Import database client 
from dbclient import dbclient as db

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/

replay_flag = 1

# Import database client 
try:
    from dbclient.dbclient import (
        # functions
        update,             # usage: update(src_loc, ball_xy, players_xy)
        select_all,         # usage: select_all(table_name)
        replay_requested,   # usage: replay_requested(), returns 0 or 1 if replay has been requested by this pi
        send_replay,         # usage: send_replay()
        clear_replay
    )
except: 
    print("[TFLITE]: Database not found!")


class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(1920,950),framerate=5,camera=0):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(camera)
        self.queue = queue.Queue(300)
        #ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is stopped
        self.stopped = False
        
        # Variable to keep track of reply frame count
        self.postReplayCount = 0

    def start(self):
    # Start the thread that reads frames from the video stream
        #threading.Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        #while True:
            # If the camera is stopped, stop the thread
        if self.stopped:
            # Close camera resources
            self.stream.release()
            return

        # Otherwise, grab the next frame from the stream
        (self.grabbed, self.frame) = self.stream.read()
        
        
        # Update queue
        if not self.queue.full():
            self.queue.put(self.frame)
        else:
            f = self.queue.get()
            del f
            self.queue.put(self.frame)
            

    def read(self):
    # Return the most recent frame
        return self.frame

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True
        
    def saveStream(self, replayName, timestamp):
        global replay_flag
        frames = np.array(self.queue.queue)
        _, height, width, _ = frames.shape
        process = (
            ffmpeg
                .input('pipe:', format='rawvideo', r=15, pix_fmt='bgr24', s='{}x{}'.format(width, height))
                .output(replayName+'.mp4', pix_fmt='yuv420p', vcodec='libx264', preset='superfast')
                .overwrite_output()
                .run_async(pipe_stdin=True)
        )
        for frame in frames:
            process.stdin.write(
                frame
                    .astype(np.uint8)
                    .tobytes()
            )
        process.stdin.close()
        process.wait()
        file = open(replayName+'.mp4', 'rb')
#        try:
        send_replay(file)
        replay_flag = 1
#        except:
#          print("Send replay failed")
        
def sendToDatabase():
    pass

def saveVideoStream(q):
    frames = np.array(q.queue)
    _, height, width, _ = frames.shape
    process = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(width, height))
            .output('replay.mp4', pix_fmt='yuv420p', vcodec='libx264', r=15, preset='superfast')
            .overwrite_output()
            .run_async(pipe_stdin=True)
    )
    for frame in frames:
        process.stdin.write(
            frame
                .astype(np.uint8)
                .tobytes()
        )
    process.stdin.close()
    process.wait()
    file = open('replay.mp4', 'rb')
    send_replay(file)
#1280x720
def main():
    tracemalloc.start()
    # Define and parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                        default='model')
    parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                        default='detect.tflite')
    parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                        default='labelmap.txt')
    parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                        default=0.5)
    parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                        default='640x480')
    parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                        action='store_true')
    parser.add_argument('--camera', help='Choose camera input',
                        default=0)

    args = parser.parse_args()

    MODEL_NAME = args.modeldir
    GRAPH_NAME = args.graph
    LABELMAP_NAME = args.labels
    min_conf_threshold = float(args.threshold)
    resW, resH = args.resolution.split('x')
    imW, imH = int(resW), int(resH)
    camera = int(args.camera)
    use_TPU = args.edgetpu
   
    # Import TensorFlow libraries
    # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
    # If using Coral Edge TPU, import the load_delegate library
    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter
        if use_TPU:
            from tflite_runtime.interpreter import load_delegate
    else:
        from tensorflow.lite.python.interpreter import Interpreter
        if use_TPU:
            from tensorflow.lite.python.interpreter import load_delegate

    # If using Edge TPU, assign filename for Edge TPU model
    if use_TPU:
        # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
        if (GRAPH_NAME == 'detect.tflite'):
            GRAPH_NAME = 'edgetpu.tflite'       

    # Get path to current working directory
    CWD_PATH = os.getcwd()

    # Path to .tflite file, which contains the model that is used for object detection
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

    # Load the label map
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Have to do a weird fix for label map if using the COCO "starter model" from
    # https://www.tensorflow.org/lite/models/object_detection/overview
    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    # Load the Tensorflow Lite model.
    # If using Edge TPU, use special load_delegate argument
    if use_TPU:
        interpreter = Interpreter(model_path=PATH_TO_CKPT,
                                experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
        print(PATH_TO_CKPT)
    else:
        interpreter = Interpreter(model_path=PATH_TO_CKPT)

    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    # Initialize frame rate calculation
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    
    # Line detection code setup
    #image_file = 'line.jpg'
    field_file = 'field.jpg'

    point_list = []
    field_point = []
    cap = cv2.VideoCapture(0)
    cap.set(3,imW)
    cap.set(4,imH)
    
    test_img = cap.read() # Initial image
    bigW = 1920
    bigH = 950
    while True:
        ret, test_img = cap.read()
        test_img = cv2.resize(test_img,(imW,imH))
        imgGray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    
        cv2.imshow("image", test_img)
    
        if cv2.waitKey(1) & 0xFF == ord('c'):
                break
    
    
    cv2.imshow("image", test_img)
    # cv2.waitKey(0)

    #Here, you need to change the image name and it's path according to your directory
    # test_img = cv2.imread(image_file)
    # cv2.imshow("image", test_img)

    #calling the mouse click event
    while len(point_list) < 3: 
        cv2.setMouseCallback("image", cc.click_event, [test_img, point_list])
        cv2.waitKey(1)

    field_img = cv2.imread(field_file)
    field_img = cv2.resize(field_img,(imW,imH))
    cv2.imshow("field_image", field_img)

    #calling the mouse click event
    while len(field_point) < 3:
        cv2.setMouseCallback("field_image", cc.click_event_2, [field_img, field_point])
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    A_matrix, translation_vector = cc.affineMatrix(point_list, field_point)

    #print(point_list, field_point)

    # print("Transform new point:")
    # test_point = [625, 200]
    # image_p = np.dot(A_matrix, test_point) + translation_vector
    # print(test_point, " mapped to: ", image_p)
    # image = cv2.circle(field_img, (int(image_p[0]), int(image_p[1])), 2, (0, 0, 255), 10)

    cv2.destroyAllWindows()
    #print("Here 3")
    cap.release()
    time.sleep(5)

    # Initialize video stream
    videostream = VideoStream(resolution=(imW,imH),framerate=10, camera=camera).start()
    time.sleep(1)
    
    flag_in = 1
    
    eventType = "TestEvent"

    #for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
    while True:
#         first = tracemalloc.take_snapshot()
        videostream.update()
        
        if videostream.postReplayCount > 0:
            videostream.postReplayCount -= 1
            if videostream.postReplayCount == 0:
                now = datetime.now()
                timestamp = now.strftime("%H-%M-%S")
                videostream.saveStream(eventType, timestamp)
                #replayThread = threading.Thread(target=videostream.saveStream(eventType, timestamp))
                #replayThread.daemon = True
                #replayThread.start()

        # Start timer (for calculating frame rate)
        t1 = cv2.getTickCount()

        # Grab frame from video stream
        frame = videostream.read()

        # Acquire frame and resize to expected shape [1xHxWx3]
        #frame = frame1.copy()
        frame = cv2.resize(frame, (imW,imH))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)
        
        

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
        #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)


        # Initialise lists to store labels and centerpoints 
        centerpoints = []
        adjustedpoints = []
        detection_labels = []
        f_img = cv2.imread(field_file)
        f_img = cv2.resize(f_img, (imW,imH))

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                
                xcen = int(xmin + (xmax-xmin)/2) 
                #ycen = int(ymin + (ymax-ymin)/2) 
                ycen = int(ymax) 
                centerpoints.append((xcen, ycen))   # Append centerpoint to list of centerpoints to be sent to database 

                # Mark centerpoint on frame to make sure we have correct image centerpoint coords 
                frame[ycen-5:ycen+5, xcen-5:xcen+5] = (0, 0, 255)

                # Aplly affine matrix
                image_p = np.dot(A_matrix, (xcen,ycen)) + translation_vector
                adjustedpoints.append(image_p)
                
                #-------------EVENT DETECTION---------------------------------------
                max_x_out = imW*(1195/1280)
                max_y_out = imH*(688/720)
                min_x_out = imW*(85/1280)
                min_y_out = imH*(31/720)
                
                goal_y_min = imH*(409/950)
                goal_y_max = imH*(543/950)
                
                flag_out = 0
                flag_goal = 0
                
                cx = int(image_p[0])
                cy = int(image_p[1])
                
                #
                #person is 0 on list
                #sports ball is 36
                currentDetect = int(classes[i])
                if currentDetect == 0:
                    
                    if (cx < min_x_out) or (cx > max_x_out):
                        if(cy > goal_y_min) and (cy < goal_y_max):
                            flag_goal = 1
                        else:
                            flag_out = 1
                    if (cy < min_y_out) or (cy > max_y_out):
                        flag_out = 1
                        
                    #Plotting dots for visualization    
                    if flag_goal == 1:
                            field_image_with_point = cv2.circle(f_img, (int(image_p[0]), int(image_p[1])), 2, (255, 255), 10)
                    elif flag_out == 1:
                            field_image_with_point = cv2.circle(f_img, (int(image_p[0]), int(image_p[1])), 2, (255, 255, 255), 10)
                    else:
                        field_image_with_point = cv2.circle(f_img, (int(image_p[0]), int(image_p[1])), 2, (0, 255, 255), 10)
                        
                    
                    #Sending Message Should only occur once unless ball is back in
                    if flag_goal == 1 and flag_in == 1:
                            print("goalllll")
                            eventType = "Goal"
                            videostream.postReplayCount = 150
                            flag_in = 0
                            now = datetime.now()
                            timestamp = now.strftime("%H-%M-%S")
                            sio.emit('message', f"{socket.gethostname()}: Goal {timestamp}")
                    elif flag_out == 1 and flag_in == 1:
                            print("outtttt")
                            eventType = "OutOfBounds"
                            flag_in = 0
                            now = datetime.now()
                            timestamp = now.strftime("%H-%M-%S")
                            sio.emit('message', f"{socket.gethostname()}: Out {timestamp}")
                    elif flag_out == 0 and flag_goal == 0:
                        flag_in = 1
                        
                        
                elif currentDetect ==36:
                    field_image_with_point = cv2.circle(f_img, (int(image_p[0]), int(image_p[1])), 2, (0, 0, 255), 10)
                
                #if we want to see other detections on the map
                else:
                    field_image_with_point = cv2.circle(f_img, (int(image_p[0]), int(image_p[1])), 2, (0, 0, 0), 10)
                    
                cv2.imshow("adjusted_image", field_image_with_point)
                
                
                # Draw Bounding Box
                #COMMMENT THIS OUT WHEN WE DON"T NEED IT
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                detection_labels.append(object_name)    # Append object name to list of object names to be sent to database 
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text


        # Send results to database 
        # print(centerpoints, ', '.join(detection_labels))  # Debug print 
        # db.update('right hand corner', centerpoints, ', '.join(detection_labels), db.engine) # Use join() to send labels as single string 

        # Draw framerate in corner of frame
        cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
        #print("Frame rate:", frame_rate_calc)

        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc= 1/time1

        # Press 'q' to quit
        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Quitting")
            break
        elif key == ord('s'):
            print("Saving")
            eventType = "Request"
            # Begin count for post-event frames
            videostream.postReplayCount = 150
#             videostream.saveStream()

        # Instead of checking keypress, query database to see if request has been made for video file,
        # if yes, execute saveStream(), then post the video to server
        
        global replay_flag
        
        try: 
          if replay_requested() and replay_flag == 1:
              print("Saving Video File to Send To Server")
              # clear_replay()
              videostream.postReplayCount = 50
              replay_flag = 0
              
              # set flag to 0  
              # videostream.saveStream()
        except: 
            pass
            #print("[TFLITE]: Error! ")
            
            
#         snap = tracemalloc.take_snapshot()
#         stats = snap.compare_to(first, 'lineno')
#         print(stats[0])
#         print(stats[0].traceback.format())

        #cv2.waitKey(0)

    # Clean up
    
    cv2.destroyAllWindows()
    sio.disconnect()
    videostream.stop()


if __name__ == '__main__':
    main()
