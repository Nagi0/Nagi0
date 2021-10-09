from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

import numpy as np
import cv2
from pyzbar.pyzbar import decode
import time
from datetime import datetime

Builder.load_file("myapplayout.kv")

code = 0

data_atual = datetime.today()


def dates_dif(date_qr, current_date):
    return (date_qr - current_date).days


class AndroidCamera(Camera):
    camera_resolution = (640, 480)

    dentro_sound = None
    fora_sound = None
    invalido_sound = None
    my_data = '0'

    def _camera_loaded(self, *largs):
        if self.dentro_sound == None:
            self.dentro_sound = SoundLoader.load('Dentro da validade.wav')
            self.fora_sound = SoundLoader.load('Fora da validade.wav')
            self.invalido_sound = SoundLoader.load('Codigo Invalido.wav')
        self.texture = Texture.create(size=np.flip(self.camera_resolution), colorfmt='rgb')
        self.texture_size = list(self.texture.size)

    def on_tex(self, *l):
        if self._camera._buffer is None:
            return None
        frame = self.frame_from_buf()
        self.frame_to_screen(frame)
        super(AndroidCamera, self).on_tex(*l)

    def frame_from_buf(self):
        w, h = self.resolution
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))
        frame_bgr = cv2.cvtColor(frame, 93)
        return np.rot90(frame_bgr, 3)

    def frame_to_screen(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        for barcode in decode(frame):
            self.my_data = barcode.data.decode('utf-8')

            self.my_data = datetime.strptime(self.my_data, '%d/%m/%Y')

            try:
                if dates_dif(self.my_data, data_atual) >= 0:
                    # print('Dentro da Validade')
                    self.dentro_sound.play()
                    time.sleep(3)
                else:
                    # print('Fora da Validade')
                    self.fora_sound.play()
                    time.sleep(3)

            except:
                self.invalido_sound.play()
                time.sleep(3)

        cv2.putText(frame_rgb, str(self.my_data), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                    cv2.LINE_AA)

        flipped = np.flip(frame_rgb, 0)
        buf = flipped.tostring()
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

class MyLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()