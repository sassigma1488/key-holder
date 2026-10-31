
class Manager:

    def __init__(self, file_path):
        self.file_path = file_path
        self.passwords = self.load()

    def load(self):
        data = []
        try:
            with open(self.file_path) as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('/')
                    if len(parts) == 3:
                        data.append({
                            'service': parts[0],
                            'login': parts[1],
                            'password': parts[2]
                        })
        except FileNotFoundError:
            pass
        return data

    def save(self):
        with open(self.file_path, 'w') as file:
            for item in self.passwords:
                line = f"{item['service']}/{item['login']}/{item['password']}\n"
                file.write(line)

    def add(self, service, login, password):
        self.passwords.append({'service': service, 'login': login, 'password': password})
        self.save()
        print('zapisь added')

    def find(self, service):
        result = []
        for item in self.passwords:
            if item['service'] == service:
                result.append(item)
        return result

class App:

    def __init__(self, manager):
        self.manager = manager

    def run(self):
        while True:
            print('\nMenu:')
            print('  1 - Dobavit porol')
            print('  2 - find polol')
            print('  3 - pokazat vse paroli')
            print('  4 - vыйti')

            choice = input('chto delat?  ')

            if choice == '1':
                self.add_password()
            elif choice == '2':
                self.find_password()
            elif choice == '3':
                self.show_all()
            elif choice == '4':
                print('bye')
                break
            else:
                print('takogo punkta net')

    def add_password(self):
        service = input('Vvedite service:  ')
        login = input('Vvedite login:  ')
        password = input('Vvedite porol:  ')
        self.manager.add(service, login, password)

    def find_password(self):
        service = input('ot kakogo service vash porol:  ')
        found = self.manager.find(service)
        if not found:
            print('nott found')
        for item in found:
            print(item['login'], ':', item['password'])

    def show_all(self):
        if not self.manager.passwords:
            print('spisok pustoi')
        for item in self.manager.passwords:
            print(item['service'], '/', item['login'], '/', item['password'])


if __name__ == '__main__':
    manager = Manager('lol')
    app = App(manager)
    app.run()