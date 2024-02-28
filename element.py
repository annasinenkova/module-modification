class Element:
    def __init__(self, elem_type, inputs_num, inputs, output, next):
        self.elem_type = elem_type
        self.inputs_num = inputs_num
        self.inputs = inputs
        self.output = output
        self.next = next

