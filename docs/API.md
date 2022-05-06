## Bot API (HTTP POST)
| endpoint   | arguments | description |
| :---       |  :----  | :---       |
| /api/1.1/add_agent | JSON object containing system information | Endpoint that allows a bot to register itself to the server |
| /api/1.1/get_command | JSON object containing "id" |Endpoint for the bot to receive commands from the server |
| /api/1.1/command_out | JSON object containing "implantID", "commandID", "output" | Endpoint for the bot to send the output of commands back to the server |
| /api/1.1/ssh_keys | JSON object containing SSH keys | Endpoint for the bot to send exfiltrated SSH keys back to the server |
| /out | JSON data {"command":command, "output":output} |Endpoint for receiving command output and writing it to DB|

## Authentication API (HTTP POST)
| endpoint   | arguments | description |
| :---       |  :----  | :---       |
| /login | email, password | Attempts to authenticate a user with the supplied credentials|
| /logout | N/A | Pops the session and logs the user out |
| /signup | email, username, password | Create an account with the given email, username, and password (case sensitive) |
