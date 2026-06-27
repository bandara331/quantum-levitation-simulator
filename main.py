
# pyrefly: ignore [missing-import]
import flet as ft
import asyncio
from groq import AsyncGroq

def main(page: ft.Page):
    page.title = "Quantum Levitation Simulator — Mission Control"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050A0F"
    page.padding = 0
    page.window.width = 1280
    page.window.height = 820

    BG_PRIMARY    = "#050A0F"
    BG_PANEL      = "#080E15"
    BG_CARD       = "#0B1520"
    ACCENT_CYAN   = "#00B4D8"
    ACCENT_WHITE  = "#E8EDF2"
    TEXT_PRIMARY  = "#C8D8E8"
    TEXT_DIM      = "#4A6070"
    TEXT_LABEL    = "#7A9AB0"
    BORDER_DARK   = "#112030"
    BORDER_ACCENT = "#1A3550"
    GREEN_STABLE  = "#00D68F"
    RED_COLLAPSE  = "#FF3860"

    def mono(text, size=11, color=None, bold=False, spacing=0):
        return ft.Text(
            text,
            size=size,
            color=color or TEXT_PRIMARY,
            font_family="Consolas",
            weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
            style=ft.TextStyle(letter_spacing=spacing) if spacing else None,
        )

    def section_label(text):
        return mono(text.upper(), size=10, color=TEXT_DIM, spacing=3)

    def panel_divider():
        return ft.Container(height=1, bgcolor=BORDER_DARK, margin=ft.Margin.symmetric(vertical=12))

    def compute_force(b, t):
        if t <= -180:
            return (b ** 2) * abs(t + 180) * 0.5
        return 0.0

    # Live value labels
    mag_value_label  = mono("2.5 T",  size=13, color=ACCENT_CYAN, bold=True)
    temp_value_label = mono("-200 C", size=13, color=ACCENT_CYAN, bold=True)

    # Sliders
    mag_slider = ft.Slider(
        min=0, max=10, divisions=100, value=2.5,
        active_color=ACCENT_CYAN, inactive_color=BORDER_ACCENT,
        thumb_color=ACCENT_WHITE,
        on_change=lambda e: _on_slider_change()
    )
    temp_slider = ft.Slider(
        min=-273, max=0, divisions=273, value=-200,
        active_color=ACCENT_CYAN, inactive_color=BORDER_ACCENT,
        thumb_color=ACCENT_WHITE,
        on_change=lambda e: _on_slider_change()
    )

    # API Key field
    api_key_input = ft.TextField(
        hint_text="gsk_...",
        password=True,
        can_reveal_password=True,
        bgcolor=BG_PRIMARY,
        border_color=BORDER_ACCENT,
        focused_border_color=ACCENT_CYAN,
        color=TEXT_PRIMARY,
        hint_style=ft.TextStyle(color=TEXT_DIM, font_family="Segoe UI"),
        text_style=ft.TextStyle(font_family="Consolas", size=13),
        height=44,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        border_radius=2,
    )

    # Quantum Core
    core_inner = ft.Container(
        width=60, height=60, border_radius=30,
        bgcolor=ACCENT_CYAN,
        shadow=ft.BoxShadow(blur_radius=40, spread_radius=8, color="#4400B4D8"),
    )
    core_ring1 = ft.Container(
        width=100, height=100, border_radius=50,
        border=ft.Border(
            top=ft.BorderSide(1, "#3300B4D8"), bottom=ft.BorderSide(1, "#3300B4D8"),
            left=ft.BorderSide(1, "#3300B4D8"), right=ft.BorderSide(1, "#3300B4D8"),
        ),
        alignment=ft.Alignment.CENTER,
    )
    core_ring2 = ft.Container(
        width=145, height=145, border_radius=73,
        border=ft.Border(
            top=ft.BorderSide(1, "#1A00B4D8"), bottom=ft.BorderSide(1, "#1A00B4D8"),
            left=ft.BorderSide(1, "#1A00B4D8"), right=ft.BorderSide(1, "#1A00B4D8"),
        ),
        alignment=ft.Alignment.CENTER,
    )
    core_ring3 = ft.Container(
        width=190, height=190, border_radius=95,
        border=ft.Border(
            top=ft.BorderSide(1, "#0D00B4D8"), bottom=ft.BorderSide(1, "#0D00B4D8"),
            left=ft.BorderSide(1, "#0D00B4D8"), right=ft.BorderSide(1, "#0D00B4D8"),
        ),
        alignment=ft.Alignment.CENTER,
    )

    core_stack = ft.Stack(
        controls=[
            ft.Container(width=190, height=190, content=core_ring3, alignment=ft.Alignment.CENTER),
            ft.Container(width=190, height=190, content=core_ring2, alignment=ft.Alignment.CENTER),
            ft.Container(width=190, height=190, content=core_ring1, alignment=ft.Alignment.CENTER),
            ft.Container(width=190, height=190, content=core_inner, alignment=ft.Alignment.CENTER),
        ],
        width=190, height=190,
    )

    core_container = ft.Container(
        content=core_stack,
        animate=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT),
    )

    # Status indicators
    status_dot   = ft.Container(width=7, height=7, border_radius=4, bgcolor=GREEN_STABLE)
    status_label = mono("STABLE QUANTUM FIELD", size=11, color=GREEN_STABLE, spacing=2)

    # Telemetry displays
    force_value    = mono("0.00", size=52, color=ACCENT_WHITE, bold=True)
    field_val_disp = mono("2.5",  size=20, color=ACCENT_CYAN, bold=True)
    temp_val_disp  = mono("-200", size=20, color=ACCENT_CYAN, bold=True)
    state_display  = mono("SUPERCONDUCTING", size=11, color=GREEN_STABLE, spacing=2)

    # AI output
    ai_text = ft.Text(
        "AWAITING INITIATION — Enter parameters and engage simulation protocol.",
        size=13, color=TEXT_LABEL, font_family="Segoe UI", selectable=True,
    )
    ai_scroll = ft.Column(controls=[ai_text], scroll=ft.ScrollMode.AUTO, expand=True)

    # Physics update
    def _on_slider_change():
        b = mag_slider.value
        t = temp_slider.value
        mag_value_label.value  = f"{b:.1f} T"
        temp_value_label.value = f"{int(t)} C"
        field_val_disp.value   = f"{b:.1f}"
        temp_val_disp.value    = f"{int(t)}"
        force = compute_force(b, t)
        force_value.value = f"{force:.2f}"

        if t <= -180:
            status_dot.bgcolor    = GREEN_STABLE
            status_label.value    = "STABLE QUANTUM FIELD"
            status_label.color    = GREEN_STABLE
            state_display.value   = "SUPERCONDUCTING"
            state_display.color   = GREEN_STABLE
            core_inner.bgcolor    = ACCENT_CYAN
            core_inner.shadow     = ft.BoxShadow(blur_radius=40, spread_radius=8, color="#4400B4D8")
        else:
            status_dot.bgcolor    = RED_COLLAPSE
            status_label.value    = "FIELD COLLAPSE — TEMP CRITICAL"
            status_label.color    = RED_COLLAPSE
            state_display.value   = "NORMAL PHASE"
            state_display.color   = RED_COLLAPSE
            core_inner.bgcolor    = RED_COLLAPSE
            core_inner.shadow     = ft.BoxShadow(blur_radius=30, spread_radius=4, color="#44FF3860")

        page.update()

    # AI fetch
    async def initiate_simulation(e):
        if not api_key_input.value:
            ai_text.value = "AUTHORIZATION FAILURE — Groq API key required to establish uplink."
            ai_text.color = RED_COLLAPSE
            page.update()
            return

        _on_slider_change()
        b = mag_slider.value
        t = temp_slider.value
        force = compute_force(b, t)

        ai_text.value = "ESTABLISHING UPLINK TO QUANTUM AI NODE . . .\n\nProcessing telemetry parameters . . ."
        ai_text.color = ACCENT_CYAN
        page.update()

        prompt = (
            f"You are a quantum systems engineer for an advanced aerospace project in 2026. "
            f"Antigravity drive simulation: Magnetic Field = {b:.1f} T, Temperature = {t} C, "
            f"Levitation Force = {force:.2f} N. "
            f"Provide rigorous scientific analysis covering: field stability, Meissner effect viability, "
            f"engineering constraints, thermal management, and optimization recommendations. "
            f"Use precise technical language. No markdown. Use plain text with ALL CAPS section headers."
        )

        try:
            client = AsyncGroq(api_key=api_key_input.value.strip())
            response = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            ai_text.value = response.choices[0].message.content
            ai_text.color = TEXT_PRIMARY
            ai_text.font_family = "Segoe UI"
        except Exception as ex:
            ai_text.value = f"UPLINK FAILURE — Connection severed.\n\n{str(ex)}"
            ai_text.color = RED_COLLAPSE

        page.update()

    # Button
    initiate_btn = ft.Container(
        content=mono("INITIATE SIMULATION", size=12, color=ACCENT_CYAN, bold=True, spacing=2),
        width=float("inf"), height=44,
        border=ft.Border(
            top=ft.BorderSide(1, ACCENT_CYAN), bottom=ft.BorderSide(1, ACCENT_CYAN),
            left=ft.BorderSide(1, ACCENT_CYAN), right=ft.BorderSide(1, ACCENT_CYAN),
        ),
        border_radius=2, bgcolor="#0A1E2E",
        alignment=ft.Alignment.CENTER,
        on_click=initiate_simulation,
        animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
    )

    # ===== LEFT PANEL =====
    left_panel = ft.Container(
        width=290, bgcolor=BG_PANEL,
        border=ft.Border(right=ft.BorderSide(1, BORDER_DARK)),
        padding=ft.Padding.all(28),
        content=ft.Column([
            section_label("System Parameters"),
            panel_divider(),
            mono("MAGNETIC FIELD", size=10, color=TEXT_DIM, spacing=2),
            ft.Container(height=4),
            ft.Row([ft.Container(expand=True), mag_value_label]),
            mag_slider,
            ft.Container(height=16),
            mono("TEMPERATURE", size=10, color=TEXT_DIM, spacing=2),
            ft.Container(height=4),
            ft.Row([ft.Container(expand=True), temp_value_label]),
            temp_slider,
            panel_divider(),
            section_label("Authorization"),
            ft.Container(height=8),
            mono("GROQ API KEY", size=10, color=TEXT_DIM, spacing=2),
            ft.Container(height=6),
            api_key_input,
            ft.Container(expand=True),
            initiate_btn,
        ], spacing=0, expand=True),
    )

    # ===== CENTER PANEL =====
    center_panel = ft.Container(
        expand=True, bgcolor=BG_PRIMARY,
        border=ft.Border(right=ft.BorderSide(1, BORDER_DARK)),
        content=ft.Column([
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=28, vertical=16),
                border=ft.Border(bottom=ft.BorderSide(1, BORDER_DARK)),
                content=ft.Row([
                    section_label("Quantum Core Visualizer"),
                    ft.Container(expand=True),
                    ft.Row([status_dot, ft.Container(width=8), status_label], spacing=0),
                ]),
            ),
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column([
                    core_container,
                    ft.Container(height=36),
                    mono("LEVITATION FORCE", size=14, color=ACCENT_CYAN, spacing=3, bold=True),
                    ft.Container(height=6),
                    ft.Row([
                        force_value,
                        ft.Container(
                            content=mono("N", size=18, color=TEXT_LABEL),
                            padding=ft.Padding.only(top=24, left=6)
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ),
            ft.Container(
                bgcolor=BG_CARD,
                border=ft.Border(top=ft.BorderSide(1, BORDER_DARK)),
                padding=ft.Padding.symmetric(horizontal=28, vertical=16),
                content=ft.Row([
                    ft.Column([
                        mono("CORE STATE", size=9, color=TEXT_DIM, spacing=2),
                        ft.Container(height=4),
                        state_display,
                    ]),
                    ft.Container(width=1, bgcolor=BORDER_DARK, margin=ft.Margin.symmetric(horizontal=24)),
                    ft.Column([
                        mono("B-FIELD", size=9, color=TEXT_DIM, spacing=2),
                        ft.Container(height=4),
                        ft.Row([field_val_disp, mono(" T", size=10, color=TEXT_LABEL)]),
                    ]),
                    ft.Container(width=1, bgcolor=BORDER_DARK, margin=ft.Margin.symmetric(horizontal=24)),
                    ft.Column([
                        mono("TEMPERATURE", size=9, color=TEXT_DIM, spacing=2),
                        ft.Container(height=4),
                        ft.Row([temp_val_disp, mono(" C", size=10, color=TEXT_LABEL)]),
                    ]),
                ]),
            ),
        ], spacing=0),
    )

    # ===== RIGHT PANEL =====
    right_panel = ft.Container(
        width=360, bgcolor=BG_PANEL,
        content=ft.Column([
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                border=ft.Border(bottom=ft.BorderSide(1, BORDER_DARK)),
                content=section_label("AI Node Analysis"),
            ),
            ft.Container(expand=True, padding=ft.Padding.all(24), content=ai_scroll),
        ], spacing=0, expand=True),
    )

    # ===== HEADER =====
    header = ft.Container(
        height=52, bgcolor=BG_PANEL,
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_DARK)),
        padding=ft.Padding.symmetric(horizontal=28),
        content=ft.Row([
            ft.Row([
                ft.Container(width=6, height=6, border_radius=3, bgcolor=ACCENT_CYAN),
                ft.Container(width=10),
                mono("QUANTUM LEVITATION SIMULATOR", size=11, color=ACCENT_WHITE, bold=True, spacing=3),
            ]),
            ft.Container(expand=True),
            mono("DEVELOPED BY SASMITHA THEJAN", size=10, color=ACCENT_CYAN, spacing=2, bold=True),
            ft.Container(width=16),
            mono("MISSION CONTROL v1.0", size=10, color=TEXT_DIM, spacing=2),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
    )

    page.add(
        ft.Column([
            header,
            ft.Row([left_panel, center_panel, right_panel], expand=True, spacing=0),
        ], spacing=0, expand=True)
    )

    _on_slider_change()


if __name__ == "__main__":
    ft.run(main)
