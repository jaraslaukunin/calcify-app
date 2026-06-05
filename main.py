from kivy.config import Config

Config.set('graphics', 'width', '420')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.properties import BooleanProperty
from kivy.core.text import LabelBase
import math
import re
from fractions import Fraction

try:
    LabelBase.register(name='JetBrainsMono',
                       fn_regular='JetBrainsMono-Regular.ttf',
                       fn_bold='JetBrainsMono-Bold.ttf')
    FONT_NAME = 'JetBrainsMono'
except:
    FONT_NAME = 'Roboto'

Window.clearcolor = get_color_from_hex('#F0F2F5')


class RoundedButton(Button):
    is_operator = BooleanProperty(False)
    is_equal = BooleanProperty(False)
    is_function = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.is_operator = kwargs.pop('is_operator', False)
        self.is_equal = kwargs.pop('is_equal', False)
        self.is_function = kwargs.pop('is_function', False)

        super().__init__(**kwargs)

        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.font_size = '18sp'
        self.bold = True
        self.font_name = FONT_NAME

        if self.is_equal:
            bg_color = get_color_from_hex('#3B82F6')
            self.color = get_color_from_hex('#FFFFFF')
        elif self.is_function:
            bg_color = get_color_from_hex('#EFF6FF')
            self.color = get_color_from_hex('#3B82F6')
        elif self.is_operator:
            bg_color = get_color_from_hex('#E5E7EB')
            self.color = get_color_from_hex('#374151')
        else:
            bg_color = get_color_from_hex('#FFFFFF')
            self.color = get_color_from_hex('#1F2937')

        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[12])

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class CalculatorApp(App):
    def build(self):
        self.title = 'Calcify Pro'
        self.expression = ''
        self.result_shown = False
        self.error_state = False
        self.mode = 'auto'

        self.root = BoxLayout(orientation='vertical', padding=12, spacing=8)

        # Дисплей (уменьшенный)
        display = BoxLayout(orientation='vertical', size_hint_y=0.28, spacing=2)

        with display.canvas.before:
            Color(*get_color_from_hex('#FFFFFF'))
            self.disp_bg = RoundedRectangle(size=display.size, pos=display.pos, radius=[16])
            display.bind(size=self._update_bg, pos=self._update_bg)

        # Индикатор режима
        self.mode_label = Label(
            text='AUTO',
            font_size='10sp',
            halign='left',
            valign='middle',
            color=get_color_from_hex('#9CA3AF'),
            padding=[20, 5],
            size_hint_y=0.12,
            markup=True,
            font_name=FONT_NAME
        )
        self.mode_label.bind(size=self.mode_label.setter('text_size'))

        # Поле выражения
        self.expr_label = Label(
            text='',
            font_size='15sp',
            halign='right',
            valign='bottom',
            color=get_color_from_hex('#6B7280'),
            padding=[20, 10],
            size_hint_y=0.45,
            markup=True,
            font_name=FONT_NAME
        )
        self.expr_label.bind(size=self.expr_label.setter('text_size'))

        # Поле результата
        self.result_label = Label(
            text='',
            font_size='26sp',
            halign='right',
            valign='middle',
            color=get_color_from_hex('#1F2937'),
            bold=True,
            padding=[20, 5],
            size_hint_y=0.43,
            markup=True,
            font_name=FONT_NAME
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))

        display.add_widget(self.mode_label)
        display.add_widget(self.expr_label)
        display.add_widget(self.result_label)
        self.root.add_widget(display)

        # Кнопки (увеличенная область)
        btn_layout = GridLayout(cols=5, spacing=5, size_hint_y=0.72)

        buttons = [
            ['RAD', 'DEG', 'sin', 'cos', 'tg'],
            ['arcsin', 'arccos', 'arctg', 'log₁₀', 'ln'],
            ['C', '(', ')', '%', '÷'],
            ['7', '8', '9', 'DEL', '×'],
            ['4', '5', '6', '±', '−'],
            ['1', '2', '3', '.', '+'],
            ['0', ',', 'π', 'e', 'ANS'],
            ['=', 'F ↔ D', '√', '^', 'log']
        ]

        self.last_result = None

        for row in buttons:
            for btn_text in row:
                is_operator = btn_text in ['÷', '×', '−', '+', '%', '±', '^', '√', 'F ↔ D', 'log', ',']
                is_equal = btn_text == '='
                is_function = btn_text in ['sin', 'cos', 'tg', 'arcsin', 'arccos', 'arctg', 'log₁₀', 'ln']
                is_mode = btn_text in ['RAD', 'DEG']

                btn = RoundedButton(
                    text=btn_text,
                    is_operator=is_operator or is_mode,
                    is_equal=is_equal,
                    is_function=is_function,
                    font_size='11sp' if is_function or is_mode or len(btn_text) > 2 else '17sp'
                )

                btn.bind(on_press=self.on_button)
                btn_layout.add_widget(btn)

        self.root.add_widget(btn_layout)
        self.update_mode_display()
        return self.root

    def _update_bg(self, instance, value):
        self.disp_bg.pos = instance.pos
        self.disp_bg.size = instance.size

    def update_mode_display(self):
        modes = {'auto': '[color=#9CA3AF]AUTO[/color]',
                 'rad': '[color=#8B5CF6]RAD[/color]',
                 'deg': '[color=#3B82F6]DEG[/color]'}
        self.mode_label.text = modes[self.mode]

    def detect_mode(self, expr):
        if self.mode != 'auto':
            return self.mode
        if 'π' in expr or 'pi' in expr.lower():
            return 'rad'
        return 'deg'

    def can_add_zero(self):
        """Проверяет, можно ли добавить ноль"""
        if not self.expression:
            return True

        # Нельзя добавить 0 после 0, если это начало числа
        if self.expression.endswith('0'):
            # Проверяем, является ли 0 единственным или после оператора
            if len(self.expression) == 1:
                return False
            if self.expression[-2] in '(),+-×÷−^':
                return False

        return True

    def has_point_in_last_number(self):
        match = re.search(r'(\d+\.?\d*)$', self.expression)
        if match:
            return '.' in match.group(1)
        return False

    def can_add_point(self):
        if not self.expression:
            return True

        if self.expression.endswith('.'):
            return False

        if self.has_point_in_last_number():
            return False

        if self.expression[-1] in '(),+-×÷−^%':
            return True

        return True

    def format_fraction_beautiful(self, num, den):
        if den == 1:
            return str(num)

        sign = ''
        if num < 0:
            sign = '-'
            num = abs(num)

        whole = num // den
        remainder = num % den

        if whole > 0 and remainder > 0:
            return f"{sign}{whole}[sup]{remainder}[/sup]⁄[sub]{den}[/sub]"
        elif whole > 0:
            return f"{sign}{whole}"
        else:
            return f"{sign}[sup]{remainder}[/sup]⁄[sub]{den}[/sub]"

    def format_pi_fraction(self, coefficient):
        if coefficient == 0:
            return "0"

        sign = ''
        if coefficient < 0:
            sign = '-'
            coefficient = abs(coefficient)

        frac = Fraction(coefficient).limit_denominator(100)

        if frac.denominator == 1:
            if frac.numerator == 1:
                return f"{sign}π"
            else:
                return f"{sign}{frac.numerator}π"
        else:
            if frac.numerator == 1:
                return f"{sign}π⁄[sub]{frac.denominator}[/sub]"
            else:
                return f"{sign}[sup]{frac.numerator}[/sup]⁄[sub]{frac.denominator}[/sub]π"

    def format_result(self, result):
        if isinstance(result, complex):
            return None

        if math.isnan(result) or math.isinf(result):
            return None

        if abs(result) < 1e-12:
            return "0"

        if abs(result) > 1e12:
            return f"{result:.6e}"

        pi_fraction = result / math.pi
        if abs(pi_fraction - round(pi_fraction, 6)) < 1e-10 and pi_fraction != 0:
            rounded = round(pi_fraction, 6)
            if abs(rounded - int(rounded)) < 1e-10:
                return self.format_pi_fraction(int(rounded))
            else:
                frac = Fraction(rounded).limit_denominator(100)
                return self.format_pi_fraction(frac.numerator / frac.denominator)

        frac = Fraction(result).limit_denominator(1000)
        if abs(float(frac) - result) < 1e-10:
            return self.format_fraction_beautiful(frac.numerator, frac.denominator)

        if result == int(result):
            return str(int(result))

        formatted = f"{result:.10f}".rstrip('0').rstrip('.')
        return formatted

    def format_expression_beautiful(self, expr):
        expr = expr.replace('*', '×')
        expr = expr.replace('/', '÷')
        expr = expr.replace('-', '−')
        expr = expr.replace('π', 'π')
        return expr

    def on_button(self, instance):
        text = instance.text

        if text == 'C':
            self.expression = ''
            self.expr_label.text = ''
            self.result_label.text = ''
            self.result_shown = False
            self.error_state = False

        elif text == 'DEL':
            if self.result_shown or self.error_state:
                self.expression = ''
                self.expr_label.text = ''
                self.result_label.text = ''
                self.result_shown = False
                self.error_state = False
            elif self.expression:
                funcs = ['sin(', 'cos(', 'tg(', 'arcsin(', 'arccos(', 'arctg(', 'log(', 'ln(', 'sqrt(', 'abs(']
                removed = False
                for func in funcs:
                    if self.expression.endswith(func):
                        self.expression = self.expression[:-len(func)]
                        removed = True
                        break
                if not removed:
                    self.expression = self.expression[:-1]
                self.expr_label.text = self.format_expression_beautiful(self.expression)

        elif text == '=':
            self.calculate()

        elif text == 'ANS':
            if self.last_result is not None:
                if self.result_shown or self.error_state:
                    self.expression = str(self.last_result)
                else:
                    self.expression += str(self.last_result)
                self.expr_label.text = self.format_expression_beautiful(self.expression)
                self.result_shown = False
                self.error_state = False

        elif text == '±':
            self.toggle_sign()

        elif text == 'RAD':
            self.mode = 'rad'
            self.update_mode_display()

        elif text == 'DEG':
            self.mode = 'deg'
            self.update_mode_display()

        elif text == 'F ↔ D':
            self.toggle_fraction_decimal()

        elif text == '1/x':
            self.reciprocal()

        elif text == 'log₁₀':
            if self.result_shown and self.last_result is not None:
                self.expression = 'log(' + str(self.last_result)
                self.result_shown = False
            else:
                self.expression += 'log('
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_label.text = ''
            self.error_state = False

        elif text == 'ln':
            if self.result_shown and self.last_result is not None:
                self.expression = 'ln(' + str(self.last_result)
                self.result_shown = False
            else:
                self.expression += 'ln('
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_label.text = ''
            self.error_state = False

        elif text == 'log':
            if self.result_shown and self.last_result is not None:
                self.expression = str(self.last_result) + 'log('
                self.result_shown = False
            else:
                self.expression += 'log('
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_label.text = '[i][color=#9CA3AF]основание, аргумент[/color][/i]'
            self.error_state = False

        elif text == ',':
            # Запятая ТОЛЬКО после цифр или закрывающей скобки
            if self.result_shown or self.error_state:
                pass
            elif self.expression and self.expression[-1] in '0123456789)':
                self.expression += ','
                self.expr_label.text = self.format_expression_beautiful(self.expression)
                self.result_label.text = ''

        elif text == '.':
            if self.can_add_point():
                if self.result_shown or self.error_state:
                    self.expression = '0.'
                    self.result_shown = False
                    self.error_state = False
                elif not self.expression or self.expression[-1] in '(),+-×÷−^%':
                    self.expression += '0.'
                else:
                    self.expression += '.'
                self.expr_label.text = self.format_expression_beautiful(self.expression)
                self.result_label.text = ''

        # ВСЕ ОПЕРАТОРЫ И СКОБКИ С ПРОВЕРКОЙ
        elif text in ['+', '−', '×', '÷', '^', '%']:
            if self.result_shown and self.last_result is not None:
                self.expression = str(self.last_result) + text
                self.result_shown = False
                self.error_state = False
            elif not self.expression:
                # Нельзя начать с оператора (кроме минуса)
                if text == '−':
                    self.expression = '-'
            else:
                last_type, last_char = self.get_last_char_info()

                # Нельзя ставить оператор после оператора
                if last_type == 'operator':
                    # Заменяем последний оператор на новый (кроме случая с минусом)
                    if text == '−' and last_char == '−':
                        pass  # Не даём два минуса подряд
                    else:
                        self.expression = self.expression[:-1] + text
                elif last_type == 'open_bracket' and text != '−':
                    pass  # После ( можно только минус
                elif last_type == 'comma':
                    pass  # После запятой нельзя оператор
                elif last_type == 'dot':
                    pass  # После точки нельзя оператор
                else:
                    self.expression += text

            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_label.text = ''

        elif text == '(':
            if self.result_shown or self.error_state:
                self.expression = '('
                self.result_shown = False
                self.error_state = False
            elif not self.expression:
                self.expression = '('
            else:
                last_type, last_char = self.get_last_char_info()
                # Открывающую скобку можно после оператора или другой скобки
                if last_type in ['operator', 'open_bracket', 'empty']:
                    self.expression += '('
                elif last_type == 'digit' or last_type == 'close_bracket':
                    # Автоматически добавляем умножение перед скобкой
                    self.expression += '×('
                else:
                    self.expression += '('
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_label.text = ''

        elif text == ')':
            if self.expression:
                last_type, last_char = self.get_last_char_info()
                # Закрывающую скобку можно после цифр, другой скобки или точки
                if last_type in ['digit', 'close_bracket']:
                    # Проверяем, есть ли открывающие скобки
                    if self.expression.count('(') > self.expression.count(')'):
                        self.expression += ')'
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_label.text = ''

        elif text in ['sin', 'cos', 'tg', 'arcsin', 'arccos', 'arctg', '√', 'sqrt']:
            if self.result_shown and self.last_result is not None:
                self.expression = str(self.last_result)
                self.result_shown = False
            func_map = {'√': 'sqrt(', 'sqrt': 'sqrt('}
            func_name = func_map.get(text, text + '(')

            if not self.expression:
                self.expression = func_name
            else:
                last_type, last_char = self.get_last_char_info()
                if last_type in ['digit', 'close_bracket']:
                    # Автоматически добавляем умножение
                    self.expression += '×' + func_name
                else:
                    self.expression += func_name

            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_label.text = ''
            self.error_state = False

        else:
            # Обработка цифр (0-9) и констант
            if text in '123456789':
                if self.result_shown or self.error_state:
                    self.expression = text
                    self.result_shown = False
                    self.error_state = False
                else:
                    if self.expression == '0':
                        self.expression = text
                    elif len(self.expression) >= 2 and self.expression[-1] == '0' and self.expression[
                        -2] in '(),+-×÷−^':
                        self.expression = self.expression[:-1] + text
                    else:
                        self.expression += text
                self.expr_label.text = self.format_expression_beautiful(self.expression)
                self.result_label.text = ''

            elif text == '0':
                if self.result_shown or self.error_state:
                    self.expression = '0'
                    self.result_shown = False
                    self.error_state = False
                else:
                    if not self.expression:
                        self.expression = '0'
                    elif self.expression[-1] in '(),+-×÷−^':
                        self.expression += '0'
                    elif self.expression[-1] in '0123456789':
                        match = re.search(r'(\d+\.?\d*)$', self.expression)
                        if match:
                            last_number = match.group(1)
                            if last_number == '0':
                                pass  # Блокируем 00
                            else:
                                self.expression += '0'
                        else:
                            self.expression += '0'
                    elif self.expression[-1] == '.':
                        self.expression += '0'
                    else:
                        self.expression += '0'
                self.expr_label.text = self.format_expression_beautiful(self.expression)
                self.result_label.text = ''

            elif text in ['π', 'e']:
                if self.result_shown or self.error_state:
                    self.expression = text
                    self.result_shown = False
                    self.error_state = False
                else:
                    last_type, last_char = self.get_last_char_info()
                    if last_type in ['digit', 'close_bracket']:
                        # Автоматически добавляем умножение
                        self.expression += '×' + text
                    else:
                        self.expression += text
                self.expr_label.text = self.format_expression_beautiful(self.expression)
                self.result_label.text = ''

    def toggle_sign(self):
        if not self.expression or self.expression == '0':
            return

        match = re.search(r'(-?\d+\.?\d*)$', self.expression)
        if match:
            num = match.group(1)
            if num.startswith('-'):
                new_num = num[1:]
            else:
                new_num = '-' + num
            self.expression = self.expression[:match.start()] + new_num
        elif self.expression.endswith('('):
            self.expression += '-'
        else:
            self.expression += '(-'

        self.expr_label.text = self.format_expression_beautiful(self.expression)

    def get_last_char_info(self):
        """Возвращает информацию о последнем символе"""
        if not self.expression:
            return 'empty', None
        last = self.expression[-1]
        if last in '+-×÷−^%':
            return 'operator', last
        elif last == '(':
            return 'open_bracket', last
        elif last == ',':
            return 'comma', last
        elif last == '.':
            return 'dot', last
        elif last in '0123456789':
            return 'digit', last
        elif last == ')':
            return 'close_bracket', last
        else:
            return 'other', last

    def toggle_fraction_decimal(self):
        if self.last_result is not None:
            frac = Fraction(self.last_result).limit_denominator(1000)
            if abs(float(frac) - self.last_result) < 1e-10:
                current_display = self.result_label.text.replace('= ', '')
                if '⁄' in current_display or '/' in current_display:
                    decimal = f"{self.last_result:.10f}".rstrip('0').rstrip('.')
                    self.result_label.text = '= ' + decimal
                else:
                    beautiful = self.format_fraction_beautiful(frac.numerator, frac.denominator)
                    self.result_label.text = '= ' + beautiful

    def reciprocal(self):
        if self.last_result is not None and self.last_result != 0:
            result = 1 / self.last_result
            self.expression = str(result)
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            formatted = self.format_result(result)
            self.result_label.text = '= ' + str(formatted)
            self.last_result = result
            self.result_shown = True
            self.error_state = False

    def absolute(self):
        if self.last_result is not None:
            result = abs(self.last_result)
            self.expression = str(result)
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            formatted = self.format_result(result)
            self.result_label.text = '= ' + str(formatted)
            self.last_result = result
            self.result_shown = True
            self.error_state = False

    def calculate(self):
        if not self.expression:
            return

        try:
            expr = self.expression
            mode = self.detect_mode(expr)

            expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')

            # Автозакрытие скобок
            open_count = expr.count('(')
            close_count = expr.count(')')
            if open_count > close_count:
                expr += ')' * (open_count - close_count)

            # Маппинг функций
            func_mapping = {
                'tg(': 'tan(',
                'arcsin(': 'asin(',
                'arccos(': 'acos(',
                'arctg(': 'atan('
            }

            for old, new in func_mapping.items():
                expr = expr.replace(old, new)

            # Обработка логарифмов В ПЕРВУЮ ОЧЕРЕДЬ
            # log(основание,аргумент) -> (log(аргумент)/log(основание))
            def replace_log_with_base(match):
                base = match.group(1).strip()
                arg = match.group(2).strip()
                return f'(log({arg})/log({base}))'

            expr = re.sub(r'log\(([^,]+),([^)]+)\)', replace_log_with_base, expr)

            # Теперь заменяем оставшиеся log и ln
            expr = expr.replace('log(', 'math.log10(')
            expr = expr.replace('ln(', 'math.log(')

            def make_trig_func(func_name, mode):
                def trig_func(x):
                    if mode == 'deg':
                        x = math.radians(x)
                    return getattr(math, func_name)(x)

                return trig_func

            def make_atrig_func(func_name, mode):
                def atrig_func(x):
                    result = getattr(math, func_name)(x)
                    if mode == 'deg':
                        result = math.degrees(result)
                    return result

                return atrig_func

            safe_dict = {
                'sin': make_trig_func('sin', mode),
                'cos': make_trig_func('cos', mode),
                'tan': make_trig_func('tan', mode),
                'asin': make_atrig_func('asin', mode),
                'acos': make_atrig_func('acos', mode),
                'atan': make_atrig_func('atan', mode),
                'sqrt': math.sqrt,
                'abs': abs,
                'pi': math.pi,
                'π': math.pi,
                'e': math.e,
                'math': math,
                '__builtins__': {}
            }

            expr = expr.replace('π', 'pi')
            expr = expr.replace('^', '**')

            result = eval(expr, safe_dict)

            formatted = self.format_result(result)
            if formatted is None:
                raise ValueError("Невозможно вычислить")

            self.result_label.text = '= ' + str(formatted)
            self.last_result = result
            self.expression = str(result)
            self.expr_label.text = self.format_expression_beautiful(self.expression)
            self.result_shown = True
            self.error_state = False

        except Exception as e:
            self.result_label.text = 'Ошибка'
            self.error_state = True


if __name__ == '__main__':
    CalculatorApp().run()