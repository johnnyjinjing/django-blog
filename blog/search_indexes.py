from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    published = indexes.BooleanField(model_attr='published')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(published=True)