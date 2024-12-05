def command_resolve(user_input: str)->str:
    if(user_input[0]=='!'):
        if(user_input=="!ping"):
            return "Pong"
        return "Invalid command"