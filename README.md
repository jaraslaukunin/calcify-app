<div align="center">

# Calcify

**Инженерный калькулятор на Python и Kivy: дроби, π, тригонометрия — один код для Android и macOS.**

[![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2-2E8B57?style=for-the-badge&logo=kivy&logoColor=white)](https://kivy.org/)
[![Android](https://img.shields.io/badge/Android-Buildozer-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://buildozer.readthedocs.io/)
[![PyInstaller](https://img.shields.io/badge/PyInstaller-Desktop-2B2B2B?style=for-the-badge)](https://pyinstaller.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-calcify--app-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jaraslaukunin/calcify-app)

**[Возможности](#возможности)** · [Режимы и вычисления](#режимы-и-вычисления) · [Технологии](#технологии) · [Быстрый старт](#быстрый-старт) · [Сборка](#сборка) · [Структура проекта](#структура-проекта) · [Лицензия](#лицензия)

</div>

---

## О проекте

**Calcify** — калькулятор с интерфейсом на Kivy: сетка из 40 кнопок, крупный дисплей с отдельной строкой выражения и результата, светлая тема и шрифт JetBrains Mono. Окно фиксированного размера 420×720 — макет рассчитан и на десктоп, и на телефон в портретной ориентации.

Помимо обычной арифметики Calcify умеет работать с дробями: результат автоматически показывается обыкновенной дробью (в том числе с целой частью), а кнопка **F ↔ D** переключает дробь и десятичную запись. Отдельно обрабатываются выражения с π — ответ тоже может выглядеть как дробь с π.

Приложение полностью локальное: без сети, базы данных и аккаунтов. Вся логика — в одном `main.py`, оформление кнопок — в `calcify.kv`.

## Возможности

| Раздел | Что умеет |
| :-- | :-- |
| Арифметика | `+`, `−`, `×`, `÷`, возведение в степень `^`, корень `√`, скобки, `±`, `DEL`, `C` |
| Тригонометрия | `sin`, `cos`, `tg` и обратные `arcsin`, `arccos`, `arctg` |
| Логарифмы | `log₁₀`, натуральный `ln` и `log` с произвольным основанием |
| Константы | `π` и `e` |
| Дроби | Дробный вывод результата, смешанные дроби, переключение **F ↔ D** |
| ANS | Вставка последнего результата в новое выражение |
| Режимы углов | `AUTO`, `RAD`, `DEG` с индикатором на дисплее |
| Ввод | Автозакрытие скобок, неявное умножение (`2π`, `3(4+1)`), защита от двойных операторов и лишних нулей |
| Ошибки | Вместо падения — сообщение «Ошибка» и возможность продолжить ввод |

## Режимы и вычисления

| Режим | Поведение |
| :-- | :-- |
| `AUTO` | Радианы, если в выражении встречается `π`, иначе градусы |
| `RAD` | Все тригонометрические функции считаются в радианах |
| `DEG` | Аргументы и результаты обратных функций переводятся в градусы |

Ввод собирается в строку, где `×`, `÷` и `−` заменяются на Python-операторы, `tg`/`arcsin`/`arctg` — на `tan`/`asin`/`atan`, а `log(основание, аргумент)` переписывается в отношение десятичных логарифмов. Вычисление идёт через `eval` с собственным словарём функций и пустым `__builtins__`; результат форматируется через `fractions.Fraction` (дроби и π) либо в экспоненциальной записи для очень больших чисел.

## Технологии

- **Python 3** — язык приложения, без сторонних библиотек кроме Kivy.
- **Kivy 2** — кроссплатформенный UI: `BoxLayout`, `GridLayout`, canvas-рисование скруглённых кнопок.
- **KV-язык** — правила оформления в `calcify.kv`.
- **Buildozer / python-for-android** — сборка debug-APK для Android.
- **PyInstaller** — сборка настольного приложения (в `Calcify.spec` описан macOS-бандл `Calcify.app`).
- **Docker** — образ на базе `kivy/buildozer` как воспроизводимое окружение сборки.
- **GitHub Actions** — workflow `build-apk.yml` собирает APK и складывает его в артефакт.

## Быстрый старт

### Требования

- Python 3.10+ (в CI используется 3.10)
- Kivy 2
- для Android — Buildozer и JDK; Android SDK/NDK Buildozer скачивает сам

### Установка и запуск

```bash
git clone https://github.com/jaraslaukunin/calcify-app.git
cd calcify-app

python3 -m venv .venv
source .venv/bin/activate
pip install kivy

python main.py
```

В репозитории нет `requirements.txt`, поэтому Kivy ставится вручную, а версия зависимости не зафиксирована. Шрифты `JetBrainsMono-Regular.ttf` и `JetBrainsMono-Bold.ttf` лежат в корне: если их не найдёт `LabelBase`, приложение откатится на встроенный в Kivy Roboto.

## Сборка

### Android (Buildozer)

```bash
pip install buildozer cython
buildozer android debug
```

Готовый APK появится в `bin/`. Настройки из `buildozer.spec`:

| Параметр | Значение |
| :-- | :-- |
| `title` | `Calcify (L28)` |
| `package.name` / `package.domain` | `calcify` / `org.jaraslaukunin` |
| `version` | `0.1` |
| `requirements` | `python3,kivy` |
| `orientation` | `portrait` |
| `android.archs` | `arm64-v8a, armeabi-v7a` |

### Docker

`Dockerfile` собирает окружение на базе `kivy/buildozer` (linux/amd64) и добавляет 32-битные библиотеки:

```bash
docker build -t calcify-build .
docker run --rm -v "$PWD":/home/user/hostcwd calcify-build buildozer android debug
```

`/home/user/hostcwd` — рабочий каталог базового образа `kivy/buildozer`, в него монтируется проект.

### Десктоп (PyInstaller)

```bash
pip install pyinstaller
pyinstaller Calcify.spec
```

Спек включает `calcify.kv` и оба шрифта в `datas`, поэтому ресурсы попадают внутрь сборки. Спек рассчитан на macOS: на выходе — `dist/Calcify.app` и рядом каталог `dist/Calcify/`.

### CI

Workflow `.github/workflows/build-apk.yml` запускается на push в `main`/`master` и вручную (`workflow_dispatch`). На `ubuntu-latest` он ставит Python 3.10, Buildozer и Cython, выполняет `buildozer android debug` и загружает артефакт `Calcify-APK` из `bin/*.apk`.

## Структура проекта

```text
calcify-app/
├── main.py                      # приложение: UI, ввод, разбор выражения, форматирование
├── calcify.kv                   # правила оформления RoundedButton и фона
├── buildozer.spec               # конфигурация Android-сборки
├── Calcify.spec                 # конфигурация PyInstaller
├── Dockerfile                   # окружение сборки на kivy/buildozer
├── .github/workflows/build-apk.yml
├── JetBrainsMono-Regular.ttf
├── JetBrainsMono-Bold.ttf
└── bin/                         # сюда Buildozer кладёт APK (в репозитории пусто)
```

Каталоги `build/`, `dist/` и `.buildozer/` — локальные артефакты сборки, в репозиторий они не входят.

## Известные ограничения

- Кнопка `%` отправляет в выражение Python-оператор остатка от деления, а не «процент от числа»: `200 % 10` вернёт `0`.
- Нет истории вычислений и ячеек памяти (`M+`, `MR`).
- В коде есть обработчики `1/x` и модуля числа, но соответствующих кнопок в сетке нет.
- Нет `requirements.txt`, `.gitignore` и тестов — версии зависимостей и артефакты сборки не зафиксированы.

## Лицензия

Проект распространяется под лицензией [**MIT**](LICENSE): код можно свободно использовать, изменять и распространять при сохранении текста лицензии и указания авторства.

---

<div align="center">

[github.com/jaraslaukunin/calcify-app](https://github.com/jaraslaukunin/calcify-app)

Если калькулятор пригодился — поставьте ⭐

</div>
