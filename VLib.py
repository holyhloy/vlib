import json
import os


class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):
        """Конструктор класса Book, который инициализирует
        объект книги с уникальным идентификатором, названием,
        автором, годом издания и статусом (по умолчанию "в наличии")"""
        self.id = book_id  # Идентификатор книги
        self.title = title  # Название книги
        self.author = author  # Автор книги
        self.year = year  # Год издания книги
        self.status = status  # Статус книги (в наличии/выдана)

    def to_dict(self):
        """Функция преобразует объект книги в словарь для удобства работы с JSON
        Возвращает словарь с данными книги"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


class Library:
    def __init__(self, filename='library.json'):
        """Конструктор класса Library, который инициализирует
        объект библиотеки и загружает книги из указанного файла JSON."""
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        """Загружает данные о книгах из файла JSON, если файл существует.
        Преобразует данные из словаря в объекты класса Book."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book(book_id=book['id'], title=book['title'], author=book['author'], year=book['year'], status=book['status']) for book in data]

    def save_books(self):
        """Сохраняет текущий список книг в файл JSON.
        Преобразует объекты класса Book обратно в словари для сериализации."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        """Добавляет новую книгу в библиотеку.
        Генерирует уникальный идентификатор на основе текущего количества книг
        и сохраняет изменения в файл."""
        book_id = len(self.books) + 1  # Генерация уникального id
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id):
        """Удаляет книгу из библиотеки по указанному идентификатору.
        Если книга не найдена, выводит сообщение об ошибке."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return
        print(f"Книга с id {book_id} не найдена.")

    def search_books(self, query):
        """Ищет книги в библиотеке по заданному запросу.
        Поиск осуществляется по названию, автору и году издания.
        Возвращает список найденных книг"""
        results = [book for book in self.books if query.lower() in book.title.lower() or
                   query.lower() in book.author.lower() or
                   query.lower() in str(book.year)]
        return results

    def display_books(self):
        """ Отображает все книги в библиотеке.
        Если библиотека пуста, выводит соответствующее сообщение."""
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(f"id:"
                  f" {book.id}, title: {book.title}, author: {book.author}, year: {book.year}, status: {book.status}")

    def change_status(self, book_id, new_status):
        """ Изменяет статус книги по ее идентификатору.
        Если книга не найдена или статус некорректен, выводит сообщение об ошибке."""
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_books()
                    return
                else:
                    print("Некорректный статус. Доступные статусы: 'в наличии', 'выдана'.")
                    return
        print(f"Книга с id {book_id} не найдена.")


def main():
    """Основная функция приложения, которая запускает цикл взаимодействия с пользователем.
    Предлагает меню с возможностью выбора действий и обрабатывает команды пользователя.
- Функционал:
  - Отображает меню команд.
  - Обрабатывает ввод пользователя и вызывает соответствующие методы класса Library для выполнения операций
  (добавление, удаление, поиск, отображение книг и изменение статуса).
  - Завершает работу приложения при выборе соответствующей команды."""
    library = Library()

    while True:
        print("\nКоманды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите команду: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)
            print("Книга добавлена.")

        elif choice == "2":
            book_id = int(input("Введите id книги для удаления: "))
            library.remove_book(book_id)

        elif choice == "3":
            query = input("Введите название или автора книги для поиска: ")
            results = library.search_books(query)
            if results:
                for book in results:
                    print(f"id: {book.id}, title: {book.title}, author: {book.author}, year: {book.year}, status: {book.status}")
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = int(input("Введите id книги для изменения статуса: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            library.change_status(book_id, new_status)

        elif choice == "6":
            break

        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")


# Запуск приложения
if __name__ == "__main__":
    """Проверяет, является ли скрипт основным модулем
    и запускает функцию main(), если это так.
    Это позволяет использовать данный код как модуль
    без автоматического запуска при импорте в другие скрипты."""
    main()
