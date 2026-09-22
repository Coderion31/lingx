# -*- coding: utf-8 -*-
import os, json

BASE = r"C:\Users\bunse\OneDrive\Документы\MultiTool\HomeChats\Chat-7"

SUBJECTS = {
    'algebra': ('Алгебра', [
        'Числа и выражения', 'Уравнения', 'Функции', 'Степени и корни', 'Логарифмы'
    ]),
    'stats': ('Вероятность и статистика', [
        'Случайные события', 'Комбинаторика', 'Статистические характеристики',
        'Математическое ожидание', 'Законы распределения'
    ]),
    'geometry': ('Геометрия', [
        'Основы геометрии', 'Треугольники', 'Окружность', 'Векторы', 'Стереометрия'
    ]),
    'russian': ('Русский язык', [
        'Фонетика и орфография', 'Морфология', 'Синтаксис', 'Пунктуация', 'Лексика'
    ]),
    'lit': ('Литература', [
        'Древнерусская литература', 'XVIII век', 'XIX век', 'XX век', 'Теория литературы'
    ]),
    'physics': ('Физика', [
        'Механика', 'Молекулярная физика', 'Электричество', 'Оптика', 'Квантовая физика'
    ]),
    'bio': ('Биология', [
        'Клетка', 'Генетика', 'Эволюция', 'Экология', 'Организм человека'
    ]),
    'geo': ('География', [
        'Земля и карты', 'Литосфера', 'Гидросфера', 'Атмосфера', 'Население мира'
    ]),
    'history': ('История', [
        'Древний мир', 'Средние века', 'Новое время', 'XX век', 'История России'
    ]),
    'english': ('Английский язык', [
        'Грамматика', 'Времена', 'Словарный запас', 'Чтение', 'Письмо'
    ])
}

with open(os.path.join(BASE, 'algebra', 'index.html'), 'r', encoding='utf-8') as f:
    template = f.read()

for code, (title, topics) in SUBJECTS.items():
    fp = os.path.join(BASE, code, 'index.html')
    os.makedirs(os.path.join(BASE, code), exist_ok=True)
    page = template.replace('Алгебра', title)
    page = page.replace('algebra', code)
    topics_html = ''.join(f'<div class="topic"><b>{t}</b><span>скоро</span></div>\n' for t in topics)
    page = page.replace(
        '<div class="topic"><b>Числа и выражения</b><span>натуральные, целые, рациональные</span></div>\n'
        '<div class="topic"><b>Уравнения</b><span>линейные, квадратные, с модулем</span></div>\n'
        '<div class="topic"><b>Функции</b><span>графики, область определения</span></div>\n'
        '<div class="topic"><b>Степени и корни</b><span>свойства, преобразования</span></div>\n'
        '<div class="topic"><b>Логарифмы</b><span>базовые свойства и уравнения</span></div>',
        topics_html.strip()
    )
    # Update menu in each subject page
    page = page.replace(
        '<a href="../">Главная</a>\n<a href="../python/">Python</a>\n<a href="algebra/">Алгебра</a>\n<a href="stats/">Вер и стат</a>\n<a href="geometry/">Геометрия</a>',
        '<a href="../">Главная</a>\n<a href="../algebra/">Алгебра</a>\n<a href="../russian/">Русский язык</a>\n<a href="../physics/">Физика</a>\n<a href="../bio/">Биология</a>\n<a href="../history/">История</a>\n<a href="../english/">Английский язык</a>'
    )
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"{code}: {title}")

print("DONE")