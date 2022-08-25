"""LIBRERIAS LAS CUALES NOS SIRVEN PARA OBTENER LA FECHA ACTUAL DE LA PC"""
from ast import For
from re import I
from statistics import correlation
from time import time

import os
from tkinter import ttk
import requests
import json

import unittest

import datetime

import holidays
from holidays.holiday_base import HolidayBase


from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import FEB,APR, MAR, JAN,JUL, MAY, AUG, OCT, NOV, DEC

'''Libreria interfas'''
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter import font

from matplotlib import pyplot 

prov=0

class FeriadoEcuador(HolidayBase):
    """
    Una clase para representar un feriado en Ecuador por provincia (FiestaEcuador)
    Su objetivo es determinar si un
    fecha específica es unas vacaciones lo más rápido y flexible posible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (Hereda la clase HelidayBase )
    ----------
    prov: str
        código de provincia según ISO3166-2
    Metodos
    -------
    __init__(self, lamina, fecha, tiempo, enLinea=False):
        Construye todos los atributos necesarios para el objeto FiestaEcuador.
    _populate(self, anio):
        Retornar si una fecha es festiva o no
    """     
    # Códigos ISO 3166-2 para las principales subdivisiones,
    # provincias llamadas
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-P"]  # TODO añadir más provincias

    def __init__(self, **kwargs):
        """
         Construye todos los atributos necesarios para el objeto HolidayEcuador.
        """         
        self.country = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):                             #
        """
        Comprueba si una fecha es festiva o no 
        Parámetros 
        ----------
             year : str año de una fecha Devuelve 
         ------
             Devuelve verdadero si una fecha es festiva de lo contrario false
        """                    
        # New Year's Day 
        self[datetime.date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"           #
        
        # Christmas
        self[datetime.date(year, DEC, 25)] = "Navidad [Christmas]"                 #

        #carnaval lunes y martes
        self[datetime.date(year, FEB, 28)] = "Carnaval [carnaval lunes]" 
        self[datetime.date(year, MAR, 1)] = "Carnaval [carnaval martes]"

        #Pascua
        self[datetime.date(year, APR, 17)] = "Dia de pascua "
        

        #semana santa
        self[datetime.date(year, APR, 2)] = "Semana Santa "
        self[datetime.date(year, APR, 3)] = "Semana Santa "
        self[datetime.date(year, APR, 4)] = "Semana Santa "
        self[datetime.date(year, APR, 5)] = "Semana Santa "
        self[datetime.date(year, APR, 6)] = "Semana Santa "
        self[datetime.date(year, APR, 7)] = "Semana Santa "
        self[datetime.date(year, APR, 8)] = "Semana Santa "

        #Dia del trabajo
        self[datetime.date(year, MAY, 1)] = "Dia del trabajo "
        self[datetime.date(year, MAY, 2)] = "Dia del trabajo "

        #Batalla de pichincha
        self[datetime.date(year, MAY, 23)] = "Baalla Pichincha"

        #Dia de simon Bolivar
        self[datetime.date(year, JUL, 25)] = "Dia simon Bolivar"

        #Dia de independencia
        self[datetime.date(year, AUG, 10)] = "Dia de independencia"

        #Dia de muertos
        self[datetime.date(year, NOV, 2)] = "Dia de muertos"

        #cantonizacion santo domingo
        self[datetime.date(year, JUL, 3)] = "Cantonizacion santo domingo"

        #provincializacion de santo domingo
        self[datetime.date(year, OCT, 6)] = "Provincializacion de sano domingo"
    


class diasFeriado:                
    '''
    Una clase la cual va a refleijar los dias de feriados . '''
    
    #Dias de la semana 
    __days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"]

    # Restricciones de las fechas de feriados
    __restrictions = {
            "Monday": [1, 2],
            "Tuesday": [3, 4],
            "Wednesday": [5, 6],
            "Thursday": [7, 8],
            "Friday": [9, 0],
            "Saturday": [],
            "Sunday": []}

    def __init__(self, date, online=False):                
        """
         Construye todos los atributos necesarios para el objeto PicoPlaca.
        
         Parámetros
         ----------
            fecha: str
                 Fecha en la que el vehículo pretende transitar
                 Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.  
            en línea: booleano, opcional
                 si en línea == Verdadero, se usará la API de días festivos abstractos (el valor predeterminado es Falso)           
        """                
        self.date = date
        self.online = online
        
        
    @property
    def date(self):
        """Gets the date attribute value"""
        return self._date


    @date.setter
    def date(self, value):
        """
        Sets the date attribute value
        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as YYYY-MM-DD (e.g.: 2021-04-02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'The date must be in the following format: YYYY-MM-DD (e.g.: 2021-04-02)') from None
        self._date = value

    def __is_holiday(self, date, online):       
        """
         Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador
         si en línea == Verdadero, utilizará una API REST, 
         de lo contrario, generará los días festivos del año examinado
        
         Parámetros
         ----------
         fecha: calle
             Está siguiendo el formato ISO 8601 AAAA-MM-DD: 
             por ejemplo, 2020-04-22
         en línea: booleano, opcional
             si en línea == Verdadero, se utilizará la API de días festivos abstractos
         Devoluciones
         -------
         Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador,
          de lo contrario, Falso
        """            
        y, m, d = date.split('-')

        if online:
            # API de vacaciones abstractapi, versión gratuita: 1000 solicitudes por mes
            # 1 solicitud por segundo
            # recuperar la clave API de la variable de entorno
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # Esto significa que falta una clave API
                raise requests.HTTPError(
                    'Falta la clave API. Guarde su clave en la variable de entorno HOLIDAYS API_KEY')
            if response.content == b'[]':  # si no hay vacaciones, obtenemos una matriz vacía
                return False
            # Arreglar el Jueves Santo incorrectamente denotado como feriado
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = FeriadoEcuador(prov='EC-SD')
            return date in ecu_holidays

    def predict(self):         
        """
         -------
         
         Verdadero si fecha  con online
           Es dia festivo
         en la fecha especificadas, de lo contrario Falso
        """
        # Check if date is a holiday
        if self.__is_holiday(self.date, self.online):       
            return True
        return False        



class IESS():
    '''
    Clase IEES():
    Una clase padre para representar el IEES
    ...
    Atributos:
    ---------
    ventana: tk
        Ventana de interfaz.
    cedula: int
        Cedula de la persona.
    fechaNacimiento: str
        Fecha de nacimiento de la persona.

    Metodos:
    --------
    def __init__(self, ventana,cedula,fechaNacimiento):
        Construye todos los atributos necesarios para el objeto IESS
    def afiliacionVoluntaria(self):
        Metodo que permite la afiliacion voluntaria de la persona.
    '''
    def __init__(self, ventana,cedula,fechaNacimiento):

        self.ventana=ventana
        self.cedula=cedula
        self.fechaNacimiento=fechaNacimiento
        
    
    def afiliacionVoluntaria(self,):
        self.ventana.withdraw()
        self.win1=tk.Toplevel()
        self.win1.geometry('750x350')
        self.win1.configure(background='Light blue')
        self.avisoIees=Label(self.win1, text= "Afiliacion: \n Registre la solicitud para afiliacion voluntaria de residentes en el Ecuador")
        self.avisoIees.pack()
        self.interfaceObjeto=Frame(self.win1,width="400",height="300")

        self.win1.title("Afiliacion Voluntaria del IESS")
   
        # rellenar fill
        # expand expandir
        self.interfaceObjeto.pack()
        #interface.iconbitmap(r'C:\Users\Equipo\Desktop\Python\IESS.ico')
        self.interfaceObjeto.config(bg='Light blue')
        self.interfaceObjeto.config(bd= 100)
    
        #INGRESAR Cedula
        Label(self.interfaceObjeto, text='Ingrese su Numero de cedula: ').grid(row=1, column=0)
        self.cedula=StringVar()
        self.textCedula = Entry(self.interfaceObjeto,textvariable=self.cedula)
        self.textCedula.focus()
        self.textCedula.grid(row=1, column=1)

        #INGRESAR Fecha de nacimiento
        Label(self.interfaceObjeto, text='Ingrese su Fecha de Nacimiento: ').grid(row=2, column=0)
        self.fechaNacimiento=StringVar()
        self.textFechaNacimiento = Entry(self.interfaceObjeto,textvariable=self.fechaNacimiento)
        self.textFechaNacimiento.focus()
        self.textFechaNacimiento.grid(row=2, column=1)

        Button(self.win1, text = "Ingresar", bg = "gold", fg = "black", command = logica.validar, cursor = "circle", font = ("Arial",14)).pack(pady=20)
    
    



class afiliado(IESS):
    '''
    Clase afiliado():

    Una clase hija para representar un Afiliado, hereda los atributos y metodos de la super clase IEES.

    ---------
    Atributos:
    ---------
    sueldo: float
        Sueldo de la persona.
    porcentaje: float
        Porcentaje de Aportacion
    provincia: str
        Provincia de la persona.
    canton: str
        Canton de la persona
    parroquia: str
        Parroquia de la persona 
    direccion: str
        Direccion de la persona
    correo: str
        E-mail de la persona
    telefono: int
        telefono de la persona
    celular: int
        celular de la persona

    -------------------
    Atributos Heredados:
    -------------------
    ventana: tk
        Ventana de interfaz.
    cedula: str
        Cedula de la persona.
    fechaNacimiento: str
        Fecha de nacimiento de la persona.

    Metodos:
    --------
    def __init__(self, ventana,cedula,fechaNacimiento,sueldo,porcentaje,provincia,canton,parroquia,direccion,correo,telefono,celular):
        super().__init__(ventana,cedula,fechaNacimiento)
        Construye todos los atributos necesarios para el objeto afiliado con sus atributos propios y los heredados de la super clase IEES.

    def registroAfiliado(self):
        Metodo que permite el registro de datos del afiliado.

    def calculoPago(self):
        Metodo que permite calcular y mostrar los datos finales para afiliación.
    '''
    def __init__(self, ventana,cedula,fechaNacimiento,sueldo,porcentaje,provincia,canton,parroquia,direccion,correo,telefono,celular):
        super().__init__(ventana,cedula,fechaNacimiento)
        '''
        Metodo Constructor: construye todos los atributos necesarios.

        -----------
        Parametros:
        -----------
        sueldo: float
            Sueldo de la persona.
        porcentaje: float
            Porcentaje de Aportacion
        provincia: str
            Provincia de la persona.
        canton: str
            Canton de la persona
        parroquia: str
            Parroquia de la persona 
        direccion: str
            Direccion de la persona
        correo: str
            E-mail de la persona
        telefono: int
            telefono de la persona
        celular: int
            celular de la persona

        -------------------
        Atributos Heredados:
        -------------------
        ventana: tk
            Ventana de interfaz.
        cedula: str
            Cedula de la persona.
        fechaNacimiento: str
            Fecha de nacimiento de la persona.
        '''
        self.sueldo=sueldo
        self.porcentaje=porcentaje
        self.provincia=provincia
        self.canton=canton
        self.parroquia=parroquia
        self.direccion=direccion
        self.correo=correo
        self.telefono=telefono
        self.celular=celular

    def Principal(self):
        
        self.ventana.withdraw()
        self.win=tk.Toplevel()
        self.win.geometry('750x350')
        self.win.configure(background='Light blue')
        self.label=tk.Label(self.win,text="Porcentaje de Aportación",bg="blue",fg="black")
        self.label.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
        self.Seleccion=Frame(self.win, width=1200,height=600)
        self.Seleccion.pack()

        Label(self.Seleccion, text= "Seleccione un porcentaje").grid(row=1, column=0)
        self.porcentaje = DoubleVar()
        self.list_porcentaje = ttk.Combobox(self.Seleccion, textvariable=self.porcentaje)
        self.list_porcentaje['values'] = [17.6,25.0,15.5,10.0]
        self.list_porcentaje['state'] = 'readonly'
        self.list_porcentaje.grid(row=1, column=1)
        '''El porcentaje de aportacion del IESS dependera del año que este se realice
        https://www.audifirm.com/uploads/documento/7.19%20LABORAL-INSTRUCTIVO_AL_REGLAMENTO_DE_AFILIACION_DEL_IESS.pdf'''

        self.registrarse=tk.Button(self.win,text='Continuar',command=afili.registroAfiliado)
        self.registrarse.pack(side=tk.TOP)
    
        self.Quitar=tk.Button(self.win,text="Salir",command=self.win.destroy)
        self.Quitar.pack(side=tk.TOP)
    

    def registroAfiliado(self):
        from tkinter import ttk

        self.ventana.withdraw()
        self.win2=tk.Toplevel()
        self.win2.geometry('750x350')
        self.win2.configure(background='Light blue')
        self.e3=tk.Label(self.win2,text="Afiliacion Voluntaria",bg="blue",fg="black")
        self.e3.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
        self.ingresoDatos=Frame(self.win2, width=1200,height=600)
        self.ingresoDatos.pack()

        Label(self.ingresoDatos, text= "Seleccione provincia").grid(row=1, column=0)
        self.provincia = StringVar()
        self.list_prov = ttk.Combobox(self.ingresoDatos, textvariable=self.provincia)
        self.list_prov['values'] = logica.queryProvincia()
        self.list_prov['state'] = 'readonly'
        self.list_prov.grid(row=1, column=1)
        self.boton5=Button(self.win2,text='Generar Cantones',command=logica.validarCan)
        self.boton5.pack(side=tk.TOP)
        self.boton5.place(x=640, y=40)

        Label(self.ingresoDatos, text= "Ingrese Parroquia").grid(row=3, column=0)
        self.parroquia=StringVar()
        self.textParroquia = Entry(self.ingresoDatos,textvariable=self.parroquia)
        self.textParroquia.focus()
        self.textParroquia.grid(row=3, column=1)

        #----------------------------------------------------
        Label(self.ingresoDatos, text= "==============================================").grid(row=4, column=0)

        Label(self.ingresoDatos, text= "Ingrese Direccion").grid(row=5, column=0)
        self.direccion=StringVar()
        self.textDireccion = Entry(self.ingresoDatos,textvariable=self.direccion)
        self.textDireccion.focus()
        self.textDireccion.grid(row=5, column=1)

        Label(self.ingresoDatos, text= "Ingrese Correo Electronico").grid(row=6, column=0)
        correo=StringVar()
        self.textCorreo = Entry(self.ingresoDatos,textvariable=correo)
        self.textCorreo.focus()
        self.textCorreo.grid(row=6, column=1)

        Label(self.ingresoDatos, text= "Ingrese Telefono").grid(row=7, column=0)
        self.telefono=StringVar()
        self.textTelefono = Entry(self.ingresoDatos,textvariable=self.telefono)
        self.textTelefono.focus()
        self.textTelefono.grid(row=7, column=1)

        Label(self.ingresoDatos, text= "Ingrese Celular").grid(row=8, column=0)
        self.celular=StringVar()
        self.textCelular = Entry(self.ingresoDatos,textvariable=self.celular)
        

        self.textCelular.focus()
        self.textCelular.grid(row=8, column=1)

        Label(self.ingresoDatos, text= "==============================================").grid(row=9, column=0)

        Label(self.ingresoDatos, text= "Ingrese Sueldo").grid(row=10, column=0)
        self.sueldo=DoubleVar()
        self.textSuedo = Entry(self.ingresoDatos,textvariable=self.sueldo)
        self.textSuedo.focus()
        self.textSuedo.grid(row=10, column=1)

        '''Boton de tercera ventana'''
        self.boton3=tk.Button(self.win2,text='Continuar',command=afili.calculoPago)
        self.boton3.pack(side=tk.TOP)
        self.boton2=tk.Button(self.win2,text='Cancelar',command=self.win2.destroy)
        self.boton2.pack(side=tk.TOP)
        self.win2.destroy


    def calculoPago(self):

        self.ventana.withdraw()
        self.ventana3=tk.Toplevel()
        self.ventana3.geometry('900x350')
        self.ventana3.configure(background='Light blue')
        self.e2=tk.Label(self.ventana3,text="Calculo de Pago Mensual",bg="white",fg="blue")
        self.e2.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)

    
        self.tabla=Frame(self.ventana3, width=1200,height=600)
        self.tabla.pack()
        self.columns = ('Tipo', 'Remu', 'Porcentaje','Aporte')
        self.table = ttk.Treeview(self.tabla, columns=self.columns, show='headings')
        self.table.heading('Tipo', text='Tipo Afiliado')
        self.table.heading('Remu', text='Sueldo')
        self.table.heading('Porcentaje', text='Porcentaje Aprobación')
        self.table.heading('Aporte', text='Aporte Mensual')

        self.table.grid(row=0, column=0, sticky=tk.NSEW)

        self.sueldoAux=self.sueldo.get()
        self.porcentajeAux=self.porcentaje.get()
        self.porcentajeTotal=self.sueldoAux*self.porcentajeAux/100

        self.table.insert('',tk.END, values=('Afiliación voluntaria Ecuatoriano y Extrangero dentro de Ecuador',str(self.sueldoAux),str(self.porcentajeAux),str(self.porcentajeTotal)))


        '''Boton de tercera ventana'''
        self.boton4=tk.Button(self.ventana3,text='Guardar',command=logica.guardarDatosAfiliado)
        self.boton4.pack(side=tk.TOP)




#Librería de mongo para poder trabajar con MongoDB
import pymongo
#Creación de una base de datos llamada dbProyecto2
myClient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myClient ["dbProyecto2"]
mycol = mydb ["Cedulas"]
mycol2 = mydb ["Provincias"]



'''
MONGO host y Port en 27017, Estos valores son los predeterminados para todas las conexiones MongoDB locales.
MONGO_TIEMPO_FUERA= time: sirve para detener el tipo de ejecución deseado
'''
MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000


'''MONGO_URI: se le utiliza para conectarse a la implementación de MongoDB: Independiente un conjunto de réplicas o un clúster(Agrupaciones) fragmentado.'''
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"


'''Se llaman a la base de datos(dbProyecto2) y las colecciónes (Cedulas)-(Provincias)'''
MONGO_BASEDATOS="dbProyecto2"
MONGO_COLLECCION="Cedulas"
MONGO_COLLECCION2="Provincias"
MONGO_COLLECCION3="Afiliados"

'''Se instancia al cliente (usuario) para almacenar las bases de datos y colecciones necesarias'''
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLLECCION]
coleccion2=baseDatos[MONGO_COLLECCION2]
coleccion3=baseDatos[MONGO_COLLECCION3]

class LogicaNegocio():

    def __init__(self):

        self.coleccionCanton2=[]
        self.coleccionProvincia=[]
        self.coleccionParroquia=[]
        self.coleccionDireccion=[]
        self.coleccionFecha=[]
        self.coleccionCorreo=[]
        self.coleccionTelefono=[]
        self.coleccionCelular=[]
        self.coleccionSueldo=[]
        self.coleccionCedulas2=[]
        self.coleccionAporte=[]

    def queryInformacion(self):
        coleccionTotal=coleccion3.find()

        for i in coleccionTotal:
            self.coleccionCedulas2.append(i['cedula'])
        for i in coleccionTotal:
            self.coleccionFecha.append(i['Fecha Nacimiento'])
        for i in coleccionTotal:
            self.coleccionProvincia.append(i['Provincia'])
        for i in coleccionTotal:
            self.coleccionCanton2.append(i['Canton'])
        for i in coleccionTotal:
            self.coleccionParroquia.append(i['Parroquia'])
        for i in coleccionTotal:
            self.coleccionDireccion.append(i['Direccion'])
        for i in coleccionTotal:
            self.coleccionCorreo.append(i['Correo'])
        for i in coleccionTotal:
            self.coleccionTelefono.append(i['Telefono'])
        for i in coleccionTotal:
            self.coleccionCelular.append(i['Celular'])
        for i in coleccionTotal:
            self.coleccionSueldo.append(i['Sueldo'])
        for i in coleccionTotal:
            self.coleccionAporte.append(i['Aporte de Afiliacion'])
       
    #Metodo para retonar lista de cedulas desde la coleccion Cedulas en MongoDB
    def queryCedulas(self):
        coleccionTotal=coleccion.find()
        coleccionCedulas=[]

        for i in coleccionTotal:
            coleccionCedulas.append(i['cedula'])
        return coleccionCedulas

    #Metodo para retonar lista de provincias desde la coleccion Provincias en MongoDB
    def queryProvincia(self):
        coleccionTotalProv=coleccion2.find()
        coleccionProv=[]

        for i in coleccionTotalProv:
            coleccionProv.append(i['prov'])
        return coleccionProv


    #Metodo para retonar las listas de cantones desde la coleccion Provincias en MongoDB
    def queryCanton(self):
        global prov
        coleccionTotalCanton=coleccion2.find()
        coleccionCanton=[]
    
        for i in coleccionTotalCanton:
            coleccionCanton.append(i['cantones'])
        return coleccionCanton
    

    #Metodo para retonar lista de edades desde la coleccion cedulas en MongoDB
    def queryEdad(self):
        myquery = {"edad": {"$gt": 18}}    
        coleccionTotalEdades=coleccion.find(myquery)
        coleccionEdad=[]

        for i in coleccionTotalEdades:
            coleccionEdad.append(i['cedula'])
        return coleccionEdad

    def validarInf(self,cedula,fechaNacimiento,sueldo,provincia,canton,parroquia,direccion,correo,telefono,celular,aporte):

        if cedula in self.coleccionCedulas2:
            return True
        elif fechaNacimiento in self.coleccionFecha:
            return True
        elif sueldo in self.coleccionSueldo:
            return True
        elif provincia in self.coleccionProvincia:
            return True
        elif canton in self.coleccionCanton2:
            return True
        elif parroquia in self.coleccionParroquia:
            return True
        elif direccion in self.coleccionDireccion:
            return True
        elif correo in self.coleccionCorreo:
            return True
        elif telefono in self.coleccionTelefono:
            return True
        elif celular in self.coleccionCelular:
            return True
        elif aporte in self.coleccionAporte:
            return True

        return False
            

    #Metodo para validar cedula y edad 
    def validar(self,cedula):
        
        cedulasTotal=self.queryCedulas()
        cedulaEdadTotal=self.queryEdad()

        if cedula in cedulasTotal:
            if cedula in cedulaEdadTotal:
                return True
            else:
                messagebox.showwarning("Error", "Cedula ingresada no es mayor de edad")
        else:
            messagebox.showwarning("Error", "Cedula ingresada no registrada")
        return False
    '''
        if datoIESS.textCedula.get() in cedulasTotal:
            if datoIESS.textCedula.get() in cedulaEdadTotal:
                afili.Principal()
                return True
            else:
                messagebox.showwarning("Error", "Cedula ingresada no es mayor de edad")
        else:
            messagebox.showwarning("Error", "Cedula ingresada no registrada")
        return False
    '''
        

    #Metodo para validar provincia ,canton, y correo
    def validarCan(self):
        provinciasTotal=self.queryProvincia()
        cantonesTotal=self.queryCanton()
        print(cantonesTotal)
        if afili.provincia.get() == provinciasTotal[0]:
            canton_list=cantonesTotal[0]
        elif afili.provincia.get() ==provinciasTotal[1]:
            canton_list=cantonesTotal[1]
        elif afili.provincia.get() ==provinciasTotal[2]:
            canton_list=cantonesTotal[2]
        elif afili.provincia.get() ==provinciasTotal[3]:
            canton_list=cantonesTotal[3]
        elif afili.provincia.get() ==provinciasTotal[4]:
            canton_list=cantonesTotal[4]
        elif afili.provincia.get() ==provinciasTotal[5]:
            canton_list=cantonesTotal[5]
        elif afili.provincia.get() ==provinciasTotal[6]:
            canton_list=cantonesTotal[6]
        elif afili.provincia.get() ==provinciasTotal[7]:
            canton_list=cantonesTotal[7]
        elif afili.provincia.get() ==provinciasTotal[8]:
            canton_list=cantonesTotal[8]
        elif afili.provincia.get() ==provinciasTotal[9]:
            canton_list=cantonesTotal[9]
        elif afili.provincia.get() ==provinciasTotal[10]:
            canton_list=cantonesTotal[10]
        elif afili.provincia.get() ==provinciasTotal[11]:
            canton_list=cantonesTotal[11]
        elif afili.provincia.get() ==provinciasTotal[12]:
            canton_list=cantonesTotal[12]
        elif afili.provincia.get() ==provinciasTotal[13]:
            canton_list=cantonesTotal[13]
        elif afili.provincia.get() ==provinciasTotal[14]:
            canton_list=cantonesTotal[14]
        elif afili.provincia.get() ==provinciasTotal[15]:
            canton_list=cantonesTotal[15]
        elif afili.provincia.get() ==provinciasTotal[16]:
            canton_list=cantonesTotal[16]
        elif afili.provincia.get() ==provinciasTotal[17]:
            canton_list=cantonesTotal[17]
        elif afili.provincia.get() ==provinciasTotal[18]:
            canton_list=cantonesTotal[18]
        elif afili.provincia.get() ==provinciasTotal[19]:
            canton_list=cantonesTotal[19]
        elif afili.provincia.get() ==provinciasTotal[20]:
            canton_list=cantonesTotal[20]
        elif afili.provincia.get() ==provinciasTotal[21]:
            canton_list=cantonesTotal[21]
        elif afili.provincia.get() ==provinciasTotal[22]:
            canton_list=cantonesTotal[22]
        elif afili.provincia.get() ==provinciasTotal[23]:
            canton_list=cantonesTotal[23]

        Label(afili.ingresoDatos, text= "Seleccione Canton").grid(row=2, column=0)
        afili.canton = StringVar()
        list_canton = ttk.Combobox(afili.ingresoDatos, textvariable=afili.canton)
        list_canton['values'] = canton_list
        list_canton['state'] = 'readonly'
        list_canton.grid(row=2, column=1)
    



    #Metodo para guardar afiliados ingresados
    def guardarDatosAfiliado (self):
        '''Creación de un diccionario con los datos ingresados'''
        datosAfiliado={'cedula': datoIESS.textCedula.get(), 'Fecha Nacimiento': datoIESS.textFechaNacimiento.get(), 'Provincia': afili.provincia.get(), 'Canton': afili.canton.get(), 'Parroquia': afili.textParroquia.get(), 'Direccion': afili.textDireccion.get(), 'Correo': afili.textCorreo.get(), 'Telefono': afili.textTelefono.get(), 'Celular': afili.textCelular.get(), 'Sueldo': afili.textSuedo.get(), 'Aporte de Afiliacion': str(afili.porcentajeTotal)}
        '''Agregamos nuetro diccionario a nuestra base de datos'''
        insertarDatosAfiliado=coleccion3.insert_one(datosAfiliado)


class Menu:

    def __init__(self,LoginMenu):
        self.LoginMenu=LoginMenu

    def administradorMetodo(self):
        afili.Principal()

    def callCenterMetodo(self):
        pass

    def SecretariaMetodo(self):
        self.grafica()

    def afiliarceMetodo(self):
        datoIESS.afiliacionVoluntaria()
    
    def Principal1(self):

        """Se crea una raiz o root de la interfaz"""
        """Nombre de la ventana"""
        self.LoginMenu.title("Menu de Valcon Servicio IESS")
        """Dimensiones de la ventana"""
        self.LoginMenu.geometry("600x400+250+100")
        """width="False", height="False, se usa para que el cliente no pueda mover el tamaño del de la ventana"""
        self.LoginMenu.resizable(width="False", height="False")
    
        mensaje = Label(self.LoginMenu, text = "Valcon Servicio IESS", font=font.Font(family="Arial", size = "13"))
        mensaje.pack()
    
        administrador=Button(self.LoginMenu,text="Administrador" ,bg= "gold", font=font.Font(family="anonymous pro font", size = "13"),command= self.administradorMetodo)
        administrador.pack()
    
        callCenter = Button(self.LoginMenu,text="Call center",bg= "gold", font=font.Font(family="anonymous pro font", size = "13"),command=self.callCenterMetodo)
        callCenter.pack()

        secretario =  Button(self.LoginMenu,text="Secretaria",bg= "gold", font=font.Font(family="anonymous pro font", size = "13"),command=self.SecretariaMetodo)
        secretario.pack()

        afiliarce =  Button(self.LoginMenu,text="Afiliacion",bg= "gold", font=font.Font(family="anonymous pro font", size = "13"),command=self.afiliarceMetodo)
        afiliarce.pack()
    
        Quitar=Button(self.LoginMenu,text="Salir",fg= "red", font=font.Font(family="Arial", size = "13"),command=self.LoginMenu.destroy)
        Quitar.pack()

    def grafica():

        edades=("Mayores de 18 años","Menores de 18 años")
        personas=(56,23)
        colores=("red","yellow")

        pyplot.pie(personas, colors=colores, labels=edades,autopct=("%1.f%%"))
        pyplot.title("Edades de Ecuatorianos")
        pyplot.show()


class TestPython(unittest.TestCase):

    def test_invalid_dato1(self):
        """
        Testea el ValueError de la cedula ingresada
        """
        cedula= "2334447920"
        fechaNacimiento='2005-09-19'

        with self.assertRaises(ValueError):
            result = logica.validar(cedula)

    
    def test_invalid_dato2(self):
        """
        Testea el ValueError de la cedula ingresada
        """
        cedula = '1694566069'
        fechaNacimiento = '13-16-2005'
        with self.assertRaises(ValueError):
            result = logica.validar(cedula)


    def test_valid_dato3(self):
        """
        Testea el ValueError de la cedula ingresada
        """
        cedula = '2319521227'
        fechaNacimiento = '30-09-1969'
        with self.assertRaises(ValueError):
            result = logica.validar(cedula)

    
    def test_valid_dato4(self):
        """
        Test that missing API key raises requests.HTTPError
        """
        cedula= "2477222964"
        fechaNacimiento= "1982-09-15"
        sueldo= 500.00
        aporte= "128"
        provincia= "Pichincha"
        canton= "San Miguel de los Bancos"
        parroquia= "Bella vista"
        direccion= "Los Rios"
        correo= "nelson@hotmail.com"
        telefono= "2744537"
        celular= "234234"
        with self.assertRaises(ValueError):
            result = logica.validarInf(cedula,fechaNacimiento,sueldo,provincia,canton,parroquia,direccion,correo,telefono,celular,aporte)


    def test_valid_dato5(self):
        """
        Test that moved new holidays are restricted
        """
        cedula= "1727249979"
        fechaNacimiento= "1982-09-15"
        sueldo= 500.00
        aporte= "228"
        provincia= "Azuay"
        canton= "Cuenca"
        parroquia= "Bella vista"
        direccion= "9 de diciembre"
        correo= "nelson@hotmail.com"
        telefono= "2283724243"
        celular= "0912312098"
        with self.assertRaises(ValueError):
            result = logica.validarInf(cedula,fechaNacimiento,sueldo,provincia,canton,parroquia,direccion,correo,telefono,celular,aporte)


    def test_valid_dato6(self):
        """
        Test that moved would-have-been holidays are not restricted
        """
        cedula= "2477222964"
        fechaNacimiento= "1982-09-15"
        sueldo= 300.00
        aporte= "428"
        provincia= "Pichincha"
        canton= "San Miguel de los Bancos"
        parroquia= "Bella vista"
        direccion= "Los Rios"
        correo= "nelson@hotmail.com"
        telefono= "2744537"
        celular= "234234"
        with self.assertRaises(ValueError):
            result = logica.validarInf(cedula,fechaNacimiento,sueldo,provincia,canton,parroquia,direccion,correo,telefono,celular,aporte)


    def test_valid_dato7(self):
        """
        Test that moved would-have-been continuous holidays are not restricted
        """
        cedula= "2477222964"
        fechaNacimiento= "1982-09-15"
        sueldo=2500.00
        aporte= "234"
        provincia= "Pichincha"
        canton= "San Miguel de los Bancos"
        parroquia= "Bella vista"
        direccion= "Los Rios"
        correo= "nelson@hotmail.com"
        telefono= "2744537"
        celular= "234234"
        with self.assertRaises(ValueError):
            result = logica.validarInf(cedula,fechaNacimiento,sueldo,provincia,canton,parroquia,direccion,correo,telefono,celular,aporte)

    



if __name__=="__main__":


    '''Insertar lista cedulas a mongo db'''
    #listaDatos=mycol.insert_many(lista)

    '''Imprimir la insertacion de listas cedulas'''
    #print(listaDatos.inserted_ids)

    '''Insertar lista provincias y cantones a mongo db'''
    #listaDatosProvincia=mycol2.insert_many(listaProvincias)

    '''Imprimir la insertacion de listas provincias y cantones'''
    #print(listaDatosProvincia.inserted_ids)
    
    fecha=datetime.datetime.now()
    fechaa= datetime.datetime.strftime(fecha, '%Y-%m-%d')
    
    #Instanciar clase diasFeriado y pasar por parametros
    pyp = diasFeriado(fechaa,online=False)
    logica=LogicaNegocio()
    if pyp.predict():
        messagebox.showwarning("Error", "No puede solicitar un servicio este día")

    else:
        '''Instanciar IEES y Afiliado '''
        interface=Tk()
        Menuu=Menu(interface)
        Menuu.Principal1()
        datoIESS=IESS(interface,cedula="",fechaNacimiento="")
        unittest.main()
        afili=afiliado(interface,cedula="",fechaNacimiento="",sueldo=0.00,porcentaje=0.00,provincia="",canton="",parroquia="",direccion="",correo="",telefono="",celular="")
        interface.mainloop()