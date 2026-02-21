class FindAndReplace:
    def __init__(self):
        self._source_folder = None
        self._word_replace = None
        self._word_find = None

    def find_and_replace(self, source_folder, word_find, word_replace):
        self._source_folder = source_folder
        self._word_find = word_find
        self._word_replace = word_replace
        print("Folder: " + self._source_folder + " Find: " + self._word_find + " And Replace: " + self._word_replace)