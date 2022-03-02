class Gene:

    def __init__(self,
                 symbol: str = None,
                 protein_name: str = None,
                 has_edges_to: list[str] = None,
                 uniprot_ac: str = None,
                 entrez: str = None,
                 ensg: list[str] = None):
        self.__symbol = symbol
        self.__protein_name = protein_name
        self.__uniprot_ac = uniprot_ac
        self.__entrez = entrez
        self.__ensg = ensg
        if has_edges_to is None:
            self.__has_edges_to = []
        else: self.__has_edges_to = has_edges_to

    def to_dict(self):
        return {
            self.__symbol: {
                "symbol": self.__symbol,
                "protein_name": self.__protein_name,
                "uniprot_ac": self.__uniprot_ac,
                "entrez": self.__entrez,
                "ensg": self.__ensg,
                "is_seed": False,
                "has_edges_to": self.__has_edges_to
            }
        }
