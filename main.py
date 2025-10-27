import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 1 — прототип)"
    )

    # Строго по требованиям: 4 настраиваемых параметра
    parser.add_argument(
        "-n", "--package_name",
        type=str,
        required=True,
        help="Имя анализируемого пакета"
    )

    parser.add_argument(
        "-u", "--repo_url",
        type=str,
        required=True,
        help="URL-адрес репозитория или путь к тестовому репозиторию"
    )

    parser.add_argument(
        "-m", "--work_mode",
        type=str,
        choices=["local", "remote", "test"],
        required=True,
        help="Режим работы с тестовым репозиторием (local, remote, test)"
    )

    parser.add_argument(
        "-f", "--filter",
        type=str,
        default="",
        help="Подстрока для фильтрации пакетов (необязательно)"
    )

    args = parser.parse_args()

    # === Вывод всех параметров в формате ключ-значение ===
    print("\n===== Настройки запуска =====")
    print(f"Имя пакета          : {args.package_name}")
    print(f"URL репозитория     : {args.repo_url}")
    print(f"Режим работы        : {args.work_mode}")
    print(f"Фильтр пакетов      : {args.filter if args.filter else '(не задан)'}")
    print("============================\n")

    # === Обработка ошибок для всех параметров ===
    try:
        # Проверка имени пакета
        if not args.package_name or not args.package_name.strip():
            raise ValueError("Имя пакета не может быть пустым")

        # Проверка URL/пути репозитория
        if not args.repo_url or not args.repo_url.strip():
            raise ValueError("URL репозитория не может быть пустым")

        # Проверка режима работы
        if args.work_mode not in ["local", "remote", "test"]:
            raise ValueError("Некорректный режим работы. Допустимые значения: local, remote, test")

        # Проверка фильтра (если указан)
        if args.filter and not isinstance(args.filter, str):
            raise ValueError("Фильтр должен быть строкой")

        print("✅ Все параметры корректны!")
        return 0

    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())