import re
import json
import os
import copy
import argparse



string_number_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                      "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                      "eleven": 11, "twelve": 12, "fifth": 5,
                      "sixteen": 16, "half": "50%"}


def delete_extra_zero(n):
    try:
        n=float(n)
    except:
        # print("None {}".format(n))
        return n
    if isinstance(n, int):
        return str(n)
    if isinstance(n, float):
        n = str(n).rstrip('0')  # Remove extra zeros after the decimal
        n = int(n.rstrip('.')) if n.endswith('.') else float(n)  # Reutrn int if only decimal point, otherwise float
        n=str(n)
        return n
    
    
class InverseQuestions:
    def __init__(self, args):

        self.output_clean_path = f"{self.input_path}-clean.json"
        self.output_path = f"{self.input_path}-backward.json"

        self.load_dataset()
        self.parse_examples()
        print(f"#samples: {len(self.input_examples)}")
        self.save_cleaned_data()

        self.unknown_var = "x"


    def replace_number_x(self, s):
        
        """
        Replaces a string representing a number with a placeholder variable.

        Args:
            s (str): The input string.

        Returns:
            str: The modified string with the number replaced by the placeholder variable.
        """

        if s in string_number_dict:
            s = str(string_number_dict[s])
        if s[-1] in (",", ".", "?", ";", "”", "'", "!", "\"", "%"):
            try:
                mo = re.match('.*([0-9])[^0-9]*$', s)
                return self.unknown_var + s[mo.end(1):]
            except:
                print(f"the string is {s}")
        elif s[0] in ("$"):
            return "$" + self.unknown_var
        else:
            return self.unknown_var


    def search_number(s):
        """
        Searches for numbers within a string.

        Args:
            s (str): The input string.

        Returns:
            bool or None: True if a number is found, False if not found, None if it's inconclusive.
        """
        if s in string_number_dict:
            return True
        if re.search('[\d]', s) is not None:
            if re.search('[a-zA-Z]', s) or re.search('[\\n:\(\)-*\"+-]', s):
                return None
            else:
                return True


    def make_inv_question(self):
        """
        Generates inverse questions from the input examples.

        This method generates inverse questions for examples containing numbers and stores them in the output_examples attribute.
        """

        self.output_examples = []
        num_example_has_backward_question = 0
        for e in self.input_examples:
            token_list = e['question'].split(' ')
            numbers_idx = [idx for idx, _ in enumerate(token_list) if self.search_number(_) is not None]
            if len(numbers_idx) > 0:
                num_example_has_backward_question += 1
                for x_idx in numbers_idx:
                    _e = copy.deepcopy(e) # create a copy of the forward questions
                    _token_list = copy.deepcopy(token_list)
                    inverse_question_answer = _token_list[x_idx]
                    _token_list[x_idx] = self.replace_number_x(_token_list[x_idx])
                    _e['inverse_question'] = " ".join(_token_list)
                    _e['inverse_question_answer'] = inverse_question_answer
                    self.output_examples.append(_e)
        print(f"has_inv_q: {num_example_has_backward_question}/{len(self.input_examples)}")

        self.save_data()


