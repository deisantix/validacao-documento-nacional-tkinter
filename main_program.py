import sys
import tkinter as tk
from validation_classes.constants_dv import *
from validation_classes.classes_validacao_info import *

"""
Classe de interface para validação de documentos no formato nacional brasileiro
feito com Tkinter
"""


class DocumentValidator(tk.Frame):
    def __init__(self, width, height, master: tk.Tk = None):
        super().__init__(master)

        """
        Criação da janela do programa
        """
        self.master = master
        self.master.title("Validação de Documentação")
        self.master.geometry(f"{width}x{height}")
        self.master.config(bg=window_bg_color)

        self.master.minsize(1200, 700)
        # self.master.maxsize(master.winfo_screenwidth(), master.winfo_screenheight())

        self.screen_focus = self.master.bind("<Button-1>", lambda event: self.close_gender_listbox_clicking_outside())

        """
        Todas as funções que desenham coisas na tela
        Em ordem:
        - criar caixa separadora onde ficam as caixas de entrada
        - criar labels de erro que mudam em caso de necessidade
        - criar header da página
        - criar heading (texto grande)
        - criar caixa de entrada do nome
        - criar lista de gêneros para seleção                                       |
        - criar canvas que desenha por cima da lista para parecer que não há lista  |-> seleção de gênero
        - criar botão que faz a lista aparecer e desaparecer                        |
        - criar caixa de entrada de email
        - criar caixa de entrada telefone
        - criar caixa de entrada de _cpf
        - criar caixa de entrada cep                    |
        - criar caixa de entrada estado                 |
        - criar caixa de entrada cidade                 |
        - criar caixa de entrada bairro                 |-> endereço
        - criar caixa de entrada logradouro             |
        - criar caixa de entrada do numero do endereço  |
        - criar caixa de entrada complemento            |
        - criar linha que separa as caixas de entrada com os botões
        - criar botão de concluir/submeter (ou Enter)
        - criar botão de sair (ou Esc)
        """
        self.create_separator_box()
        self.create_errors_labels()
        self.create_header()
        self.create_heading()

        self.create_name_widgets()
        self.create_birthday_widgets()

        self.gender_list_selection()
        self.gender_listbox_deactivate()
        self.gender_button()

        self.create_email_widgets()
        self.create_telefone_widgets()
        self.create_cpf_widgets()

        self.create_cep_widgets()
        self.cep_button_search()

        self.create_estado_widgets()
        self.create_cidade_widgets()
        self.create_bairro_widgets()
        self.create_logradouro_widgets()
        self.create_numend_widgets()
        self.create_complemento_widgets()

        self.create_fineline()
        self.create_concluir_widgets()
        self.create_exit_widgets()


    """
    PARTE DE CIMA DA PÁGINA
    """
    def create_header(self):
        # header
        self.c = tk.Canvas(
            self.master,
            width=self.master.winfo_screenwidth(),
            height=50,
            bg=header_bg_color
        )
        self.c.create_text(
            115, 25,
            text="ValDoc BancoTM",
            font="Times 20 bold",
            fill="white"
        )
        self.c.pack(
            side="top",
            pady=0
        )

    def create_heading(self):
        self.heading = tk.Label(
            self.master,
            text="Insira suas informações pessoais",
            font="Times 32 bold",
            bg=window_bg_color,
        )
        self.heading.pack()
        self.heading.place(x=20, y=100)

    def create_separator_box(self):
        self.canvas_box = tk.Canvas(
            self.master,
            width=self.master.winfo_screenwidth() - 40,
            height=self.master.winfo_screenheight() - 300,
            bg=sepbox_bg_color
        )
        self.canvas_box.pack()
        self.canvas_box.place(x=20, y=160)

    def create_errors_labels(self):
        self.error_name_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_birthday_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_gender_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_email_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_telefone_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_cpf_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_cep_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_estado_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_cidade_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_bairro_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_logradouro_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )
        self.error_numend_text = tk.Label(
            self.master,
            text="",
            fg="red3",
            font="Times 12",
            bg=sepbox_bg_color
        )


        self.obligatory = lambda: tk.Label(
            self.master,
            text="*",
            fg="red3",
            bg=sepbox_bg_color
        )

    """
    # começo de caixas de entrada
    CAIXA DE ENTRADA PARA INSERÇÃO DO NOME
    """
    def create_name_widgets(self):
        self.name_label = tk.Label(
            self.master,
            text="Nome completo do usuário:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        # self.name_var = tk.StringVar()
        self.name_entry_box = tk.Entry(
            self.master,
            # textvariable=self.name_var,
            font=f"Times {FONT_SIZE}",
            width=90
        )

        self.name_label.place(x=NAME_ENTRY_BOX_X, y=NAME_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=NAME_ENTRY_BOX_X + 210, y=NAME_ENTRY_BOX_Y - 23)
        self.name_entry_box.place(x=NAME_ENTRY_BOX_X, y=NAME_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA DE DATA DE NASCIMENTO
    """
    def create_birthday_widgets(self):
        self.birth_label = tk.Label(
            self.master,
            text="Data de nascimento:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )

        self.birth_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=23
        )

        self.birth_label.place(x=BIRTHDAY_ENTRY_BOX_X, y=BIRTHDAY_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=BIRTHDAY_ENTRY_BOX_X + 160, y=BIRTHDAY_ENTRY_BOX_Y - 23)
        self.birth_entry_box.place(x=BIRTHDAY_ENTRY_BOX_X, y=BIRTHDAY_ENTRY_BOX_Y)

    """
    INTERFACE DE SELEÇÃO DE GÊNERO
    """
    def gender_button(self):
        self.gender_listbox = "desativado"

        self.gender_b = tk.Button(
            self.master,
            name="genderButton",
            text="Selecione aqui",
            bg=sepbox_bg_color,
            relief="flat",
            width=19,
            height=1,
            anchor="w",
            padx=3,
            command=lambda: self.activate_gender_listbox("button")
        )
        self.gender_b.pack()
        self.gender_b.place(x=GENDER_BOX_X, y=GENDER_BOX_Y + 2)

    def gender_list_selection(self):
        # gender label - text above the list
        self.gender_label = tk.Label(
            self.master,
            text="Selecione seu gênero:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        # gender listbox creation
        self.gender_selection = tk.Listbox(
            self.master,
            selectmode="single",
            height=4
        )
        self.gender_label.place(x=GENDER_BOX_X, y=GENDER_BOX_Y - 25)
        self.obligatory().place(x=GENDER_BOX_X + 165, y=GENDER_BOX_Y - 23)
        self.gender_selection.pack(expand="NO", fill="y")
        self.gender_selection.place(x=GENDER_BOX_X, y=GENDER_BOX_Y + 30)

        gender_list = ("Selecione aqui", "Masculino", "Feminino", "Não-binário")

        for each_item in range(len(gender_list)):
            self.gender_selection.insert("end", gender_list[each_item])

        self.gender_selection.bind("<Double-Button-1>", lambda event: self.change_gender_var())

    def gender_listbox_deactivate(self):
        self.gender_listbox_deactive = tk.Canvas(
            self.master,
            width=165,
            height=77,
            bg=sepbox_bg_color,
            highlightthickness=0,
            bd=0
        )
        self.gender_listbox_deactive.place(x=GENDER_BOX_X, y=GENDER_BOX_Y + 32)

    """
    BACKEND DE SELEÇÃO DE GÊNERO
    - faz a lista aparecer ou sumir quando apertado no botão abaixo de "Selecione seu gênero"
        # que é um botão, embora foi feito para não parecer ser um
    - muda o texto dentro do botão e fecha automaticamente
    """
    def change_gender_var(self):
        if self.gender_selection.curselection() != ():
            self.gender_b['text'] = self.gender_selection.get('anchor')
            self.activate_gender_listbox()

    def close_gender_listbox_clicking_outside(self):
        screen_focus = self._return_screen_focus()

        if self.gender_listbox == "ativado" and ".!listbox" not in screen_focus:
            self.activate_gender_listbox()

    def activate_gender_listbox(self, come_from=None):
        gender_functions = {
            "ativado": self.gender_list_selection,
            "desativado": self.gender_listbox_deactivate
        }

        if come_from == "button":
            self.gender_listbox = "ativado"
        else:
            self.gender_listbox = "desativado"

        gender_functions[self.gender_listbox]()

    """
    CAIXA DE ENTRADA PARA INSERÇAO DO EMAIL
    """
    def create_email_widgets(self):
        self.email_label = tk.Label(
            self.master,
            text="Email do usuário:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.email_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=40
        )

        self.email_label.place(x=EMAIL_ENTRY_BOX_X, y=EMAIL_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=EMAIL_ENTRY_BOX_X + 135, y=EMAIL_ENTRY_BOX_Y - 23)
        self.email_entry_box.place(x=EMAIL_ENTRY_BOX_X, y=EMAIL_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA INSERÇÃO DE NÚMERO DE TELEFONE CELULAR
    """
    def create_telefone_widgets(self):
        self.telefone_label = tk.Label(
            self.master,
            text="Telefone do usuário:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )

        self.telefone_text = tk.StringVar()
        self.telefone_text.set("+55 ")

        self.telefone_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            textvariable=self.telefone_text
        )

        self.telefone_label.place(x=TELEFONE_ENTRY_BOX_X, y=TELEFONE_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=TELEFONE_ENTRY_BOX_X + 155, y=TELEFONE_ENTRY_BOX_Y - 23)
        self.telefone_entry_box.place(x=TELEFONE_ENTRY_BOX_X, y=TELEFONE_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA INSERÇÃO DO CPF ou CNPJ
    """
    def create_cpf_widgets(self):
        self.cpf_label = tk.Label(
            self.master,
            text="CPF/CNPJ:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        # self.cpf_variant = tk.StringVar()
        self.cpf_entry_box = tk.Entry(
            self.master,
            # textvariable=self.cpf_variant,
            font=f"Times {FONT_SIZE}"
        )

        self.cpf_label.place(x=CPF_ENTRY_BOX_X, y=CPF_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=CPF_ENTRY_BOX_X + 90, y=CPF_ENTRY_BOX_Y - 23)
        self.cpf_entry_box.place(x=CPF_ENTRY_BOX_X, y=CPF_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA CEP
    """
    def create_cep_widgets(self):
        self.cep_label = tk.Label(
            self.master,
            text="CEP:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.cep_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}"
        )

        self.cep_label.place(x=CEP_ENTRY_BOX_X, y=CEP_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=CEP_ENTRY_BOX_X + 45, y=CEP_ENTRY_BOX_Y - 23)
        self.cep_entry_box.place(x=CEP_ENTRY_BOX_X, y=CEP_ENTRY_BOX_Y)

    def cep_button_search(self):
        self.search_button = tk.PhotoImage(file='validation_classes/search_symbol.png')

        sb_dummy = tk.Button(
            self.master,
            image=self.search_button,
            borderwidth=0,
            bg="gray60",
            command=self.fill_address_cep
        )
        sb_dummy.place(x=CEP_ENTRY_BOX_X + 185, y=CEP_ENTRY_BOX_Y)

    def fill_address_cep(self):
        self.address_info = self._verify_cep_informations()[1]

        if type(self.address_info) == dict:
            self.estado_var.set(self.address_info["uf"])
            self.cidade_var.set(self.address_info["localidade"])
            self.bairro_var.set(self.address_info["bairro"])
            self.logradouro_var.set(self.address_info["logradouro"])
            self.complemento_var.set(self.address_info["complemento"])

    """
    CAIXA DE ENTRADA PARA ESTADO
    """
    def create_estado_widgets(self):
        self.estado_label = tk.Label(
            self.master,
            text="Estado:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.estado_var = tk.StringVar()
        self.estado_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=25,
            textvariable=self.estado_var
        )

        self.estado_label.place(x=ESTADO_ENTRY_BOX_X, y=ESTADO_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=ESTADO_ENTRY_BOX_X + 60, y=ESTADO_ENTRY_BOX_Y - 23)
        self.estado_entry_box.place(x=ESTADO_ENTRY_BOX_X, y=ESTADO_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA CIDADE
    """
    def create_cidade_widgets(self):
        self.cidade_label = tk.Label(
            self.master,
            text="Cidade:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.cidade_var = tk.StringVar()
        self.cidade_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=25,
            textvariable=self.cidade_var
        )

        self.cidade_label.place(x=CIDADE_ENTRY_BOX_X, y=CIDADE_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=CIDADE_ENTRY_BOX_X + 60, y=CIDADE_ENTRY_BOX_Y - 23)
        self.cidade_entry_box.place(x=CIDADE_ENTRY_BOX_X, y=CIDADE_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA BAIRRO
    """
    def create_bairro_widgets(self):
        self.bairro_label = tk.Label(
            self.master,
            text="Bairro:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.bairro_var = tk.StringVar()
        self.bairro_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=25,
            textvariable=self.bairro_var
        )

        self.bairro_label.place(x=BAIRRO_ENTRY_BOX_X, y=BAIRRO_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=BAIRRO_ENTRY_BOX_X + 55, y=BAIRRO_ENTRY_BOX_Y - 23)
        self.bairro_entry_box.place(x=BAIRRO_ENTRY_BOX_X, y=BAIRRO_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA LOGRADOURO
    """
    def create_logradouro_widgets(self):
        self.logradouro_label = tk.Label(
            self.master,
            text="Logradouro:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.logradouro_var = tk.StringVar()
        self.logradouro_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=30,
            textvariable=self.logradouro_var
        )

        self.logradouro_label.place(x=LOGRADOURO_ENTRY_BOX_X, y=LOGRADOURO_ENTRY_BOX_Y - 25)
        self.obligatory().place(x=LOGRADOURO_ENTRY_BOX_X + 95, y=LOGRADOURO_ENTRY_BOX_Y - 23)
        self.logradouro_entry_box.place(x=LOGRADOURO_ENTRY_BOX_X, y=LOGRADOURO_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA NUMERO DO ENDERECO
    """
    def create_numend_widgets(self):
        self.numend_label = tk.Label(
            self.master,
            text="Número:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.numend_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=10
        )

        self.numend_label.place(x=NUMEND_ENTRY_BOX_X, y=NUMEND_ENTRY_BOX_Y - 25)
        self.numend_entry_box.place(x=NUMEND_ENTRY_BOX_X, y=NUMEND_ENTRY_BOX_Y)

    """
    CAIXA DE ENTRADA PARA COMPLEMENTO
    """
    def create_complemento_widgets(self):
        self.complemento_label = tk.Label(
            self.master,
            text="Complemento:",
            font=f"Times {FONT_SIZE}",
            bg=sepbox_bg_color
        )
        self.complemento_var = tk.StringVar()
        self.complemento_entry_box = tk.Entry(
            self.master,
            font=f"Times {FONT_SIZE}",
            width=32,
            textvariable=self.complemento_var
        )

        self.complemento_label.place(x=COMPLEMENTO_ENTRY_BOX_X, y=COMPLEMENTO_ENTRY_BOX_Y - 25)
        self.complemento_entry_box.place(x=COMPLEMENTO_ENTRY_BOX_X, y=COMPLEMENTO_ENTRY_BOX_Y)

    """
    LINHA PARA SEPARAR AS CAIXAS DOS BOTÕES
    """
    def create_fineline(self):
        self.fineline = tk.Canvas(
            self.master,
            width=self.master.winfo_screenwidth() - 280,
            height=1,
            bg=window_bg_color
        )
        self.fineline.place(x=110, y=540)

    """
    BOTÃO DE CONCLUSÃO
    """
    def create_concluir_widgets(self):
        # BOTÃO DE CONCLUIR
        self.concluir = tk.Button(
            self.master,
            text="Concluir",
            height=2,
            width=10,
            command=self.concluir_return,
            bg=header_bg_color,
            fg="white",
            relief="groove",
            activebackground=window_bg_color,
            activeforeground=header_bg_color
        )
        self.concluir.place(x=110, y=560)
        self.master.bind("<Return>", lambda event: self.concluir_return())

    """
    BOTÃO DE SAIR
    """
    def create_exit_widgets(self):
        self.exit = tk.Button(
            self.master,
            text="Sair",
            height=2,
            width=10,
            command=sys.exit,
            bg=window_bg_color,
            fg="black",
            relief="groove",
            activebackground=header_bg_color,
            activeforeground=window_bg_color
        )
        self.exit.place(x=260, y=560)
        self.master.bind("<Escape>", lambda event: sys.exit())

    """
    FUNÇÃO QUE VERIFICA TODAS AS INFORMAÇÕES
    APÓS CLICAR NO BOTÃO DE CONCLUSÃO
    """
    def concluir_return(self):
        self.funcoes_verifica = [
            self._verify_name_informations,
            self._verify_birthday_informations,
            self._verify_gender_informations,
            self._verify_telefone_informations,
            self._verify_email_informations,
            self._verify_cpf_informations,
            self._verify_cep_informations,
            self._verify_estado_informations,
            self._verify_cidade_informations,
            self._verify_bairro_informations,
            self._verify_logradouro_informations,
            self._verify_numend_informations,
            self._verify_complemento_informations
        ]
        self.tudo_valido = []

        for func in self.funcoes_verifica:
            x = func()[0]
            self.tudo_valido.append(x)

        if bool(False) not in self.tudo_valido:
            self.create_final_window()

    """
    FUNÇÕES DE VERIFICAÇÃO DAS INFORMAÇÕES
    """
    def _verify_name_informations(self):
        self.name_variavel = str(self.name_entry_box.get())
        self.name_verification = any(i.isdigit() for i in self.name_variavel)

        self.name_bool = False
        if not self.name_variavel:
            self.name_string = "Campo obrigatório"
        elif self.name_verification:
            self.name_string = "Por favor, insira um nome válido"
        elif len(self.name_variavel.split()) <= 2:
            self.name_string = "Por favor, insira seu nome completo"
        else:
            self.name_string = ""
            self.name_bool = True

        self.error_name_text.config(text=self.name_string)
        self.error_name_text.place(x=NAME_ENTRY_BOX_X, y=NAME_ENTRY_BOX_Y + 30)

        return self.name_bool, self.name_string

    def _verify_birthday_informations(self):
        self.birthday_variavel = str(self.birth_entry_box.get())
        self.birthday_object = DataByteBank(self.birthday_variavel)
        self.birthday_verification = DataByteBank.eh_valido(self.birthday_variavel)

        if not self.birthday_variavel:
            self.birth_string = "Campo obrigatório"
        elif not self.birthday_verification[0]:
            self.birth_string = self.birthday_verification[1]
        else:
            self.birth_string = ""

        self.error_birthday_text.config(text=self.birth_string)
        self.error_birthday_text.place(x=BIRTHDAY_ENTRY_BOX_X, y=BIRTHDAY_ENTRY_BOX_Y + 30)

        return self.birthday_verification

    def _verify_gender_informations(self):
        self.gender_var = False
        if self.gender_b["text"] != "Selecione aqui":
            self.gender_var = self.gender_b["text"]

        if (type(self.gender_var) == str) and (self.gender_var != "Selecione aqui"):
            self.gender_var = True
            self.gender_string = ""
        else:
            self.gender_var = False
            self.gender_string = "Gênero não selecionado"

        self.error_gender_text.config(text=self.gender_string)
        self.error_gender_text.place(x=GENDER_BOX_X + 170, y=GENDER_BOX_Y + 5)

        return self.gender_var, ""

    def _verify_email_informations(self):
        self.email_variavel = str(self.email_entry_box.get())
        self.email_verification = EmailByteBank.eh_valido(self.email_variavel)

        if not self.email_variavel:
            self.email_string = "Campo obrigatório"
        elif not self.email_verification[0]:
            self.email_string = self.email_verification[1]
        else:
            self.email_string = ""

        self.error_email_text.config(text=self.email_string)
        self.error_email_text.place(x=EMAIL_ENTRY_BOX_X, y=EMAIL_ENTRY_BOX_Y + 30)

        return self.email_verification

    def _verify_telefone_informations(self):
        self.telefone_variavel = str(self.telefone_entry_box.get())
        self.telefone_object = TelefoneByteBank(self.telefone_variavel)
        self.telefone_verification = TelefoneByteBank.eh_valido(self.telefone_variavel)

        if not self.telefone_variavel:
            self.telefone_string = "Campo obrigatório"
        elif not self.telefone_verification[0]:
            self.telefone_string = self.telefone_verification[1]
        else:
            self.telefone_string = ""

        self.error_telefone_text.config(text=self.telefone_string)
        self.error_telefone_text.place(x=TELEFONE_ENTRY_BOX_X, y=TELEFONE_ENTRY_BOX_Y + 30)

        return self.telefone_verification

    def _verify_cpf_informations(self):
        self.cpf_variavel = str(self.cpf_entry_box.get())

        if CPFByteBank.eh_valido(self.cpf_variavel)[0]:
            self.cpf_object = CPFByteBank(self.cpf_variavel)
            self.cpf_verification = CPFByteBank.eh_valido(self.cpf_variavel)

        elif CNPJByteBank.eh_valido(self.cpf_variavel)[0]:
            self.cpf_object = CNPJByteBank(self.cpf_variavel)
            self.cpf_verification = CNPJByteBank.eh_valido(self.cpf_variavel)

        else:
            self.cpf_verification = (False, "CPF ou CNPJ inválido")

        if not self.cpf_variavel:
            self.cpf_string = "Campo obrigatório"
        elif not self.cpf_verification[0]:
            self.cpf_string = self.cpf_verification[1]
        else:
            self.cpf_string = ""

        self.error_cpf_text.config(text=self.cpf_string)
        self.error_cpf_text.place(x=CPF_ENTRY_BOX_X, y=CPF_ENTRY_BOX_Y + 30)

        return self.cpf_verification

    def _verify_cep_informations(self):
        self.cep_variavel = str(self.cep_entry_box.get())
        self.cep_object = CEPByteBank(self.cep_variavel)
        self.cep_verification = CEPByteBank.eh_valido(self.cep_variavel)

        if not self.cep_variavel:
            self.cep_string = "Campo obrigatório"
        elif not self.cep_verification[0]:
            self.cep_string = self.cep_verification[1]
        else:
            self.cep_string = ""

        self.error_cep_text.config(text=self.cep_string)
        self.error_cep_text.place(x=CEP_ENTRY_BOX_X, y=CEP_ENTRY_BOX_Y + 30)

        return self.cep_verification

    def _verify_estado_informations(self):
        self.estado_variavel = str(self.estado_entry_box.get()).upper()
        estados_do_brasil = procurar_estados()[0]

        self.estado_bool = False
        if not self.estado_variavel:
            self.estado_string = "Campo obrigatório"
        elif (self.estado_variavel not in estados_do_brasil) and (self.estado_variavel not in estados_do_brasil.values()):
            self.estado_string = "Estado inválido"
        else:
            self.estado_string = ""
            self.estado_bool = True

        self.error_estado_text.config(text=self.estado_string)
        self.error_estado_text.place(x=ESTADO_ENTRY_BOX_X, y=ESTADO_ENTRY_BOX_Y + 30)

        return self.estado_bool, self.estado_string

    def _verify_cidade_informations(self):
        self.cidade_variavel = str(self.cidade_entry_box.get()).upper()

        self.cidade_bool = False
        if not self.cidade_variavel:
            self.cidade_string = "Campo obrigatório"

        elif self.cidade_variavel and not self.estado_variavel:
            self.cidade_string = "Informe o estado"

        elif self.cidade_variavel and self.estado_variavel:
            municipios = procurar_municipios_por_distrito(self.estado_variavel)

            if "erro" in municipios:
                self.cidade_string = "Estado inválido"
            elif self.cidade_variavel not in municipios:
                self.cidade_string = "Cidade inválida"
            else:
                self.cidade_string = ""
                self.cidade_bool = True

        else:
            self.cidade_string = ""
            self.cidade_bool = True

        self.error_cidade_text.config(text=self.cidade_string)
        self.error_cidade_text.place(x=CIDADE_ENTRY_BOX_X, y=CIDADE_ENTRY_BOX_Y + 30)

        return self.cidade_bool, self.cidade_string

    def _verify_bairro_informations(self):
        self.bairro_variavel = str(self.bairro_entry_box.get())

        self.bairro_bool = False
        if not self.bairro_variavel:
            self.bairro_string = "Campo obrigatório"
        elif len(self.bairro_variavel) < 5:
            self.bairro_string = "Bairro inválido"
        else:
            self.bairro_string = ""
            self.bairro_bool = True

        self.error_bairro_text.config(text=self.bairro_string)
        self.error_bairro_text.place(x=BAIRRO_ENTRY_BOX_X, y=BAIRRO_ENTRY_BOX_Y + 30)

        return self.bairro_bool, self.bairro_string

    def _verify_logradouro_informations(self):
        self.logradouro_variavel = str(self.logradouro_entry_box.get())

        self.logradouro_bool = False
        if not self.logradouro_variavel:
            self.logradouro_string = "Campo obrigatório"
        else:
            self.logradouro_string = ""
            self.logradouro_bool = True

        self.error_logradouro_text.config(text=self.logradouro_string)
        self.error_logradouro_text.place(x=LOGRADOURO_ENTRY_BOX_X, y=LOGRADOURO_ENTRY_BOX_Y + 30)

        return self.logradouro_bool, self.logradouro_string

    def _verify_numend_informations(self):
        self.numend_variavel = str(self.numend_entry_box.get())
        return True, ""

    def _verify_complemento_informations(self):
        self.complemento_variavel = str(self.complemento_entry_box.get())
        return True, ""

    def _return_screen_focus(self):
        return str(self.master.focus_get())

    """
    CRIAR NOVA JANELA PARA MOSTRAR
    OS RESULTADOS DO CADASTRO
    """
    def create_final_window(self):
        self.janela_conclusao = tk.Toplevel(self.master)
        self.janela_conclusao.geometry("500x500")
        self.janela_conclusao.bind("<Escape>", lambda event: sys.exit())
        self.janela_conclusao.config(bg=window_bg_color)

        info_cadastro = {
            "hora e dia": DataByteBank(),
            "nome": self.name_variavel,
            "data de nascimento": self.birthday_object.data_nascimento,
            "genero": self.gender_b["text"],
            "email": self.email_variavel,
            "telefone": self.telefone_object,
            "cpf/cnpj": self.cpf_object,
            "cep": self.cep_object,
            "estado": self.estado_variavel,
            "cidade": self.cidade_variavel,
            "bairro": self.bairro_variavel,
            "logradouro": self.logradouro_variavel,
            "numero": self.numend_variavel,
            "complemento": self.complemento_variavel
        }

        self.final_exit = tk.Button(
            self.janela_conclusao,
            text="Sair",
            height=2,
            width=10,
            command=sys.exit,
            bg=header_bg_color,
            fg=window_bg_color,
            relief="groove",
            activebackground=window_bg_color,
            activeforeground=header_bg_color
        )
        self.final_exit.pack(side="bottom", anchor="center", pady=10)

        x, y = 10, 10
        for rotulo, info in info_cadastro.items():
            rotulo_label = tk.Label(
                self.janela_conclusao,
                font=f"Times {FONT_SIZE}",
                text=f"{rotulo}:",
                bg=window_bg_color
            )
            info_label = tk.Label(
                self.janela_conclusao,
                font=f"Times {FONT_SIZE}",
                text=info,
                bg=window_bg_color
            )

            rotulo_label.place(x=x, y=y)
            info_label.place(x=x + 160, y=y)

            y += 30


if __name__ == '__main__':
    root = tk.Tk()
    doc_val = DocumentValidator(1200, 700, master=root)
    doc_val.mainloop()
