import run_script as a_system
help_string='''!ping - gives the status of the bot
!system_start - starts airio
!system_stop - stops airio, make sure you use !quit command on LFS server first just in case'''

def command_resolve(user_input: str,user: str,channel: str,elv_channel: str)->str:
    if(user_input[0]=='!'):
        if(channel!=elv_channel):
            if(user_input=="!ping"):
                return "Pong"
            else:
                return "Invalid command"
        else:
            match user_input:
                case "!system_start":
                    a_system.start_airio()
                    return "Starting the airio system..."
                case "!system_stop":
                    a_system.stop_airio()
                    return "Stopping the airio system..."
                case "!ping":
                    return "The bot is working properly. Pong."
                case "!help":
                    return help_string
                case _:
                    return "Invalid command"