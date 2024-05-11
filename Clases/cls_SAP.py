from Clases.cls_Paquete import clsPaquete, enumTransaccion


class clsSAP(clsPaquete):

    def __init__(self, booStart: bool, LayOutSAP: str):

        self.booStartSAP: bool = booStart
        self.LayOutSAP: str = LayOutSAP

        match self.eTransaccion:
            case enumTransaccion.eZARPM_CERT_NOTIF:
                self.LayOutSAP = "ZARPM_CERT_NOTIF"
            case enumTransaccion.eEKKO:
                self.LayOutSAP = "E"
            case _:
                self.LayOutSAP = ""

    def CJI3(self, session: object, booStart: bool):

        if booStart:
            session.StartTransaction("CJI3")

            if session.Info.ScreenNumber == 600:
                session.FindById("wnd[1]/usr/ctxtTCNT-PROF_DB").Text = "000000000001"
                session.FindById("wnd[1]/tbar[0]/btn[0]").Press()

            session.FindById("wnd[0]/usr/ctxtCN_PROJN-LOW").ShowContextMenu()
            session.FindById("wnd[0]/usr").SelectContextMenuItem = "DELACTX"
            session.FindById("wnd[0]/usr/ctxtCN_NETNR-LOW").ShowContextMenu()
            session.FindById("wnd[0]/usr").SelectContextMenuItem = "DELACTX"
            session.FindById("wnd[0]/usr/ctxtCN_ACTVT-LOW").ShowContextMenu()
            session.FindById("wnd[0]/usr").SelectContextMenuItem = "DELACTX"
            session.FindById("wnd[0]/usr/ctxtCN_MATNR-LOW").ShowContextMenu()
            session.FindById("wnd[0]/usr").SelectContextMenuItem = "DELACTX"
            session.FindById("wnd[0]/usr/ctxtR_KSTAR-LOW").ShowContextMenu()
            session.FindById("wnd[0]/usr").SelectContextMenuItem = "DELACTX"

            session.FindById("wnd[0]/usr/ctxtKOAGR").Text = ""

            session.FindById("wnd[0]/usr/btnBUT1").Press()
            session.FindById("wnd[1]/usr/txtKAEP_SETT-MAXSEL").Text = "9999999"
            session.FindById("wnd[1]/tbar[0]/btn[0]").Press()

            session.FindById("wnd[0]/usr/ctxtP_DISVAR").Text = self.LayOutSAP
            # Seleccionar PEPs
            session.FindById("wnd[0]/usr/ctxtCN_PSPNR-LOW").ShowContextMenu()
            session.FindById("wnd[0]/usr").SelectContextMenuItem = "DELACTX"
            session.FindById("wnd[0]/usr/btn%_CN_PSPNR_%_APP_%-VALU_PUSH").Press()
            session.FindById("wnd[1]/tbar[0]/btn[24]").Press()
            # Pegar todo
            session.FindById("wnd[1]/tbar[0]/btn[8]").Press()

        session.FindById("wnd[0]/usr/ctxtR_BUDAT-LOW").Text = self.datInicio.strptime("dd.mm.yyyy")
        session.FindById("wnd[0]/usr/ctxtR_BUDAT-HIGH").Text = self.datFin.strptime("dd.mm.yyyy")
