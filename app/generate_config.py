import os
import configparser

def generate_config():
    config = configparser.ConfigParser()
    
    # Секция DEFAULT
    config['DEFAULT'] = {
        'image_directory': os.getenv('IMAGE_DIRECTORY', './images'),
        'upload_dir': os.getenv('UPLOAD_DIR', 'uploads')
    }
    
    # Секция Superset
    config['Superset'] = {
        'host': os.getenv('SUPERSET_HOST', 'localhost'),
        'port': os.getenv('SUPERSET_PORT', '8088'),
        'username': os.getenv('SUPERSET_USERNAME', 'AIPlotter'),
        'password': os.getenv('SUPERSET_PASSWORD', 'secret123'),
        "object_expire_time":os.getenv('OBJECT_EXPIRE_TIME',10080),
        'clean_time':os.getenv("CLEAN_TIME",1200)
    }
    
    # Записываем конфиг
    with open('/app/config.ini', 'w') as configfile:
        config.write(configfile)
    
    print("Config file generated successfully")

if __name__ == "__main__":
    generate_config()