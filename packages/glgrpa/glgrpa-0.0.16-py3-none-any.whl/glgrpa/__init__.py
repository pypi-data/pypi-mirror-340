from .Chrome import Chrome
from .Windows import Windows
from .Terminal import Terminal
from .ARCA import ARCA
from .AplicativoCartasDePorteElectronicas import AplicativoCartaDePorteElectronica
from .Excel import Excel

class glgrpa:
    def __init__(self):
        self.Chrome = Chrome()
        self.Windows = Windows()
        self.Terminal = Terminal()
        self.ARCA = ARCA(usuario="", clave="")
        self.AplicativoCartaDePorteElectronica = AplicativoCartaDePorteElectronica(usuario="", clave="")
        self.Excel = Excel(ruta="")

__all__ = ["glgrpa"]
