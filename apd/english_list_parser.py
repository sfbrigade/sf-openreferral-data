import re

class EnglishListParser:
    @classmethod
    def strip(self, string):
        string = re.sub(r'\. *$', '', string)
        return str.strip(string)

    @classmethod
    def parse_list(self, list_string):
        split_list = list_string \
                .replace(" or ", " and ") \
                .replace(" & ", " and ") \
                .replace(", and ", " and ") \
                .replace(" and ", ",") \
                .split(",")

        return map(self.strip, split_list)
