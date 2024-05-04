from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel
from PyQt5.QtGui import QColor, QTextCursor,QPixmap, QIcon
from PyQt5.QtCore import Qt
import re
import random

# Definición de la clase para la interfaz del chat
class ChatInterface(QWidget):
    def __init__(self):
        super().__init__() 
        #self.setWindowIcon()
        self.setWindowTitle("COVI-CHAT")
        self.setWindowIcon(QIcon("C:/Users/gonza/OneDrive/Escritorio/imagenes-proyecto/logo.jpg"))
        self.setStyleSheet("QWidget {"
                      "background-color: #f0f0f0;"  # Color de fondo de la ventana
                  "}")

        self.setup_ui()
# Método para configurar la interfaz de usuario
    def setup_ui(self):
        self.layout = QVBoxLayout()

        

        self.chat_display = QTextEdit()  # Cuadro de texto para mostrar el chat
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        self.input_layout = QHBoxLayout() # Diseño horizontal para el cuadro de entrada y el botón de enviar
        self.input_box = QLineEdit()       # Cuadro de entrada de texto
        self.input_box.setPlaceholderText("Escriba su mensaje aquí")
        #Estilo del cuadro de entrada
        self.input_box.setStyleSheet("QLineEdit {"
                                "background-color: #f0f0f0;"
                                "border: 2px solid #ccc;"
                                "border-radius: 5px;"
                                "padding: 5px;"
                                "}"
                                "QLineEdit:focus {"
                                "border-color: #0084ff;"
                                "}"
                                "QLineEdit::placeholder {"
                                "color: #999;"  # Color del texto de marcador de posición
                                "}"
                                )

        self.send_button = QPushButton("Enviar")  #Boton enviar
        self.send_button.setStyleSheet("QPushButton {" #estilos del boton enviar
                                "background-color: #0084ff;"
                                "color: white;"
                                "border: 2px solid #0084ff;"
                                "border-radius: 5px;"
                                "padding: 5px 10px;"
                              "}"
                              "QPushButton:hover {"
                                "background-color: #0056b3;"
                              "}"
                              "QPushButton:pressed {"
                                "background-color: #003366;"
                              "}"
                              "QPushButton:focus {"
                                "outline: none;"
                              "}")
           # Agrega cuadro de entrada y botón al diseño horizontal
        self.input_layout.addWidget(self.input_box)
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)

        self.setLayout(self.layout)
         # Conectar eventos de clic y presionar enter con el método para enviar mensajes
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)
    #Metodo para enviar mensaje 
    def send_message(self):
        user_input = self.input_box.text()
        if user_input:
            # Mostrar mensaje del usuario en el chat
            self.display_message("Tu", user_input, "green")
            # Obtiene y muestra la respuesta del bot
            response = get_response(user_input)
            self.display_message("Covi", response, "#0084ff")
            self.input_box.clear()  # Limpiar el cuadro de entrada después de enviar el mensaje

    # Método para mostrar mensajes en el chat
    def display_message(self, sender, message, color):
        self.chat_display.setTextColor(QColor(color))
       
        
        self.chat_display.setAlignment(Qt.AlignLeft if sender == "Tu" else Qt.AlignRight)  #Alinea el texto
        self.chat_display.moveCursor(QTextCursor.End)
        # Agrega el mensaje al chat con formato
        self.chat_display.append(f'<div style="color: {color}; padding: 5px; border-radius: 20px;">{sender}: {message}</div>')
        self.chat_display.moveCursor(QTextCursor.End)
        
# Función para obtener la respuesta del bot
def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower()) # divide el mensaje en palabras
    response = check_all_messages(split_message) # obtiene la respuesta del bot
    return response

# Función para calcular la probabilidad de coincidencia de un mensaje con palabras clave
def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty +=1

    percentage = float(message_certainty) / float (len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

# Función para verificar todas las posibles respuestas
def check_all_messages(message):
    highest_prob = {}


#Funcion en donde se define las posibles respuestas del chat de acuerdo a las palabras clave
    def response(bot_response, list_of_words, single_response = False, required_words = []):
        nonlocal highest_prob
        highest_prob[bot_response] = message_probability(message, list_of_words, single_response, required_words)
        
    response('Hola, aqui te ayudare con las dudas sobre el covid-19',
             ['hola', 'buenos', 'saludos', 'buenas','buen','dias', 'dia','tarde','tardes','noche','noches'], single_response = True)
    response('Estoy bien y tú?',
             ['como', 'estas', 'va', 'vas', 'sientes'], required_words=['como'])
    response('Posiblemente y de acuerdo a los sintomas que presenta puede ser un caso de covid-19, porfavor acercarse al centro de atencion mas cercano.¿Otra Consulta?', 
             ['fiebre', 'dolor de cabeza', 'olfato','perdida','gusto', 'tengo'], required_words=['sintomas'], single_response =True)
    response('Los sintomas de Covid-19 son los siguientes: Fiebre, dolor de cabeza,dolor de garganta,tos,diarrea, dificultad para respirar, perdida de el olfato y el gusto entre otros, por favor si posee algunos de los sintomas acercarse al centro de salud mas cercano.¿Otra Consulta? ',
             ['sintomas','que','cuales','sintoma','son','saber'], required_words=['sintomas',],single_response=True)
    response('Por favor, comunicarse al siguiente numero de emergencia 0800-222-0651,¿Otra Consulta?', 
             ['numero','emergencia','llamar'],required_words= ['numero'],single_response=True)
    response('Por favor, comunicarse al siguiente numero para sacar un turno para una atención médica o bien para hacerse el test de covid 0800-222-0651.¿Otra Consulta?', 
             ['numero','turno','reservar','sacar','llamar'],required_words= ['numero'],single_response=True)
    response('Por favor, no medicarse sin antes recibir la atencion de un profesional quien le brindara los medicamentos correspondientes.¿Otra Consulta?', 
             ['que','remedios','tomar','medicar','puedo','medicamento','medicamentos'],required_words= ['puedo'],single_response=True)
    response('Por favor, no medicarse sin antes recibir la atencion de un profesional quien le brindara los medicamentos correspondientes.¿Otra Consulta?', 
             ['que','remedios','tomar','medicar','puedo','medicamento','medicamentos'],required_words= ['remedios'],single_response=True)
    response('Por favor, no medicarse sin antes recibir la atencion de un profesional quien le brindara los medicamentos correspondientes.¿Otra Consulta?', 
             ['que','remedios','tomar','medicar','puedo','medicamento','medicamentos'],required_words= ['remedio'],single_response=True)
    response('Por favor, mantenerse aislado en su domicilio y llame al siguiente numero (0800-222-0651)para saber como seguir o dirigirse al centro medico mas cercano.¿Otra Consulta?', 
             ['covid','covid-19'],required_words= ['tengo'],single_response=True)
    response('Para saber si usted tiene covid debe hacerse el test de covid-19 en el centro de salud mas cercano.¿Otra Consulta?', 
             ['como','saber','se','tengo','covid','covid-19'],required_words= ['saber'],single_response=True)
    response('En el siguiente link encontrará toda la información con respecto a las vacunas:https://www.argentina.gob.ar/coronavirus/vacuna/cuales. ¿Otra Consulta?',
             ['vacunas', 'vacuna','cual', 'cuales'],single_response=True)
    response('Gracias por comunicarte.Espero te haya sido de ayuda.', 
             ['chau','gracias','no','hasta','luego','adios'],required_words= ['adios'],single_response=True)
    
     
    best_match = max(highest_prob, key=highest_prob.get)

    return unknown() if highest_prob[best_match] < 1 else best_match
#funcion para manejar respuestas desconocidas
def unknown():
    response = ['Hola,aqui te brindaremos informacion sobre el covid-19. Por favor ingrasar palabras clave, para poder respoder de manera precisa'][random.randrange(1)]
    return response
#Inicia la aplicacion y se ejecuta la interfaz
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    chat_interface = ChatInterface()
    chat_interface.show()
    sys.exit(app.exec_())

