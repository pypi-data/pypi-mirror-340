import base64
import os
import textwrap

import yaml
from PyQt5.QtCore import QObject, pyqtSignal

from easyconfig2.easydialog import EasyDialog
from easyconfig2.easynodes import Root, EasySubsection, EasyPrivateNode, EasyNode
from easyconfig2.easytree import EasyTree


class EasyConfig2(QObject):
    edited = pyqtSignal()

    def __init__(self, **kwargs):
        super().__init__()
        self.section_name = kwargs.pop("name", None)
        self.globally_encoded = kwargs.pop("encoded", False)
        self.filename = kwargs.pop("filename", None)
        self.easyconfig_private = {}
        self.tree = None
        self.dependencies = {}
        self.root_node = Root(self, **kwargs)
        self.private = self.root_node.add_child(EasySubsection("easyconfig", hidden=True))
        self.collapsed = self.private.add_child(EasyPrivateNode("collapsed", default=""))
        self.hidden = self.private.add_child(EasyPrivateNode("hidden", default=None, save_if_none=False))
        self.disabled = self.private.add_child(EasyPrivateNode("disabled", default=None, save_if_none=False))
        self.whole_file = None
        self.loaded_values = {}

    def root(self):
        return self.root_node

    def add(self, node):
        self.root_node.add_child(node)
        return node

    def transform_dict(self, d):
        new_dict = {}
        for key, value in d.items():
            if ":" in key:
                main_key, suffix = key.split(":", 1)
            else:
                main_key, suffix = key, None

            if isinstance(value, dict):
                new_dict[main_key] = (self.transform_dict(value), suffix)
            else:
                new_dict[main_key] = (value, suffix)

        return new_dict

    def create_dictionary(self, node, values=None):
        # create a dictionary to store the values traversing the tree

        if values is None:
            values = {}
        # iterate over the children of the node
        for child in node.get_children():
            # if the child is a subsection, traverse it
            if isinstance(child, EasySubsection):
                if child.is_savable():
                    new_dict = {}
                    self.create_dictionary(child, new_dict)
                    values[child.get_key()] = new_dict
            else:
                # if the child is a TextLine, store the value in the dictionary
                if child.is_savable():
                    if child.get() is not None or child.is_savable_if_none():
                        if child.is_base64() and child.get() is not None:
                            # Encode in base64 if required
                            # NOTE: we use yaml to dump the value to ensure that
                            # the value is stored according to the type it has and
                            # to take into account that might be a list or a dict
                            encoded = base64.b64encode(yaml.dump(child.get()).encode()).decode()
                            encoded = " ".join(textwrap.wrap(encoded, 80))
                            values[child.get_key()] = encoded
                        else:
                            values[child.get_key()] = child.get()

    def get_dictionary(self):
        values = {}
        self.create_dictionary(self.root_node, values)
        return values

    def load(self, filename=None, emit=False):
        filename = filename or self.filename
        if not os.path.exists(filename):
            return

        with open(filename, "r") as f:
            string = f.read()
            if self.section_name is None and not self.globally_encoded:
                self.loaded_values = yaml.safe_load(string)

            elif self.section_name is None and self.globally_encoded:
                string = base64.b64decode(string).decode()
                self.loaded_values = yaml.safe_load(string)

            elif not self.globally_encoded:

                # The section name is NOT None
                # and globally encoded is False
                data = yaml.safe_load(string)
                self.loaded_values = data.get(self.section_name, {})
            else:

                # Section name is NOT None and globally encoded is True
                data = yaml.safe_load(string)
                string = data.get(self.section_name, None)
                if string is not None:
                    string = base64.b64decode(string).decode()
                    self.loaded_values = yaml.safe_load(string)
                else:
                    self.loaded_values = {}

            self.parse_dictionary_into_node(self.loaded_values, self.root_node, emit)

            for key in self.hidden.get([]):
                self.root_node.get_node(key).set_hidden(True)

    def parse(self, dictionary):
        self.parse_dictionary_into_node(dictionary, self.root_node)

    def populate(self, node: EasyNode):
        if not isinstance(node, EasySubsection):
            raise ValueError("Node must be a subsection")
        if node not in self.root_node.get_children():
            print(self.root_node.get_children())
            raise ValueError("Node is not a child of the root node")

        dictionary = self.loaded_values.get(node.get_key(), None)

        if dictionary is not None:
            self.parse_dictionary_into_node(dictionary, node)

    def save(self, filename=None):
        filename = filename or self.filename
        if filename is None:
            raise ValueError("Filename not provided")
        values = self.get_dictionary()

        if self.section_name is None:
            # Apply the new values to the loaded values
            # and save them to the *exclusive* file (section_name is None)
            self.loaded_values.update(values)
            if not self.globally_encoded:
                string = yaml.dump(self.loaded_values)
            else:
                string = base64.b64encode(yaml.dump(self.loaded_values).encode()).decode()

            with open(filename, "w") as f:
                f.write(string)
        else:
            # Section name is NOT None
            data = {}
            if os.path.exists(filename):
                # We reload the file to get updated values
                with open(filename, "r") as f:
                    data = yaml.safe_load(f)

            if not self.globally_encoded:
                data[self.section_name] = values
            else:
                data[self.section_name] = base64.b64encode(yaml.dump(values).encode()).decode()

            with open(filename, "w") as f:
                yaml.dump(data, f)

    def edit(self, min_width=None, min_height=None, parent=None):
        dialog = EasyDialog(EasyTree(self.root_node, self.dependencies), parent=parent)
        if min_width is not None:
            dialog.setMinimumWidth(min_width)
        if min_height is not None:
            dialog.setMinimumHeight(min_height)

        dialog.set_collapsed(self.collapsed.get())
        if dialog.exec():
            dialog.collect_widget_values()
            self.collapsed.set(dialog.get_collapsed())
            self.edited.emit()
            return True
        return False

    def parse_dictionary_into_node(self, dictionary, root_node, emit=False):

        def parse_recursive(node, values):
            for child in node.get_children():
                if isinstance(child, EasySubsection):
                    inner_dict = values.get(child.get_key(), {})
                    parse_recursive(child, inner_dict)
                else:
                    value = values.get(child.get_key(), child.value)
                    # Decode base64 if needed
                    if child.is_base64() and value is not None:
                        print("value", value)
                        value = value.replace(" ", "")
                        value = yaml.safe_load(base64.b64decode(value))

                    # TODO: Decision made here
                    # In this way the widgets, if visible, are not updated
                    if not emit and False:
                        child.value = value
                    else:
                        child.set(value)

        parse_recursive(root_node, dictionary)

    def add_dependencies(self, dependencies):
        for dep in dependencies:
            self.add_dependency(dep)

    def add_dependency(self, dep):
        if self.dependencies.get(dep.master, None) is None:
            self.dependencies[dep.master] = []
        self.dependencies[dep.master].append(dep)
