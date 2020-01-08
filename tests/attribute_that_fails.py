def make_attributes_with_value_0_fail(*args):
    # 3rd arg is the data (value of the attribute)
    attribute_value = args[2]
    if attribute_value == 0:
        raise ValueError("This attribute is supposed to fail for testing purposes")
