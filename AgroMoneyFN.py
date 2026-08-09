import flet as ft
import json, random, uuid
from pathlib import Path

DATA_FILE = Path("agromoney_data.json")

THEMES = {
    "Plantação": "🌾",
    "Laboratório": "🧪",
    "Mercado": "🏪",
    "Rio": "🌊",
    "Evento": "⚡",
}
COLORS = ["#2F7D4A", "#4B88C8", "#E5AD32", "#C55B7A", "#7B62A8", "#D46B38"]

DEMO_CARDS = [
    {"id": str(uuid.uuid4()), "theme": "Plantação", "title": "Pragas atacaram sua plantação",
     "text": "Uma infestação ameaça sua produção.",
     "a": {"label": "Usar pesticida forte", "money": 2, "health": -1, "contam": 2},
     "b": {"label": "Usar controle biológico", "money": -1, "health": 1, "contam": -1}},
    {"id": str(uuid.uuid4()), "theme": "Rio", "title": "Resíduos químicos no rio",
     "text": "Uma atividade próxima contaminou parte do rio.",
     "a": {"label": "Ignorar o problema", "money": 1, "health": -2, "contam": 2},
     "b": {"label": "Investir na limpeza", "money": -2, "health": 2, "contam": -2}},
    {"id": str(uuid.uuid4()), "theme": "Mercado", "title": "Mercado oferece preço melhor",
     "text": "Você precisa decidir entre aumentar a produção ou manter uma prática mais sustentável.",
     "a": {"label": "Aumentar a produção", "money": 3, "health": 0, "contam": 2},
     "b": {"label": "Manter produção sustentável", "money": 1, "health": 1, "contam": -1}},
    {"id": str(uuid.uuid4()), "theme": "Laboratório", "title": "Análise de inseticida",
     "text": "O laboratório apresenta informações sobre os impactos do uso inadequado de inseticidas.",
     "a": {"label": "Aplicar a orientação técnica", "money": 1, "health": 1, "contam": -1}},
    {"id": str(uuid.uuid4()), "theme": "Evento", "title": "Fiscalização ambiental",
     "text": "Uma fiscalização visita a região e observa as práticas dos produtores.",
     "a": {"label": "Cooperar com a fiscalização", "money": -1, "health": 1, "contam": -2},
     "b": {"label": "Ignorar as orientações", "money": 2, "health": -1, "contam": 2}},
]

session = {
    "room_code": None,
    "player_index": 0
}

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "cards": DEMO_CARDS,
        "rooms": {}
    }

data = load_data()

def save():
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main(page: ft.Page):
    page.title = "AgroMoney"
    page.theme = ft.Theme(color_scheme_seed="#2F7D4A")
    page.bgcolor = "#F3F7F2"
    page.padding = 18
    page.scroll = ft.ScrollMode.AUTO

    def get_current_room():
        code = session["room_code"]
        if code and code in data.get("rooms", {}):
            return data["rooms"][code]
        return None

    def go(view):
        data["view"] = view
        save()
        render()

    def snack(msg, color="#173522"):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def header():
        room = get_current_room()
        controls = [ft.Text("🌱 AgroMoney", size=25, weight=ft.FontWeight.BOLD, color="#173522")]
        if room and room.get("started"):
            controls.append(ft.Container(
                ft.Text(f"🔑 Sala: {session['room_code']}", weight=ft.FontWeight.BOLD, color="#2F7D4A"),
                bgcolor="#E2EAE3", padding=8, border_radius=8
            ))
            controls.append(ft.Row([
                ft.TextButton("🌎 Partida", on_click=lambda e: go("dashboard")),
                ft.TextButton("👤 Meu painel", on_click=lambda e: go("me")),
                ft.TextButton("🃏 Cartas", on_click=lambda e: go("cards")),
                ft.TextButton("🛠️ Criadores", on_click=lambda e: go("admin")),
            ], scroll=ft.ScrollMode.AUTO))
        return ft.Row(controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True)

    def card(content, padding=18, expand=None):
        return ft.Container(content=content, bgcolor="white", border_radius=18, padding=padding,
                            border=ft.Border.all(1, "#DDE8DF"), expand=expand)

    def stat(title, value, icon):
        return ft.Container(ft.Column([
            ft.Text(f"{icon} {title}", size=13),
            ft.Text(str(value), size=25, weight=ft.FontWeight.BOLD)
        ]), bgcolor="#F7F5ED", border_radius=14, padding=15)

    def home():
        join_code_field = ft.TextField(label="Código da Sala", hint_text="Ex.: AGRO-5824", width=200)

        def join_room(e):
            code = join_code_field.value.strip().upper()
            if not code:
                return snack("Digite o código da sala!")
            if code not in data.get("rooms", {}):
                return snack("Sala não encontrada! Verifique o código.")
            session["room_code"] = code
            go("dashboard")

        return ft.Column([
            card(ft.Column([
                ft.Text("🌱", size=55, text_align=ft.TextAlign.CENTER),
                ft.Text("AgroMoney", size=40, weight=ft.FontWeight.BOLD, color="#173522", text_align=ft.TextAlign.CENTER),
                ft.Text("Jogo de tabuleiro + painel digital para acompanhar jogadores, cartas, recursos e impactos ambientais.",
                        text_align=ft.TextAlign.CENTER, color="#68766D"),
                ft.Divider(),
                ft.ElevatedButton("🎲 Criar Nova Partida", on_click=lambda e: go("setup"), bgcolor="#2F7D4A", color="white", height=48),
                ft.Text("OU", size=12, color="#68766D", weight=ft.FontWeight.BOLD),
                ft.Row([
                    join_code_field,
                    ft.ElevatedButton("Entrar na Sala", on_click=join_room, bgcolor="#4B88C8", color="white", height=48)
                ], alignment=ft.MainAxisAlignment.CENTER, wrap=True)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14), padding=28),
            ft.Row([
                card(ft.Column([ft.Text("🌎 Estado geral", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text("Rio, hospital e sustentabilidade para todos acompanharem.")]), expand=True),
                card(ft.Column([ft.Text("🃏 Baralho editável", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text("Adicione as cartas conforme forem ficando prontas.")]), expand=True)
            ], wrap=True)
        ], spacing=15)

    def setup():
        name = ft.TextField(label="Nome da partida", value="AgroMoney")
        players = []

        def add_existing(p_name=""):
            i = len(players)
            tf = ft.TextField(label=f"Jogador {i+1}", value=p_name)
            players.append(tf)
            players_col.controls.append(tf)
            page.update()

        players_col = ft.Column()
        add_existing("Jogador 1")
        add_existing("Jogador 2")

        def add(e):
            if len(players) < 8:
                add_existing()
            else:
                snack("Máximo de 8 jogadores.")

        def start(e):
            names = [x.value.strip() or f"Jogador {i+1}" for i, x in enumerate(players)]
            room_code = f"AGRO-{random.randint(1000, 9999)}"
            
            if "rooms" not in data:
                data["rooms"] = {}

            data["rooms"][room_code] = {
                "name": name.value.strip() or "AgroMoney",
                "started": True,
                "players": [{"name": n, "color": COLORS[i % len(COLORS)], "money": 1000, "health": 100,
                             "contam": 0, "position": "", "cards": []} for i, n in enumerate(names)],
                "current": 0,
                "global": {"river": 20, "hospital": 10, "sustain": 70},
                "log": [f'Partida "{name.value.strip() or "AgroMoney"}" criada com o código {room_code}.']
            }
            session["room_code"] = room_code
            save()
            go("dashboard")

        return card(ft.Column([
            ft.Text("🎮 Nova partida", size=28, weight=ft.FontWeight.BOLD),
            name,
            ft.Text("👥 Jogadores", size=18, weight=ft.FontWeight.BOLD),
            players_col,
            ft.Row([
                ft.OutlinedButton("＋ Adicionar jogador", on_click=add),
                ft.ElevatedButton("Começar partida 🚀", on_click=start, bgcolor="#2F7D4A", color="white")
            ], wrap=True)
        ], spacing=12))

    def dashboard():
        room = get_current_room()
        if not room:
            return card(ft.Text("Nenhuma partida ativa. Volte ao início."))

        players = room["players"]
        cur = players[room["current"]] if players else None
        global_values = room["global"]
        pcols = []

        for i, p in enumerate(players):
            pcols.append(ft.Container(ft.Row([
                ft.Container(width=15, height=15, bgcolor=p["color"], border_radius=20),
                ft.Column([
                    ft.Text(p["name"], weight=ft.FontWeight.BOLD),
                    ft.Text(("É a vez deste jogador" if i == room["current"] else "Aguardando") +
                            (f" · Casa {p['position']}" if p.get("position") else ""), size=12, color="#68766D")
                ], expand=True),
                ft.Text(f"🪙 {p['money']}", weight=ft.FontWeight.BOLD)
            ]), padding=10, border=ft.Border.all(1, "#E2EAE3"), border_radius=12))

        log = room.get("log", [])
        top_controls = [ft.Column([
            ft.Text("🌎 Painel da partida", size=25, weight=ft.FontWeight.BOLD),
            ft.Text(f"{room['name']} (Código: {session['room_code']})", color="#68766D")
        ], expand=True)]

        if cur:
            top_controls.append(ft.ElevatedButton(
                f"🎲 Vez de {cur['name']}", on_click=lambda e: go("turn"),
                bgcolor="#2F7D4A", color="white"))

        top_card = card(ft.Column([
            ft.Row(top_controls),
            ft.Row([
                stat("Rio", global_values["river"], "💧"),
                stat("Hospital", global_values["hospital"], "🏥"),
                stat("Sustentabilidade", global_values["sustain"], "♻️")
            ], wrap=True)
        ]))

        log_content = [ft.Text("📰 O que está acontecendo?", size=20, weight=ft.FontWeight.BOLD)]
        if log:
            log_content.extend(ft.Text(x, size=13) for x in reversed(log[-20:]))
        else:
            log_content.append(ft.Text("Nenhum acontecimento ainda.", color="#68766D"))

        return ft.Column([
            top_card,
            card(ft.Column([ft.Text("👥 Jogadores", size=20, weight=ft.FontWeight.BOLD), *pcols])),
            card(ft.Column(log_content))
        ], spacing=14)

    def me():
        room = get_current_room()
        if not room: return card(ft.Text("Nenhuma partida ativa."))
        p = room["players"][room["current"]] if room["players"] else None
        if not p: return card(ft.Text("Nenhum jogador."))

        mylog = [x for x in room.get("log", []) if p["name"] in x]
        return ft.Column([
            card(ft.Column([
                ft.Text(f"👤 {p['name']}", size=26, weight=ft.FontWeight.BOLD),
                ft.Row([stat("Moedas", p["money"], "🪙"), stat("Saúde", p["health"], "❤️"),
                        stat("Contaminação", p["contam"], "☣️")], wrap=True),
                ft.Text(f"📍 Casa {p['position'] or 'não registrada'} · 🃏 {len(p['cards'])} carta(s) usada(s)")
            ])),
            card(ft.Column([ft.Text("📜 Meu histórico", size=20, weight=ft.FontWeight.BOLD),
                             *(ft.Text(x, size=13) for x in reversed(mylog[-20:]))] if mylog else
                            [ft.Text("Nenhum registro para este jogador.", color="#68766D")]))
        ], spacing=14)

    def turn():
        room = get_current_room()
        if not room: return card(ft.Text("Nenhuma partida ativa."))
        p = room["players"][room["current"]]
        pos = ft.TextField(label="Casa (opcional)", hint_text="Ex.: 18")

        def choose(theme):
            if pos.value.strip(): p["position"] = pos.value.strip()
            pool = [c for c in data["cards"] if c["theme"] == theme]
            if not pool: return snack(f"Ainda não há cartas em {theme}. Adicione em Criadores.")
            room["active_card"] = random.choice(pool)
            save()
            show_card()

        buttons = [ft.ElevatedButton(f"{emoji} {t}", on_click=lambda e, t=t: choose(t)) for t, emoji in THEMES.items()]

        return card(ft.Column([
            ft.Text(f"🎲 Vez de {p['name']}", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Jogue o dado e mova o peão no tabuleiro físico. Depois informe onde caiu.", color="#68766D"),
            ft.Container(ft.Text("1. Jogue o dado  ·  2. Mova o peão  ·  3. Escolha o tipo da casa"), bgcolor="#FFF7DB", padding=14, border_radius=12),
            ft.Text("📍 Onde você caiu?", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(buttons, wrap=True), pos
        ], spacing=14))

    def show_card():
        room = get_current_room()
        c = room.get("active_card")
        p = room["players"][room["current"]]

        def effects(e):
            return f"🪙 {e.get('money',0):+d}  ·  ❤️ {e.get('health',0):+d}  ·  ☣️ {e.get('contam',0):+d}"

        def apply(key):
            e = c[key]
            p["money"] += e.get("money", 0)
            p["health"] = max(0, min(100, p["health"] + e.get("health", 0)))
            p["contam"] = max(0, min(100, p["contam"] + e.get("contam", 0)))
            p["cards"].append(c["id"])

            gl = room["global"]
            delta = e.get("contam", 0)
            gl["river"] = max(0, min(100, gl["river"] + delta))
            gl["sustain"] = max(0, min(100, gl["sustain"] - delta + (1 if e.get("health", 0) > 0 else 0)))
            gl["hospital"] = max(0, min(100, gl["hospital"] - e.get("health", 0)))

            room["log"].append(f'{p["name"]} resolveu "{c["title"]}" ({key.upper()}). {effects(e)}')
            room["current"] = (room["current"] + 1) % len(room["players"])
            room.pop("active_card", None)
            save()
            go("dashboard")

        choices = []
        for k in ["a", "b"]:
            if k in c:
                e = c[k]
                choices.append(ft.ElevatedButton(
                    f"{k.upper()} — {e['label']}\n{effects(e)}",
                    on_click=lambda ev, k=k: apply(k), width=500, height=65))

        page.clean()
        page.add(header(), card(ft.Column([
            ft.Text(f"{THEMES.get(c['theme'],'🃏')} {c['theme']}", size=13),
            ft.Text(c["title"], size=28, weight=ft.FontWeight.BOLD),
            ft.Text(c["text"], size=16, color="#68766D"),
            *choices
        ], spacing=14), padding=26))
        page.update()

    def cards_view():
        tabs = [ft.Text(f"{e} {t}: {len([c for c in data['cards'] if c['theme']==t])}", weight=ft.FontWeight.BOLD) for t, e in THEMES.items()]
        return card(ft.Column([
            ft.Text("🃏 Baralho", size=27, weight=ft.FontWeight.BOLD),
            ft.Text("As cartas podem ser adicionadas aos poucos em Criadores.", color="#68766D"),
            *tabs
        ], spacing=12))

    def admin():
        theme = ft.Dropdown(label="Tema", options=[ft.dropdown.Option(x) for x in THEMES], value="Plantação")
        title = ft.TextField(label="Título")
        desc = ft.TextField(label="Descrição", multiline=True, min_lines=3)
        al = ft.TextField(label="Opção A")
        am = ft.TextField(label="🪙 Moedas A", value="0", keyboard_type=ft.KeyboardType.NUMBER)
        ah = ft.TextField(label="❤️ Saúde A", value="0", keyboard_type=ft.KeyboardType.NUMBER)
        ac = ft.TextField(label="☣️ Contaminação A", value="0", keyboard_type=ft.KeyboardType.NUMBER)
        bl = ft.TextField(label="Opção B (opcional)")
        bm = ft.TextField(label="🪙 Moedas B", value="0", keyboard_type=ft.KeyboardType.NUMBER)
        bh = ft.TextField(label="❤️ Saúde B", value="0", keyboard_type=ft.KeyboardType.NUMBER)
        bc = ft.TextField(label="☣️ Contaminação B", value="0", keyboard_type=ft.KeyboardType.NUMBER)

        def num(x):
            try: return int(x.value or 0)
            except: return 0

        def add(e):
            if not title.value.strip(): return snack("Digite o título.")
            c = {"id": str(uuid.uuid4()), "theme": theme.value, "title": title.value.strip(), "text": desc.value.strip(),
                 "a": {"label": al.value.strip() or "Opção A", "money": num(am), "health": num(ah), "contam": num(ac)}}
            if bl.value.strip():
                c["b"] = {"label": bl.value.strip(), "money": num(bm), "health": num(bh), "contam": num(bc)}
            data["cards"].append(c)
            save()
            snack("Carta adicionada!")
            go("admin")

        def delete(cid):
            data["cards"] = [c for c in data["cards"] if c["id"] != cid]
            save()
            go("admin")

        listing = [ft.Container(ft.Row([
            ft.Text(f"{THEMES.get(c['theme'],'🃏')}", size=22),
            ft.Column([ft.Text(c["title"], weight=ft.FontWeight.BOLD), ft.Text(c["theme"], size=12, color="#68766D")], expand=True),
            ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=lambda e, cid=c["id"]: delete(cid))
        ]), padding=10, border=ft.Border.all(1, "#E2EAE3"), border_radius=12) for c in data["cards"]]

        return ft.Column([
            card(ft.Column([
                ft.Text("🛠️ Área dos criadores", size=27, weight=ft.FontWeight.BOLD),
                ft.Text("Adicione novas cartas sem precisar alterar o código.", color="#68766D"),
                theme, title, desc, ft.Text("Opção A", size=18, weight=ft.FontWeight.BOLD), al,
                ft.Row([am, ah, ac], wrap=True), ft.Text("Opção B (opcional)", size=18, weight=ft.FontWeight.BOLD), bl,
                ft.Row([bm, bh, bc], wrap=True),
                ft.ElevatedButton("＋ Salvar carta", on_click=add, bgcolor="#2F7D4A", color="white")
            ])),
            card(ft.Column([ft.Text(f"Cartas cadastradas: {len(data['cards'])}", size=20, weight=ft.FontWeight.BOLD), *listing]))
        ], spacing=14)

    def render():
        page.clean()
        page.add(header())
        view = data.get("view", "home")
        if view == "setup": page.add(setup())
        elif view == "dashboard": page.add(dashboard())
        elif view == "me": page.add(me())
        elif view == "turn": page.add(turn())
        elif view == "cards": page.add(cards_view())
        elif view == "admin": page.add(admin())
        else: page.add(home())
        page.update()

    render()

if __name__ == "__main__":
    ft.app(target=main)
