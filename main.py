import argparse
import sys
import requests
import json
from urllib.parse import urljoin
from typing import List, Dict, Any


class DependencyAnalyzer:
    def __init__(self, package_name: str, repo_url: str, work_mode: str, filter_str: str = ""):
        self.package_name = package_name
        self.repo_url = repo_url
        self.work_mode = work_mode
        self.filter_str = filter_str

    def get_npm_package_info(self) -> Dict[str, Any]:

        if self.work_mode == "test":
            # Для тестового режима используем локальные данные
            return self._get_test_package_info()


        npm_registry_url = "https://registry.npmjs.org"
        package_url = f"{npm_registry_url}/{self.package_name}"

        try:
            response = requests.get(package_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при получении информации о пакете: {e}")

    def _get_test_package_info(self) -> Dict[str, Any]:


        test_packages = {
            "react": {
                "name": "react",
                "version": "18.2.0",
                "dependencies": {
                    "loose-envify": "^1.1.0",
                    "object-assign": "^4.1.1"
                }
            },
            "express": {
                "name": "express",
                "version": "4.18.2",
                "dependencies": {
                    "accepts": "~1.3.8",
                    "array-flatten": "1.1.1",
                    "body-parser": "1.20.1",
                    "content-disposition": "0.5.4",
                    "cookie": "0.5.0",
                    "cookie-signature": "1.0.6"
                }
            },
            "lodash": {
                "name": "lodash",
                "version": "4.17.21",
                "dependencies": {}
            },
            "vue": {
                "name": "vue",
                "version": "3.3.4",
                "dependencies": {
                    "@vue/compiler-dom": "3.3.4",
                    "@vue/compiler-sfc": "3.3.4",
                    "@vue/reactivity": "3.3.4",
                    "@vue/runtime-dom": "3.3.4",
                    "@vue/shared": "3.3.4"
                }
            }
        }

        if self.package_name.lower() in test_packages:
            return test_packages[self.package_name.lower()]
        else:

            return {
                "name": self.package_name,
                "version": "1.0.0",
                "dependencies": {
                    "dep1": "^1.0.0",
                    "dep2": "^2.0.0",
                    "dep3": "^3.0.0"
                }
            }

    def get_direct_dependencies(self) -> List[str]:

        package_info = self.get_npm_package_info()

        dependencies = []


        if "dependencies" in package_info and package_info["dependencies"]:
            dependencies.extend(list(package_info["dependencies"].keys()))


        for dep_type in ["devDependencies", "peerDependencies", "optionalDependencies"]:
            if dep_type in package_info and package_info[dep_type]:
                dependencies.extend(list(package_info[dep_type].keys()))


        if self.filter_str:
            dependencies = [dep for dep in dependencies if self.filter_str.lower() in dep.lower()]


        return sorted(list(set(dependencies)))

    def analyze_dependencies(self):

        try:
            print(f"\n  Анализ зависимостей для пакета: {self.package_name}")
            print(f"  Режим работы: {self.work_mode}")
            print(f"  Источник: {self.repo_url}")

            if self.filter_str:
                print(f"  Фильтр: '{self.filter_str}'")

            print("\n" + "=" * 50)


            package_info = self.get_npm_package_info()
            print(f"  Информация о пакете:")
            print(f"   Имя: {package_info.get('name', 'N/A')}")
            print(f"   Версия: {package_info.get('version', 'N/A')}")
            print(f"   Описание: {package_info.get('description', 'N/A')}")

            print("\n  Прямые зависимости:")
            dependencies = self.get_direct_dependencies()

            if not dependencies:
                print("    Пакет не имеет зависимостей")
            else:
                for i, dep in enumerate(dependencies, 1):
                    print(f"   {i:2d}. {dep}")

                print(f"\n Всего прямых зависимостей: {len(dependencies)}")

            return dependencies

        except Exception as e:
            print(f"  Ошибка при анализе зависимостей: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 2 — сбор данных)"
    )

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


    print("\n===== Настройки запуска =====")
    print(f"Имя пакета          : {args.package_name}")
    print(f"URL репозитория     : {args.repo_url}")
    print(f"Режим работы        : {args.work_mode}")
    print(f"Фильтр пакетов      : {args.filter if args.filter else '(не задан)'}")
    print("============================\n")

    try:

        if not args.package_name or not args.package_name.strip():
            raise ValueError("Имя пакета не может быть пустым")

        if not args.repo_url or not args.repo_url.strip():
            raise ValueError("URL репозитория не может быть пустым")

        if args.work_mode not in ["local", "remote", "test"]:
            raise ValueError("Некорректный режим работы. Допустимые значения: local, remote, test")

        if args.filter and not isinstance(args.filter, str):
            raise ValueError("Фильтр должен быть строкой")

        print(" Все параметры корректны!")


        analyzer = DependencyAnalyzer(
            package_name=args.package_name,
            repo_url=args.repo_url,
            work_mode=args.work_mode,
            filter_str=args.filter
        )


        dependencies = analyzer.analyze_dependencies()

        return 0

    except ValueError as e:
        print(f"  Ошибка: {e}")
        return 1
    except Exception as e:
        print(f" Неожиданная ошибка: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())