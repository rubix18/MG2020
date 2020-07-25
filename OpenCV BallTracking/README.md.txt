# OpenCV Ball Tracking

This python script uses cascade classifiers to identify a sports ball. Once detected, the ball will be tracked with OpenCV trackers such as KCF or MOSSE. This should speed up the tracking a whole bunch. If the ball moves too fast or goes out of frame, and the object tracker loses it. The cascade classifier will kick in again and try to detect a ball.