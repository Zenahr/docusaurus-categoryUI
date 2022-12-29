"""NOTES
folders: contain _category_.json file. "position".
top-level md or mdx files: contain "sidebar_position" in frontmatter.
md or mdx files inside folders: contain "sidebar_position" in frontmatter.

Things to check for:

- No duplicate position value
- No duplicate sidebar_position value ()

Features (in order of priority):

- support _category_.json (category folders)
  - show category folders as JSON
  - show category folders in sidebar with their attributes as a tree
  - change position property via drag and drop
  - allow instant renaming
"""

import json
from typing import List
from glob import glob
from flask import Flask, jsonify

app = Flask(__name__)

class Category:
    def __init__(self, path):
        self.path = path
        self.json = self.get_json()
        self.title = self.get_title()
        self.position = self.get_position()

    def get_json(self):
        """Returns the JSON object of the category folder."""
        # if type(self.path) == str:
        with open(self.path, 'r') as f:
                    return json.load(f)
        # if type(self.path) == Category:
        #     raise TypeError('Path must be a string.')
        
    def get_title(self):
        """Returns the title of the category folder."""
        return self.json['label']

    def get_position(self):
        """Returns the position of the category folder."""
        return self.json['position']

    def set_position(self, position): # NOTE: NOT TESTED, can be optimized
        """Sets the position of the category folder. Check for duplicates first, if any, swap positions."""
        self.json['position'] = position
        # if(self.is_position_duplicate()[0]):
        #     self.swap_positions(self.is_position_duplicate()[1])
        with open(self.path, 'w') as f:
            json.dump(self.json, f, indent=2)

    def swap_positions(self, position): # NOTE: NOT TESTED, can be optimized
        """Swaps the position of the category folder with the category folder with the same position."""
        file_manager = FileManager(r'website\docs')
        categories = file_manager.get_top_level_sidebar_categories()
        for category in categories:
            if Category(category).position == position:
                category_to_swap = Category(category)
                category_to_swap.set_position(self.position)
                break

    def is_position_duplicate(self): # NOTE: NOT TESTED
        """Checks if there are any duplicate position values in the docs folder. Returns a tuple of (True, position) if there is a duplicate, else (False, None)."""
        file_manager = FileManager(r'website\docs')
        categories = file_manager.get_top_level_sidebar_categories()
        positions = [Category(category).position for category in categories]
        for position in positions:
            if position == self.position:
                return True, position
        return False

    def __repr__(self):
        return f'Category({self.title}, {self.position})'

class FileManager:
    """Class handling updates and read operations on docusaurus docs files and folders."""

    def __init__(self, docs_path):
        self.docs_path = docs_path # Path to docs folder

    def get_docs(self):
        """Returns a list of all docs files (.md, .mdx extensions only) and folders."""
        docs_files = glob(self.docs_path + '/**/*.md', recursive=True)
        docs_folders = glob(self.docs_path + '/**/_category_.json', recursive=True)
        return docs_files + docs_folders

    def get_top_level_sidebar_categories(self) -> List[Category]:
        """Returns a list of paths to all _category_.json files."""
        category_paths = glob(self.docs_path + '/**/_category_.json', recursive=True)
        categories = [Category(path) for path in category_paths]
        categories.sort(key=lambda category: category.position)
        return categories

@app.get('/')
def api():
    all_categories = FileManager(r'website\docs').get_top_level_sidebar_categories()
    categories_as_json = [category.json for category in all_categories]
    return jsonify(categories_as_json)

if __name__ == '__main__':
    # all_categories = FileManager(r'website\docs').get_top_level_sidebar_categories()
    # category = all_categories[0]
    # category.set_position(11)
    # all_categories = FileManager(r'website\docs').get_top_level_sidebar_categories()
    # print(all_categories)
    app.run(debug=True)