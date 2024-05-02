import cv2
from cvzone.HandTrackingModule import HandDetector
import paho.mqtt.client as paho
import time

try:
    btns = ["ON", "OFF"]
    data = 0

    def on_publish(client, userdata, mid):
        print("mid: " + str(mid)) 

    client = paho.Client(client_id=None)
    client.on_publish = on_publish
    client.connect('broker.mqttdashboard.com', 1883)
    client.loop_start()

    # Function to draw all buttons
    def Drawalll(frame, bl):
        for button in bl:
            # Load the appropriate image based on button text
            if button.text == "ON":
                img = cv2.imread(r"green.png", cv2.IMREAD_UNCHANGED)
            elif button.text == "OFF":
                img = cv2.imread(r"red.png", cv2.IMREAD_UNCHANGED)
            # Resize the image to make it 250x250
            img = cv2.resize(img, (250, 250))

            alpha = img[:, :, 3]

            for c in range(0, 3):
                frame[button.pos[1]:button.pos[1]+button.size[1], button.pos[0]:button.pos[0]+button.size[0], c] = \
                    img[:, :, c] * (alpha / 255.0) + frame[button.pos[1]:button.pos[1]+button.size[1],
                                                            button.pos[0]:button.pos[0]+button.size[0], c] * (1.0 - alpha / 255.0)
        return frame


    def hover(button):
        pass


    def pressed(button):
        global data

        img = cv2.imread(r"blue.png", cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (250, 250))
        alpha = img[:, :, 3]
        for c in range(0, 3):
            frame[button.pos[1]:button.pos[1]+button.size[1], button.pos[0]:button.pos[0]+button.size[0], c] = \
                img[:, :, c] * (alpha / 255.0) + frame[button.pos[1]:button.pos[1]+button.size[1],
                                                        button.pos[0]:button.pos[0]+button.size[0], c] * (1.0 - alpha / 255.0)
        cv2.imshow("vid", frame)
        cv2.waitKey(1000)

        Drawalll(frame, btnls)
        cv2.imshow("vid", frame)
        cv2.waitKey(1)


        if button.text == "ON":
            data = 1
        elif button.text == "OFF":
            data = 0
        (rc, mid) = client.publish('virtualnest', str(data), qos=1)

    class Button():
        def __init__(self, pos, text, size=[250, 250]):
            self.pos = pos
            self.size = size
            self.text = text

    btnls = [
        Button([50, 100], "ON"),
        Button([930, 100], "OFF")
    ]

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.85)
    while True:
        ret, frame = cap.read()
        hands, frame = detector.findHands(frame)
        frame = Drawalll(frame, btnls)
        if hands:
            lmlist1 = hands[0]['lmList']
            pix = lmlist1[8][0]
            piy = lmlist1[8][1]
            pmx = lmlist1[12][0]
            pmy = lmlist1[12][1]
            for button in btnls:
                x, y = button.pos
                w, h = button.size
                if (x < pix < x+w) and (y < piy < y+h):
                    hover(button)
                    if (x < pmx < x+w) and (y < pmy < y+h):
                        pressed(button)
        cv2.imshow("vid", frame)
        cv2.waitKey(1)

except Exception as e:
    print("The error is: ", e)
