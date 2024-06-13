import json

# Clase Cuenta: Representa una cuenta bancaria con operaciones básicas.
class Cuenta:
    # Constructor: Inicializa una cuenta con número de cuenta, PIN y saldo opcional.
    def __init__(self, numero_cuenta, pin, saldo=0):
        self.numero_cuenta = numero_cuenta
        self.pin = pin
        self.saldo = saldo

    # Verifica si el PIN ingresado es correcto.
    def verificar_pin(self, pin):
        return self.pin == pin

    # Deposita una cantidad de dinero en la cuenta.
    def depositar(self, cantidad):
        self.saldo += cantidad

    # Retira una cantidad de dinero si hay saldo suficiente.
    def retirar(self, cantidad):
        if self.saldo >= cantidad:
            self.saldo -= cantidad
            return True
        else:
            return False

    # Obtiene el saldo actual de la cuenta.
    def obtener_saldo(self):
        return self.saldo

    # Transfiere una cantidad a otra cuenta si hay saldo suficiente.
    def transferir(self, cuenta_destino, cantidad):
        if self.retirar(cantidad):
            cuenta_destino.depositar(cantidad)
            return True
        else:
            return False

# Clase Banco: Representa un banco con múltiples cuentas.
class Banco:
    # Constructor: Inicializa un diccionario para almacenar cuentas.
    def __init__(self):
        self.cuentas = {}
        self.cargar_cuentas()

    # Agrega una cuenta al banco.
    def agregar_cuenta(self, cuenta):
        self.cuentas[cuenta.numero_cuenta] = cuenta
        self.guardar_cuentas()

    # Obtiene una cuenta por su número de cuenta.
    def obtener_cuenta(self, numero_cuenta):
        return self.cuentas.get(numero_cuenta)

    # Crea una nueva cuenta en el banco.
    def crear_cuenta(self):
        numero_cuenta = int(input("Ingrese el número de cuenta para la nueva cuenta: "))
        pin = int(input("Ingrese un PIN para la nueva cuenta: "))
        if numero_cuenta in self.cuentas:
            print("El número de cuenta ya existe.")
        else:
            nueva_cuenta = Cuenta(numero_cuenta, pin)
            self.agregar_cuenta(nueva_cuenta)
            print("Cuenta creada exitosamente.")

    # Guarda las cuentas en un archivo JSON.
    def guardar_cuentas(self):
        with open('cuentas.json', 'w') as archivo:
            json.dump({numero: cuenta.__dict__ for numero, cuenta in self.cuentas.items()}, archivo, indent=4)

    # Carga las cuentas desde un archivo JSON.
    def cargar_cuentas(self):
        try:
            with open('cuentas.json', 'r') as archivo:
                datos_cuentas = json.load(archivo)
                for numero_cuenta, datos_cuenta in datos_cuentas.items():
                    self.cuentas[numero_cuenta] = Cuenta(**datos_cuenta)
        except FileNotFoundError:
            pass

# Clase CajeroAutomatico: Representa la interfaz de usuario para interactuar con el banco.
class CajeroAutomatico:
    # Constructor: Inicializa el banco y la cuenta actual.
    def __init__(self, banco):
        self.banco = banco
        self.cuenta_actual = None

    # Autentica a un usuario con número de cuenta y PIN.
    def autenticar_usuario(self, numero_cuenta, pin):
        cuenta = self.banco.obtener_cuenta(numero_cuenta)
        if cuenta and cuenta.verificar_pin(pin):
            self.cuenta_actual = cuenta
            return True
        else:
            return False

    # Muestra el menú de opciones al usuario.
    def mostrar_menu(self):
        if self.cuenta_actual:
            print("1. Consultar saldo")
            print("2. Depositar")
            print("3. Retirar")
            print("4. Transferir")
            print("5. Cambiar usuario")
            print("6. Salir")
            print("-" * 50)
            opcion = input("Elija una opción: ")
            return opcion
        else:
            print("No hay usuario autenticado")
            return None

    # Inicia sesión o agrega una cuenta al inicio del programa.
    def iniciar(self):
        while True:
            print("1. Agregar cuenta")
            print("2. Iniciar sesión")
            opcion = input("Elija una opción: ")
            if opcion == '1':
                self.banco.crear_cuenta()
            elif opcion == '2':
                self.iniciar_sesion()
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    # Inicia sesión en una cuenta existente.
    def iniciar_sesion(self):
        numero_cuenta = int(input("Ingrese su número de cuenta: "))
        pin = int(input("Ingrese su PIN: "))
        if self.autenticar_usuario(numero_cuenta, pin):
            print("Autenticación exitosa.")
            self.menu_principal()
        else:
            print("Número de cuenta o PIN incorrecto.")

    # Cambia al usuario actual por otro.
    def cambiar_usuario(self):
        self.cuenta_actual = None
        self.iniciar_sesion()

    # Muestra y maneja las opciones del menú principal.
    def menu_principal(self):
        while True:
            opcion = self.mostrar_menu()
            if opcion == '1':
                print(f"Su saldo es {self.cuenta_actual.obtener_saldo()}.")
            elif opcion == '2':
                cantidad = float(input("Ingrese la cantidad a depositar: "))
                self.cuenta_actual.depositar(cantidad)
                print(f"Se han depositado {cantidad}.")
                self.banco.guardar_cuentas()
            elif opcion == '3':
                cantidad = float(input("Ingrese la cantidad a retirar: "))
                if self.cuenta_actual.retirar(cantidad):
                    print(f"Se han retirado {cantidad}.")
                else:
                    print("Fondos insuficientes.")
                self.banco.guardar_cuentas()
            elif opcion == '4':
                numero_cuenta_destino = int(input("Ingrese el número de cuenta destino: "))
                cuenta_destino = self.banco.obtener_cuenta(numero_cuenta_destino)
                if cuenta_destino:
                    cantidad = float(input("Ingrese la cantidad a transferir: "))
                    if self.cuenta_actual.transferir(cuenta_destino, cantidad):
                        print(f"Se han transferido {cantidad}.")
                    else:
                        print("Fondos insuficientes.")
                    self.banco.guardar_cuentas()
                else:
                    print("Cuenta destino no encontrada.")
            elif opcion == '5':
                self.cambiar_usuario()
            elif opcion == '6':
                print("Saliendo del sistema.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

# Creación de un objeto Banco y agregando cuentas
banco = Banco()

# Creación de un objeto CajeroAutomatico
cajero = CajeroAutomatico(banco)

# Iniciar el programa para agregar cuenta o iniciar sesión
cajero.iniciar()
