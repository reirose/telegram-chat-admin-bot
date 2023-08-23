# Telegram chat administrator helper Bot
## Installation
Copy the code to your local machine and cd to the directory
```commandline
git clone https://www.github.com/reirose/telegram-chat-admin-bot.git
cd .\telegram-chat-admin-bot
```
Install dependencies
```commandline
pip install python-telegram-bot
```
Now, you are ready to start the bot
```commandline
python main.py --token TELEGRAM BOT TOKEN
```
## Available commands
**All users**:\
```/report``` — report a message to administrator\
```/roll``` — roll a number from 1 to 100\
**Moderators**:\
```/ban``` — ban a user from chat (by reply)\
```/kick``` — kick a user from chat (by reply)\
```/mute [n]``` — mute a user for ```n``` minutes (by reply)\
**Administrators**:\
_Everything available for moderators plus:_\
```/promote [type]``` — promote a user. Available types: VIP, Moderator, 
Administrator (case sensitive) (by reply)\
```/vip_mode``` — toggle VIP mode in a chat. VIP mode allows only VIPs, moderators and 
administrators to write.