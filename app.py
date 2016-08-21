#!/usr/bin/env python3
"""
This module implements a contact book application with two functionalites
i.e Add Contact and Search Contact.
A Contact can have name i.e first_name and last_name.
Trie is used to implement a contact book application.
The module is consist of Trie class and few other functions.

Example:
    This module require Python3.4 to run. To execute this program run following
    command on terminal ::
    $ python3 app.py

Author : Rajat Mhetre
"""
import traceback
import logging

class Trie:
    """
        Trie class
        Inserts and search for string in trie
        Note:
            Do not include the `self` parameter in the ``Args`` section.
    """

    def __init__(self):
        """ Initialise trie """
        self.root = {}

    def add(self, name):
        """
            Adds a name to the Trie
            Args:
                name (str): Name of the contact.
        """

        # no need to add first_name while adding full_name
        name_list = name.strip().split()[1:]
        name_list.append(name)
        for item in set(name_list):
            node = self.root
            # check for every char in word, i.e. check whether is it in trie
            # if yes, then move forward over that path
            # else, add node with given char
            for char in item.lower():
                if char not in node:
                    node[char] = {}
                node = node[char]

            if "NAME" in node:
                node["NAME"].append(name)
            else:
                node["NAME"] = [name]

    def find(self, prefix):
        """
            Returns node after searching for given prefix
            Args:
                prefix (str): Prefix / Query String
        """
        node = self.root
        for char in prefix:
            if char not in node.keys():
                return None
            node = node[char]

        return node

    def list_contacts(self, prefix):
        """
            Search for contacts with given prefix
            Args:
                prefix (str): Prefix / Query String
        """
        sub_trie = self.find(prefix.lower())
        _crawl_trie(sub_trie, prefix)

result = [] # Contains list of names find for particular searched query
def _crawl_trie(subtrie, prefix):
    """
        Search for prefix in subtrie recursively.
        If prefix is found, then it simply inserts contact's name into result list.
    """
    for key in subtrie.keys():
        if key == "NAME":
            result.extend(subtrie.get(key))
        else:
            _crawl_trie(subtrie[key], prefix + key)


def add_contact(trie, name):
    """
        Adds contact into trie
        Args:
                name (str): Name of the contact
                trie (Trie) : Instance of Trie class
        Returns:
            True if name is added into trie, else False
    """
    if len(name) > 50:
        print("Name cannot be more than 50 characters.")
        return False
    elif not ("".join(name.split())).isalpha():
        print("Name can have letters only.")
        return False
    else:
        trie.add(name)
        return True


def search(trie, query):
    """
        Search for query in trie
        Args:
            query (str): Query given by user
            trie (Trie) : Instance of Trie class
        Returns:
            If found, then prints results else prints Not Found.
    """
    try:
        trie.list_contacts(query)
        for value, _ in distance_words(result, query):
            print(value)
    except Exception:
        logging.debug(traceback.format_exc())
        print("Not Found!")


def exit_program():
    """
        Exits from program and prints good bye message.
    """
    print("Good Bye! Happy Searching...")


def distance_words(result, query):
    """
        Calculate distance between two strings
        Algorithm : Levenshtein distance
        Lower distance means higher order in result
        Args :
            result (list) : List of names found by search function
            query (str) : Query asked by user
        Returns:
            Dictionary with word as key and distance as value,
            which is sorted by value in ascending order.
    """
    distance_dict = {}
    # for each word in result find distance between that word and query word
    # i.e. number of insert/update/delete operations required to change query word to result word
    # smallest distance means closest word to query, therefore it will be
    # shown at the top
    for word in result:
        distances = list(range(len(query) + 1))
        for index_word, char_word in enumerate(word):
            another_distances = [index_word + 1]
            for index_query, char_query in enumerate(query):
                if char_query == char_word:
                    another_distances.append(distances[index_query])
                else:
                    another_distances.append(1 + min((distances[index_query],
                                                      distances[
                                                          index_query + 1],
                                                      another_distances[-1])))
            distances = another_distances
        distance_dict.update({word: distances[-1]})
    # sort dict by value in ascending order ( smaller to larger distance )
    return sorted(distance_dict.items(), key=lambda x: x[1])


def main():
    """
        Main Function : Implements Program Flow
    """
    trie = Trie()  # Create new trie
    while True:
        try:
            control_query = int(input("1) Add Contact    2) Search    3) Exit \n"))
            if control_query == 3:
                exit_program()
                break
            elif control_query == 2:
                parameter_query = input("Type query :").strip()
                search(trie, parameter_query)
                del result[:]  # clear result list data after every search
            elif control_query == 1:
                parameter_name = input("Enter Name :").strip()
                add_contact(trie, parameter_name)
            else:
                print("Please provide valid number. [1, 2 or 3]")
        except ValueError:
            print("Please provide valid number. [1, 2 or 3]")
        except Exception:
            logging.debug(traceback.format_exc())
            print("Invalid operation performed. Please try again.")


if __name__ == '__main__':
    main()
