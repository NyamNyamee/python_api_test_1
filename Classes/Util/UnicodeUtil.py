import unicodedata


class UnicodeUtil:
    @staticmethod
    def fill_str_with_space(string='', max_size=30, fill_char=' '):
        """
        - 길이가 긴 문자는 2칸으로 체크하고, 짧으면 1칸으로 체크함.
        - 최대 길이(max_size)는 40이며, string의 실제 길이가 이보다 짧으면
        남은 문자를 fill_char로 채운다.
        """
        letter_lenght = 0
        for char in string:
            if unicodedata.east_asian_width(char) in ['F', 'W']:
                letter_lenght += 2
            else:
                letter_lenght += 1

        # print(string + '의 길이: ' + str(letter_lenght))
        return string + fill_char * round(max_size - letter_lenght)
