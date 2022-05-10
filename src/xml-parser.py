from xml.dom.minidom import Element
import xml.etree.ElementTree as ET


class XMLParser:
    def __init__(self, file_path: str):
        with open(file_path, "rb") as file:
            self.xmlTree = ET.parse(file)

    def get_root(self) -> Element:
        return self.xmlTree.getroot()
