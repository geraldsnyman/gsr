# Contributing to Gerald's Screen Recorder

Thank you for your interest in contributing to **Gerald's Screen Recorder (GSR)**! We welcome improvements, bug fixes, and suggestions to make this the best lightweight screen recording tool for developers and creators.

## Getting Started

1.  **Fork the Repository**: Click the "Fork" button on the top right of the repository page.
2.  **Clone Your Fork**:
    ```bash
    git clone https://github.com/geraldsnyman/ScreenRecorder.git
    cd ScreenRecorder
    ```
3.  **Set Up Environment**:
    We recommend using a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Development Workflow

1.  **Create a Branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  **Make Changes**: Implement your feature or fix.
    - Keep code clean and commented.
    - Follow existing style (snake_case for Python).
3.  **Test Your Changes**:
    - Run the app via `./run.sh` or `python3 src/main.py`.
    - Verify basic functionality (Start/Stop, Settings Save/Load).
4.  **Commit Changes**:
    ```bash
    git commit -m "Add descriptive message about your change"
    ```
5.  **Push and Open a Pull Request**:
    ```bash
    git push origin feature/your-feature-name
    ```
    - Go to the original repository and open a Pull Request (PR).
    - Describe your changes clearly.

## Reporting Bugs

- Use the **Issues** tab to report bugs.
- Include steps to reproduce, your OS version, and any error logs from the terminal.

## Feature Requests

- Have an idea? Open an Issue with the tag `enhancement`.
- Describe the problem it solves and your proposed solution.

## Code of Conduct

- Be respectful and constructive.
- Help others learn and grow.
- Harassment of any kind will not be tolerated.

---
*Happy Coding!*
