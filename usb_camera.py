import cv2
cap = cv2.VideoCapture(5)
if not (cap.isOpened()):
    print("Could not open video device")
# The device number might be 0 or 1 depending on the device and the webcam
while cap.isOpened():
    print('capture in progress')
    success, frame = cap.read()
    cv2.imshow('Frame', frame)
    cv2.waitKey(0)
    if not success:
        print('No Image')
        break
cap.release()
cv2.destroyAllWindows()

# cap.open(0, cv2.CAP_DSHOW)
# while(True):
#     ret, frame = cap.read()
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()