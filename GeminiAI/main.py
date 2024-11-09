import os
from pyexpat import model
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress
from pathlib import Path
import requests
import PIL.Image
import time

load_dotenv()

console = Console()

default_api_key = "API_KEY_GEMINI_REQUIERED"
usage_count = 0
language = 'id'  # Bahasa default adalah Indonesia

conversation_history = []  # Menyimpan riwayat percakapan

def setup_api_key():
    api_key = Prompt.ask("Masukkan API key Gemini Anda", default=default_api_key)
    if not api_key:
        console.print("API key tidak boleh kosong. Silakan coba lagi.", style="bold red")
        return setup_api_key()
    return api_key

def start_gemini_ai():
    console.print("Memulai Gemini AI, harap tunggu...", style="bold green")
    return "gemini-1.5-pro-latest"

def process_image(image_path):
    # Menambahkan logika untuk memproses gambar sebelum diupload
    try:
        img = PIL.Image.open(image_path)
        img = img.convert("RGB")  # Mengubah gambar menjadi format RGB
        processed_image_path = "processed_" + os.path.basename(image_path)
        img.save(processed_image_path)
        return processed_image_path
    except Exception as e:
        console.print(f"Terjadi kesalahan saat memproses gambar: {str(e)}", style="bold red")
        return None

def upload_image(image_path):
    processed_image_path = process_image(image_path)  # Memproses gambar sebelum upload
    if processed_image_path is None:
        return None
    url = "https://api.example.com/upload"
    try:
        with open(processed_image_path, 'rb') as img:
            response = requests.post(url, files={'file': img})
        if response.status_code == 200:
            return response.json().get('link')
        else:
            console.print("Gagal mengupload gambar. Status: " + str(response.status_code), style="bold red")
            return None
    except Exception as e:
        console.print(f"Terjadi kesalahan saat mengupload gambar: {str(e)}", style="bold red")
        return None

def check_api_limit():
    global usage_count
    console.print(f"Jumlah penggunaan API saat ini: {usage_count}", style="bold blue")  # Menampilkan penggunaan API saat ini

    # Menggunakan limit statis jika tidak bisa mendapatkan dari API
    api_limit = 2000000  # Ganti dengan limit yang sesuai jika Anda tahu

    # Peringatan jika mendekati limit
    if usage_count >= api_limit * 0.9:  # Misalnya, jika mendekati 90% dari limit
        console.print("Peringatan: API key token Anda mungkin sudah basi. Pertimbangkan untuk mengganti auth token yang baru.", style="bold red")

def chat_with_gemini(prompt, model):
    global usage_count
    check_api_limit()  # Memeriksa penggunaan API jika perlu

    genai.configure(api_key=api_key)

    model_instance = genai.GenerativeModel(model)  # Menggunakan model yang dipilih
    chat = model_instance.start_chat(
        history=conversation_history  # Menggunakan riwayat percakapan
    )
    response = chat.send_message(prompt, stream=True)
    full_response = ""
    
    for chunk in response:
        # Menggabungkan teks dari chunk tanpa menghapus spasi
        full_response += chunk.text + " "  # Menambahkan spasi setelah setiap chunk

    # Menghapus spasi berlebih di akhir respons
    full_response = full_response.strip()
    
    console.print(f"[AI] {full_response}", style="bold white")
    console.print("_" * 80)

    # Menyimpan percakapan ke riwayat
    conversation_history.append({"role": "user", "parts": prompt})
    conversation_history.append({"role": "model", "parts": full_response})
    
    usage_count += 1  # Memperbarui penggunaan API setelah berhasil menggunakan API

def generate_code(prompt, model):
    global usage_count
    check_api_limit()  # Memeriksa penggunaan API jika perlu

    genai.configure(api_key=api_key)
    response = genai.GenerativeModel(model).generate_content(f"Buatkan kode pemrograman yang kompleks untuk: {prompt}" if language == 'id' else f"Generate complex programming code for: {prompt}")
    usage_count += 1  # Memperbarui penggunaan API setelah berhasil menggunakan API
    return response.text

def view_api_key_usage():
    console.print(f"API Key: {api_key}", style="bold blue")
    console.print(f"Jumlah penggunaan API: {usage_count}" if language == 'id' else f"API Usage Count: {usage_count}", style="bold blue")

def custom_prompt_menu():
    console.print(Panel("Menu Kustom Prompt" if language == 'id' else "Custom Prompt Menu", title="Kustom Prompt" if language == 'id' else "Custom Prompt", title_align="left"))
    console.print("1. Latih AI dengan Prompt Baru" if language == 'id' else "1. Train AI with New Prompt")
    console.print("2. Lihat Ingatan AI" if language == 'id' else "2. View AI Memory")
    console.print("3. Kembali ke Menu Utama" if language == 'id' else "3. Return to Main Menu")
    
    choice = Prompt.ask("Pilih opsi (1/2/3)" if language == 'id' else "Choose option (1/2/3)")
    if choice == '1':
        new_prompt = Prompt.ask("Masukkan prompt baru untuk melatih AI" if language == 'id' else "Enter new prompt to train AI")
        console.print(f"Melatih AI dengan prompt: {new_prompt}" if language == 'id' else f"Training AI with prompt: {new_prompt}", style="bold yellow")
    elif choice == '2':
        console.print("Menampilkan ingatan AI..." if language == 'id' else "Displaying AI memory...", style="bold yellow")
    elif choice == '3':
        return
    else:
        console.print("Pilihan tidak valid. Silakan coba lagi." if language == 'id' else "Invalid choice. Please try again.", style="bold red")
        custom_prompt_menu()

def global_gemini_command(prompt):
    try:
        chat_with_gemini(prompt, model)  # Menggunakan fungsi chat_with_gemini
    except Exception as e:
        console.print(f"Terjadi kesalahan: {str(e)}" if language == 'id' else f"An error occurred: {str(e)}", style="bold red")

def change_model_menu():
    global model
    console.print("Pilih model AI yang ingin digunakan:" if language == 'id' else "Choose the AI model to use:", style="bold yellow")
    console.print("1. Gemini 1.5 Pro" if language == 'id' else "1. Gemini 1.5 Pro")
    console.print("2. Gemini 1.5 Flash" if language == 'id' else "2. Gemini 1.5 Flash")
    console.print("3. Gemini 1.5 Flash 002" if language == 'id' else "3. Gemini 1.5 Flash 002")
    console.print("4. Gemini 1.5 Pro 002" if language == 'id' else "4. Gemini 1.5 Pro 002")
    console.print("5. Gemini 1.5 Flash 8B" if language == 'id' else "5. Gemini 1.5 Flash 8B")
    
    model_choice = Prompt.ask("Masukkan pilihan model (1/2/3/4/5):" if language == 'id' else "Enter model choice (1/2/3/4/5):")
    if model_choice == '1':
        model = "gemini-1.5-pro"
    elif model_choice == '2':
        model = "gemini-1.5-flash"
    elif model_choice == '3':
        model = "gemini-1.5-flash-002"
    elif model_choice == '4':
        model = "gemini-1.5-pro-002"
    elif model_choice == '5':
        model = "gemini-1.5-flash-8b"
    else:
        console.print("Pilihan tidak valid. Model tidak diubah." if language == 'id' else "Invalid choice. Model not changed.", style="bold red")
        return

    console.print(f"Model AI telah diubah menjadi: {model}" if language == 'id' else f"AI model has been changed to: {model}", style="bold green")

def main():
    global language, model
    console.clear()
    console.print(Panel("🌟 Selamat datang di AI Gemini Terminal 🌟" if language == 'id' else "🌟 Welcome to AI Gemini Terminal 🌟", title="Gemini AI", title_align="left", border_style="bold cyan"))
    console.print(Text("✨ Kredit Pencipta: Rayhan Dzaky Al Mubarok ✨" if language == 'id' else "✨ Creator Credit: Rayhan Dzaky Al Mubarok ✨", style="bold magenta"))
    
    language_choice = Prompt.ask("Pilih bahasa / Choose language: (1) Indonesia (2) English")
    if language_choice == '1':
        language = 'id'
        console.print("Anda memilih Bahasa Indonesia.", style="bold green")
    elif language_choice == '2':
        language = 'en'
        console.print("You have chosen English.", style="bold green")
    else:
        console.print("Pilihan tidak valid. Menggunakan Bahasa Indonesia sebagai default." if language == 'id' else "Invalid choice. Defaulting to Indonesian.", style="bold red")

    global api_key
    api_key = setup_api_key()
    
    # Memperbarui pilihan model AI dengan tampilan menjorok ke bawah
    change_model_menu()  # Memanggil fungsi untuk memilih model di awal

    console.clear()
    console.print(Panel("🌟 Selamat datang di AI Gemini Terminal 🌟" if language == 'id' else "🌟 Welcome to AI Gemini Terminal 🌟", title="Gemini AI", title_align="left", border_style="bold cyan"))
    console.print(Text("✨ Kredit Pencipta: Rayhan Dzaky Al Mubarok ✨" if language == 'id' else "✨ Creator Credit: Rayhan Dzaky Al Mubarok ✨", style="bold magenta"))
    console.print("Ketik 'keluar' untuk mengakhiri percakapan." if language == 'id' else "Type 'exit' to end the conversation.")
    console.print("Ketik 'menu' untuk kembali ke menu." if language == 'id' else "Type 'menu' to return to the menu.")
    console.print("Ketik 'kustom' untuk membuka menu kustom prompt." if language == 'id' else "Type 'custom' to open the custom prompt menu.")
    console.print("Ketik 'ganti model' untuk mengganti model AI." if language == 'id' else "Type 'change model' to change the AI model.", style="bold yellow")
    console.print("-" * 50)
    
    while True:
        user_input = Prompt.ask(Text("Anda " if language == 'id' else "You ", style="bold yellow"))
        if user_input.lower() == 'ganti model' or user_input.lower() == 'change model':
            change_model_menu()  # Memanggil fungsi untuk mengganti model
            continue
        elif user_input.lower().startswith('gemini '):  # Menambahkan logika untuk perintah "gemini"
            prompt = user_input[len('gemini '):]  # Mengambil teks pertanyaan setelah "gemini"
            global_gemini_command(prompt)  # Memanggil fungsi global
            continue
        elif user_input.lower() == 'keluar' or user_input.lower() == 'exit':
            console.print("Terima kasih telah menggunakan AI Gemini. Sampai jumpa!" if language == 'id' else "Thank you for using AI Gemini. See you!", style="bold green")
            break
        elif user_input.lower() == 'menu':
            console.clear()
            console.print(Panel("🌟 Selamat datang di AI Gemini Terminal 🌟" if language == 'id' else "🌟 Welcome to AI Gemini Terminal 🌟", title="Gemini AI", title_align="left", border_style="bold cyan"))
            console.print(Text("✨ Kredit Pencipta: Rayhan Dzaky Al Mubarok ✨" if language == 'id' else "✨ Creator Credit: Rayhan Dzaky Al Mubarok ✨", style="bold magenta"))
            console.print("Ketik 'keluar' untuk mengakhiri percakapan." if language == 'id' else "Type 'exit' to end the conversation.")
            console.print("Ketik 'menu' untuk membuka menu." if language == 'id' else "Type 'menu' to open the menu.")
            console.print("Ketik 'api key view' untuk melihat API key dan jumlah penggunaan." if language == 'id' else "Type 'api key view' to see API key and usage count.")
            console.print("Ketik 'kustom' untuk membuka menu kustom prompt." if language == 'id' else "Type 'custom' to open the custom prompt menu.")
            console.print("-" * 50)
            continue
        elif user_input.lower() == 'api key view':
            view_api_key_usage()
            continue
        elif user_input.lower() == 'kustom':
            custom_prompt_menu()
            continue
        elif user_input.lower().startswith('upload '):
            image_path = user_input.split(' ', 1)[1]
            if Path(image_path).is_file():
                console.print("Mengupload gambar, harap tunggu..." if language == 'id' else "Uploading image, please wait...", style="bold yellow")
                link = upload_image(image_path)
                if link:
                    console.print(f"Gambar berhasil diupload! Link: {link}" if language == 'id' else f"Image uploaded successfully! Link: {link}", style="bold blue")
            else:
                console.print("File tidak ditemukan. Silakan coba lagi." if language == 'id' else "File not found. Please try again.", style="bold red")
            continue
        elif user_input.lower().startswith('kode '):
            code_prompt = user_input.split(' ', 1)[1]
            try:
                response = generate_code(code_prompt, model)
                console.print(Text(f"Kode:\n{response}" if language == 'id' else f"Code:\n{response}", style="bold blue"))
            except Exception as e:
                console.print(f"Terjadi kesalahan: {str(e)}" if language == 'id' else f"An error occurred: {str(e)}", style="bold red")
            continue
        
        try:
            chat_with_gemini(user_input, model)
        except Exception as e:
            console.print(f"Terjadi kesalahan: {str(e)}" if language == 'id' else f"An error occurred: {str(e)}", style="bold red")
        
        console.print("-" * 50)

if __name__ == "__main__":
    main()
