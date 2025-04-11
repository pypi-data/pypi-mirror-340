import json
import os
import traceback
import inspect

# --- Конфигурация ---
ZEPPELIN_BASE_DIR = "/notebook" # Убедитесь, что этот путь корректен

# --- find_notebook_path остается без изменений ---
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
    print(f"[DEBUG] Ищем ноутбук с базовым именем '{notebook_base_name}' в директории: {target_dir}") # Добавил DEBUG

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
        print(f"Найден один совпадающий ноутбук: {matches[0]}") # Эта строка у вас печатается
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
    """
    print(f"[DEBUG] Читаю файл: {full_notebook_path}") # Добавил DEBUG

    if not os.path.exists(full_notebook_path):
        print(f"ОШИБКА: Файл ноутбука не найден: {full_notebook_path}")
        return False

    try:
        with open(full_notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        print(f"[DEBUG] JSON успешно загружен.") # Добавил DEBUG

        python_code_to_execute = ""
        found_python_paragraph = False # Флаг для отладки

        # Проходим по всем параграфам
        for i, paragraph in enumerate(notebook_data.get("paragraphs", [])):
            paragraph_index = i + 1
            code = paragraph.get("text", "")
            print(f"\n[DEBUG] Параграф {paragraph_index}: Проверяю код (первые 50 символов): '{code[:50]}...'") # Добавил DEBUG

            if not code or not code.strip():
                print(f"[DEBUG] Параграф {paragraph_index}: Пустой или содержит только пробелы.")
                continue # Пропускаем пустые параграфы

            # Убираем начальные пробелы/табуляции для надежной проверки префикса
            stripped_code = code.lstrip()
            lines = code.splitlines() # Разбиваем на строки СРАЗУ
            first_line = lines[0] if lines else ""

            # Проверяем, является ли параграф Python-параграфом
            is_python = False
            if stripped_code.startswith(("%python", "%spark.pyspark", "%flink.pyflink")):
                is_python = True
                print(f"[DEBUG] Параграф {paragraph_index}: Обнаружен Python (стандартный). Первая строка: '{first_line}'")
            elif stripped_code.startswith("%jdbc(python)"):
                is_python = True
                print(f"[DEBUG] Параграф {paragraph_index}: Обнаружен Python (jdbc). Первая строка: '{first_line}'")
            else:
                print(f"[DEBUG] Параграф {paragraph_index}: Не является Python параграфом (пропускаем). Первая строка: '{first_line}'")

            if is_python:
                found_python_paragraph = True # Отмечаем, что нашли хотя бы один
                # --- УЛУЧШЕННАЯ ЛОГИКА ИЗВЛЕЧЕНИЯ КОДА ---
                # Просто берем все строки, начиная со второй
                if len(lines) > 1:
                    actual_code = "\n".join(lines[1:])
                    print(f"[DEBUG] Параграф {paragraph_index}: Извлечен код (строки 2+).")
                    if actual_code.strip():
                        print(f"--- Добавляю код из параграфа {paragraph_index} ---")
                        python_code_to_execute += actual_code + "\n\n" # Добавляем код
                    else:
                        print(f"[DEBUG] Параграф {paragraph_index}: Код после первой строки пуст.")
                else:
                    # Если только одна строка (магическая команда) - кода нет
                    print(f"[DEBUG] Параграф {paragraph_index}: Содержит только одну строку (магическую команду), кода нет.")
            # --- КОНЕЦ УЛУЧШЕННОЙ ЛОГИКИ ---

        print("\n[DEBUG] Проверка после цикла обработки параграфов:") # Добавил DEBUG
        print(f"[DEBUG] Найден хотя бы один Python параграф: {found_python_paragraph}") # Добавил DEBUG
        print(f"[DEBUG] Длина собранного кода python_code_to_execute: {len(python_code_to_execute)}") # Добавил DEBUG

        if python_code_to_execute:
            print("-" * 20)
            print("Итоговый Python код для выполнения:")
            print(python_code_to_execute.strip())
            print("-" * 20)

            caller_frame = None
            caller_globals = None
            try:
                stack = inspect.stack()
                print(f"[DEBUG] Глубина стека вызовов: {len(stack)}") # Добавил DEBUG
                # Печать имен функций в стеке для диагностики
                # for idx, frame_info in enumerate(stack):
                #     print(f"[DEBUG] Стек[{idx}]: {frame_info.function} в {os.path.basename(frame_info.filename)}")

                if len(stack) > 2:
                   caller_frame_info = stack[2]
                   caller_globals = caller_frame_info.frame.f_globals
                   print(f"[DEBUG] Выполняю код в глобальной области видимости модуля: {caller_globals.get('__name__', 'N/A')}")
                   exec(python_code_to_execute, caller_globals) # Используем найденные globals
                   print(f"Выполнение кода из {os.path.basename(full_notebook_path)} завершено.")
                   return True
                else:
                    print("ПРЕДУПРЕЖДЕНИЕ: Не удалось получить глобальную область видимости вызывающего кода через стек (глубина < 3). Использую globals() модуля.")
                    exec(python_code_to_execute, globals()) # Старое поведение
                    print(f"Выполнение кода из {os.path.basename(full_notebook_path)} завершено (в области видимости модуля).")
                    return True # Технически успешно, но не то, что нужно

            except Exception as exec_err:
                 print(f"ОШИБКА ВО ВРЕМЯ ВЫПОЛНЕНИЯ 'exec':")
                 traceback.print_exc()
                 return False # Явно указываем на ошибку выполнения
            finally:
                # Очистка ссылок
                del caller_frame
                # del stack # Локальная переменная очистится сама
                # print("[DEBUG] Ссылки на фреймы очищены.")

        elif found_python_paragraph:
             print(f"В ноутбуке {os.path.basename(full_notebook_path)} найдены Python параграфы, но они не содержат исполняемого кода (после удаления магических команд).")
             return True # Считаем успешным, т.к. ошибок не было
        else:
            print(f"В ноутбуке {os.path.basename(full_notebook_path)} не найдено параграфов с исполняемым Python кодом (например, %python, %spark.pyspark).")
            return True # Считаем успешным

    except json.JSONDecodeError:
        print(f"ОШИБКА: Не удалось распарсить JSON файл: {full_notebook_path}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"ОШИБКА: Произошла непредвиденная ошибка при обработке {full_notebook_path}")
        traceback.print_exc()
        return False

# --- Оберточная функция import_note остается без изменений ---
def import_note(notebook_path_prefix, base_dir=ZEPPELIN_BASE_DIR):
    """
    Находит и выполняет Python-код из другого ноутбука Zeppelin,
    указанного по префиксу пути, делая его определения доступными
    в области видимости вызывающего кода.
    """
    try:
        full_path = find_notebook_path(notebook_path_prefix, base_dir)
        return import_zeppelin_notebook_from_path(full_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"ОШИБКА ИМПОРТА: {e}")
        return False
    except Exception as e:
        print(f"НЕПРЕДВИДЕННАЯ ОШИБКА при поиске или импорте '{notebook_path_prefix}':")
        traceback.print_exc()
        return False