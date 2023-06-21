from textual import on
from textual.app import App
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.validation import Number
from textual.widgets import *

from logic.system import PecuniaryManager

from datetime import datetime

# 30-12-2022 / "%d-%m-%Y"
DATE_FORMAT = "%d-%m-%Y"

manager = PecuniaryManager()

class PecManager(App):
    
    CSS_PATH = "./style.css"
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Fecha o programa"),
    ]
    TITLE = f"Gerenciamento de Caixa | R$ {manager.currency:.2f}"
    
    def update_title(self):
        self.title = f"Gerenciamento de Caixa | R$ {manager.currency:.2f}"
    
    def compose(self):
        self.currency = manager.currency
        self.manager = manager
        self.radioset_value = ""
        
        yield Header(show_clock=True)
        
        with Container(classes='main_container'):
            
            with Horizontal(classes="mini_container"):
                self.input_value = Input(id="value", placeholder="Valor",validators=[
                    Number(minimum=0, maximum=999999)])
                yield self.input_value
                
                with RadioSet():
                    self.radio_entrada = RadioButton('Entrada', name='entrada')
                    self.radio_saida = RadioButton('Saída', name='saida')
                    yield self.radio_entrada
                    yield self.radio_saida
                    
            with Horizontal(classes="description_container"):  
                self.input_description = Input(id='description', placeholder="Descrição")    
                yield self.input_description
                
            with Horizontal(classes="button_container"):
                yield Button("Registrar", name="register", id="register")
                yield Button("Cancelar", name="cancel", id="cancel")
            
        yield Footer()
        
    def on_mount(self) -> None:
        self.query_one(RadioSet).focus()
        
    def on_radio_set_changed(self, event: RadioSet.Changed):
        
        # capture the value of the radio button to be used in the register method
        self.radioset_value = event.pressed.name
        print(self.radioset_value)
        
    
    @on(Button.Pressed)
    def register(self, event: Button.Pressed):
        if event.button.id == "register":
            data = {
                'date': datetime.now().strftime(DATE_FORMAT),
                'value': float(self.input_value.value),
                'description': self.input_description.value,
                'category': str(self.radioset_value)
            }
            
            self.manager.insert(data)
            self.input_value.value = ""
            self.input_description.value = ""
        elif event.button.id == "cancel":
            self.input_value.value = ""
            self.input_description.value = ""
        
        self.manager.calculate_currency()
        self.update_title()
        

if __name__ == "__main__":
    app = PecManager()
    app.run()