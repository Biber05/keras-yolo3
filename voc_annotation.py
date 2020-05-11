import logging
import os
import xml.etree.ElementTree as ET

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog",
           "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor", "ball"]


class VocConverter(object):
    def __init__(self, data_dir: str, precision: int = 10, debug_mode=False):
        self.precision = precision
        self.sets = self._get_sets(data_dir)
        self.LOGGER = logging.getLogger(__name__)
        self.LOGGER.setLevel(logging.INFO) if debug_mode else self.LOGGER.setLevel(logging.ERROR)
        self.LOGGER.debug("Sets: {}".format(self.sets))

    def _get_sets(self, folder: str) -> list:
        dirs = os.listdir(folder)
        return list(filter(lambda x: os.path.isdir(x), map(lambda y: os.path.join(folder, y), dirs)))

    def _convert_annotation(self, annotation_dir: str, image_id) -> str:
        in_file = open(os.path.join(annotation_dir, "{}.xml".format(image_id)))
        tree = ET.parse(in_file)
        root = tree.getroot()

        objects = ""
        for obj in root.iter('object'):
            cls = obj.find('name').text

            cls_id = classes.index(cls)

            xmlbox = obj.find('bndbox')

            try:
                b = (float(xmlbox.find('xmin').text),
                     float(xmlbox.find('ymin').text),
                     float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymax').text))

                objects += " " + ",".join([str(a) for a in b]) + ',' + str(cls_id)
            except ValueError as e:
                print("{} - Error reading parse int on annotation {} ".format(e, image_id))

        return objects

    def _get_ids(self, path) -> [str]:
        files = os.listdir(path)
        return list(map(lambda y: y[:-4], filter(lambda x: "xml" in x, files)))

    def convert(self):
        for path in self.sets:
            annotation_dir = os.path.join(path, "Annotations")
            image_dir = os.path.join(path, "JPEGImages")

            image_ids = self._get_ids(annotation_dir)
            self.LOGGER.debug("Found {} files".format(len(image_ids)))
            list_file = open(os.path.join(path, 'annotations.txt'), 'w')

            for i, image_id in enumerate(image_ids):
                list_file.write(os.path.join(image_dir, "{}.jpg".format(image_id)))
                annotation = self._convert_annotation(annotation_dir, image_id)
                list_file.write(annotation + "\n")
                self.LOGGER.debug("{}/{} ".format(i, len(image_ids)))
            list_file.close()


if __name__ == '__main__':
    VocConverter("/Users/philipp/Git/master/pbp-recommendation/SHARE/data_tracking/own", True).convert()
