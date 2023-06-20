from textual.app import App
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.validation import Number
from textual.widgets import *

class PecManager(App):
    CSS_PATH = "./style.css"
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Fecha o programa"),
        Binding("ctrl+h", "help", "Abre a tela de ajuda"),
    ]
    TITLE = "Movimentação Pecuária"
    def compose(self):
        yield Header(show_clock=True)
        with Container(classes='main_container'):
            yield Input(id="value", value='R$ ', placeholder="Valor",validators=[
                Number(minimum=0, maximum=999999)
            ])
            yield Input(id='description', placeholder="Descrição")
            with RadioSet():
                yield RadioButton('Entrada', name='type', value='entrada')
                yield RadioButton('Saída', name='type', value='saida')
        yield Footer()
        

if __name__ == "__main__":
    app = PecManager()
    app.run()