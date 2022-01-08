from kivy.app import App, Widget
from kivy.lang import Builder
from datetime import datetime
from dateutil import relativedelta
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.metrics import cm
import time


class ImageButton(ButtonBehavior, Image):
    pass


def dates_dif_v2(date_qr, current_date):
    dates_diff = relativedelta.relativedelta(date_qr, current_date)
    days = dates_diff.days
    mounths = dates_diff.months
    years = dates_diff.years
    return days, mounths, years


data_atual = datetime.today()


KV = """
<MyLayout>
    #:import ZBarCam kivy_garden.zbarcam.ZBarCam
    FloatLayout:
        size: root.width, root.height
        orientation: 'vertical'
        ImageButton:
            id: botao_calar
            source: "unmute.png"
            pos_hint:{"right": 1, "top": 1}
            size_hint: 1, 0.1
            on_release:
                root.calar_voz()
                app.calar_voz()
            font_size: 32
        ZBarCam:
            pos_hint:{"right": 1, "top": 0.90}
            size_hint: 1, 0.80
            id: qrcodecam
        Label:
            id: code_label
            pos_hint:{"right": 1, "top": 0.1}
            size_hint: 1, 0.1
            font_size: cm(1.0)
            text: app.print_code(', '.join([str(symbol.data) for symbol in qrcodecam.symbols]))
"""


class MyLayout(Widget):
    calar = False

    def calar_voz(self):
        if self.calar:
            self.calar = False
            self.ids.botao_calar.source = "unmute.png"
        else:
            self.calar = True
            self.ids.botao_calar.source = "mute.png"

    def print_code(self, code):
        code = code[2:12]
        code = str(code)
        self.ids.code_label.text = code


Builder.load_string(KV)


class MainApp(App):
    code = ''
    calar = False
    dia_sound = None
    dias_sound = None
    venceu_sound = None
    vence_sound = None
    vence_hoje_sound = None
    ano_sound = None
    anos_sound = None
    mes_sound = None
    meses_sound = None
    d = {}
    for i in range(32):
        d["{0} dias".format(i)] = None
    dentro_sound_sp2 = None
    fora_sound_sp2 = None

    def on_start(self):
        if self.dentro_sound_sp2 == None:
            self.dentro_sound_sp2 = SoundLoader.load('Dentro da validade 1.2x.wav')
            self.fora_sound_sp2 = SoundLoader.load('Fora da validade 1.2x.wav')
            self.vence_hoje_sound = SoundLoader.load('Vence hoje.wav')
            self.vence_sound = SoundLoader.load('Vence em.wav')
            self.venceu_sound = SoundLoader.load('Venceu a.wav')
            self.ano_sound = SoundLoader.load('Ano.wav')
            self.anos_sound = SoundLoader.load('Anos.wav')
            self.mes_sound = SoundLoader.load('Mes.wav')
            self.meses_sound = SoundLoader.load('Meses.wav')
            self.dia_sound = SoundLoader.load('Dia.wav')
            self.dias_sound = SoundLoader.load('Dias.wav')
            self.d = {}
            for i in range(32):
                self.d["{0} dias".format(i)] = SoundLoader.load('{} dias.wav'.format(i))

    def build(self):
        return MyLayout()

    def calar_voz(self):
        if self.calar:
            self.calar = False
        else:
            self.calar = True

    def print_code(self, code):
        code = code[2:12]
        code = str(code)
        if self.calar:
            return code
        try:
            code_dt = datetime.strptime(code, '%d/%m/%Y')
            dd_mm_yy = dates_dif_v2(code_dt, data_atual)
            if dd_mm_yy[0] >= 0 and dd_mm_yy[1] >= 0 and dd_mm_yy[2] >= 0:
                print(dd_mm_yy)
                # print('Dentro da validade')
                if dd_mm_yy[0] == 0:
                    self.vence_hoje_sound.play()
                    time.sleep(1.25)
                else:
                    self.dentro_sound_sp2.play()
                    time.sleep(1.75)
                    self.vence_sound.play()
                    time.sleep(1.5)

                    if abs(dd_mm_yy[2]) == 0:
                        pass
                    else:
                        self.d['{} dias'.format(abs(dd_mm_yy[2]))].play()
                        time.sleep(1.25)
                        if abs(dd_mm_yy[2]) == 1:
                            self.ano_sound.play()
                            time.sleep(1)
                        else:
                            self.anos_sound.play()
                            time.sleep(1)

                    if abs(dd_mm_yy[1]) == 0:
                        pass
                    else:
                        self.d['{} dias'.format(abs(dd_mm_yy[1]))].play()
                        time.sleep(1.25)
                        if abs(dd_mm_yy[1]) == 1:
                            self.mes_sound.play()
                            time.sleep(1)
                        else:
                            self.meses_sound.play()
                            time.sleep(1)

                    if abs(dd_mm_yy[0]) == 0:
                        pass
                    else:
                        self.d['{} dias'.format(abs(dd_mm_yy[0]))].play()
                        time.sleep(1.5)
                        if abs(dd_mm_yy[0]) == 1:
                            self.dia_sound.play()
                            time.sleep(1)
                        else:
                            self.dias_sound.play()
                            time.sleep(1)

            else:
                # print('Fora da validade')
                print(dd_mm_yy)
                self.fora_sound_sp2.play()
                time.sleep(1.75)
                self.venceu_sound.play()
                time.sleep(1.5)
                if abs(dd_mm_yy[2]) == 0:
                    pass
                else:
                    self.d['{} dias'.format(abs(dd_mm_yy[2]))].play()
                    time.sleep(1.25)
                    if abs(dd_mm_yy[2]) == 1:
                        self.ano_sound.play()
                        time.sleep(1)
                    else:
                        self.anos_sound.play()
                        time.sleep(1)

                if abs(dd_mm_yy[1]) == 0:
                    pass
                else:
                    self.d['{} dias'.format(abs(dd_mm_yy[1]))].play()
                    time.sleep(1.25)
                    if abs(dd_mm_yy[1]) == 1:
                        self.mes_sound.play()
                        time.sleep(1)
                    else:
                        self.meses_sound.play()
                        time.sleep(1)

                if abs(dd_mm_yy[0]) == 0:
                    pass
                else:
                    self.d['{} dias'.format(abs(dd_mm_yy[0]))].play()
                    time.sleep(1.5)
                    if abs(dd_mm_yy[0]) == 1:
                        self.dia_sound.play()
                        time.sleep(1)
                    else:
                        self.dias_sound.play()
                        time.sleep(1)

        except:
            return ''
        self.code = str(code)
        return self.code


MainApp().run()
