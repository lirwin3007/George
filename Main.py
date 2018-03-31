import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

print config.get('motors', 'A_L_ELBOW')
