import threading
import customtkinter as ctk
from tkinter import messagebox
from google import genai
# ---------- THEME ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#080F24"
SIDEBAR = "#101A38"
PANEL = "#111B37"
CARD = "#192747"
PURPLE = "#7048F5"
BLUE = "#3985FF"
WHITE = "#F4F6FF"
MUTED = "#A6B6DD"
GREEN = "#36D6A0"

client = None
chat = None
busy = False

# ---------- MAIN WINDOW ----------
app = ctk.CTk()
app.title("My Gen AI Chatbot")
app.geometry("1200x760")
app.minsize(900, 600)
app.configure(fg_color=BG)

# ---------- LAYOUT ----------
sidebar = ctk.CTkFrame(
    app, width=285, corner_radius=0,
    fg_color=SIDEBAR
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main = ctk.CTkFrame(
    app, corner_radius=0, fg_color=BG
)
main.pack(side="left", fill="both", expand=True)

# ---------- SIDEBAR ----------
ctk.CTkLabel(
    sidebar, text="✦",
    font=("Segoe UI", 58, "bold"),
    text_color="#A88BFF"
).pack(pady=(25, 0))

ctk.CTkLabel(
    sidebar, text="MY GEN AI",
    font=("Segoe UI", 23, "bold"),
    text_color=WHITE
).pack()

ctk.CTkLabel(
    sidebar, text="Your AI assistant is here!",
    font=("Segoe UI", 12, "italic"),
    text_color=MUTED
).pack(pady=(5, 25))

def side_button(text, command=None):
    ctk.CTkButton(
        sidebar, text=text, command=command,
        height=43, corner_radius=12,
        anchor="w", font=("Segoe UI", 14),
        fg_color="#302C70" if text == "☏   Chat" else "transparent",
        hover_color="#302C70",
        text_color=WHITE
    ).pack(fill="x", padx=17, pady=4)

side_button("☏   Chat")

def show_about():
    messagebox.showinfo(
        "About",
        "My Gen AI Chatbot\nPowered by Google's Gemini API."
    )

side_button("ⓘ   About", show_about)

# ---------- API KEY CARD ----------
key_card = ctk.CTkFrame(
    sidebar, fg_color=PANEL,
    corner_radius=18, border_width=1,
    border_color="#34446F"
)
key_card.pack(fill="x", padx=15, pady=(24, 12))

ctk.CTkLabel(
    key_card, text="🔑  Gemini API Key",
    font=("Segoe UI", 14, "bold"),
    text_color=WHITE
).pack(anchor="w", padx=14, pady=(15, 8))

key_entry = ctk.CTkEntry(
    key_card, placeholder_text="Paste your API key...",
    show="*", height=42, corner_radius=10,
    fg_color=CARD, border_color="#53658E"
)
key_entry.pack(fill="x", padx=12, pady=5)

def connect_api():
    global client, chat

    api_key = key_entry.get().strip()
    if not api_key:
        messagebox.showwarning(
            "Missing key", "Please paste your Gemini API key."
        )
        return

    connect_button.configure(
        state="disabled", text="Connecting..."
    )
    status_label.configure(
        text="● Connecting...", text_color="#FFC857"
    )

    def task():
        global client, chat
        try:
            # Check the key by making a small API request.
            new_client = genai.Client(api_key=api_key)
            new_client.models.generate_content(
                model="gemini-3.8-flash",
                contents="Reply with OK."
            )
            new_chat = new_client.chats.create(
                model="gemini-3.5-flash"
            )
            app.after(
                0, lambda: connection_result(
                    new_client, new_chat, None
                )
            )
        except Exception as error:
            app.after(
                0, lambda e=str(error): connection_result(
                    None, None, e
                )
            )

    threading.Thread(target=task, daemon=True).start()

def connection_result(new_client, new_chat, error):
    global client, chat

    connect_button.configure(
        state="normal", text="✦   Connect to Gemini"
    )

    if error:
        status_label.configure(
            text="● Connection failed",
            text_color="#FF7777"
        )
        messagebox.showerror("Connection Error", error)
        return

    client = new_client
    chat = new_chat
    status_label.configure(
        text="● Connected successfully",
        text_color=GREEN
    )
    add_message(
        "AI",
        "Hello! 👋 I'm your Gemini AI assistant. "
        "Ask me anything and let's explore ideas together."
    )

connect_button = ctk.CTkButton(
    key_card, text="✦   Connect to Gemini",
    command=connect_api, height=43,
    corner_radius=11, fg_color=PURPLE,
    hover_color=BLUE, font=("Segoe UI", 13, "bold")
)
connect_button.pack(fill="x", padx=12, pady=(8, 8))

status_label = ctk.CTkLabel(
    key_card, text="● Not connected",
    text_color="#FFC857",
    font=("Segoe UI", 12)
)
status_label.pack(pady=(2, 14))

# ---------- QUICK TIPS ----------
tips = ctk.CTkFrame(
    sidebar, fg_color=PANEL,
    corner_radius=18, border_width=1,
    border_color="#34446F"
)
tips.pack(fill="x", padx=15, pady=8)

ctk.CTkLabel(
    tips, text="💡  Quick Tips",
    font=("Segoe UI", 14, "bold"),
    text_color=WHITE
).pack(anchor="w", padx=13, pady=(12, 7))

ctk.CTkLabel(
    tips,
    text="• Ask clear questions\n\n"
         "• Explore Python and AI\n\n"
         "• Keep your API key private",
    justify="left", wraplength=225,
    font=("Segoe UI", 12), text_color=MUTED
).pack(anchor="w", padx=13, pady=(0, 13))

ctk.CTkLabel(
    sidebar, text="✦  Better questions\n     Brighter answers  ♡",
    font=("Segoe UI", 15, "italic"),
    text_color="#B7A6FF"
).pack(side="bottom", pady=25)

# ---------- MAIN HEADER ----------
header = ctk.CTkFrame(
    main, fg_color="transparent", height=95
)
header.pack(fill="x", padx=25, pady=(20, 8))

ctk.CTkLabel(
    header, text="✦  My Gen AI Chatbot",
    font=("Segoe UI", 29, "bold"),
    text_color=WHITE
).pack(anchor="w")

ctk.CTkLabel(
    header, text="Ask anything  •  Get instant answers  •  Powered by Gemini",
    font=("Segoe UI", 13), text_color=MUTED
).pack(anchor="w", pady=(4, 0))

# ---------- CHAT PANEL ----------
chat_panel = ctk.CTkFrame(
    main, fg_color="#0C142B",
    corner_radius=20, border_width=1,
    border_color="#26385F"
)
chat_panel.pack(
    fill="both", expand=True,
    padx=20, pady=(0, 12)
)

chat_area = ctk.CTkScrollableFrame(
    chat_panel, fg_color="transparent",
    corner_radius=15
)
chat_area.pack(
    fill="both", expand=True,
    padx=12, pady=12
)

def add_message(sender, message):
    is_user = sender == "You"

    bubble = ctk.CTkFrame(
        chat_area,
        fg_color="#39318A" if is_user else CARD,
        corner_radius=16
    )
    bubble.pack(
        anchor="e" if is_user else "w",
        padx=(65, 8) if is_user else (8, 65),
        pady=9
    )

    ctk.CTkLabel(
        bubble, text="You" if is_user else "✦  Gemini",
        font=("Segoe UI", 12, "bold"),
        text_color="#D5CAFF" if is_user else "#8FE9D0"
    ).pack(anchor="w", padx=15, pady=(11, 3))

    ctk.CTkLabel(
        bubble, text=message,
        font=("Segoe UI", 14),
        text_color=WHITE,
        wraplength=650,
        justify="left"
    ).pack(anchor="w", padx=15, pady=(2, 12))

def send_message(event=None):
    global busy

    question = message_entry.get().strip()
    if not question or busy:
        return

    if chat is None:
        messagebox.showwarning(
            "Connect first",
            "Enter your API key and click Connect to Gemini."
        )
        return

    message_entry.delete(0, "end")
    add_message("You", question)

    busy = True
    send_button.configure(
        state="disabled", text="Thinking..."
    )

    thinking_label = ctk.CTkLabel(
        chat_area, text="✦  Gemini is thinking...",
        text_color=MUTED, font=("Segoe UI", 12, "italic")
    )
    thinking_label.pack(anchor="w", padx=15, pady=8)

    def task():
        try:
            response = chat.send_message(question)
            answer = response.text or "No text response received."
        except Exception as error:
            answer = "Sorry, an error occurred:\n" + str(error)

        app.after(
            0, lambda: finish_response(answer, thinking_label)
        )

    threading.Thread(target=task, daemon=True).start()

def finish_response(answer, thinking_label):
    global busy

    thinking_label.destroy()
    add_message("AI", answer)
    busy = False
    send_button.configure(
        state="normal", text="➤  Send"
    )
    message_entry.focus_set()

# ---------- MESSAGE COMPOSER ----------
composer = ctk.CTkFrame(
    main, fg_color=PANEL,
    corner_radius=18, border_width=1,
    border_color="#26385F"
)
composer.pack(fill="x", padx=20, pady=(0, 10))

message_entry = ctk.CTkEntry(
    composer, placeholder_text="Type your message here...",
    height=48, corner_radius=12,
    border_width=0, fg_color="transparent",
    font=("Segoe UI", 14)
)
message_entry.pack(
    side="left", fill="x", expand=True,
    padx=(15, 8), pady=10
)
message_entry.bind("<Return>", send_message)

send_button = ctk.CTkButton(
    composer, text="➤  Send",
    command=send_message, width=115,
    height=44, corner_radius=13,
    fg_color=PURPLE, hover_color=BLUE,
    font=("Segoe UI", 13, "bold")
)
send_button.pack(side="right", padx=10, pady=10)

def clear_chat():
    if busy:
        return

    for widget in chat_area.winfo_children():
        widget.destroy()

    add_message(
        "AI",
        "Chat cleared! ✨ What would you like to talk about?"
    )

footer = ctk.CTkFrame(main, fg_color="transparent")
footer.pack(fill="x", padx=22, pady=(0, 15))

ctk.CTkButton(
    footer, text="▤  Clear Chat",
    command=clear_chat, width=115, height=34,
    corner_radius=10, fg_color=CARD,
    hover_color="#303D60", text_color=WHITE
).pack(side="left")

ctk.CTkLabel(
    footer, text="Small steps  ✦  Big dreams  ♡",
    text_color=MUTED, font=("Segoe UI", 11)
).pack(side="right")

add_message(
    "AI",
    "Hello! 👋 Welcome to your personal AI space.\n\n"
    "Connect your Gemini API key in the sidebar, "
    "then ask me anything!"
)

app.mainloop()
