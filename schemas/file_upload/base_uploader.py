from abc import ABC


class AbstractFileUploader(ABC):

    def upload(self, file, **options):
        raise NotImplementedError

    def delete(self, file, **options):
        raise NotImplementedError