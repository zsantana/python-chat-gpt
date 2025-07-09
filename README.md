# Python Chat GPT

A simple Python project that integrates with OpenAI's ChatGPT API to create a terminal-based chatbot. This project allows users to interact with ChatGPT directly from the command line, providing a straightforward way to leverage the power of conversational AI.

## Features

- **Terminal-Based Interaction**: Engage with ChatGPT through a command-line interface.
- **Conversation History**: Maintains a log of the conversation for reference.
- **Easy Configuration**: Uses environment variables for secure API key management.
- **Customizable Prompts**: Allows users to set system messages to define the assistant's behavior.

## Requirements

- Python 3.10 or later
- OpenAI Python library (`openai`)
- A valid OpenAI API key

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zsantana/python-chat-gpt.git
   cd python-chat-gpt
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Your OpenAI API Key**:
   - Rename `test.env` to `.env`:
     ```bash
     mv test.env .env
     ```
   - Open the `.env` file and add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your-api-key-here
     ```
   - You can obtain an API key from [OpenAI's platform](https://platform.openai.com/account/api-keys).

## Usage

1. **Run the Chatbot**:
   ```bash
   python chatgpt.py
   ```

2. **Interact with the Chatbot**:
   - Type your messages in the terminal and press Enter to send.
   - The chatbot will respond, and the conversation will be logged in `chatgpt-chat.txt` for later reference.
   - To exit, type `exit` and press Enter.

## Example

```bash
$ python chatgpt.py
👨‍💻: What's the best way to learn Python?
🤖: The best way to learn Python is to start with the basics—understand variables, data types, loops, and functions through interactive tutorials like Codecademy or freeCodeCamp. Then, build small projects like a calculator or a to-do list to apply what you’ve learned. Reading Python’s official documentation and exploring libraries like pandas or requests can deepen your knowledge. Practice consistently, and try solving problems on platforms like LeetCode or HackerRank. Want tips for a specific Python topic?
👨‍💻: exit
```

## Project Structure

```
python-chat-gpt/
├── chatgpt.py          # Main script for running the chatbot
├── requirements.txt    # List of required Python libraries
├── .env                # Environment file for storing API key
├── chatgpt-chat.txt    # Log file for conversation history
└── README.md           # Project documentation
```

## Troubleshooting

- **Rate Limit Error**: If you see a `RateLimitError`, check your OpenAI plan and billing details to ensure you have sufficient quota.
- **Module Not Found**: Ensure all dependencies are installed by running `pip install -r requirements.txt`. If issues persist, try `pip3 install openai`.
- **API Key Issues**: Verify that your `.env` file contains a valid OpenAI API key and that it’s correctly formatted.

## Contributing

Contributions are welcome! If you’d like to improve this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using the [OpenAI Python library](https://github.com/openai/openai-python).
- Inspired by the need for a simple, terminal-based interface to interact with ChatGPT.