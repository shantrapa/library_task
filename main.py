import json
import os

class LibraryManagementSystem:
    def __init__(self, storage_file='library_books.json'):
        self.storage_file = storage_file
        self.books = self.load_books()
        self.max_id = max([book['id'] for book in self.books], default=0)

    # загружает книги из json формата
    def load_books(self):
        try:
            if not os.path.exists(self.storage_file):
                return []
            
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(f"Error reading {self.storage_file}. Starting with an empty library.")
            return []

    # сохраняет данные книги в json формате
    def save_books(self):
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except IOError:
            print(f"Не получилось добавить книгу в {self.storage_file}")

    # 
    def add_book(self, title, author, year):
        if not all([title, author, str(year).strip()]):
            raise ValueError("title, author, year не могут иметь пустые значения")
        
        try:
            year = int(year)
        except ValueError:
            raise ValueError("Год должен быть числом. Повторите снова")

        self.max_id += 1

        # создаем новую книгу
        new_book = {
            'id': self.max_id,
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии'
        }
        
        self.books.append(new_book)
        self.save_books()
        return new_book

    # удаление книги из библиотеки по book_id
    def delete_book(self, book_id):
        try:
            book_id = int(book_id)
        except ValueError:
            raise ValueError("ID книги должно быть числом. Повторите снова")

        for book in self.books:
            if book['id'] == book_id:
                deleted_book = book
                self.books.remove(book)
                self.save_books()
                return deleted_book
        
        raise ValueError(f"Книга с ID {book_id} не найдена")

    # поиск книги по title, author, year
    def search_books(self, query, search_type):
        if search_type not in ['title', 'author', 'year']:
            raise ValueError("Некорректный тип поиска. Используйте 'title', 'author' или 'year'")

        if search_type == 'year':
            try:
                query = int(query)
            except ValueError:
                raise ValueError("Для поиска по году введите корректное число")

        results = [
            book for book in self.books 
            if str(query).lower() in str(book[search_type]).lower()
        ]
        return results

    # show books
    def show_books(self):
        return self.books

    # изменить book status по book_id
    def update_book_status(self, book_id, new_status):
        try:
            book_id = int(book_id)
        except ValueError:
            raise ValueError("ID книги должен быть целым числом")

        statuses = {'1': 'в наличии',
                    '2': 'выдано'}
        if new_status not in ['1', '2']:
            raise ValueError(f"Недопустимый статус. Используйте: 1 для \"в наличии\" или 2 для \"выдано\"")

        for book in self.books:
            if book['id'] == book_id:
                book['status'] = statuses[new_status]
                self.save_books()
                return book
        
        raise ValueError(f"Книга с ID {book_id} не найдена")

    def check_authors(self):
        return sorted(set(book['author'] for book in self.books))

def main():
    library = LibraryManagementSystem()

    while True:
        print("\n--- Наша библиотека ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие (1-6): ").strip()

        try:
            # Добавление книги
            if choice == '1':
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                year = input("Введите год издания: ").strip()
                book = library.add_book(title, author, year)
                print(f"Книга добавлена. ID: {book['id']}")

            # Удаление книги
            elif choice == '2':
                book_id = input("Введите ID книги для удаления: ").strip()
                deleted_book = library.delete_book(book_id)
                print(f"Книга удалена: {deleted_book['title']}")

            # Поиск книги
            elif choice == '3':
                # Search Books
                print("\nПоиск книг:")
                print("1. По названию")
                print("2. По автору")
                print("3. По году")
                search_choice = input("Выберите тип поиска (1-3): ").strip()
                
                search_types = {
                    '1': 'title',
                    '2': 'author', 
                    '3': 'year'
                }
                
                if search_choice not in search_types:
                    print("Неверный инпут.")
                    continue

                if search_choice == '2':
                    unique_authors = library.check_authors()
                    if unique_authors:
                        print("\nДоступные авторы:")
                        for i, author in enumerate(unique_authors, 1):
                            print(f"{i}. {author}")
                        print("\nВы можете ввести номер автора или его имя.")
                    else:
                        print("В библиотеке пока нет книг.")

                query = input("Введите поисковый запрос: ").strip()
                
                if search_choice == '2' and query.isdigit():
                    try:
                        index = int(query) - 1
                        query = unique_authors[index]
                    except (ValueError, IndexError):
                        print("Неверный номер автора.")
                        continue

                results = library.search_books(query, search_types[search_choice])
                
                if results:
                    print("\nНайденные книги:")
                    for book in results:
                        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
                else:
                    print("Книги не найдены.")

            # Отображение всех книг
            elif choice == '4':
                books = library.show_books()
                if books:
                    print("\nВсе книги в библиотеке:")
                    for book in books:
                        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, Год: {book['year']}, Статус: {book['status']}")
                else:
                    print("Библиотека пуста.")

            # Изменение статуса книги
            elif choice == '5':
                book_id = input("Введите ID книги: ").strip()
                print("\nВозможные статусы:")
                print("1. В наличии")
                print("2. Выдано")
                status_choice = input("Выберите новый статус (1-2): ").strip()
                
                if status_choice not in ['1', '2']:
                    print("Неверный инпут.")
                    continue

                updated_book = library.update_book_status(book_id, status_choice)
                print(f"Статус книги обновлен: {updated_book['title']} - {updated_book['status']}")

            # Выход из приложения
            elif choice == '6':
                print("bb")
                break

            else:
                print("Неверный инпут. Введите число от 1 до 6 включительно")

        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()