from database import init_db
from crud import create_universe, list_universes, edit_universe, delete_universe, create_character, edit_character, delete_character, list_characters
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lorekeeper")
        self.geometry("500x350")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for Page in (DashboardPage,
                    ViewUniversePage,
                    UniverseFormPage,
                    ViewCharacterPage,
                    CharacterFormPage):
            frame = Page(container, self)
            self.frames[Page] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # Initial page: dashboard
        self.display_page(DashboardPage)

    def display_page(self, page) -> None:
        frame = self.frames[page]

        if (page == ViewUniversePage):
            frame.refresh()
        elif (page == ViewCharacterPage):
            frame.refresh()

        frame.tkraise()

    def show_universe_form(self, universe_id=None) -> None:
        frame = self.frames[UniverseFormPage]
        frame.load_universe(universe_id)
        frame.tkraise()

    def show_character_form(self, universe_id=None, character_id=None) -> None:
        frame = self.frames[CharacterFormPage]
        frame.load_character(universe_id, character_id)
        frame.tkraise()


# ========== Helper functions ==========
def find_universe_by_id(universe_id=None) -> dict:
    universe = next(
                (
                    u for u in list_universes()
                    if u["id"] == universe_id
                ),
                None
            )
    return universe


def find_character_by_id(universe_id=None, char_id=None) -> dict:
    if universe_id is None or char_id is None:
        return
    char = next(
        (
            c for c in list_characters(universe_id)
            if c["id"] == char_id
        ),
        None
    )
    return char


# ========== Pages ==========
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        tk.Label(self, text="Dashboard", font=("Arial", 24)).pack(pady=20)

        tk.Button(self, text="View Universes", command=lambda: controller.display_page(ViewUniversePage)).pack(pady=5)
        tk.Button(self, text="Create a new universe", command=lambda: controller.show_universe_form()).pack(pady=5)


class ViewUniversePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        tk.Label(self, text="My Universes", font=("Arial", 24)).pack(pady=20)

        self.universe_list = tk.Frame(self)
        self.universe_list.pack(fill="both", expand=True)

        tk.Button(self, text="Back to home", command=lambda: controller.display_page(DashboardPage)).pack(pady=5)

    def refresh(self) -> None:
        for widget in self.universe_list.winfo_children():
            widget.destroy()

        for universe in list_universes():
            tk.Button(self.universe_list, text=universe["name"], width=30, command=lambda uid=universe["id"]: self.controller.show_universe_form(uid)).pack(pady=5)


# For creating and editing
class UniverseFormPage(ttk.Frame):
    def __init__(self, parent, controller, universe_id=None):
        super().__init__(parent)

        self.controller = controller
        self.universe_id = universe_id

        tk.Label(self, text="Universe name:").pack(pady=20)
        self.universe_name = tk.Entry(self, width=30)
        self.universe_name.pack(pady=5) # Have to do it seperately

        tk.Label(self, text="Universe description:").pack(pady=20)
        self.universe_desc = tk.Entry(self, width=30)
        self.universe_desc.pack(pady=5)

        tk.Button(self, text="Save changes", command=lambda: self.submit_text()).pack(pady=5)
        tk.Button(self, text="Delete entry", command=lambda: self.destroy_universe()).pack(pady=5)
        tk.Button(self, text="View Characters", command=lambda: self.view_characters()).pack(pady=5)
        tk.Button(self, text="Back to universes", command=lambda: controller.display_page(ViewUniversePage)).pack(pady=5)

    def submit_text(self) -> None:
        name_entry = self.universe_name.get().strip()
        desc_entry = self.universe_desc.get().strip()

        if not name_entry:
            tk.Message(self, text="Name entry cannot be empty.")
            return
        
        if self.universe_id is None:
            create_universe(name_entry, desc_entry)
        else:
            edit_universe(self.universe_id, name_entry, desc_entry)

        self.controller.display_page(ViewUniversePage)
            

    def load_universe(self, universe_id=None) -> None:
        self.universe_id = universe_id

        self.universe_name.delete(0, tk.END)
        self.universe_desc.delete(0, tk.END)

        if universe_id is None:
            return

        universe = find_universe_by_id(universe_id)

        # Display existing name/description if applicable
        if universe is not None:
            self.universe_name.insert(0, universe["name"] or "")
            self.universe_desc.insert(0, universe["description"] or "")

    def destroy_universe(self) -> None: # Delete current and go to dashboard
        if self.universe_id is not None:
            delete_universe(self.universe_id)
            self.universe_id = None

        self.controller.display_page(DashboardPage)

    def view_characters(self) -> None:
        frame = self.controller.frames[ViewCharacterPage]
        frame.universe_id = self.universe_id
        frame.refresh()
        frame.tkraise()


class ViewCharacterPage(ttk.Frame):
    def __init__(self, parent, controller, universe_id=None):
        super().__init__(parent)

        self.controller = controller
        self.universe_id = universe_id

        tk.Label(self, text="Characters", font=("Arial", 24)).pack(pady=20)
        
        self.character_list = tk.Frame(self)
        self.character_list.pack(fill="both", expand=True)

        tk.Button(self, text="Create a character", command=lambda: self.create_new_character()).pack(pady=5)
        tk.Button(self, text="Back to universe", command=lambda: self.show_universe()).pack(pady=5)

    def refresh(self) -> None:
        for widget in self.character_list.winfo_children():
            widget.destroy()

        if self.universe_id is None:
            return

        for character in list_characters(self.universe_id):
            tk.Button(self.character_list, text=character["name"], width=30, command=lambda cid=character["id"]: self.controller.show_character_form(self.universe_id, cid)).pack(pady=5)

    def create_new_character(self) -> None:
        if self.universe_id is None:
            return

        self.controller.show_character_form(self.universe_id, None)

    def show_universe(self) -> None:
            frame = self.controller.frames[UniverseFormPage]
            frame.universe_id = self.universe_id
            frame.tkraise()


class CharacterFormPage(ttk.Frame):
    def __init__(self, parent, controller, universe_id=None, char_id=None):
        super().__init__(parent)

        self.controller = controller
        self.universe_id = universe_id
        self.character_id = char_id
        
        tk.Label(self, text="Name:").pack(pady=20)
        self.character_name = tk.Entry(self, width=30)
        self.character_name.pack(pady=5)

        tk.Label(self, text="Description:").pack(pady=20)
        self.character_desc = tk.Entry(self, width=30)
        self.character_desc.pack(pady=5)

        tk.Button(self, text="Save changes", command=lambda: self.submit_text()).pack(pady=5)
        tk.Button(self, text="Delete character", command=lambda: self.destroy_character()).pack(pady=5)
        tk.Button(self, text="Back to characters", command=lambda: self.show_characters()).pack(pady=5)

    def submit_text(self) -> None:
        name_entry = self.character_name.get().strip()
        desc_entry = self.character_desc.get().strip()

        if not name_entry:
            tk.Message(self, text="Name entry cannot be empty.")
            return

        if self.universe_id is None:
            tk.Message(self, text="Universe cannot be none.")
            return
        else:
            if self.character_id is None:
                create_character(self.universe_id, name_entry, desc_entry)
            else:
                edit_character(self.character_id, name_entry, desc_entry)

        self.show_characters()

    def load_character(self, universe_id=None, character_id=None) -> None:
        self.universe_id = universe_id
        self.character_id = character_id

        self.character_name.delete(0, tk.END)
        self.character_desc.delete(0, tk.END)

        if self.character_id is None:
            return

        character = find_character_by_id(self.universe_id, character_id)

        # Display existing name/description if applicable
        if character is not None:
            self.character_name.insert(0, character["name"] or "")
            self.character_desc.insert(0, character["description"] or "")

    def destroy_character(self) -> None: # Delete current and go to dashboard
        if self.character_id is not None:
            delete_character(self.character_id)
            self.character_id = None

        self.show_characters()

    def show_characters(self) -> None:
        frame = self.controller.frames[ViewCharacterPage]
        frame.universe_id = self.universe_id
        frame.refresh()
        frame.tkraise()


# ========== Run the application ==========
def main():
    init_db()

    app = App()
    app.mainloop()


if __name__=="__main__":
    main()