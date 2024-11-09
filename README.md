# Linux-Gemini-AI
Gemini AI in Terminal

# Panduan Penginstalan / Installation Guide

## Prasyarat / Prerequisites
Sebelum memulai, pastikan Anda memiliki hal-hal berikut:  
Before you begin, ensure you have the following:
- Python 3.x
- pip (manajer paket Python)  
- Git (untuk mengkloning repositori)  

## Instalasi di Termux / Installation on Termux

1. **Perbarui paket dan instal Python dan Git:**  
   **Update packages and install Python and Git:**
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   ```

2. **Kloning repositori:**  
   **Clone the repository:**
   ```bash
   git clone https://github.com/ZetaGo-Aurum/Linux-Gemini-AI.git
   cd GeminiAI
   ```

3. **Instal dependensi:**  
   **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Buat file `.env` untuk menyimpan API key:**  
   **Create a `.env` file to store the API key:**
   ```bash
   touch .env
   nano .env
   ```
   Tambahkan baris berikut ke dalam file `.env`:  
   Add the following line to the `.env` file:
   ```
   API_KEY_GEMINI_REQUIERED=your_api_key_here
   ```

5. **Jalankan aplikasi:**  
   **Run the application:**
   ```bash
   python3 main.py
   ```

## Instalasi di Linux (Ubuntu/Debian) / Installation on Linux (Ubuntu/Debian)

1. **Perbarui paket dan instal Python dan Git:**  
   **Update packages and install Python and Git:**
   ```bash
   sudo apt update && sudo apt upgrade
   sudo apt install python3 python3-pip git
   ```

2. **Kloning repositori:**  
   **Clone the repository:**
   ```bash
   git clone https://github.com/ZetaGo-Aurum/Linux-Gemini-AI.git
   cd GeminiAI
   ```

3. **Instal dependensi:**  
   **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Buat file `.env` untuk menyimpan API key:**  
   **Create a `.env` file to store the API key:**
   ```bash
   touch .env
   nano .env
   ```
   Tambahkan baris berikut ke dalam file `.env`:  
   Add the following line to the `.env` file:
   ```
   API_KEY_GEMINI_REQUIERED=your_api_key_here
   ```

5. **Jalankan aplikasi:**  
   **Run the application:**
   ```bash
   python3 main.py
   ```

## Catatan / Notes
- Pastikan untuk mengganti `your_api_key_here` dengan API key yang valid.  
- Make sure to replace `your_api_key_here` with a valid API key.
- Jika Anda mengalami masalah, pastikan semua dependensi telah terinstal dengan benar.  
- If you encounter issues, ensure all dependencies are installed correctly.
