# BlockCoins

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/uukelele-scratch/blockcoin/publish.yml)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/uukelele-scratch/blockcoin)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr/uukelele-scratch/blockcoin)
![PyPI - License](https://img.shields.io/pypi/l/blockcoin)
![GitHub Repo stars](https://img.shields.io/github/stars/uukelele-scratch/blockcoin)
![PyPI - Version](https://img.shields.io/pypi/v/blockcoin)

Automate BlockCoin farming on https://blockcoin.vercel.app with ease.

## 📦 Installation

```bash
pip install blockcoins
```

## 🚀 Features

- Multi-threaded automated post creation
- Automatic liking of posts (two like methods)
- Target-based coin farming
- Thread-safe logging of created posts
- Graceful error handling and recovery
- Real-time stats on earnings and performance

## 🔧 Usage

```python
from blockcoin import BlockCoinFarm

# Your login credentials
username = "your_username"
password = "your_password"

# Initialize the farming bot
farm = login(username, password)

# Post contents and prices
texts = ["Farming blockcoins!", "Let's go!", "Boost me up!"]
prices = [1, 2, 3, 4, 5]

# Start farming
stats = farm.get_blockcoins(
    post_texts=texts,
    prices=prices,
    thread_count=3,
    amount_of_blockcoins=100,
    like=1  # like method: 1 = raw request, 2 = API method
)

# Print results
print(stats)
```

## ⚙️ Class: BlockCoinFarm

### __init__(username, password)
Initializes the bot with your login details.

### login()
Logs into blockcoin.vercel.app and stores the session.

### get_blockcoins(post_texts, prices, thread_count=1, amount_of_blockcoins=None, like=1)
Starts the farming process.

Arguments:
- post_texts: List of text strings to be posted
- prices: List of prices for the posts
- thread_count: Number of concurrent threads (default 1)
- amount_of_blockcoins: Stop when target is reached (optional)
- like: Liking method (1 = raw HTTP, 2 = API-based)

Returns a dictionary with:
- initial_balance
- final_balance
- coins_earned
- target_reached (True/False)
- time_took (formatted time string)
- posts_created (int)
- average_price (float)
- coins_per_minute (float)
- like_method_used (int)
- details (list of created post dicts)

## 🧠 Notes

- Threaded execution ensures high performance farming.
- If a thread encounters a "No `const data = [`" error, it will retry intelligently.
- You can stop the farming process anytime with Ctrl+C.
- The like method is optional — use `like=2` if the default fails.

## 🛠 Example Output

{
    'initial_balance': 50,
    'final_balance': 150,
    'coins_earned': 100,
    'target_reached': True,
    'time_took': '0:01:32.141245',
    'posts_created': 48,
    'average_price': 2.3,
    'coins_per_minute': 65.21,
    'like_method_used': 1,
    'details': [...]
}

## 💬 Support

Issues or questions? Hit up the dev or open an issue on the GitHub repo.
