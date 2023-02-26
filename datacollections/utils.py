import petl


class InspectData(object):

    def read_table_from_csv(self, path):
        return petl.fromcsv(path)

    def get_data(self, dataset):
        table = self.read_table_from_csv(dataset.file_path)
        return petl.data(table)

    def get_headers(self, dataset):
        table = self.read_table_from_csv(dataset.file_path)
        return petl.fieldnames(table)

    def inspect_dataset(self, dataset):
        table = petl.fromcsv(dataset.file_path)
        table_headers = petl.fieldnames(table)
