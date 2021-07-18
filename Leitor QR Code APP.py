from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from pyzbar.pyzbar import decode
from playsound import playsound
import time


code = 0
data_atual = time.localtime()
data_hora = {'ano': data_atual.tm_year,
             'mes': data_atual.tm_mon,
             'dia': data_atual.tm_mday,
             'hora': data_atual.tm_hour,
             'dia da semana': data_atual.tm_wday
             }

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

            for barcode in decode(frame):
                myData = barcode.data.decode('utf-8')
                #print(myData)

                dia_v = myData[0:2]
                mes_v = myData[2:4]
                ano_v = myData[4:]

                if (int(data_hora['mes'])) > (int(mes_v)) or (int(data_hora['ano'])) > (int(ano_v)):
                    #print('passou da validade')
                    playsound('Fora da validade.mp3')
                elif (int(data_hora['dia'])) > (int(dia_v)) and (int(data_hora['mes']) == (int(mes_v))) and \
                        (int(data_hora['ano']) == (int(ano_v))):
                    #print('passou da validade')
                    playsound('Fora da validade.mp3')

                else:
                    #print('dentro da validade')
                    playsound('Dentro da validade.mp3')

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