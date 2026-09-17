# -*- coding: utf-8 -*-
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, 'template.txt'), 'r', encoding='utf-8') as f:
    TEMPLATE = f.read()

def T(code):
    return code.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

def J(obj):
    return json.dumps(obj, ensure_ascii=False)

# ============ C ============
c_lessons = [
{"title":"Основы printf","icon":"1","tasks":[
 {"name":"Hello World","code":'#include <stdio.h>\n\nint main() {\n    printf("Привет, мир!\\n");\n    return 0;\n}',"expect":"Привет, мир!","sample":"Привет, мир!","hint":"printf(\"текст\\n\") — вывод"},
 {"name":"Несколько строк","code":'#include <stdio.h>\n\nint main() {\n    printf("Строка 1\\n");\n    printf("Строка 2\\n");\n    return 0;\n}',"expect":"Строка 1\nСтрока 2","sample":"Строка 1\\nСтрока 2","hint":"\\n — перенос строки"},
 {"name":"Числа","code":'#include <stdio.h>\n\nint main() {\n    printf("%d\\n", 42);\n    return 0;\n}',"expect":"42","sample":"42","hint":"%d — вывод целого числа"}
]},
{"title":"Переменные","icon":"2","tasks":[
 {"name":"Типы","code":'#include <stdio.h>\n\nint main() {\n    int age = 10;\n    double pi = 3.14;\n    char letter = \'A\';\n    printf("%d %.2f %c", age, pi, letter);\n    return 0;\n}',"expect":"10 3.14 A","sample":"10 3.14 A","hint":"%d — int, %.2f — double, %c — char"},
 {"name":"Ввод scanf","code":'#include <stdio.h>\n\nint main() {\n    int x;\n    scanf("%d", &x);\n    printf("%d", x * 2);\n    return 0;\n}',"expect":"","sample":"12 (если ввести 6)","hint":"scanf(\"%d\", &x) — ввод"}
]},
{"title":"Математика","icon":"+","tasks":[
 {"name":"Арифметика","code":'#include <stdio.h>\n\nint main() {\n    int a = 10, b = 3;\n    printf("%d\\n", a + b);\n    printf("%d\\n", a - b);\n    printf("%d\\n", a * b);\n    printf("%d\\n", a / b);\n    return 0;\n}',"expect":"13\n7\n30\n3","sample":"13\\n7\\n30\\n3","hint":"int / int = int. 10 / 3 = 3"},
 {"name":"Остаток","code":'#include <stdio.h>\n\nint main() {\n    printf("%d", 17 % 5);\n    return 0;\n}',"expect":"2","sample":"2","hint":"% — остаток от деления"}
]},
{"title":"Условия","icon":"⚖️","tasks":[
 {"name":"if/else","code":'#include <stdio.h>\n\nint main() {\n    int age = 12;\n    if (age >= 18) {\n        printf("Взрослый");\n    } else {\n        printf("Ребёнок");\n    }\n    return 0;\n}',"expect":"Ребёнок","sample":"Ребёнок","hint":"if (условие) { } else { }"},
 {"name":"else if","code":'#include <stdio.h>\n\nint main() {\n    int mark = 85;\n    if (mark >= 90) {\n        printf("Отлично");\n    } else if (mark >= 70) {\n        printf("Хорошо");\n    } else {\n        printf("Нормально");\n    }\n    return 0;\n}',"expect":"Хорошо","sample":"Хорошо","hint":"else if — несколько условий"}
]},
{"title":"Циклы","icon":"🔄","tasks":[
 {"name":"for","code":'#include <stdio.h>\n\nint main() {\n    for (int i = 0; i < 5; i++) {\n        printf("%d\\n", i);\n    }\n    return 0;\n}',"expect":"0\n1\n2\n3\n4","sample":"0\\n1\\n2\\n3\\n4","hint":"for (начало; условие; шаг)"},
 {"name":"while","code":'#include <stdio.h>\n\nint main() {\n    int n = 3;\n    while (n > 0) {\n        printf("%d\\n", n);\n        n--;\n    }\n    return 0;\n}',"expect":"3\n2\n1","sample":"3\\n2\\n1","hint":"while (условие) — пока верно"}
]},
{"title":"Массивы","icon":"📋","tasks":[
 {"name":"Массив","code":'#include <stdio.h>\n\nint main() {\n    int nums[3] = {10, 20, 30};\n    printf("%d\\n", nums[0]);\n    printf("%d\\n", nums[2]);\n    return 0;\n}',"expect":"10\n30","sample":"10\\n30","hint":"int arr[N] = {...} — счёт с 0"},
 {"name":"Сумма","code":'#include <stdio.h>\n\nint main() {\n    int nums[4] = {5, 10, 15, 20};\n    int sum = 0;\n    for (int i = 0; i < 4; i++) {\n        sum += nums[i];\n    }\n    printf("%d", sum);\n    return 0;\n}',"expect":"50","sample":"50","hint":"sum += nums[i]"}
]},
{"title":"Указатели","icon":"👉","tasks":[
 {"name":"& и *","code":'#include <stdio.h>\n\nint main() {\n    int x = 10;\n    int *p = &x;\n    printf("%d\\n", *p);\n    *p = 20;\n    printf("%d", x);\n    return 0;\n}',"expect":"10\n20","sample":"10\\n20","hint":"&x — адрес, *p — значение по адресу"},
 {"name":"Указатель в функции","code":'#include <stdio.h>\n\nvoid addOne(int *n) {\n    (*n)++;\n}\n\nint main() {\n    int a = 5;\n    addOne(&a);\n    printf("%d", a);\n    return 0;\n}',"expect":"6","sample":"6","hint":"Передача по указателю меняет оригинал"}
]},
{"title":"Функции","icon":"⚙️","tasks":[
 {"name":"Функция","code":'#include <stdio.h>\n\nvoid greet() {\n    printf("Привет!\\n");\n}\n\nint main() {\n    greet();\n    return 0;\n}',"expect":"Привет!","sample":"Привет!","hint":"void имя() { } — ничего не возвращает"},
 {"name":"return","code":'#include <stdio.h>\n\nint square(int x) {\n    return x * x;\n}\n\nint main() {\n    printf("%d", square(7));\n    return 0;\n}',"expect":"49","sample":"49","hint":"int — возвращает число"},
 {"name":"Факториал (рекурсия)","code":'#include <stdio.h>\n\nint fact(int n) {\n    if (n <= 1) return 1;\n    return n * fact(n - 1);\n}\n\nint main() {\n    printf("%d", fact(5));\n    return 0;\n}',"expect":"120","sample":"120","hint":"n! = n * (n-1)!"}
]},
{"title":"Структуры","icon":"🏗️","tasks":[
 {"name":"struct","code":'#include <stdio.h>\n\nstruct Cat {\n    char name[20];\n    int age;\n};\n\nint main() {\n    struct Cat cat;\n    cat.age = 3;\n    printf("%d", cat.age);\n    return 0;\n}',"expect":"3","sample":"3","hint":"struct — свой тип данных"},
 {"name":"typedef","code":'#include <stdio.h>\n\ntypedef struct {\n    int x;\n    int y;\n} Point;\n\nint main() {\n    Point p = {3, 4};\n    printf("%d", p.x + p.y);\n    return 0;\n}',"expect":"7","sample":"7","hint":"typedef — короткое имя для типа"}
]}
]

# ============ C# ============
cs_lessons = [
{"title":"Основы","icon":"1","tasks":[
 {"name":"Hello World","code":'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Привет, мир!");\n    }\n}',"expect":"Привет, мир!","sample":"Привет, мир!","hint":"Console.WriteLine — вывод с новой строки"},
 {"name":"Две строки","code":'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Строка 1");\n        Console.WriteLine("Строка 2");\n    }\n}',"expect":"Строка 1\nСтрока 2","sample":"Строка 1\\nСтрока 2","hint":"WriteLine — каждая строка отдельно"}
]},
{"title":"Переменные","icon":"2","tasks":[
 {"name":"var и типы","code":'using System;\n\nclass Program {\n    static void Main() {\n        int age = 10;\n        double pi = 3.14;\n        string name = "Аня";\n        bool ok = true;\n        Console.WriteLine($"{age} {pi} {name} {ok}");\n    }\n}',"expect":"10 3.14 Аня True","sample":"10 3.14 Аня True","hint":"$ — интерполяция строк"},
 {"name":"Ввод Console.ReadLine","code":'using System;\n\nclass Program {\n    static void Main() {\n        string name = Console.ReadLine();\n        Console.WriteLine("Привет, " + name);\n    }\n}',"expect":"","sample":"Привет, Аня (если ввести Аня)","hint":"Console.ReadLine() — чтение строки"}
]},
{"title":"Математика","icon":"+","tasks":[
 {"name":"Арифметика","code":'using System;\n\nclass Program {\n    static void Main() {\n        int a = 10, b = 3;\n        Console.WriteLine(a + b);\n        Console.WriteLine(a - b);\n        Console.WriteLine(a * b);\n        Console.WriteLine(a / b);\n        Console.WriteLine(a % b);\n    }\n}',"expect":"13\n7\n30\n3\n1","sample":"13\\n7\\n30\\n3\\n1","hint":"% — остаток, int / int = int"},
 {"name":"Math класс","code":'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine(Math.Max(5, 9));\n        Console.WriteLine(Math.Abs(-7));\n        Console.WriteLine(Math.Pow(2, 3));\n    }\n}',"expect":"9\n7\n8","sample":"9\\n7\\n8","hint":"Math.Max, Math.Abs, Math.Pow"}
]},
{"title":"Условия","icon":"⚖️","tasks":[
 {"name":"if/else","code":'using System;\n\nclass Program {\n    static void Main() {\n        int age = 12;\n        if (age >= 18) {\n            Console.WriteLine("Взрослый");\n        } else {\n            Console.WriteLine("Ребёнок");\n        }\n    }\n}',"expect":"Ребёнок","sample":"Ребёнок","hint":"if (условие) { } else { }"},
 {"name":"switch","code":'using System;\n\nclass Program {\n    static void Main() {\n        int day = 3;\n        switch (day) {\n            case 1: Console.WriteLine("Пн"); break;\n            case 2: Console.WriteLine("Вт"); break;\n            case 3: Console.WriteLine("Ср"); break;\n            default: Console.WriteLine("Другой"); break;\n        }\n    }\n}',"expect":"Ср","sample":"Ср","hint":"switch (значение) { case N: break; }"}
]},
{"title":"Циклы","icon":"🔄","tasks":[
 {"name":"for","code":'using System;\n\nclass Program {\n    static void Main() {\n        for (int i = 0; i < 5; i++) {\n            Console.WriteLine(i);\n        }\n    }\n}',"expect":"0\n1\n2\n3\n4","sample":"0\\n1\\n2\\n3\\n4","hint":"for (начало; условие; шаг)"},
 {"name":"foreach","code":'using System;\n\nclass Program {\n    static void Main() {\n        string[] fruits = {"яблоко", "банан", "вишня"};\n        foreach (string f in fruits) {\n            Console.WriteLine("Я люблю " + f);\n        }\n    }\n}',"expect":"Я люблю яблоко\nЯ люблю банан\nЯ люблю вишня","sample":"Я люблю яблоко\\nЯ люблю банан\\nЯ люблю вишня","hint":"foreach (тип перем in коллекция)"}
]},
{"title":"Массивы","icon":"📋","tasks":[
 {"name":"Массив","code":'using System;\n\nclass Program {\n    static void Main() {\n        int[] nums = {10, 20, 30};\n        Console.WriteLine(nums[0]);\n        Console.WriteLine(nums.Length);\n    }\n}',"expect":"10\n3","sample":"10\\n3","hint":"nums.Length — длина"},
 {"name":"Сумма","code":'using System;\n\nclass Program {\n    static void Main() {\n        int[] nums = {1, 2, 3, 4, 5};\n        int sum = 0;\n        foreach (int n in nums) {\n            sum += n;\n        }\n        Console.WriteLine(sum);\n    }\n}',"expect":"15","sample":"15","hint":"sum += n"}
]},
{"title":"Методы","icon":"⚙️","tasks":[
 {"name":"Метод","code":'using System;\n\nclass Program {\n    static void Greet() {\n        Console.WriteLine("Привет!");\n    }\n    \n    static void Main() {\n        Greet();\n        Greet();\n    }\n}',"expect":"Привет!\nПривет!","sample":"Привет!\\nПривет!","hint":"static void Имя() — метод"},
 {"name":"Метод с return","code":'using System;\n\nclass Program {\n    static int Square(int x) {\n        return x * x;\n    }\n    \n    static void Main() {\n        Console.WriteLine(Square(7));\n    }\n}',"expect":"49","sample":"49","hint":"static int Имя(int x) { return ...; }"}
]},
{"title":"Классы и ООП","icon":"🏛️","tasks":[
 {"name":"Класс","code":'using System;\n\nclass Cat {\n    public string Name;\n    public void Meow() {\n        Console.WriteLine(Name + ": Мяу!");\n    }\n}\n\nclass Program {\n    static void Main() {\n        Cat cat = new Cat();\n        cat.Name = "Барсик";\n        cat.Meow();\n    }\n}',"expect":"Барсик: Мяу!","sample":"Барсик: Мяу!","hint":"class Имя { } + new"},
 {"name":"Конструктор","code":'using System;\n\nclass Dog {\n    public string Name;\n    public Dog(string n) {\n        Name = n;\n    }\n    public void Bark() {\n        Console.WriteLine(Name + ": Гав!");\n    }\n}\n\nclass Program {\n    static void Main() {\n        Dog d = new Dog("Рекс");\n        d.Bark();\n    }\n}',"expect":"Рекс: Гав!","sample":"Рекс: Гав!","hint":"Конструктор — метод с именем класса"}
]},
{"title":"LINQ и async","icon":"📦","tasks":[
 {"name":"LINQ Where","code":'using System;\nusing System.Linq;\nusing System.Collections.Generic;\n\nclass Program {\n    static void Main() {\n        int[] nums = {1, 2, 3, 4, 5, 6};\n        var even = nums.Where(n => n % 2 == 0);\n        foreach (var n in even) {\n            Console.WriteLine(n);\n        }\n    }\n}',"expect":"2\n4\n6","sample":"2\\n4\\n6","hint":"Where(условие) — фильтр. => — лямбда"},
 {"name":"async/await","code":'using System;\nusing System.Threading.Tasks;\n\nclass Program {\n    static async Task Main() {\n        await Task.Delay(100);\n        Console.WriteLine("Готово");\n    }\n}',"expect":"Готово","sample":"Готово","hint":"async — асинхронный метод, await — ожидание"}
]}
]

# ============ HTML ============
html_lessons = [
{"title":"Структура документа","icon":"1","tasks":[
 {"name":"Базовая страница","code":"<!DOCTYPE html>\n<html>\n<head>\n    <title>Моя страница</title>\n</head>\n<body>\n    <p>Привет, мир!</p>\n</body>\n</html>","expect":"Привет, мир!","sample":"Привет, мир!","hint":"<p> — абзац. Открой в браузере"},
 {"name":"Комментарии","code":"<!-- Это комментарий -->\n<p>Видимый текст</p>","expect":"Видимый текст","sample":"Видимый текст","hint":"<!-- ... --> — комментарий"}
]},
{"title":"Теги","icon":"2","tasks":[
 {"name":"Заголовки","code":"<h1>Большой</h1>\n<h2>Средний</h2>\n<h3>Маленький</h3>","expect":"Большой\nСредний\nМаленький","sample":"Большой/Средний/Маленький","hint":"h1..h6 — заголовки"},
 {"name":"Форматирование","code":"<p><b>Жирный</b> и <i>курсив</i></p>\n<p><u>Подчёркнутый</u></p>","expect":"Жирный и курсив\nПодчёркнутый","sample":"Жирный и курсив / Подчёркнутый","hint":"<b>, <i>, <u> — формат"}
]},
{"title":"Ссылки и картинки","icon":"🔗","tasks":[
 {"name":"Ссылка","code":"<a href=\"https://python.org\">Сайт Python</a>","expect":"Сайт Python","sample":"Сайт Python (кликабельная ссылка)","hint":"<a href=\"URL\">текст</a>"},
 {"name":"Картинка","code":"<img src=\"https://www.python.org/static/img/python-logo.png\" alt=\"Логотип Python\" width=\"200\">","expect":"Логотип Python","sample":"Картинка с логотипом","hint":"<img src=\"URL\" alt=\"описание\">"}
]},
{"title":"Списки","icon":"📃","tasks":[
 {"name":"Маркированный","code":"<ul>\n    <li>Яблоко</li>\n    <li>Банан</li>\n    <li>Вишня</li>\n</ul>","expect":"• Яблоко\n• Банан\n• Вишня","sample":"Список с точками","hint":"<ul> + <li> — маркированный"},
 {"name":"Нумерованный","code":"<ol>\n    <li>Первый</li>\n    <li>Второй</li>\n</ol>","expect":"1. Первый\n2. Второй","sample":"Нумерованный список","hint":"<ol> — нумерованный"}
]},
{"title":"Таблицы","icon":"📊","tasks":[
 {"name":"Таблица","code":"<table border=\"1\">\n    <tr><th>Имя</th><th>Возраст</th></tr>\n    <tr><td>Аня</td><td>10</td></tr>\n</table>","expect":"Имя | Возраст\nАня | 10","sample":"Таблица 2x2","hint":"<table> <tr> — строка, <td> — ячейка, <th> — заголовок"}
]},
{"title":"Формы","icon":"📝","tasks":[
 {"name":"Форма входа","code":"<form>\n    <label>Email:</label>\n    <input type=\"email\" placeholder=\"email@example.com\">\n    <button type=\"submit\">Войти</button>\n</form>","expect":"Email: [поле] [Войти]","sample":"Форма с полем и кнопкой","hint":"<input type=\"email\">, <button>"}
]},
{"title":"Семантика","icon":"🏗️","tasks":[
 {"name":"Семантическая структура","code":"<header>Шапка</header>\n<nav>Меню</nav>\n<main>Контент</main>\n<footer>Подвал</footer>","expect":"Шапка\nМеню\nКонтент\nПодвал","sample":"Структура страницы","hint":"header, nav, main, footer — семантические теги"}
]},
{"title":"Медиа","icon":"🎬","tasks":[
 {"name":"Видео","code":"<video controls width=\"320\">\n    <source src=\"movie.mp4\" type=\"video/mp4\">\n</video>","expect":"Видеоплеер","sample":"Встраиваемый видеоплеер","hint":"<video controls> + <source>"}
]}
]

# ============ CSS ============
css_lessons = [
{"title":"Селекторы","icon":"1","tasks":[
 {"name":"Базовые селекторы","code":"p {\n    color: red;\n}\n\n.class-name {\n    font-size: 20px;\n}\n\n#unique {\n    font-weight: bold;\n}","expect":"p — красный, .class — крупнее, #id — жирный","sample":"Примеры селекторов","hint":"тег, .класс, #ид"},
 {"name":"Вложенные","code":"div p {\n    color: blue;\n}\n\ndiv > p {\n    color: green;\n}","expect":"Вложенные p — синие, прямые дети — зелёные","sample":"Комбинированные селекторы","hint":"пробел — потомок, > — прямой ребёнок"}
]},
{"title":"Цвета и шрифты","icon":"🎨","tasks":[
 {"name":"Цвета","code":"h1 {\n    color: #ff0000;\n    background-color: rgb(0, 0, 255);\n}","expect":"Красный текст на синем фоне","sample":"Цвет текста и фона","hint":"hex (#ff0000), rgb(0,0,255)"},
 {"name":"Шрифты","code":"body {\n    font-family: Arial, sans-serif;\n    font-size: 16px;\n    font-weight: 400;\n    line-height: 1.5;\n}","expect":"Шрифт Arial, 16px, обычный","sample":"Настройки шрифта","hint":"font-family, font-size, font-weight, line-height"}
]},
{"title":"Боксовая модель","icon":"📦","tasks":[
 {"name":"margin и padding","code":".box {\n    width: 200px;\n    padding: 20px;    /* внутри */\n    margin: 10px;     /* снаружи */\n    border: 2px solid black;\n}","expect":"Отступы, рамка, размер","sample":"Коробка","hint":"padding — внутри, margin — снаружи"},
 {"name":"border-radius","code":".btn {\n    background: #3182ce;\n    color: white;\n    padding: 10px 20px;\n    border-radius: 8px;\n    border: none;\n}","expect":"Скруглённая кнопка","sample":"Кнопка с углами","hint":"border-radius — скругление"}
]},
{"title":"Flexbox","icon":"➡️","tasks":[
 {"name":"Основы flex","code":".container {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    gap: 10px;\n}","expect":"Элементы по центру с промежутком","sample":"Flex-контейнер","hint":"display:flex, justify-content, align-items, gap"},
 {"name":"Направление","code":".row {\n    display: flex;\n    flex-direction: row;\n}\n\n.column {\n    display: flex;\n    flex-direction: column;\n}","expect":"Ряд / колонка","sample":"Направление flex","hint":"flex-direction: row / column"}
]},
{"title":"Grid","icon":"🔲","tasks":[
 {"name":"Сетка","code":".grid {\n    display: grid;\n    grid-template-columns: 1fr 1fr 1fr;\n    gap: 15px;\n}","expect":"3 колонки с промежутками","sample":"CSS Grid","hint":"grid-template-columns: 1fr 1fr 1fr"},
 {"name":"Области","code":".layout {\n    display: grid;\n    grid-template-areas:\n        \"header header\"\n        \"sidebar content\";\n}","expect":"Шапка сверху, ниже сайдбар и контент","sample":"Макет страницы","hint":"grid-template-areas — раскладка"}
]},
{"title":"Анимация","icon":"✨","tasks":[
 {"name":"Transition","code":".btn {\n    transition: all 0.3s ease;\n}\n\n.btn:hover {\n    background: #2b6cb0;\n    transform: scale(1.05);\n}","expect":"Плавное изменение при наведении","sample":"Анимация наведения","hint":"transition + :hover"},
 {"name":"Keyframes","code":"@keyframes pulse {\n    0% { opacity: 1; }\n    50% { opacity: 0.5; }\n    100% { opacity: 1; }\n}\n\n.element {\n    animation: pulse 2s infinite;\n}","expect":"Мерцание элемента","sample":"Кадровая анимация","hint":"@keyframes + animation"}
]},
{"title":"Адаптивность","icon":"📱","tasks":[
 {"name":"Media queries","code":".container {\n    display: flex;\n}\n\n@media (max-width: 768px) {\n    .container {\n        flex-direction: column;\n    }\n}","expect":"На телефоне — колонкой","sample":"Адаптивная вёрстка","hint":"@media (max-width: 768px) { }"},
 {"name":"Единицы","code":".text {\n    font-size: 2rem;      /* в 2 раза больше корневого */\n    width: 50vw;          /* половина ширины экрана */\n    height: 100vh;        /* вся высота экрана */\n}","expect":"Адаптивные размеры","sample":"rem, vw, vh","hint":"rem, vw, vh — относительные единицы"}
]},
{"title":"Позиционирование","icon":"📍","tasks":[
 {"name":"position","code":".fixed {\n    position: fixed;\n    top: 0;\n    left: 0;\n}\n\n.absolute {\n    position: absolute;\n    right: 10px;\n    bottom: 10px;\n}","expect":"Фиксированный и абсолютный","sample":"Способы позиционирования","hint":"fixed — привязан к экрану, absolute — к родителю"}
]}
]

# ============ JS ============
js_lessons = [
{"title":"Основы","icon":"1","tasks":[
 {"name":"console.log","code":"console.log(\"Привет, мир!\");","expect":"Привет, мир!","sample":"Привет, мир!","hint":"console.log — вывод в консоль"},
 {"name":"Комментарии","code":"// Это комментарий\n/* Тоже\n   комментарий */\nconsole.log(42);","expect":"42","sample":"42","hint":"// и /* */ — комментарии"}
]},
{"title":"Переменные","icon":"2","tasks":[
 {"name":"let и const","code":"let age = 10;\nconst name = \"Аня\";\nage = 11;\nconsole.log(age, name);","expect":"11 Аня","sample":"11 Аня","hint":"let — можно менять, const — нельзя"},
 {"name":"Типы","code":"console.log(typeof \"текст\");\nconsole.log(typeof 42);\nconsole.log(typeof true);\nconsole.log(typeof [1,2]);","expect":"string\nnumber\nboolean\nobject","sample":"string/number/boolean/object","hint":"typeof — тип значения"}
]},
{"title":"Функции","icon":"⚙️","tasks":[
 {"name":"Функция","code":"function greet(name) {\n    return \"Привет, \" + name + \"!\";\n}\nconsole.log(greet(\"Макс\"));","expect":"Привет, Макс!","sample":"Привет, Макс!","hint":"function имя(параметр) { }"},
 {"name":"Стрелочная","code":"const double = (x) => x * 2;\nconsole.log(double(5));","expect":"10","sample":"10","hint":"const f = (x) => x * 2 — стрелочная функция"}
]},
{"title":"Условия","icon":"⚖️","tasks":[
 {"name":"if/else","code":"let age = 12;\nif (age >= 18) {\n    console.log(\"Взрослый\");\n} else {\n    console.log(\"Ребёнок\");\n}","expect":"Ребёнок","sample":"Ребёнок","hint":"if (условие) { } else { }"},
 {"name":"Тернарный","code":"let x = 5;\nlet result = x > 0 ? \"Плюс\" : \"Минус\";\nconsole.log(result);","expect":"Плюс","sample":"Плюс","hint":"условие ? да : нет"}
]},
{"title":"Циклы","icon":"🔄","tasks":[
 {"name":"for","code":"for (let i = 0; i < 5; i++) {\n    console.log(i);\n}","expect":"0\n1\n2\n3\n4","sample":"0\\n1\\n2\\n3\\n4","hint":"for (начало; условие; шаг)"},
 {"name":"for...of","code":"let fruits = [\"яблоко\", \"банан\"];\nfor (let f of fruits) {\n    console.log(\"Я люблю \" + f);\n}","expect":"Я люблю яблоко\nЯ люблю банан","sample":"Я люблю яблоко\\nЯ люблю банан","hint":"for (let x of массив)"}
]},
{"title":"Массивы","icon":"📋","tasks":[
 {"name":"Методы","code":"let nums = [1, 2, 3];\nnums.push(4);\nconsole.log(nums.length);\nconsole.log(nums.includes(2));","expect":"4\ntrue","sample":"4\\ntrue","hint":"push, length, includes"},
 {"name":"map и filter","code":"let nums = [1, 2, 3, 4];\nlet doubled = nums.map(n => n * 2);\nlet even = nums.filter(n => n % 2 === 0);\nconsole.log(doubled);\nconsole.log(even);","expect":"[2, 4, 6, 8]\n[2, 4]","sample":"[2, 4, 6, 8] [2, 4]","hint":"map — преобразует, filter — фильтрует"}
]},
{"title":"Объекты","icon":"📖","tasks":[
 {"name":"Объект","code":"let person = {\n    name: \"Дима\",\n    age: 10\n};\nconsole.log(person.name);\nconsole.log(person[\"age\"]);","expect":"Дима\n10","sample":"Дима\\n10","hint":"obj.ключ или obj[\"ключ\"]"},
 {"name":"Деструктуризация","code":"let {name, age} = {name: \"Аня\", age: 9};\nconsole.log(name, age);","expect":"Аня 9","sample":"Аня 9","hint":"let {ключ} = объект"}
]},
{"title":"DOM","icon":"🖥️","tasks":[
 {"name":"Выбор элементов","code":"// В браузере:\ndocument.querySelector(\"#app\").textContent = \"Привет\";\ndocument.querySelectorAll(\".item\").length;","expect":"Элемент #app = Привет","sample":"Работа с DOM","hint":"querySelector, querySelectorAll"},
 {"name":"Создание элемента","code":"let div = document.createElement(\"div\");\ndiv.textContent = \"Новый\";\ndocument.body.appendChild(div);","expect":"div добавлен в body","sample":"Создание и вставка","hint":"createElement + appendChild"}
]},
{"title":"События","icon":"🔔","tasks":[
 {"name":"addEventListener","code":"let btn = document.querySelector(\"button\");\nbtn.addEventListener(\"click\", () => {\n    console.log(\"Клик!\");\n});","expect":"Клик! по нажатию","sample":"Обработчик клика","hint":"addEventListener(\"click\", функция)"}
]},
{"title":"Fetch и async","icon":"🌐","tasks":[
 {"name":"fetch","code":"fetch(\"https://api.example.com/data\")\n    .then(r => r.json())\n    .then(data => console.log(data));","expect":"Данные с сервера","sample":"Запрос к API","hint":"fetch + .then + .json()"},
 {"name":"async/await","code":"async function load() {\n    let res = await fetch(\"https://api.example.com/data\");\n    let data = await res.json();\n    console.log(data);\n}\nload();","expect":"Данные с сервера","sample":"Асинхронная загрузка","hint":"async function + await"}
]},
{"title":"Продвинутое","icon":"🚀","tasks":[
 {"name":"Классы","code":"class Cat {\n    constructor(name) {\n        this.name = name;\n    }\n    meow() {\n        return this.name + \": Мяу!\";\n    }\n}\nlet cat = new Cat(\"Барсик\");\nconsole.log(cat.meow());","expect":"Барсик: Мяу!","sample":"Барсик: Мяу!","hint":"class + constructor + new"},
 {"name":"Spread","code":"let a = [1, 2];\nlet b = [3, 4];\nlet c = [...a, ...b];\nconsole.log(c);","expect":"[1, 2, 3, 4]","sample":"[1, 2, 3, 4]","hint":"... — распаковка массива"}
]}
]

langs = [
    ("c",      "C",      "🔧", c_lessons),
    ("csharp", "C#",     "💎", cs_lessons),
    ("html",   "HTML",   "🌐", html_lessons),
    ("css",    "CSS",    "🎨", css_lessons),
    ("js",     "JavaScript", "🚀", js_lessons),
]

for pfx, lang, logo, lessons in langs:
    folder = os.path.join(BASE, pfx)
    os.makedirs(folder, exist_ok=True)
    html = TEMPLATE.replace('__PFX__', pfx).replace('__LANG__', lang).replace('__LOGO__', logo)
    lessons_json = json.dumps(lessons, ensure_ascii=False)
    html = html.replace('__LESSONS__', lessons_json)
    with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"OK {pfx} ({len(lessons)} lessons, {sum(len(l['tasks']) for l in lessons)} tasks)")