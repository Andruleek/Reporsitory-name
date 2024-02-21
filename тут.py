import os
import shutil
import datetime
import spacy

# Завантаження моделі spaCy для англійської мови
nlp = spacy.load("en_core_web_sm")

class Note:
    def __init__(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags

class PersonalBot:
    def __init__(self):
        self.notes = []

    def add_note(self, title, content, tags):
        note = Note(title, content, tags)
        self.notes.append(note)

    def search_notes_by_tag(self, tag):
        found_notes = []
        for note in self.notes:
            if tag in note.tags:
                found_notes.append(note)
        return found_notes

def sort_files_by_category(folder_path):
    if not os.path.exists(folder_path):
        print("Шлях не існує.")
        return
    
    categories = {
        'зображення': ['.jpg', '.jpeg', '.png', '.gif'],
        'відео': ['.mp4', '.avi', '.mkv'],
        'документи': ['.pdf', '.doc', '.docx', '.txt'],
        'інше': []  
    }
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_name)
            found_category = False
            for category, extensions in categories.items():
                if file_extension.lower() in extensions:
                    found_category = True
                    category_folder = os.path.join(folder_path, category)
                    if not os.path.exists(category_folder):
                        os.makedirs(category_folder)
                    shutil.move(file_path, os.path.join(category_folder, file_name))
                    break
            if not found_category:
                other_folder = os.path.join(folder_path, 'інше')
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                shutil.move(file_path, os.path.join(other_folder, file_name))
    
    print("Сортування завершено!")

contacts = {
    'Іван': '1990-05-15',
    'Марія': '1987-10-20',
    'Петро': '1995-02-10',
}

def find_birthdays_in_n_days(n_days):
    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=n_days)
    upcoming_birthdays = []

    for contact, dob in contacts.items():
        dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
        if (dob_date - today).days == n_days:
            upcoming_birthdays.append((contact, dob_date))

    return upcoming_birthdays

def process_text(input_text):
    # Обробка тексту за допомогою spaCy
    doc = nlp(input_text)
    
    # Аналіз токенів та визначення наміру
    intent = None
    for i in range(len(doc)):
        if doc[i].text.lower() == 'upcoming' and i < len(doc) - 1 and doc[i+1].text.lower() == 'birthdays':
            intent = 'upcoming_birthdays'
            break
        elif doc[i].text.lower() == 'sort' or doc[i].text.lower() == 'organize':
            intent = 'sort_files'
            break
        elif doc[i].text.lower() == 'search' or doc[i].text.lower() == 'find':
            intent = 'search_notes'
            break
    
    return intent


def main():
    bot = PersonalBot()
    folder_to_sort = ''
    n_days = 0

    while True:
        command = input("Введіть ваш запит: ").lower()
        intent = process_text(command)

        if command == 'help':
            print("Доступні команди:")
            print("- sort files: Сортування файлів у заданій папці за категоріями.")
            print("- search notes: Пошук нотаток за тегами.")
            print("- upcoming birthdays: Вивід списку контактів, у яких день народження через задану кількість днів від поточної дати.")
            print("- exit: Вихід з програми.")
        elif intent == 'sort_files':
            folder_to_sort = input("Введіть шлях до папки: ")
            sort_files_by_category(folder_to_sort)
        elif intent == 'search_notes':
            tag = input("Введіть тег для пошуку нотаток: ")
            found_notes = bot.search_notes_by_tag(tag)
            if found_notes:
                print("Знайдені нотатки:")
                for note in found_notes:
                    print(f"Назва: {note.title}, Зміст: {note.content}, Теги: {note.tags}")
            else:
                print("Нотатки за цим тегом не знайдені.")
        elif intent == 'upcoming_birthdays':
            n_days = int(input("Введіть кількість днів: "))
            upcoming_birthdays = find_birthdays_in_n_days(n_days)
            if upcoming_birthdays:
                print(f"Контакти з днем народження через {n_days} днів:")
                for contact, dob in upcoming_birthdays:
                    print(f"{contact}: {dob.strftime('%Y-%m-%d')}")
            else:
                print(f"Немає контактів з днем народження через {n_days} днів.")
        elif command == 'exit':
            break
        else:
            print("Не вдалося визначити намір. Введіть 'help' для відображення доступних команд.")

if __name__ == "__main__":
    main()