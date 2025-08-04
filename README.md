# Subtl (Rewrite)

![Subtl Logo](https://imgur.com/a/68ggd9i)

**Subtl** is a powerful, modern desktop application designed to help you edit and manipulate subtitle files with ease. This project is a complete architectural rewrite of the original Subtl, built from the ground up with Python and PySide6 to provide a more flexible, robust, and user-friendly experience.

The new Subtl features a sleek, Chrome-inspired tabbed interface, allowing you to work on multiple subtitle tasks simultaneously in a clean and organized workspace.

## ✨ Core Features

This rewrite introduces a completely new architecture focused on usability and extensibility:

*   **Modern Tab-Based Workflow**: Open multiple tools at once in separate tabs. Each tab manages its own context and navigation history.
*   **Custom Frameless UI**: A polished, custom-drawn interface, including a draggable title bar and window resizing, provides a seamless, modern look and feel.
*   **Integrated Tool Dashboard**: New tabs open to a central "Dashboard" where you can easily browse and launch any of the available subtitle tools.
*   **Per-Tab Navigation**: Each tab has its own back and forward navigation history, allowing you to move between the dashboard and your opened tool effortlessly.
*   **Extensible Tool Architecture**: Tools are managed centrally, making it simple for developers to add new subtitle manipulation utilities to the application.
*   **Customizable Theming**: Easily switch between different visual themes (e.g., Dark, Light) to suit your preference.

## 🛠️ Tools Overview

Subtl provides a suite of tools to handle your subtitle editing needs.

*   **📏 Minimum Length**: Adjust the minimum display time of subtitles.
*   **📏 Maximum Length**: Adjust the maximum display time of subtitles. *(Placeholder)*
*   **🔗 Merge Lines**: Combine multiple subtitle lines into one. *(Placeholder)*
*   **✂️ Split Lines**: Split long subtitle lines into two. *(Placeholder)*
*   **⏰ Subtitle Shifter**: Shift subtitle timings forwards or backwards. *(Placeholder)*
*   **🔄 Subtitle Converter**: Convert subtitles to various formats. *(Placeholder)*
*   **🌍 Multilingual Merge**: Merge subtitles from different languages. *(Placeholder)*

*(Note: While the framework is complete, many tools from the original application are currently implemented as placeholders and will be developed in future updates.)*

## 🚀 Installation

Installers for Windows, macOS, and Linux are coming soon. In the meantime, you can run the application from the source code.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Subtl.git
    cd Subtl
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install PySide6 qtawesome
    ```
3.  **Run the application:**
    ```bash
    python main.py
    ```

## 🖥️ Usage Guide

1.  **Launch Subtl**: An initial window will open with a single "Dashboard" tab.
2.  **Open a Tool**: From the Dashboard, click on the button for the tool you wish to use. The tool's interface will load within the current tab.
3.  **Navigate**: Use the **Back** (`<`) and **Forward** (`>`) buttons in the top-left to navigate between the Dashboard and the tool within the active tab.
4.  **Work with Multiple Tools**: Click the **Add Tab** (`+`) button to open a new Dashboard tab. You can then launch another tool, allowing you to work on different tasks in parallel.
5.  **Manage Tabs**: Switch between tools by clicking on the corresponding tab. Close a tab by clicking the `x` icon on the tab itself.

## 🤝 Contributing

We welcome contributions from the community! The new modular architecture makes it easy to add new tools or improve existing ones.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeatureName`).
3.  Implement your feature or bug fix. To add a new tool, create a new `QWidget` class for its UI and register it in `tool_manager.py`.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/YourFeatureName`).
6.  Open a Pull Request.

## 📄 License

Subtl is licensed under the MIT License. See the `LICENSE` file for more details.

## 🙏 Acknowledgments

*   Built with the amazing **PySide6** (Qt for Python) framework.
*   Icons provided by the **QtAwesome** library.
*   Thanks to all future contributors who will help make Subtl even better.

---

**Subtl** is developed with ❤️ by SubtlDevTeams. Happy editing