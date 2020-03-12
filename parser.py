class Parser:
    def __init__(self, urls):
        self.urls = urls


    attrs_list = []

    def remove_symbols(self, string):
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',']

        for letter in string:
            if letter not in digits:
                string = string.replace(letter, "")

        # print(string)

        string = string.replace('.', ',')
        # print(string)
        position = string.find(',')
        # print(position)
        string = string[0:3]

        if string[-1] in [',', '.']:
            string = string[0:-1]
        # print(string)

        return string

    def scrap_catalog(self):
        pass

