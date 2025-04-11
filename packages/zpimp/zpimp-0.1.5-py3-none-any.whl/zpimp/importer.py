# import json
# import os
# import traceback

# # --- Конфигурация ---
# # Базовый путь к директории, где Zeppelin хранит все ноутбуки.
# # Убедитесь, что этот путь корректен для вашей установки Zeppelin.
# # Возможно, понадобится полный абсолютный путь, например, /zeppelin/notebook
# # Или относительный путь, если ваш скрипт запускается из определенной директории.

# ZEPPELIN_BASE_DIR = "/notebook" # Используем /notebook как пример базовой директории

# def find_notebook_path(notebook_path_prefix, base_dir=ZEPPELIN_BASE_DIR):
#     """
#     Находит полный путь к файлу ноутбука Zeppelin по его префиксу пути.

#     Args:
#         notebook_path_prefix (str): Путь к ноутбуку без ID и расширения,
#                                      например "Libraries/main_config" или "MyFolder/SubFolder/MyNotebook".
#         base_dir (str): Базовая директория, где Zeppelin хранит ноутбуки.

#     Returns:
#         str: Полный путь к найденному файлу ноутбука .zpln.

#     Raises:
#         FileNotFoundError: Если ноутбук не найден или директория не существует.
#         ValueError: Если найдено несколько ноутбуков, соответствующих префиксу.
#     """
#     # Нормализуем префикс пути (убираем '/' в начале/конце, если есть)
#     normalized_prefix = notebook_path_prefix.strip('/')

#     # Разделяем путь на директорию и базовое имя файла
#     if '/' in normalized_prefix:
#         parts = normalized_prefix.rsplit('/', 1)
#         notebook_dir_relative = parts[0]
#         notebook_base_name = parts[1]
#     else:
#         # Если путь без '/', значит ноутбук в корневой директории относительно base_dir
#         notebook_dir_relative = ""
#         notebook_base_name = normalized_prefix

#     # Формируем полный путь к директории, где должен лежать ноутбук
#     target_dir = os.path.join(base_dir, notebook_dir_relative)

#     print(f"Ищем ноутбук с базовым именем '{notebook_base_name}' в директории: {target_dir}")

#     if not os.path.isdir(target_dir):
#         raise FileNotFoundError(f"Директория не найдена: {target_dir}")

#     matches = []
#     try:
#         for filename in os.listdir(target_dir):
#             # Проверяем, что файл имеет расширение .zpln
#             if filename.endswith(".zpln"):
#                 # Убираем расширение
#                 name_without_ext = filename[:-5] # Длина ".zpln" = 5
#                 # Ищем последний символ '_' который разделяет имя и ID
#                 last_underscore_index = name_without_ext.rfind('_')

#                 # Проверяем, что '_' найден и часть до него совпадает с искомым базовым именем
#                 if last_underscore_index != -1 and name_without_ext[:last_underscore_index] == notebook_base_name:
#                      # Проверяем, что ID после '_' не пустой (на всякий случай)
#                      if last_underscore_index < len(name_without_ext) - 1:
#                          matches.append(os.path.join(target_dir, filename))

#     except OSError as e:
#         raise FileNotFoundError(f"Ошибка доступа к директории {target_dir}: {e}")

#     # Анализируем результаты поиска
#     if not matches:
#         raise FileNotFoundError(f"Ноутбук с префиксом '{notebook_path_prefix}' не найден в '{target_dir}'.")
#     elif len(matches) == 1:
#         print(f"Найден один совпадающий ноутбук: {matches[0]}")
#         return matches[0]
#     else:
#         # Найдено несколько совпадений (на случай, если заметку создали не из UI: в UI стоит проверка на одинаковые имена)
#         error_message = (
#             f"Найдено несколько ноутбуков, соответствующих префиксу '{notebook_path_prefix}' в '{target_dir}':\n"
#             f"{chr(10).join(matches)}\n" # chr(10) это перевод строки \n
#             "Пожалуйста, укажите полный путь к файлу ноутбука, включая его ID и расширение .zpln.\n"
#             "ID ноутбука обычно виден в его URL в адресной строке браузера (например, .../notebook/ID_НОУТБУКА)."
#         )
#         raise ValueError(error_message)

# def import_zeppelin_notebook_from_path(full_notebook_path):
#     """
#     Выполняет Python-код из указанного файла ноутбука Zeppelin
#     в текущем глобальном пространстве имен. Игнорирует параграфы не на Python.

#     Args:
# full_notebook_path (str): Полный путь к файлу .zpln ноутбука.

#     Returns:
#         bool: True если выполнение прошло успешно (или не было Python кода), False при ошибке.
#     """
#     print(f"Пытаюсь прочитать и выполнить код из: {full_notebook_path}")

#     if not os.path.exists(full_notebook_path):
#         print(f"ОШИБКА: Файл ноутбука не найден: {full_notebook_path}")
#         # В новой логике эта проверка дублируется с find_notebook_path,
#         # но оставим на случай прямого вызова этой функции
#         return False

#     try:
#         with open(full_notebook_path, 'r', encoding='utf-8') as f:
#             notebook_data = json.load(f)

#         python_code_to_execute = ""

#         # Проходим по всем параграфам
#         for i, paragraph in enumerate(notebook_data.get("paragraphs", [])):
#             code = paragraph.get("text", "")

#             # Проверяем, является ли параграф Python-параграфом
#             # (%python, %spark.pyspark, %flink.pyflink, %jdbc(python) и т.д.)
#             # Используем более гибкую проверку
#             if code and code.strip().startswith(("%python", "%spark.pyspark", "%flink.pyflink")):
#                 # Убираем строку с магической командой и лишние пробелы/переводы строк
#                 lines = code.splitlines()
#                 if lines:
#                     actual_code = "\n".join(lines[1:]) # Пропускаем первую строку
#                     if actual_code.strip():
#                         print(f"--- Добавляю код из параграфа {i+1} ---")
#                         python_code_to_execute += actual_code + "\n\n" # Добавляем код
#                 else:
#                      print(f"--- Параграф {i+1} пуст (после удаления магической команды) ---")

#             # Можно добавить обработку %jdbc(python) если нужно
#             elif code and code.strip().startswith("%jdbc(python)"):
#                  lines = code.splitlines()
#                  if len(lines) > 1: # Обычно первая строка - конфигурация JDBC
#                      actual_code = "\n".join(lines[1:])
#                      if actual_code.strip():
#                         print(f"--- Добавляю код из параграфа %jdbc(python) {i+1} ---")
#                         python_code_to_execute += actual_code + "\n\n"


#         if python_code_to_execute:
#             print("-" * 20)
#             print("Итоговый Python код для выполнения:")
#             print(python_code_to_execute.strip())
#             print("-" * 20)

#             # Выполняем собранный код в глобальном пространстве имен текущего ноутбука
#             exec(python_code_to_execute, globals())
#             print(f"Выполнение кода из {os.path.basename(full_notebook_path)} завершено.")
#             return True
#         else:
#             print(f"В ноутбуке {os.path.basename(full_notebook_path)} не найдено параграфов с исполняемым Python кодом.")
#             return True # Считаем успешным, т.к. ошибок не было, просто нечего было выполнять

#     except json.JSONDecodeError:
#         print(f"ОШИБКА: Не удалось распарсить JSON файл: {full_notebook_path}")
#         traceback.print_exc()
#         return False
#     except Exception as e:
#         print(f"ОШИБКА: Произошла непредвиденная ошибка при обработке {full_notebook_path}")
#         traceback.print_exc()
#         return False

# # --- Оберточная функция ---
# def import_note(notebook_path_prefix, base_dir=ZEPPELIN_BASE_DIR):
#     """
#     Находит и выполняет Python-код из другого ноутбука Zeppelin,
#     указанного по префиксу пути.

#     Args:
#         notebook_path_prefix (str): Префикс пути к ноутбуку, например "Libraries/main_config".
#         base_dir (str): Базовая директория ноутбуков Zeppelin.

#     Returns:
#         bool: Результат выполнения import_zeppelin_notebook_from_path.
#     """
#     try:
#         full_path = find_notebook_path(notebook_path_prefix, base_dir)
#         return import_zeppelin_notebook_from_path(full_path)
#     except (FileNotFoundError, ValueError) as e:
#         print(f"ОШИБКА ИМПОРТА: {e}")
#         return False
#     except Exception as e:
#         print(f"НЕПРЕДВИДЕННАЯ ОШИБКА при поиске или импорте '{notebook_path_prefix}':")
#         traceback.print_exc()
#         return False

import json
import os
import traceback
import inspect

# --- Конфигурация ---
ZEPPELIN_BASE_DIR = "/notebook"

def find_notebook_path(notebook_path_prefix, base_dir=ZEPPELIN_BASE_DIR):
    """
    Находит полный путь к файлу ноутбука Zeppelin по его префиксу пути.
    (Код этой функции остается без изменений)
    """
    normalized_prefix = notebook_path_prefix.strip('/')
    if '/' in normalized_prefix:
        parts = normalized_prefix.rsplit('/', 1)
        notebook_dir_relative = parts[0]
        notebook_base_name = parts[1]
    else:
        notebook_dir_relative = ""
        notebook_base_name = normalized_prefix

    target_dir = os.path.join(base_dir, notebook_dir_relative)
    print(f"Ищем ноутбук с базовым именем '{notebook_base_name}' в директории: {target_dir}")

    if not os.path.isdir(target_dir):
        raise FileNotFoundError(f"Директория не найдена: {target_dir}")

    matches = []
    try:
        for filename in os.listdir(target_dir):
            if filename.endswith(".zpln"):
                name_without_ext = filename[:-5]
                last_underscore_index = name_without_ext.rfind('_')
                if last_underscore_index != -1 and name_without_ext[:last_underscore_index] == notebook_base_name:
                     if last_underscore_index < len(name_without_ext) - 1:
                         matches.append(os.path.join(target_dir, filename))
    except OSError as e:
        raise FileNotFoundError(f"Ошибка доступа к директории {target_dir}: {e}")

    if not matches:
        raise FileNotFoundError(f"Ноутбук с префиксом '{notebook_path_prefix}' не найден в '{target_dir}'.")
    elif len(matches) == 1:
        print(f"Найден один совпадающий ноутбук: {matches[0]}")
        return matches[0]
    else:
        error_message = (
            f"Найдено несколько ноутбуков, соответствующих префиксу '{notebook_path_prefix}' в '{target_dir}':\n"
            f"{chr(10).join(matches)}\n"
            "Пожалуйста, укажите полный путь к файлу ноутбука, включая его ID и расширение .zpln.\n"
            "ID ноутбука обычно виден в его URL в адресной строке браузера (например, .../notebook/ID_НОУТБУКА)."
        )
        raise ValueError(error_message)

def import_zeppelin_notebook_from_path(full_notebook_path):
    """
    Выполняет Python-код из указанного файла ноутбука Zeppelin
    в глобальном пространстве имен ВЫЗЫВАЮЩЕГО кода.
    Игнорирует параграфы не на Python.

    Args:
        full_notebook_path (str): Полный путь к файлу .zpln ноутбука.

    Returns:
        bool: True если выполнение прошло успешно, False при ошибке.
    """
    print(f"Пытаюсь прочитать и выполнить код из: {full_notebook_path}")

    if not os.path.exists(full_notebook_path):
        print(f"ОШИБКА: Файл ноутбука не найден: {full_notebook_path}")
        return False

    try:
        with open(full_notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)

        python_code_to_execute = ""

        for i, paragraph in enumerate(notebook_data.get("paragraphs", [])):
            code = paragraph.get("text", "")
            # Убираем начальные пробелы/табуляции для надежной проверки префикса
            stripped_code = code.lstrip()

            # Проверяем на Python-магию
            is_python = False
            magic_line = ""
            if stripped_code.startswith(("%python", "%spark.pyspark", "%flink.pyflink")):
                is_python = True
                # Находим первую строку (магическую команду)
                lines = code.splitlines()
                if lines:
                    magic_line = lines[0]
            elif stripped_code.startswith("%jdbc(python)"):
                 # %jdbc(python) часто имеет конфигурацию в первой строке,
                 # но сам код выполняется как Python
                 is_python = True
                 lines = code.splitlines()
                 if lines:
                     magic_line = lines[0] # Сохраняем первую строку как "магическую"

            if is_python:
                # Убираем магическую строку (если она есть) и пустые строки в начале/конце
                if magic_line:
                    # Убедимся, что удаляем только первую строку, если она совпадает
                    if code.startswith(magic_line):
                         actual_code = code[len(magic_line):].lstrip('\n\r') # Удаляем магию и переводы строк после нее
                    else: # Если магия была с отступом, lstrip уже мог её изменить
                         lines = code.splitlines()
                         actual_code = "\n".join(lines[1:])
                else: # Если магии не было найдено (например, пустой параграф)
                    actual_code = code

                if actual_code.strip():
                    print(f"--- Добавляю код из параграфа {i+1} ('{magic_line[:20]}...') ---")
                    python_code_to_execute += actual_code + "\n\n"
                # else:
                #    print(f"--- Параграф {i+1} ('{magic_line[:20]}...') пуст или содержит только магию ---")

        if python_code_to_execute:
            print("-" * 20)
            print("Итоговый Python код для выполнения:")
            print(python_code_to_execute.strip())
            print("-" * 20)

            # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
            # Получаем фрейм вызывающего кода (тот, кто вызвал import_note)
            # Мы должны подняться на 2 уровня:
            # 1. Текущий фрейм (import_zeppelin_notebook_from_path)
            # 2. Фрейм обертки (import_note)
            # 3. Фрейм вызывающего кода (параграф в ноутбуке)
            caller_frame = None
            try:
                # inspect.stack() возвращает список кортежей FrameInfo
                # stack()[0] - текущий фрейм
                # stack()[1] - вызвавший текущую функцию (import_note)
                # stack()[2] - вызвавший import_note (параграф ноутбука)
                stack = inspect.stack()
                if len(stack) > 2:
                   caller_frame_info = stack[2] # FrameInfo для вызывающего кода
                   caller_globals = caller_frame_info.frame.f_globals
                   # Опционально: также можно передать locals вызывающего кода,
                   # хотя для определения функций/переменных обычно достаточно globals
                   # caller_locals = caller_frame_info.frame.f_locals
                   print(f"Выполняю код в глобальной области видимости модуля: {caller_globals.get('__name__', 'N/A')}")

                   # Выполняем собранный код в глобальном пространстве имен ВЫЗЫВАЮЩЕГО кода
                   exec(python_code_to_execute, caller_globals) # Используем найденные globals

                else:
                    # Если стек слишком короткий (неожиданно), используем обычные globals
                    # Это приведет к старому поведению (переменные в модуле)
                    print("ПРЕДУПРЕЖДЕНИЕ: Не удалось получить глобальную область видимости вызывающего кода через стек. Использую globals() модуля.")
                    exec(python_code_to_execute, globals())

            finally:
                # Важно удалить ссылки на фреймы после использования,
                # чтобы избежать утечек памяти (согласно документации inspect)
                del caller_frame # Если бы мы сохраняли фрейм
                # del stack # stack() возвращает список, он очистится сам

            print(f"Выполнение кода из {os.path.basename(full_notebook_path)} завершено.")
            return True
        else:
            print(f"В ноутбуке {os.path.basename(full_notebook_path)} не найдено параграфов с исполняемым Python кодом.")
            return True

    except json.JSONDecodeError:
        print(f"ОШИБКА: Не удалось распарсить JSON файл: {full_notebook_path}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"ОШИБКА: Произошла непредвиденная ошибка при обработке {full_notebook_path}")
        traceback.print_exc()
        return False

# --- Оберточная функция ---
def import_note(notebook_path_prefix, base_dir=ZEPPELIN_BASE_DIR):
    """
    Находит и выполняет Python-код из другого ноутбука Zeppelin,
    указанного по префиксу пути, делая его определения доступными
    в области видимости вызывающего кода.

    Args:
        notebook_path_prefix (str): Префикс пути к ноутбуку, например "Libraries/main_config".
        base_dir (str): Базовая директория ноутбуков Zeppelin.

    Returns:
        bool: Результат выполнения import_zeppelin_notebook_from_path.
    """
    # Эта функция теперь просто обертка, основная логика в import_zeppelin_notebook_from_path
    try:
        full_path = find_notebook_path(notebook_path_prefix, base_dir)
        # Вызываем внутреннюю функцию, которая сама определит область видимости
        return import_zeppelin_notebook_from_path(full_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"ОШИБКА ИМПОРТА: {e}")
        return False
    except Exception as e:
        print(f"НЕПРЕДВИДЕННАЯ ОШИБКА при поиске или импорте '{notebook_path_prefix}':")
        traceback.print_exc()
        return False