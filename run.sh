#!/bin/bash

exec python telegram_bot.py & 
exec python vk_bot.py &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?