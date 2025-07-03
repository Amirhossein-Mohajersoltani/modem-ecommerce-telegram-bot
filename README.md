# Modem E-commerce Telegram Bot

This project is a Telegram bot for managing an e-commerce platform focused on selling modems and SIM cards. It provides both admin and user panels, allowing for product management, order processing, and user interactions, all through Telegram.

## Features
- **Admin Panel**: Add/edit/delete products, manage users and admins, broadcast messages, approve or decline orders, and more.
- **User Panel**: Browse products, buy modems or SIM cards, make payments, and view order status.
- **Database Integration**: All data is stored and managed via a MySQL database.
- **Modular Structure**: Code is organized for maintainability and scalability.

## Project Structure
```
modem-ecommerce-telegram-bot/
  bot/
    admin/         # Admin panel logic and conversations
    user/          # User panel logic and conversations
    core/          # Shared utilities, database, config, filters
    main.py        # Entry point for the bot
    say_hello.py   # Example handler
  requirements.txt # Python dependencies
  README.md        # Project documentation
  tests/           # (Optional) Test files
```

## Setup & Usage
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure environment**:
   - Set up your `.env` file and database credentials as needed in `bot/core/config.py`.
3. **Run the bot**:
   ```bash
   python -m bot.main
   ```

## Contributing
Feel free to fork the repo and submit pull requests for improvements or bug fixes.

## License
MIT License
