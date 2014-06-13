from haystack import indexes
from base.models import MediaProperty, SubjectProperty

class MediaPropertyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return MediaProperty

class SubjectPropertyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return SubjectProperty