Certify
🎓 Certificate Designer - Python GUI Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Built with](https://img.shields.io/badge/built%20with-Tkinter%20%2B%20Pillow-orange)

> A no-code, drag-and-drop certificate generator powered by Python! Create professional certificates from Excel in minutes. 🎉

---


✨ Features

- 🖼️ **Interactive Canvas**: Draw text boxes on your certificate template with real-time mouse input.
- 📄 **Excel Integration**: Auto-map certificate fields from Excel sheet columns.
- 🖍️ **Custom Fonts & Styles**: Set font style, size, and color for each field.
- 👁️ **Live Preview**: Preview the first certificate before batch generation.
- 🖨️ **Bulk Export**: Generate personalized certificates for hundreds of participants.
- 📁 **Save as PNG**: Certificates saved to a `certificates/` folder for easy access.

---

🚀 Quick Start

1️⃣ Requirements


pip install pillow pandas openpyxl
2️⃣ Run the App
bash
Copy
Edit
python certificate_gui.py
🧠 How It Works
Load your certificate template image (JPG/PNG).

Load your Excel file (.xlsx) with participant data.

Draw a rectangle for each column (e.g., Name, Event, Date).

Choose your font style, size, and color per field.

Preview the output.

Hit "Generate All" to export certificates!

📁 File Structure

certificate_gui.py     # Main GUI logic
certificates/          # Auto-created folder with generated PNGs
preview.png            # Sample preview image
🧩 Tech Stack
Python 3.x

Tkinter – GUI interface

Pillow – Image processing

pandas – Excel (.xlsx) reading

openpyxl – Backend engine for .xlsx files

🎯 Use Cases
College and school event certifications 🏫

Hackathon participation awards 👨‍💻

Webinar/Workshop attendance proof 🎤

Volunteer appreciation 🎗️

🙌 Contributing
Pull requests are welcome. Feel free to open an issue to discuss improvements or ideas 💡.

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.

🧑‍💻 Developed by
Muthukumaran S
✨ Follow me on GitHub: @MuthuKumaran-Dev-10000 (https://github.com/MuthuKumaran-Dev-10000)


---

Let me know if you want:
- 🎨 Badge styles for dark themes
- 📌 Sample certificate template and Excel
- 📦 To package it into a PyPI installable package

Happy shipping your library! 🚀