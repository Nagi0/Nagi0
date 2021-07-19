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

Builder.load_file("myapplayout.kv")


code = 0
data_atual = time.localtime()
data_hora = {'ano': data_atual.tm_year,
             'mes': data_atual.tm_mon,
             'dia': data_atual.tm_mday,
             'hora': data_atual.tm_hour,
             'dia da semana': data_atual.tm_wday
             }


class AndroidCamera(Camera):
    camera_resolution = (640, 480)

    def _camera_loaded(self, *largs):
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
            my_data = barcode.data.decode('utf-8')

            dia_v = my_data[0:2]
            mes_v = my_data[2:4]
            ano_v = my_data[4:]

            if (int(data_hora['mes'])) > (int(mes_v)) or (int(data_hora['ano'])) > (int(ano_v)):
                # print('passou da validade')
                sound = SoundLoader.load('Fora da validade.mp3')
                if sound:
                    sound.play()

            elif (int(data_hora['dia'])) > (int(dia_v)) and (int(data_hora['mes']) == (int(mes_v))) and \
                    (int(data_hora['ano']) == (int(ano_v))):
                # print('passou da validade')
                sound = SoundLoader.load('Fora da validade.mp3')
                if sound:
                    sound.play()

            else:
                # print('dentro da validade')
                sound = SoundLoader.load('Dentro da validade.mp3')
                if sound:
                    sound.play()

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
