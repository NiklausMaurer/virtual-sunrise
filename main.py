from sunrise.settings import get_settings
from sunrise.sunrise import Sunrise

if __name__ == '__main__':
    settings = get_settings()
    sunrise = Sunrise(settings)
    sunrise.run()
