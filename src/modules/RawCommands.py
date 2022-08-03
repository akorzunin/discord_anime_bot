from datetime import datetime

class RawCommands:
    async def ping_command(self,) -> str:
        time_to_response = round(self.bot.latency * 1000)
        return f'{datetime.now()} ping: {time_to_response}ms'
    
    async def uptime_command(self,) -> str:
        u = datetime.now() - self.start_time
        upt = u.seconds
        days = upt//(60*60*24) # dddd
        hours = upt//(60*60) - days*24 # hh
        minutes = upt//(60) - hours*60 - days*24*60# mm
        seconds = upt - minutes*60 - hours*60*60 - days*60*60*24 #ss
        return f'uptime: {days}:{hours}:{minutes}:{seconds}'
    
