class FailedAttribute:
    def __init__(self, object_label, attribute_label, error, data):
        self.object_label = object_label
        self.attribute_label = attribute_label
        self.error = error
        self.data = data
