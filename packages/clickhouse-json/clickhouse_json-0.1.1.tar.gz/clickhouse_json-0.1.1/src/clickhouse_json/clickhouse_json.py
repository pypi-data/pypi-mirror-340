import clickhouse_connect  # Импорт библиотеки для работы с ClickHouse
import logging
import json
from typing import List, Dict, Any  # Импорт типов для аннотации
# cannot store nested lists

def escape_sql_string(html_string: str) -> str:
    """
    Экранирует специальные символы в строке для безопасной вставки в SQL-запросы.

    Args:
        html_string (str): Исходная строка с HTML-разметкой или текстом

    Returns:
        str: Экранированная строка, безопасная для использования в SQL
    """
    if html_string is None:  # Проверка на None для корректной обработки пустых значений
        return "NULL"  # Возвращаем строку "NULL" для вставки в SQL

    # Последовательное экранирование специальных символов
    escaped = html_string.replace("\\", "\\\\")  # Замена \ на \\ для корректной обработки слешей
    escaped = escaped.replace("'", "''")         # Замена ' на '' для защиты от SQL-инъекций
    escaped = escaped.replace('"', '\\"')        # Замена " на \" для корректной работы с кавычками
    escaped = escaped.replace("\0", "\\0")       # Экранирование нулевого символа
    escaped = escaped.replace("\n", "\\n")       # Замена новой строки на \n
    escaped = escaped.replace("\r", "\\r")       # Замена возврата каретки на \r
    escaped = escaped.replace("\t", "\\t")       # Замена табуляции на \t

    return escaped  # Возвращаем экранированную строку

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Преобразует вложенный словарь в плоский с составными ключами.

    Args:
        d (Dict[str, Any]): Исходный словарь
        parent_key (str): Префикс для ключей (используется при рекурсии)
        sep (str): Разделитель для составных ключей

    Returns:
        Dict[str, Any]: Плоский словарь
    """
    items = []  # Список для хранения пар ключ-значение
    for key, value in d.items():  # Итерация по ключам и значениям словаря
        # Формирование нового ключа с учетом родительского ключа
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):  # Если значение - словарь
            # Рекурсивно обрабатываем вложенный словарь
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:  # Если значение - не словарь
            items.append((new_key, value))  # Добавляем пару в список
    return dict(items)  # Преобразуем список пар в словарь

def merge_dicts(dict1, dict2):
    """
    Объединяет два словаря. Если есть повторяющиеся ключи, значения из dict2 перезапишут значения из dict1.

    :param dict1: Первый словарь
    :param dict2: Второй словарь
    :return: Новый объединённый словарь
    """
    merged = dict1.copy()  # Создаем копию первого словаря, чтобы не изменять исходные данные
    merged.update(dict2)   # Добавляем элементы из второго словаря
    return merged

def infer_table_structure(json_data: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Определяет структуру таблицы на основе первого элемента JSON-данных.

    Args:
        json_data (List[Dict[str, Any]]): Список словарей с данными

    Returns:
        Dict[str, str]: Словарь с именами колонок и их типами данных
    """
    sample_entry = json_data[0]  # Берем первый элемент как образец
    flat_entry = flatten_dict(sample_entry)  # Преобразуем в плоский вид
    structure = {}  # Словарь для хранения структуры таблицы

    for key, value in flat_entry.items():  # Итерация по ключам и значениям
        if isinstance(value, int):
            structure[key] = "UInt32 DEFAULT NULL"  # Целые числа с DEFAULT NULL
        elif isinstance(value, float):
            structure[key] = "Float64 DEFAULT NULL"  # Дробные числа с DEFAULT NULL
        elif isinstance(value, str):
            structure[key] = "String DEFAULT NULL"  # Строки с DEFAULT NULL
        elif isinstance(value, list):
            if not value:
                structure[key] = "Array(String)"  # Пустые списки → массив строк
            elif all(isinstance(i, dict) for i in value):
                nested_keys = value[0].keys()
                # Убрано DEFAULT NULL из Tuple()
                structure[key] = f"Array(Tuple({', '.join(f'{k} String' for k in nested_keys)}))"
            else:
                structure[key] = "Array(String)"  # Массив строк
        elif value is None:
            structure[key] = "String DEFAULT NULL"  # NULL по умолчанию
        else:
            structure[key] = "String DEFAULT NULL"  # По умолчанию строки с DEFAULT NULL

    return structure



def load_data_from_json(filename):
    with open(filename, 'r') as f:
        prices = json.load(f)
    return prices

def save_data_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def make_connection_string(host, username='default',password='',port=8123):
    return f"http://{username}:{password}@{host}:{port}/"


class ClickHouseJSONHandler:
    """Класс для работы с JSON-данными и их вставкой в ClickHouse."""


    #Инициализация клиента ClickHouse.
    def __init__(self, connection_string, database, table_name=None, json_as_string=False):
        self.connection_string = connection_string
        self.database_name = database
        self.table_name = table_name
        self.json_as_string = json_as_string
        self.client = self._get_client()

    def _get_client(self):
        try:
            return clickhouse_connect.get_client(dsn=self.connection_string, database=self.database_name)
        except Exception as e:
            logging.error(f"Error connecting to Clickhouse: {e}")
            return None

    def _ensure_connection(self):
        if self.client is None or not self.client.ping():
            logging.warning("Reconnecting to Clickhouse...")
            self.client = self._get_client()


    def create_table(self, table_name: str, structure: Dict[str, str]):
        """
        Создает таблицу в ClickHouse на основе заданной структуры.

        Args:
            table_name (str): Название таблицы
            structure (Dict[str, str]): Структура таблицы (колонки и типы)
        """
        self._ensure_connection()
        # Формируем строку с определением колонок
        columns = ",\n        ".join(f"{col} {dtype} " for col, dtype in structure.items())
        # SQL-запрос для создания таблицы с движком MergeTree
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id UUID DEFAULT generateUUIDv4(),
            __metatimestamp_timestamp DateTime DEFAULT now(),
            {columns}
        ) ENGINE = MergeTree
        ORDER BY tuple()  -- Простой порядок сортировки
        '''
        self.client.command(query)  # Выполняем запрос

    def insert_json_data(self, table_name: str, json_data: List[Dict[str, Any]]):
        """
        Вставляет JSON-данные в таблицу ClickHouse.

        Args:
            table_name (str): Название таблицы
            json_data (List[Dict[str, Any]]): Список словарей с данными
        """

        try:
            self._ensure_connection()
            formatted_data = []  # Список для хранения отформатированных записей
            columns = set()  # Множество для хранения всех уникальных колонок

            # Подготовка данных для вставки
            for entry in json_data:
                flat_entry = flatten_dict(entry)  # Преобразуем в плоский вид
                formatted_entry = {}

                for key, value in flat_entry.items():
                    columns.add(key)
                    if isinstance(value, list):
                        if not value:
                            formatted_entry[key] = []
                        elif all(isinstance(i, dict) for i in value):
                            formatted_entry[key] = [tuple(item.get(k, "NULL") for k in item.keys()) for item in
                                                    value]
                        else:
                            formatted_entry[key] = [v if v is not None else "NULL" for v in value]
                    else:
                        formatted_entry[key] = value
                formatted_data.append(formatted_entry)

            columns = sorted(columns)
            values = []

            # Формирование строк значений для SQL
            for entry in formatted_data:
                row_values = []
                for col in columns:
                    value = entry.get(col, None)
                    if isinstance(value, str):
                        escaped_value = escape_sql_string(value)
                        row_values.append(f"'{escaped_value}'")
                    elif value is None:
                        row_values.append("NULL")
                    elif isinstance(value, list):
                        row_values.append(str([tuple("NULL" if v is None else v for v in item)
                                               if isinstance(item, tuple) else item
                                               for item in value]))
                    else:
                        row_values.append(str(value))
                values.append(f"({', '.join(row_values)})")

            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {', '.join(values)}"

            try:
                self.client.command(query)
            except Exception as e:
                logging.error(f"Ошибка при выполнении SQL-запроса: {e}")
                raise

        except Exception as e:
            logging.error(f"Ошибка при обработке JSON-данных: {e}")
            raise

        return True



def main():
    """Основная функция для демонстрации работы с ClickHouse."""
    # Создаем экземпляр обработчика с указанием хоста и базы данных
    connection_string = make_connection_string(host='192.168.192.42')
    handler = ClickHouseJSONHandler(connection_string, database='mart')

    # Определяем структуру таблицы на основе JSON
    json_data = load_data_from_json("../../../data/complex_data.json")
    structure = infer_table_structure([json_data])
    # Создаем таблицу в ClickHouse
    table_name = "complex_data_test"
    handler.create_table(table_name, structure)
    # Вставляем данные в таблицу
    handler.insert_json_data(table_name, [json_data])
    print("Данные успешно вставлены в ClickHouse")


if __name__ == "__main__":
    main()  # Запуск основной функции при выполнении скрипта