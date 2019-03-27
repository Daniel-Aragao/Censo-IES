import csv


class Importer:

    @staticmethod
    def import_csv(path, delimiter="|"):
        lines = []

        with open(path, encoding='iso-8859-14') as file_obj_control:
            reader = csv.DictReader(file_obj_control, delimiter=delimiter)

            for row in reader:
                lines.append(row)
        
        return lines



