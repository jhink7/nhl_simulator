import wpf

from System.Windows import Window

class temp(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'temp.xaml')
