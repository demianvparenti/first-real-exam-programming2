import tkinter as tk
from tkinter import ttk, messagebox
from db.customermanager import CustomerManager
from model.customer import Customer

# Clase Application para implementar la vista con Tkinter:
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NicBread - Gestión de Clientes")
        self.geometry("800x250")

        self.customer_manager = CustomerManager()

        self.create_menu()
        self.create_table_view()

        # Cuando inicia la aplicación refresca la tabla clientes
        self.refresh_table()
        
    # Método que crea el menú:
    def create_menu(self):
        self.menu_bar = tk.Menu(self)

        # Opciones del menú
        customers_menu = tk.Menu(self.menu_bar, tearoff=0)
        customers_menu.add_command(
            label="Agregar cliente", command=self.add_customer)
        customers_menu.add_command(
            label="Modificar cliente", command=self.update_customer)
        customers_menu.add_command(
            label="Eliminar cliente", command=self.delete_customer)
        customers_menu.add_command(
            label="Listar todos", command=self.list_all_customers)
        customers_menu.add_command(
            label="Buscar cliente", command=self.search_customer)

        self.menu_bar.add_cascade(label="Clientes", menu=customers_menu)
        self.config(menu=self.menu_bar)

    # Método que crea la vista en tabla para listar todos los clientes.
    def create_table_view(self):
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame, columns=(
            "id", "name", "surname", "address"),
            show='headings')
        self.table.heading("id", text="Código")
        self.table.heading("name", text="Nombre")
        self.table.heading("surname", text="Apellido")
        self.table.heading("address", text="Dirección")
        self.table.pack()

    # Método que refresca la tabla para mostrar los datos de los clientes guardados
    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        customers = self.customer_manager.get_all_customers()
        if customers:
            for customer in customers:
                self.table.insert("", "end", values=(
                    customer.id, customer.name, customer.surname, customer.address))
        else:
            self.table.insert("", "end", values=(
                "No hay clientes cargados.", "", "", ""))
        print("Tabla de clientes actualizada.")
            
    # Método de vista para mostrar el formulario de inserción de un cliente
    def add_customer(self):
        add_window = tk.Toplevel(self)
        add_window.title("Agregar un cliente")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Nombre:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Apellido:").pack()
        surname_entry = tk.Entry(add_window)
        surname_entry.pack()

        tk.Label(add_window, text="Dirección:").pack()
        address_entry = tk.Entry(add_window)
        address_entry.pack()

        def save_customer():
            name = name_entry.get()
            surname = surname_entry.get()
            address = address_entry.get()
            if not name or not surname or not address:
                print("Todos los campos son obligatorios.")
                return
            customer = Customer(id, name, surname, address)
            self.customer_manager.insert_customer(customer)
            add_window.destroy()
            self.refresh_table()

        tk.Button(add_window, text="Guardar", command=save_customer).pack()
        print("Se agregó un cliente:", name_entry.get(), surname_entry.get(), address_entry.get())

    # Método de vista para mostrar el formulario de borrado de un cliente
    def delete_customer(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Eliminar un cliente")
        delete_window.geometry("200x100")

        tk.Label(delete_window, text="Código:").pack()
        id_entry = tk.Entry(delete_window)
        id_entry.pack()

        def delete():
            try:
                id = int(id_entry.get())
                self.customer_manager.delete_customer(id)
                delete_window.destroy()
                self.refresh_table()
            except ValueError:
                print("Código inválido.")
                return

        tk.Button(delete_window, text="Eliminar", command=delete).pack()
        print("Se eliminó un cliente con código:", id_entry.get())

    # Método de vista para mostrar el formulario de modificación de un cliente
    def update_customer(self):
        # Ventana inicial para ingresar el código del cliente a modificar
        initial_window = tk.Toplevel(self)
        initial_window.title("Modificar un cliente")
        initial_window.geometry("300x200")

        tk.Label(initial_window, text="Código:").pack()
        id_entry = tk.Entry(initial_window)
        id_entry.pack()
        
        # Función interna para abrir la ventana de edición
        def open_edit_window(customer):
            edit_window = tk.Toplevel(self)
            edit_window.title("Modificar un cliente")
            edit_window.geometry("300x200")

            tk.Label(edit_window, text="Nombre:").pack()
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, customer.name)
            name_entry.pack()

            tk.Label(edit_window, text="Apellido:").pack()
            surname_entry = tk.Entry(edit_window)
            surname_entry.insert(0, customer.surname)
            surname_entry.pack()

            tk.Label(edit_window, text="Dirección:").pack()
            address_entry = tk.Entry(edit_window)
            address_entry.insert(0, customer.address)
            address_entry.pack()

            # Función para enviar los datos modificados
            def confirm_update():
                customer.name = name_entry.get()
                customer.surname = surname_entry.get()
                customer.address = address_entry.get()
                self.customer_manager.update_customer(customer)
                edit_window.destroy()
                self.refresh_table()

            tk.Button(edit_window, text="Guardar", command=confirm_update).pack()

        # Función con la lógica de validación de la búsqueda del cliente a modificar
        def update():
            try:
                id = int(id_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Código inválido")
                return

            customer = self.customer_manager.get_customer(id)
            if customer:
                initial_window.destroy()
                # Retrasa el abrir la segunda ventana
                self.after(100, lambda: open_edit_window(customer))
            else:
                messagebox.showerror("Error", f"No se encontró cliente con código {id}")

        tk.Button(initial_window, text="Modificar", command=update).pack()

        print("Se modificó un cliente con código:", id_entry.get())

    # Método de vista para mostrar los clientes en la tabla y por consola
    def list_all_customers(self):
        # Refrescar el listado de clientes en la tabla de Tkinter
        self.refresh_table()
        
        # Listar los clientes por consola para ver salida de la transacción
        customers = self.customer_manager.get_all_customers()
        if customers:
            print("Lista de clientes:")
            for customer in customers:
                print(f"Código: {customer.id}")
                print(f"Nombre: {customer.name}")
                print(f"Apellido: {customer.surname}")
                print(f"Dirección: {customer.address}")
                print("-------------------")
        else:
            print("No se encontraron clientes.")

    # Método de vista para buscar un cliente por código
    def search_customer(self):
        search_window = tk.Toplevel(self)
        search_window.title("Buscar un cliente")
        search_window.geometry("200x100")

        tk.Label(search_window, text="Código:").pack()
        id_entry = tk.Entry(search_window)
        id_entry.pack()

        def search():
            try:
                print("Buscando cliente...")
                id = int(id_entry.get())
            except ValueError:
                print("Código inválido.")
                return
            
            customer = self.customer_manager.get_customer(id)
            search_window.destroy()

            #Vacía la tabla antes de mostrar el resultado
            self.table.delete(*self.table.get_children())

            if customer is not None:
                #Muestra el cliente encontrado en la tabla
                self.table.insert("", "end", values=(
                    customer.id, customer.name, customer.surname, customer.address))
                print(f"Código: {customer.id}")
                print(f"Nombre: {customer.name}")
                print(f"Apellido: {customer.surname}")
                print(f"Dirección: {customer.address}")
            else:
                messagebox.showinfo("Resultado de búsqueda", "Cliente no encontrado.")
                print("Cliente no encontrado.")
                self.table.insert("", "end", values=(
                    "Cliente no encontrado.", "", "", ""))
                
        tk.Button(search_window, text="Buscar", command=search).pack()
        print("Se busca un cliente por código:", id_entry.get())