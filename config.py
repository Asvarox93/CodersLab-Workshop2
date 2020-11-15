from configparser import SafeConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = SafeConfigParser()
    parser.read(filename)


    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in {filename} file')

    return db

if __name__ == '__main__':
    config()
