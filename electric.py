# electric.py
import os
import math
from math import sin, pi
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

# Optional: desktop window size for testing — remove or comment on mobile
Window.size = (400, 760)
Window.clearcolor = (1, 1, 1, 1)  # white base


# ---------- Chakra Widget (big, centered, rotating + glowing) ----------
class ChakraWidget(AnchorLayout):
    """
    Draws a big centered Ashoka Chakra that rotates slowly and pulses (glow).
    No external image needed — drawn with Kivy graphics.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.size_hint = (1, 1)
        # internal animation values
        self._angle = 0.0
        self._glow_t = 0.0
        # schedule update loop
        Clock.schedule_interval(self._update, 1 / 60.0)

    def _update(self, dt):
        self._angle = (self._angle + 0.2) % 360
        self._glow_t += dt * 1.2
        self.canvas.before.clear()
        with self.canvas.before:
            # draw tricolor background bands (fixed saffron/white/green)
            # saffron top
            Color(1.0, 0.6, 0.0, 1.0)
            Rectangle(pos=(0, Window.height * 2 / 3), size=(Window.width, Window.height / 3))
            # white middle
            Color(1.0, 1.0, 1.0, 1.0)
            Rectangle(pos=(0, Window.height / 3), size=(Window.width, Window.height / 3))
            # green bottom
            Color(0.0, 0.5, 0.0, 1.0)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height / 3))

            # Chakra center coordinates (slightly above center to look good)
            cx = Window.width / 2
            cy = Window.height * 0.55
            radius = min(Window.width, Window.height) * 0.18  # big and centered

            # glow alpha oscillates
            glow_alpha = 0.18 + 0.12 * (0.5 + 0.5 * sin(self._glow_t * 2 * pi))
            # soft halo (multiple concentric ellipses)
            Color(0.0, 0.2, 1.0, glow_alpha)
            for mul in (1.6, 1.25, 1.0):
                Ellipse(pos=(cx - radius * mul, cy - radius * mul), size=(2 * radius * mul, 2 * radius * mul))

            # deep-blue ring (chakra outer)
            Color(0.05, 0.1, 0.6, 1.0)
            Line(circle=(cx, cy, radius), width=3.0)

            # spokes — 24 spokes, rotated by _angle
            Color(0.05, 0.1, 0.6, 0.95)
            spokes = 24
            for i in range(spokes):
                theta = math.radians(self._angle + (360.0 / spokes) * i)
                r_inner = radius * 0.12
                x1 = cx + r_inner * math.cos(theta)
                y1 = cy + r_inner * math.sin(theta)
                x2 = cx + radius * math.cos(theta)
                y2 = cy + radius * math.sin(theta)
                Line(points=[x1, y1, x2, y2], width=1.6)

            # inner small circle
            Color(0.05, 0.1, 0.6, 1.0)
            Ellipse(pos=(cx - radius * 0.12, cy - radius * 0.12), size=(radius * 0.24, radius * 0.24))


# ---------- Ripple button helper ----------
def apply_orange_green_ripple(btn: Button):
    """
    Apply a short orange->green color ripple and a quick size bounce to the button.
    """
    # original color fallback
    orig = getattr(btn, 'background_color', [1, 1, 1, 1])
    try:
        orig = list(btn.background_color)
    except Exception:
        orig = [1, 1, 1, 1]

    # small bounce: increase height then return
    orig_height = btn.height
    bounce = Animation(height=orig_height * 1.08, d=0.09, t='out_quad') + Animation(height=orig_height, d=0.12, t='out_quad')
    # color change: saffron -> green -> original
    anim_color_1 = Animation(background_color=(1.0, 0.6, 0.0, 1.0), d=0.09)
    anim_color_2 = Animation(background_color=(0.0, 0.6, 0.0, 1.0), d=0.12)
    anim_color_3 = Animation(background_color=tuple(orig), d=0.12)
    # run both animations
    try:
        bounce.start(btn)
        (anim_color_1 + anim_color_2 + anim_color_3).start(btn)
    except Exception:
        pass


class RippleButton(Button):
    """
    Button subclass that uses the ripple helper on_press to produce orange-green ripple + bounce.
    """
    def on_press(self):
        apply_orange_green_ripple(self)
        return super().on_press()


# ---------- Screens ----------
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main = BoxLayout(orientation='vertical', padding=16, spacing=10)

        # logo
        if os.path.exists("logo.png"):
            logo = Image(source="logo.png", size_hint=(1, 0.30))
        else:
            logo = Label(text="[b]LOGO NOT FOUND[/b]", markup=True, size_hint=(1, 0.30))
        main.add_widget(logo)

        # title in tricolor
        title = Label(text='[b][color=#FF9933]BHARAT[/color]  [color=#000080]⚡[/color]  [color=#138808]BIJLI[/color][/b]',
                      markup=True, font_size='34sp', size_hint=(1, 0.12))
        main.add_widget(title)
        main.add_widget(Label(text="Smart energy tools for everyday life", font_size='14sp', size_hint=(1, 0.06)))

        # buttons list (one per screen)
        grid = GridLayout(cols=1, spacing=10, size_hint=(1, 0.56))
        btn_specs = [
            ("⚡ Bill Estimator", "bill"),
            ("💡 Power Saving Tips", "tips"),
            ("☀️ Solar Panel Advisor", "solar"),
            ("🔌 Load Management", "load"),
            ("🧠 Smart Load Suggestion", "suggest"),
            ("📉 Smart Power Cut Tracker", "tracker"),
        ]
        for text, screenname in btn_specs:
            b = RippleButton(text=text, size_hint=(1, None), height=56, bold=True)
            b.background_color = [1, 1, 1, 0.95]
            b.color = [0, 0, 0, 1]
            b.bind(on_release=lambda inst, sn=screenname: self.goto(sn))
            grid.add_widget(b)

        main.add_widget(grid)
        self.add_widget(main)

    def goto(self, screenname):
        self.manager.transition = SlideTransition(direction="left", duration=0.28)
        self.manager.current = screenname


# ---------- Feature screens ----------
class BillScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical', padding=16, spacing=10)
        box.add_widget(Label(text="[b]Bill Estimator[/b]", markup=True, font_size='22sp'))
        box.add_widget(Label(text="Enter monthly units (kWh):"))
        self.units_in = TextInput(hint_text="e.g. 250", multiline=False, input_filter='int')
        box.add_widget(self.units_in)
        calc = Button(text="Calculate", size_hint=(1, None), height=48, background_color=(1, 0.6, 0.2, 1))
        calc.bind(on_press=self.calculate)
        box.add_widget(calc)
        self.res = Label(text="", font_size=16)
        box.add_widget(self.res)
        box.add_widget(self.back_btn())
        self.add_widget(box)

    def calculate(self, instance):
        try:
            u = int(self.units_in.text)
            if u <= 100:
                amt = u * 5
            elif u <= 300:
                amt = 100 * 5 + (u - 100) * 7
            else:
                amt = 100 * 5 + 200 * 7 + (u - 300) * 10
            amt += 50
            self.res.text = f"Estimated Bill: ₹{amt:.2f}"
        except:
            self.res.text = "Enter a valid number"

    def back_btn(self):
        b = Button(text="⬅ Back", size_hint=(1, None), height=44)
        b.bind(on_release=self.go_back)
        return b

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right", duration=0.28)
        self.manager.current = 'home'


class TipsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical', padding=16, spacing=10)
        box.add_widget(Label(text="[b]Power Saving Tips[/b]", markup=True, font_size='22sp'))
        tips = [
            "Switch off lights and fans when not in the room.",
            "Use LED bulbs — they consume less power.",
            "Unplug chargers and appliances when idle.",
            "Run washing machine on full load.",
            "Keep AC filters clean for efficient cooling."
        ]
        scroll = ScrollView(size_hint=(1, 0.8))
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8, padding=6)
        inner.bind(minimum_height=inner.setter('height'))
        for t in tips:
            inner.add_widget(Label(text="• " + t, size_hint_y=None, height=36, font_size=16))
        scroll.add_widget(inner)
        box.add_widget(scroll)
        box.add_widget(self.back_btn())
        self.add_widget(box)

    def back_btn(self):
        b = Button(text="⬅ Back", size_hint=(1, None), height=44)
        b.bind(on_release=self.go_back)
        return b

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right", duration=0.28)
        self.manager.current = 'home'


class SolarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical', padding=16, spacing=10)
        box.add_widget(Label(text="[b]Solar Panel Advisor[/b]", markup=True, font_size='22sp'))
        box.add_widget(Label(text="Enter average monthly units:"))
        self.units_in = TextInput(hint_text="e.g. 300", multiline=False, input_filter='int')
        box.add_widget(self.units_in)
        btn = Button(text="Get Suggestion", size_hint=(1, None), height=48, background_color=(1, 0.8, 0.2, 1))
        btn.bind(on_press=self.recommend)
        box.add_widget(btn)
        self.res = Label(text="", font_size=16)
        box.add_widget(self.res)
        box.add_widget(self.back_btn())
        self.add_widget(box)

    def recommend(self, instance):
        try:
            u = int(self.units_in.text)
            kw = u / 120.0
            cost = int(kw * 70000)
            self.res.text = f"Recommend: {kw:.1f} kW (approx. ₹{cost})"
        except:
            self.res.text = "Enter valid units"

    def back_btn(self):
        b = Button(text="⬅ Back", size_hint=(1, None), height=44)
        b.bind(on_release=self.go_back)
        return b

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right", duration=0.28)
        self.manager.current = 'home'


class LoadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical', padding=16, spacing=10)
        box.add_widget(Label(text="[b]Load Management[/b]", markup=True, font_size='22sp'))
        box.add_widget(Label(text="Enter total connected load (Watts):"))
        self.load_in = TextInput(hint_text="e.g. 2500", multiline=False, input_filter='int')
        box.add_widget(self.load_in)
        btn = Button(text="Analyze", size_hint=(1, None), height=48, background_color=(0.4, 0.7, 1, 1))
        btn.bind(on_press=self.analyze)
        box.add_widget(btn)
        self.res = Label(text="", font_size=16)
        box.add_widget(self.res)
        box.add_widget(self.back_btn())
        self.add_widget(box)

    def analyze(self, instance):
        try:
            l = int(self.load_in.text)
            if l < 1000:
                self.res.text = "Light load — good!"
            elif l < 3000:
                self.res.text = "Moderate load — avoid simultaneous heavy devices."
            else:
                self.res.text = "High load — split appliances across time."
        except:
            self.res.text = "Enter valid load"

    def back_btn(self):
        b = Button(text="⬅ Back", size_hint=(1, None), height=44)
        b.bind(on_release=self.go_back)
        return b

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right", duration=0.28)
        self.manager.current = 'home'


class SmartLoadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical', padding=16, spacing=10)
        box.add_widget(Label(text="[b]Smart Load Suggestion[/b]", markup=True, font_size='22sp'))
        box.add_widget(Label(text="Enter appliance power (kW):"))
        self.kw_in = TextInput(hint_text="e.g. 1.5", multiline=False, input_filter='float')
        box.add_widget(self.kw_in)
        box.add_widget(Label(text="Enter runtime (hours):"))
        self.hrs_in = TextInput(hint_text="e.g. 2", multiline=False, input_filter='float')
        box.add_widget(self.hrs_in)
        btn = Button(text="Suggest cheapest start hours", size_hint=(1, None), height=48, background_color=(1, 0.6, 0.2, 1))
        btn.bind(on_press=self.suggest)
        box.add_widget(btn)
        self.res = Label(text="", font_size=16)
        box.add_widget(self.res)
        box.add_widget(self.back_btn())
        self.add_widget(box)

    def suggest(self, instance):
        try:
            kw = float(self.kw_in.text)
            hrs = max(1, int(round(float(self.hrs_in.text))))
            tariffs = [5 + (i % 6) * 0.5 for i in range(24)]
            costs = []
            for start in range(24):
                cost = sum(tariffs[(start + h) % 24] * kw for h in range(hrs))
                costs.append((start, round(cost, 2)))
            costs.sort(key=lambda x: x[1])
            top = costs[:3]
            out = "Top 3 cheapest start hours:\n"
            for s, c in top:
                out += f"{s}:00 — ₹{c}\n"
            self.res.text = out
        except:
            self.res.text = "Enter valid numbers"

    def back_btn(self):
        b = Button(text="⬅ Back", size_hint=(1, None), height=44)
        b.bind(on_release=self.go_back)
        return b

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right", duration=0.28)
        self.manager.current = 'home'


class PowerCutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical', padding=16, spacing=10)
        box.add_widget(Label(text="[b]Smart Power-Cut Tracker[/b]", markup=True, font_size='22sp'))
        box.add_widget(Label(text="Enter area/city:"))
        self.area_in = TextInput(hint_text="e.g. Mumbai", multiline=False)
        box.add_widget(self.area_in)
        box.add_widget(Label(text="Start time (e.g. 15:00):"))
        self.start_in = TextInput(hint_text="e.g. 15:00", multiline=False)
        box.add_widget(self.start_in)
        box.add_widget(Label(text="End time (e.g. 17:00):"))
        self.end_in = TextInput(hint_text="e.g. 17:00", multiline=False)
        box.add_widget(self.end_in)
        box.add_widget(Label(text="Reason (optional):"))
        self.reason_in = TextInput(hint_text="Maintenance", multiline=False)
        box.add_widget(self.reason_in)
        save_btn = Button(text="Save Schedule", size_hint=(1, None), height=48, background_color=(0.2, 0.9, 0.4, 1))
        save_btn.bind(on_press=self.save_schedule)
        box.add_widget(save_btn)
        view_btn = Button(text="View saved schedules", size_hint=(1, None), height=44)
        view_btn.bind(on_press=self.view_schedules)
        box.add_widget(view_btn)
        self.res = Label(text="", font_size=16)
        box.add_widget(self.res)
        box.add_widget(self.back_btn())
        self.add_widget(box)
        self.storage_file = "powercuts.txt"
        if not os.path.exists(self.storage_file):
            open(self.storage_file, "a", encoding="utf-8").close()

    def save_schedule(self, instance):
        a = self.area_in.text.strip().title()
        s = self.start_in.text.strip()
        e = self.end_in.text.strip()
        r = self.reason_in.text.strip() or "Not specified"
        if not a or not s or not e:
            self.res.text = "[color=ff3333]Fill all fields[/color]"
            return
        with open(self.storage_file, "a", encoding="utf-8") as f:
            f.write(f"{a} | {s} - {e} | {r}\n")
        self.res.text = "[color=00aa00]Saved schedule[/color]"

    def view_schedules(self, instance):
        lines = []
        with open(self.storage_file, "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if ln:
                    lines.append(ln)
        if not lines:
            self.res.text = "No saved schedules"
            return
        out = "Saved schedules:\n" + "\n".join(lines[-6:][::-1])
        self.res.text = out

    def back_btn(self):
        b = Button(text="⬅ Back", size_hint=(1, None), height=44)
        b.bind(on_release=self.go_back)
        return b

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right", duration=0.28)
        self.manager.current = 'home'


# ---------- App ----------
class BharatBijliApp(App):
    def build(self):
        # Prepare ScreenManager
        sm = ScreenManager(transition=SlideTransition())

        # Add screens
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(BillScreen(name='bill'))
        sm.add_widget(TipsScreen(name='tips'))
        sm.add_widget(SolarScreen(name='solar'))
        sm.add_widget(LoadScreen(name='load'))
        sm.add_widget(SmartLoadScreen(name='suggest'))
        sm.add_widget(PowerCutScreen(name='tracker'))

        # Root layout: chakra at bottom, screens on top
        root = BoxLayout(orientation='vertical')
        chakra = ChakraWidget()
        # chakra draws background in its canvas.before; adding chakra first places it visually behind SM
        root.add_widget(chakra)
        root.add_widget(sm)

        # expose sm for debugging if needed
        self.sm = sm
        return root


if __name__ == "__main__":
    BharatBijliApp().run()
