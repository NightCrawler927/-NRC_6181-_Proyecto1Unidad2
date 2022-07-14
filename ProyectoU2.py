"""LIBRERIAS LAS CUALES NOS SIRVEN PARA OBTENER LA FECHA ACTUAL DE LA PC"""
from ast import For
from time import time

import os
import requests
import json

from datetime import date,datetime

import holidays
from holidays.holiday_base import HolidayBase


from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import FEB,APR, MAR, JAN,JUL, MAY, AUG, OCT, NOV, DEC

class HolidayEcuador(HolidayBase):    #
    """
   Clase para hacer mas sencillo los feriados.
        el cual tendra referncia las provincias las cuales son pasados por herencia.
                     https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...
    Atributos (clase padre) 
    ---------- prov: str código de provincia según ISO3166-2 Métodos ------- 
        __init__(self, plate, date, time, online=False) : 
                 Construye todos los atributos necesarios para el objeto HolidayEcuador.
        _populate(self, year): Devuelve si una fecha es festiva o no
        """     
    # Códigos ISO 3166-2 (estan en los metodos)), 
    # # llamadas provincias
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-SD"]  # TODO add more provinces        #

    def __init__(self, **kwargs):                    # 
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
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"           #
        
        # Christmas
        self[date(year, DEC, 25)] = "Navidad [Christmas]"                 #

        #carnaval lunes y martes
        self[date(year, FEB, 28)] = "Carnaval [carnaval lunes]" 
        self[date(year, MAR, 1)] = "Carnaval [carnaval martes]"

        #Pascua
        self[date(year, APR, 17)] = "Dia de pascua "
        

        #semana santa
        self[date(year, APR, 2)] = "Semana Santa "
        self[date(year, APR, 3)] = "Semana Santa "
        self[date(year, APR, 4)] = "Semana Santa "
        self[date(year, APR, 5)] = "Semana Santa "
        self[date(year, APR, 6)] = "Semana Santa "
        self[date(year, APR, 7)] = "Semana Santa "
        self[date(year, APR, 8)] = "Semana Santa "

        #Dia del trabajo
        self[date(year, MAY, 1)] = "Dia del trabajo "
        self[date(year, MAY, 2)] = "Dia del trabajo "

        #Batalla de pichincha
        self[date(year, MAY, 23)] = "Baalla Pichincha"

        #Dia de simon Bolivar
        self[date(year, JUL, 25)] = "Dia simon Bolivar"

        #Dia de independencia
        self[date(year, AUG, 10)] = "Dia de independencia"

        #Dia de muertos
        self[date(year, NOV, 2)] = "Dia de muertos"

        #cantonizacion santo domingo
        self[date(year, JUL, 3)] = "Cantonizacion santo domingo"

        #provincializacion de santo domingo
        self[date(year, OCT, 6)] = "Provincializacion de sano domingo"
    




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
            fecha: calle
                 Fecha en la que el vehículo pretende transitar
                 Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.  
            en línea: booleano, opcional
                 si en línea == Verdadero, se usará la API de días festivos abstractos (el valor predeterminado es Falso)           
        """                
        self.date = date
        self.online = online
        
        
    @property                   
    def date(self):
        """ Obtiene el valor del atributo de fecha"""
        return self._date

    @date.setter                    
    def date(self, value):
        """
      Establece el valor del atributo de fecha
         Parámetros
         ----------
         valor: cadena
        
         aumenta
         ------
         ValorError
             Si la cadena de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021-04-02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
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
            ecu_holidays = HolidayEcuador(prov='EC-SD')
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





class IEES:
    '''
    Clase IEES():
    Una clase padre para representar el IEES

    ...
    Atributos:
    ---------
    cedula: int
        Cedula de la persona.
    fechaNacimiento: str
        Fecha de nacimiento de la persona.
    tipoAfiliado: str 
        Tipo de afiliado de la persona.

    Metodos:
    --------
    def __init__(self, nombre, edad, legajo, sueldo):
        Construye todos los atributos necesarios para el objeto IESS

    def afiliacionVoluntaria(self):
        Metodo que permite la afiliacion voluntaria de la persona.
    '''
    def __init__(self, cedula,fechaNacimiento,tipoAfiliado):
        '''Metodo Constructor: construye todos los atributos necesarios de la clase IEES

        Parametros:
        -----------
        cedula: int
            Cedula de la persona.
        fechaNacimiento: str
            Fecha de nacimiento de la persona.
        tipoAfiliado: str 
            Tipo de afiliado de la persona.
        '''
        self.cedula=cedula
        self.fechaNacimiento=fechaNacimiento
        self.tipoAfiliado=tipoAfiliado

    def afiliacionVoluntaria(self):
        '''Metodo de afiliacion voluntaria 

        Parametros:
        ------------

    
        '''
        print("mostrar registro afiliado: ")

class afiliado(IEES):
    def __init__(self, nombre,genero,edad,estadoCivil,direccion,email,telefono,celular,valorSuperior):
        '''Metodo Constructor: construye todos los atributos necesarios de la clase IEES

        Parametros:
        -----------
        nombre: str
            nombre de la persona.
        genero: str
            genero de la persona.
        edad: int
            edad de la persona.
        estadoCivil: str
            estado civil de la persona
        direccion: str
            direccion de la persona
        email: str
            email de la persona
        telefono: int
            telefono de la persona
        celular: int
            celular de la persona
        valorSuperior: float
            valor superior de la persona a pagar
        '''
        self.nombre=nombre
        self.genero=genero
        self.edad=edad
        self.estadoCivil=estadoCivil
        self.direccion=direccion
        self.email=email
        self.telefono=telefono
        self.celular=celular
        self.valorSuperior=valorSuperior

    def registroAfiliado(self):
        '''Metodo  ristro Afiliado

        Parametros:
        ------------
        '''

        print("mostrar registro afiliado: ")

    def calculoPago(self):
        print("Valor calculado fianl: ")
