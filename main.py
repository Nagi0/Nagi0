from kivy.app import App
from kivy.lang import Builder
from datetime import datetime
from playsound import playsound

data_atual = datetime.today()


def dates_dif(date_qr, current_date):
    return (date_qr - current_date).days


class MainApp(App):

    def build(self):
        return Builder.load_string(
"""
#:import ZBarCam kivy_garden.zbarcam.ZBarCam
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: qrcodecam
    Label:
        size_hint: None, None
        size: self.texture_size[0], 50
        text: ', '.join([str(symbol.data) for symbol in qrcodecam.symbols])
    Button:
        on_release:
            app.print_code(', '.join([str(symbol.data) for symbol in qrcodecam.symbols]))
            
"""
)

    def on_start(self):
        pass

    def print_code(self, code):
        code = code[2:12]
        code = str(code)
        try:
            code = datetime.strptime(code, '%d/%m/%Y')
            if dates_dif(code, data_atual) >= 0:
                print('Dentro da validade')
                playsound('Dentro da validade.mp3')

            else:
                print('Fora da validade')
                playsound('Fora da validade.mp3')

        except:
            print('Invalido')
            playsound('Código Inválido.mp3')


MainApp().run()