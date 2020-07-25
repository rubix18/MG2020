import cv2

tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[6]
ballCascade = cv2.CascadeClassifier('ball_cascade.xml')

tracker = cv2.TrackerKCF_create()

cap = cv2.VideoCapture(0)

ret, img = cap.read()

success = False
ok = False

ball = ballCascade.detectMultiScale(img, 1.1, 4)
for (x, y, w, h) in ball:
    success = tracker.init(img, (x, y, w, h))

while True:
    ret, img = cap.read()
    if not ret:
        break
    if success:
        ok, bbox = tracker.update(img)

    if ok:
        cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), (0, 0, 255), 1)
    else:
        cv2.putText(img, "Tracking failed", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        ball = ballCascade.detectMultiScale(img, 1.1, 4)
        for (x, y, w, h) in ball:
            tracker = cv2.TrackerMOSSE_create()
            success = tracker.init(img, (x, y, w, h))

    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()