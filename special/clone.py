from decoration import Decoration
from attribute.clonebay import CloneBay

class ClonePod(Decoration):
    def __init__(self):
        Decoration.__init__(self, 'Clone Pod', 'a cloning pod',
            'The cloning pod sits quietly in the corner, a multitude of '
            'small objects floating inside, ready to spring into action '
            'should a replacement be needed.', ['pod', 'clone pod'],
            [CloneBay()])
