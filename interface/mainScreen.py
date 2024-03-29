from textual import on
from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Grid
from textual.validation import Number
from textual.widgets import Button, Header, Footer, Input, RadioSet, RadioButton, TabbedContent, TabPane, DataTable, Label
from rich.text import Text
from logic.system import PecuniaryManager
from logic.utils import db_to_rows
from controller.manager import TransferManager

from datetime import datetime

# 30-12-2022 / "%d-%m-%Y"
DATE_FORMAT = "%d-%m-%Y"
DATE_FORMAT_PRINT = "%d/%m/%Y"

manager = PecuniaryManager()
transfers = TransferManager()


class PecManager(App):

    CSS_PATH = "./style.css"

    TITLE = f"Gerenciamento de Caixa | R$ {manager.cashier:.2f}"

    BINDINGS = [
        Binding("escape", "quit", "Sair"),
        Binding("f1", "show_tab('movimentacao')", "Movimentação"),
        Binding("f2", "show_tab('historico')", "Histórico"),
        Binding("f5", "change_sort", "Altera ordenação da tabela")
    ]

    def action_quit(self):
        self.exit(0)

    def action_show_tab(self, tab: str):
        self.get_child_by_type(TabbedContent).active = tab

    def action_change_sort(self):
        next_method = self.sort_methods[(self.sort_methods.index(
            self.current_method) + 1) % len(self.sort_methods)]
        self.current_method = next_method
        self.update_datatable(next_method)

    def get_rows(self):
        rows = db_to_rows(data=self.transfers.get_all(),
                          headers=[
                              ("Data", "Valor", "Descrição", "Categoria"),],
                          keys=['date', 'value', 'description', 'category'])

        return rows

    def select_sort_method(self, method: str = "date"):
        methods = {

            'date': sorted(self.rows[1:], key=lambda x: datetime.strptime(x[0], DATE_FORMAT_PRINT), reverse=True),
            'category': sorted(self.rows[1:], key=lambda x: x[3]),
            'value': sorted(self.rows[1:], key=lambda x: x[1], reverse=True),
            'category-value': sorted(self.rows[1:], key=lambda x: (x[3], x[1]), reverse=True),
            'default': self.rows[1:]
        }

        return methods[method]

    def update_datatable(self, method: str):
        self.rows = self.get_rows()
        self.datatable.clear()

        selected_sort = self.select_sort_method(method)
        self.update_title(extra=f"Ordem: {self.sort_methods_pt[method]}")

        for row in selected_sort:
            styled_row = [
                Text(str(cell), style="bold", justify="right") for cell in row
            ]
            self.datatable.add_row(*styled_row)

    def update_title(self, extra: str = ""):
        self.title = f"Gerenciamento de Caixa | R$ {manager.cashier:.2f} | {extra}"

    def compose(self) -> ComposeResult:
        self.currency = manager.cashier
        self.manager = manager
        self.transfers = transfers
        self.radioset_value = ""
        self.sort_methods = ['date', 'category',
                             'value', 'category-value', 'default']

        self.sort_methods_pt = {
            'date': 'Data',
            'category': 'Categoria',
            'value': 'Valor',
            'category-value': 'Categoria-Valor',
            'default': 'Padrão'
        }
        self.current_method = self.sort_methods[4]

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

            with TabPane("Histórico", id="historico", classes="main_container"):

                self.update_title(
                    extra=f"Ordem: {self.sort_methods_pt[self.current_method]}")

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
                    'date': datetime.now().strftime(DATE_FORMAT_PRINT),
                    'value': float(self.input_value.value),
                    'description': self.input_description.value,
                    'category': str(self.radioset_value)
                }
                self.transfers.insert(data)
                self.clear_inputs()
                self.update_datatable(self.current_method)

            except:
                self.clear_inputs()

        elif event.button.id == "cancel":
            self.clear_inputs()

        self.manager.calculate_cashier()
        self.update_title(
            extra=f"Ordem: {self.sort_methods_pt[self.current_method]}")


if __name__ == "__main__":
    app = PecManager()
    app.run()
