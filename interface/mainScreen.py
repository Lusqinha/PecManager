from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.validation import Number
from textual.widgets import Button, Header, Footer, Input, RadioSet, RadioButton, TabbedContent, TabPane, DataTable, Label
from rich.text import Text
from logic.system import PecuniaryManager

from datetime import datetime

# 30-12-2022 / "%d-%m-%Y"
DATE_FORMAT = "%d-%m-%Y"
DATE_FORMAT_PRINT = "%d/%m/%Y"

manager = PecuniaryManager()


class PecManager(App):

    CSS_PATH = "./style.css"
    
    TITLE = f"Gerenciamento de Caixa | R$ {manager.currency:.2f}"
     
    BINDINGS = [
        Binding("escape", "quit", "Fecha o programa"),
        Binding("f1", "show_tab('movimentacao')", "Aba de movimentação"),
        Binding("f2", "show_tab('relatorio')", "Aba de relatório"),
        Binding("f5", "change_sort", "Muda o método de ordenação da tabela")
    ]
    
    def action_quit(self):
        self.exit(0)
    
    def action_show_tab(self, tab: str):
        self.get_child_by_type(TabbedContent).active = tab
    
    def action_change_sort(self):
      next_method = self.sort_methods[(self.sort_methods.index(self.current_method) + 1) % len(self.sort_methods)]
      self.current_method = next_method  
      self.update_datatable(next_method)
    
    def get_rows(self):
        return self.manager.convert_db_to_rows()

    def select_sort_method(self, method: str="date"):
        methods = {
            'date' : sorted(self.rows[1:], key=lambda x: datetime.strptime(x[0], DATE_FORMAT_PRINT)),
            'category' : sorted(self.rows[1:], key=lambda x: x[3]),
            'value' : sorted(self.rows[1:], key=lambda x: x[1]),
            'category-value' : sorted(self.rows[1:], key=lambda x: (x[3], x[1])),
        }
        
        return methods[method]
    
    def update_datatable(self, method:str):
        self.rows = self.get_rows()
        self.datatable.clear()
        
        selected_sort = self.select_sort_method(method)
        
        for row in selected_sort[1:]:
            styled_row = [
                Text(str(cell), style="bold", justify="right") for cell in row
            ]
            self.datatable.add_row(*styled_row)

    def update_title(self):
        self.title = f"Gerenciamento de Caixa | R$ {manager.currency:.2f}"

    def compose(self) -> ComposeResult:
        self.currency = manager.currency
        self.manager = manager
        self.radioset_value = ""
        self.sort_methods = ['date', 'category', 'value', 'category-value']
        self.sort_methods_pt = {
            'date' : 'Data',
            'category' : 'Categoria',
            'value' : 'Valor',
            'category-value' : 'Categoria-Valor'
        }
        self.current_method = self.sort_methods[1]
        self.rows = self.get_rows()

        yield Header(show_clock=True)

        with TabbedContent(initial="movimentacao"):
            with TabPane("Movimentação", id="movimentacao", classes="main_container"):
                with Horizontal(classes="mini_container"):
                    self.input_value = Input(id="value", placeholder="Valor", validators=[
                        Number(minimum=0, maximum=999999)])
                    yield self.input_value

                    with RadioSet():
                        self.radio_entrada = RadioButton(
                            'Entrada', name='entrada')
                        self.radio_saida = RadioButton('Saída', name='saida')
                        yield self.radio_entrada
                        yield self.radio_saida

                with Horizontal(classes="description_container"):
                    self.input_description = Input(
                        id='description', placeholder="Descrição")
                    yield self.input_description

                with Horizontal(classes="button_container"):
                    yield Button("Registrar", name="register", id="register")
                    yield Button("Cancelar", name="cancel", id="cancel")

            with TabPane("Relatório", id="relatorio", classes="main_container"):
                
                
                yield Label(f"Filtro: {self.sort_methods_pt[self.current_method]}")
                self.datatable = DataTable(zebra_stripes=True)
                yield self.datatable
                self.datatable.add_columns(*self.rows[0])
                self.update_datatable(self.current_method)

        yield Footer()

    def on_mount(self) -> None:
        self.query_one(RadioSet).focus()
        

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.radioset_value = event.pressed.name
    
    def clear_inputs(self):
        self.input_value.value = ""
        self.input_description.value = ""
    
    @on(Button.Pressed)
    def register(self, event: Button.Pressed):
        if event.button.id == "register":
            try:
                data = {
                    'date': datetime.now().strftime(DATE_FORMAT),
                    'value': float(self.input_value.value),
                    'description': self.input_description.value,
                    'category': str(self.radioset_value)
                }
                self.manager.insert(data)
                self.clear_inputs()
                self.update_datatable(self.get_curent_method())
            except:
                self.clear_inputs()

        elif event.button.id == "cancel":
            self.clear_inputs()

        self.manager.calculate_currency()
        self.update_title()


if __name__ == "__main__":
    app = PecManager()
    app.run()
