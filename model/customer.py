# Clase POJO que representa al cliente:
class Customer:
    def __init__(self, id, name, surname, address):
        self.__id = id
        self.__name = name
        self.__surname = surname
        self.__address = address
        
    # PROPERTIES para clase Customers
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        self.__surname = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value