# 🚀 Forklift Safety Guard - AI-Developed Game

🚧 **This game is an experiment:** It **must only be developed further using AI!** 🚧  

> **❗️ Development Rule:**
> - **No human should write a single line of code.**
> - **AI (e.g., ChatGPT, Copilot, or other LLMs) must generate all code.**
> - **Only parameter adjustments (e.g., speed, colors, screen size) are allowed.**

👷‍♂️ This game is meant for fun and testing **AI-driven game logic**, **procedural development**, and **parameterization**.

---

## 📜 Rules for Development

1. **👨‍💻 No manual coding!**  
   - You **may only modify parameters** (e.g., screen size, speed values, difficulty settings).  
   - If a new feature is needed, **AI must generate the code**.  

2. **🤖 AI as the Only Developer!**  
   - Use **ChatGPT, GitHub Copilot, Bard, Claude, or any LLM** to generate all new code.  
   - **You may copy-paste from AI, but not write logic manually.**  

3. **📌 Parameterization is OK!**  
   - Changing values in `config.py` (like `SCREEN_WIDTH`, `FORKLIFT_SPEED`) is fine.  
   - Adjusting difficulty settings, colors, and UI elements is **allowed**.  
   - **No manual function implementations or refactoring!**  

---

## 🕹️ How to Play

🚜 **You control a forklift in a warehouse** where you:  
- Pick up **packages** using the forklift forks.  
- Deliver them to the **drop-off zone**.  
- Avoid crashing into **shelves or pedestrians**.  
- Use the **Safety Guard feature** to slow down pedestrians, but be careful—it slows you down too!

### 🎮 Controls
- `Arrow Keys` → Move the forklift 🚜  
- `SPACE` → Pick up or drop a package 📦  
- `S` → Activate **Safety Guard Mode** (slows pedestrians but also slows you down)  

### 🚧 Game Over Conditions
- ❌ **Hitting a wall**  
- ❌ **Crashing into a shelf**  
- ❌ **(Unless Safety Guard is active) Colliding with a pedestrian**  

---

## 💾 Installation & Running the Game

### **1️⃣ Install dependencies using Pipenv**
```sh
pipenv install
```

### **2️⃣ Activate the virtual environment**
```sh
pipenv shell
```

### **3️⃣ Run the game**
```sh
python forky.py
```

---

## ⚙️ Configuration (Allowed Edits)

You can change values in **`config.py`** (but not the game logic itself).  

Example:
```python
SCREEN_WIDTH = 1600  # ✅ Allowed
FORKLIFT_SPEED = 5   # ✅ Allowed
```

---

## 🌍 Contributions & AI Development Process

Since **all code must be AI-generated**, if you want to contribute:  
1. **Describe the feature you need** (e.g., "Add a high-score system").  
2. **Use AI to generate the code** (ChatGPT, Copilot, etc.).  
3. **Copy-paste it into the game**.  
4. **Commit the AI-generated changes.**  

✅ **Allowed:**  
- AI-generated code  
- Changing configuration values  
- Modifying UI settings (colors, fonts, screen size)  

❌ **Not Allowed:**  
- Manually writing or modifying functions  
- Refactoring code manually  
- Debugging without AI assistance  

---

## 📜 License

This game is released under the **MIT License**.

✅ **You may use, modify, and share it freely.**  
❌ **No manual code contributions—only AI-generated code is allowed.**  

---

## 👨‍🔬 Why This Experiment?

This project is an experiment in **fully AI-driven game development**.  
- 🤖 **Can AI develop a full, working game?**  
- 🔄 **How does AI refactor and extend codebases over time?**  
- ⚙️ **How does parameterization allow humans to control AI-generated code?**  

Join the experiment and see how far **AI-driven development** can go! 🚀  

---

## 📌 Final Note

🚧 **🚜 Every line of logic in this game is AI-generated! 🚜🚧**  
If you find a bug or need a new feature, **ask AI to generate a fix!**  

---

### ✅ Done! Your Git Repo is Ready

- **`.gitignore` to keep the repo clean**  
- **`LICENSE` (MIT) for easy sharing**  
- **`README.md` to enforce AI-only development**  

🚀 **Have fun experimenting with AI-driven development!** 😊
