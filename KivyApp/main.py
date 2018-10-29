from kivy.app import App
import kivy.uix.screenmanager as sp
import matplotlib.pyplot as plt
import libs.garden.garden_graph.backend_kivyagg as gr
from NumericalMethods.app_manager import GraphsBuilder
from kivy.properties import ObjectProperty


class Main(App):
    main_screen = None
    plot_screen = None
    error_screen = None

    def build(self):
        sm = sp.ScreenManager()
        Main.input_screen = InputScreen(name='input')
        Main.plot_screen = PlotScreen(name='Plot')
        Main.error_screen = ErrorScreen(name='error')
        sm.add_widget(Main.input_screen)
        sm.add_widget(Main.plot_screen)
        sm.add_widget(Main.error_screen)

        return sm


class InputScreen(sp.Screen):
    inp_x0 = ObjectProperty(None)
    inp_y0 = ObjectProperty(None)
    inp_n = ObjectProperty(None)
    inp_xn = ObjectProperty(None)
    btn1 = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.btn1.bind(on_press=self.callback)

    def callback(self, instance):
        data = self.inp_x0.text, self.inp_y0.text, self.inp_n.text, self.inp_xn.text
        try:
            if self.validate_data(data):
                Main.plot_screen.small_box.remove_widget(Main.plot_screen.graph)
                Main.error_screen.small_box.remove_widget(Main.error_screen.graph1)
                Main.error_screen.small_box.remove_widget(Main.error_screen.graph2)

                x0, y0, xn = [float(i) for i in [self.inp_x0.text, self.inp_y0.text,
                                                 self.inp_xn.text]]
                n = int(self.inp_n.text)

                gm = GraphsBuilder(x0, y0, n, xn)
                gf = gm.get_graph()
                error_gf = gm.local_error_graph()
                global_error_gf = gm.global_error_graph()
                Main.plot_screen.graph = gr.FigureCanvasKivyAgg(gf)
                Main.error_screen.graph1 = gr.FigureCanvasKivyAgg(error_gf)
                Main.error_screen.graph2 = gr.FigureCanvasKivyAgg(global_error_gf)
                Main.plot_screen.small_box.add_widget(Main.plot_screen.graph)
                Main.error_screen.small_box.add_widget(Main.error_screen.graph1)
                Main.error_screen.small_box.add_widget(Main.error_screen.graph2)
                self.parent.transition = sp.SlideTransition(direction='left')
                self.parent.current = "Plot"
            else:
                self.inp_x0.text, self.inp_y0.text, self.inp_n.text, self.inp_xn.text = ['WRONG DATA' for i in range(4)]

        except ValueError and ZeroDivisionError:
            self.inp_x0.text, self.inp_y0.text, self.inp_n.text, self.inp_xn.text = ['WRONG DATA' for i in range(4)]

    def validate_data(self, arr):
        if float(self.inp_x0.text) > float(self.inp_xn.text) or float(self.inp_n.text) <= 10 or float(self.inp_y0.text) == 0:
            return False

        return True


class PlotScreen(sp.Screen):
    main_box = ObjectProperty(None)
    small_box = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.graph = gr.FigureCanvasKivyAgg(plt.gcf())
        self.small_box.add_widget(self.graph)


class ErrorScreen(sp.Screen):
    main_box = ObjectProperty(None)
    small_box = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.graph1 = gr.FigureCanvasKivyAgg(plt.gcf())
        self.graph2 = gr.FigureCanvasKivyAgg(plt.gcf())
        self.small_box.add_widget(self.graph1)
        self.small_box.add_widget(self.graph2)


if __name__ == '__main__':
    Main().run()
