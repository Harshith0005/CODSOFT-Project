import tkinter as tk
from tkinter import messagebox, simpledialog

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email} | {self.address}"

class ContactManager:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, email, address):
        new_contact = Contact(name, phone, email, address)
        self.contacts.append(new_contact)

    def view_contacts(self):
        return [str(contact) for contact in self.contacts]

    def search_contact(self, query):
        results = [contact for contact in self.contacts if query.lower() in contact.name.lower() or query in contact.phone]
        return results

    def update_contact(self, name, new_name=None, new_phone=None, new_email=None, new_address=None):
        for contact in self.contacts:
            if contact.name == name:
                if new_name:
                    contact.name = new_name
                if new_phone:
                    contact.phone = new_phone
                if new_email:
                    contact.email = new_email
                if new_address:
                    contact.address = new_address
                return True
        return False

    def delete_contact(self, name):
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                del self.contacts[i]
                return True
        return False

class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Management System")

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Contact", command=self.add_contact).grid(row=0, column=0)
        tk.Button(btn_frame, text="View Contacts", command=self.view_contacts).grid(row=0, column=1)
        tk.Button(btn_frame, text="Search Contact", command=self.search_contact).grid(row=0, column=2)
        tk.Button(btn_frame, text="Update Contact", command=self.update_contact).grid(row=0, column=3)
        tk.Button(btn_frame, text="Delete Contact", command=self.delete_contact).grid(row=0, column=4)

    def add_contact(self):
        name = simpledialog.askstring("Input", "Enter Name:")
        phone = simpledialog.askstring("Input", "Enter Phone Number:")
        email = simpledialog.askstring("Input", "Enter Email:")
        address = simpledialog.askstring("Input", "Enter Address:")
        
        if name and phone and email and address:
            self.manager.add_contact(name, phone, email, address)
            messagebox.showinfo("Success", f"Contact '{name}' added successfully.")
            self.view_contacts()
    
    def view_contacts(self):
        self.listbox.delete(0, tk.END)
        contacts = self.manager.view_contacts()
        
        for contact in contacts:
            self.listbox.insert(tk.END, contact)

    def search_contact(self):
        query = simpledialog.askstring("Input", "Enter Name or Phone Number to Search:")
        
        if query:
            results = self.manager.search_contact(query)
            self.listbox.delete(0, tk.END)
            
            for contact in results:
                self.listbox.insert(tk.END, str(contact))
                
            if not results:
                messagebox.showinfo("Search Result", "No contacts found.")

    def update_contact(self):
        name = simpledialog.askstring("Input", "Enter the Name of the Contact to Update:")
        
        if name:
            new_name = simpledialog.askstring("Input", "Enter New Name (leave blank to keep current):")
            new_phone = simpledialog.askstring("Input", "Enter New Phone (leave blank to keep current):")
            new_email = simpledialog.askstring("Input", "Enter New Email (leave blank to keep current):")
            new_address = simpledialog.askstring("Input", "Enter New Address (leave blank to keep current):")
            
            updated = self.manager.update_contact(name,
                                                  new_name if new_name else None,
                                                  new_phone if new_phone else None,
                                                  new_email if new_email else None,
                                                  new_address if new_address else None)

            if updated:
                messagebox.showinfo("Success", f"Contact '{name}' updated successfully.")
                self.view_contacts()
            else:
                messagebox.showwarning("Update Failed", f"Contact '{name}' not found.")

    def delete_contact(self):
        name = simpledialog.askstring("Input", "Enter the Name of the Contact to Delete:")
        
        if name:
            deleted = self.manager.delete_contact(name)
            
            if deleted:
                messagebox.showinfo("Success", f"Contact '{name}' deleted successfully.")
                self.view_contacts()
            else:
                messagebox.showwarning("Delete Failed", f"Contact '{name}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
