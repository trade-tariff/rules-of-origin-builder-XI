import os
import json

from classes.classic_roo import ClassicRoo


class ClassicRooFolder(object):
    def __init__(self, country_code, scheme_code):
        print("Processing data for {country_code} ({scheme_code})".format(country_code=country_code, scheme_code=scheme_code))
        self.country_code = country_code
        self.scheme_code = scheme_code
        self.rule_sets = []

    def get_json_path(self):
        self.json_path = os.getcwd()
        self.json_path = os.path.join(self.json_path, "resources", "json", self.country_code)
        a = 1

    def process_roo_classic(self):
        self.make_export_folder()
        self.get_jason_strategic_filename()
        self.get_json_path()
        self.get_json_files()
        self.process_files()
        self.write_json_data()

    def process_files(self):
        valid = ["85"]
        valid = []
        for json_file in self.json_files:
            if len(valid) == 0:
                rule_sets = self.process_file(json_file)
                if rule_sets is not None:
                    self.rule_sets += rule_sets
            else:
                tmp = json_file.replace(".json", "").replace("chapter_", "")
                if tmp in valid:
                    rule_sets = self.process_file(json_file)
                    if rule_sets is not None:
                        self.rule_sets += rule_sets

    def process_file(self, json_file):
        subheading = json_file.replace(".json", "")
        json_file_path = os.path.join(self.json_path, json_file)
        f = open(json_file_path)
        data_json = json.load(f)
        classic_roo = ClassicRoo(data_json, subheading, self.country_code, self.scheme_code)
        self.rule_sets += classic_roo.rules_json
        f.close()

    def make_export_folder(self):
        self.json_strategic_folder = os.getcwd()
        self.json_strategic_folder = os.path.join(self.json_strategic_folder, "resources")
        self.json_strategic_folder = os.path.join(self.json_strategic_folder, "json_strategic")
        if not os.path.isdir(self.json_strategic_folder):
            os.mkdir(self.json_strategic_folder)

    def get_jason_strategic_filename(self):
        self.json_strategic_filename = os.path.join(self.json_strategic_folder, self.scheme_code + ".json")

    def write_json_data(self):
        data = {
            "rule_sets": self.rule_sets
        }
        f = open(self.json_strategic_filename, "w")
        json.dump(data, f, indent=4)
        f.close()

    def get_json_files(self):
        self.json_files = []
        files = os.listdir(self.json_path)
        for file in files:
            if ".json" in file:
                self.json_files.append(file)
        self.json_files.sort()
