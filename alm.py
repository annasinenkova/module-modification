from element import Element

class ALM:
    n = 9
    N = 16
    outputs = [4, 6, 7, 8, 12]
    elements = [
        Element("LUT", 4, [19, 20, 21, 22], False, []          ),
        Element("LUT", 4, [19, 20, 21, 22], False, []          ),
        Element("LUT", 4, [19, 20, 23, 24], False, []          ),
        Element("LUT", 4, [19, 20, 23, 24], False, []          ),
        Element("MUX", 3, [0, 1, 16]      , True , [4, 7]      ),
        Element("MUX", 3, [2, 3, 16]      , False, [5, 7]      ),
        Element("MUX", 3, [2, 3, 17]      , True , [6]         ),
        Element("MUX", 3, [4, 5, 17]      , True , [7]         ),
        Element("XOR", 2, [18, 0]         , True , [8]         ),
        Element("MUX", 3, [18, 1, 0]      , False, [9, 12]     ),
        Element("AND", 2, [0, 2]          , False, [10, 14]    ),
        Element("AND", 2, [1, 2]          , False, [11, 13, 14]),
        Element("XOR", 2, [9, 2]          , True , [12]        ),
        Element("OR" , 2, [11, 3]         , False, [13, 14]    ),
        Element("MUX", 3, [18, 13, 10]    , True , [14]        ),
        Element("UNDEFINED", 2,[]         , False, [15]        )
    ]

