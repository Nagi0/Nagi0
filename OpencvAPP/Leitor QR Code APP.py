from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from pyzbar.pyzbar import decode
from playsound import playsound

import time
from datetime import datetime
from datetime import datetime
from kivy.core.audio import SoundLoader


code = 0
data_atual = datetime.today()


def dates_dif(date_qr, current_date):
    return (date_qr - current_date).days


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.my_data = '0'
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

            for barcode in decode(frame):
                self.my_data = barcode.data.decode('utf-8')

                self.my_data = datetime.strptime(self.my_data, '%d/%m/%Y')
                try:
                    if dates_dif(self.my_data, data_atual) >= 0:
                        print('Dentro da Validade')
                        # self.dentro_sound.play()
                        # time.sleep(3)
                    else:
                        print('Fora da Validade')
                        # self.fora_sound.play()
                        # time.sleep(3)

                except:
                    pass
                    # self.invalido_sound.play()
                    # time.sleep(3)
            tecla = cv2.waitKey(2)

            if tecla == 27:
                ret.release()
                cv2.destroyAllWindows()


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        self.capture.release()


CamApp().run()
