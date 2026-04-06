'''Exemplo de uso do widget Scale (Slider)''' #Botão que se movimenta
'''(.get)captura o valor'''#Não está sendo usado no evento

from customtkinter import *

class App(CTk):
    def __nit__(self):
        super().__init__()

        self.title("Exemplo do Scale")
        self.geometry('400x300')

        self.slider = CTkSlider(
            self,
            from_=0 #Vá de...
            to=100, #Até...
            width=200, #Largura
            height=30, #Altura
            button_color='green', #Cor do botão de arraste (obs: cores diferentes)
            progress_color='blue', #Preenchimento da escala fixa (obs: cores diferentes)
            fg_color='lightgray', #Preechimento do progresso (obs: cores diferentes)
            number_of_steps=3, #Número se saltos fixo do botão (._._.)/steps=10(._._._._._._._._._._)
        )

        self.slider.pack(pady=20)

    def slider_event(self, value):
        print(f'Valor selecionado: {value:.2f}')

if__name__ == "__main__":
app = App()
app.mainloop()
