import configparser


class Config():

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')

    def get_weekly_limit(self):
        return int(self.config['MONEY']['WEEKLY_LIMIT'])
    
    def get_daily_limit(self):
        return int(self.config['MONEY']['DAILY_LIMIT'])