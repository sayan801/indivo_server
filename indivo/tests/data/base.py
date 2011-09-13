import hashlib

class TestXMLDoc(object):
    def __init__(self, xml, label='testing'):
        self.xml = xml
        self._len = None
        self._digest = None
        self.label = label

    def size(self):
        if not self._len:
            self._len = len(self.xml)
        return self._len

    def digest(self):
        if not self._digest:
            md = hashlib.sha256()
            md.update(self.xml)
            self._digest = md.hexdigest()
        return self._digest

class TestModel(object):
    model_fields = [] # A list of field names needed to construct a Django Model
    model_class = None # The Django Model Subclass to construct

    def __init__(self):
        raise NotImplementedError("TestModel is a virtual class: subclass me!")

    def __setattr__(self, item, value):
        """Update our django_object whenever our fields get updated"""
        if hasattr(self, 'django_obj') and self.django_obj:
            setattr(self.django_obj, item, value)
        return super(TestModel, self).__setattr__(item, value)

    def build_django_obj(self):
        model_args = {}
        for f in self.model_fields:
            if hasattr(self, f):
                model_args[f] = getattr(self, f)
        self.django_obj = self.model_class(**model_args)

    def save(self):
        if not hasattr(self, 'django_obj') or not self.django_obj:
            self.build_django_obj()
        self.django_obj.save()

def raw_data_to_objs(data_list, target_object):
    return [target_object(**raw_data) for raw_data in data_list]
