# AI-Powered Quantum Levitation Simulator 🚀

**Developed by Sasmitha Thejan**

A cutting-edge, interactive desktop application that simulates a futuristic Antigravity Drive and Quantum Core. Built with **Python** and **Flet** for a native desktop experience, featuring a dynamic SpaceX-inspired Mission Control UI and real-time scientific analysis powered by the **Groq AI (Llama 3 70B)** model.

## ✨ Features
- **Quantum Core Visualizer:** A pulsing, animated UI that reacts to state changes (Superconducting vs. Normal Phase).
- **Real-Time Physics Engine:** Calculates the Meissner effect levitation force dynamically as you adjust Magnetic Field and Temperature parameters.
- **AI Node Uplink:** Connects to Groq's blazing-fast inference API to generate expert-level, scientifically grounded analysis based on your exact simulation telemetry.
- **SpaceX-Inspired UI:** Glassmorphism, deep space color palettes, and strict monospace typography.
- **Standalone Executable:** Packaged natively for Windows — no Python installation required for end users.

## 🛠️ Tech Stack
- **Frontend/GUI:** [Flet](https://flet.dev/) (Python framework for Flutter-based UIs)
- **AI Integration:** `groq` Python SDK
- **LLM Engine:** `llama-3.3-70b-versatile`
- **Packaging:** PyInstaller (via Flet Pack)

## 🚀 Quick Start (For Developers)
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the simulator: `python main.py`
4. Enter your [Groq API Key](https://console.groq.com/keys) in the app to activate the AI.

## 📦 Building the Executable
To package the app into a standalone `.exe` for Windows:
```bash
flet pack main.py --name "Quantum_Simulator" --icon "icon.ico"
```
