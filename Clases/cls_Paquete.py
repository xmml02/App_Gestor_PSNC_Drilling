from datetime import datetime, date
from re import Match
from tkinter import messagebox
from dateutil.relativedelta import relativedelta
from enum import Enum
from Clases.cls_SAP import clsSAP
import os
import shutil


class enumUnidadTiempo(Enum):
    dia = 1
    mes = 2
    quarter = 3
    anio = 4


class enumTransaccion(Enum):
    eZARPM_CERT_NOTIF = 1
    eEKKO = 2
    eEKPO = 3
    eMSRV6 = 4
    ePA0001 = 5
    eESSR_REL = 6
    eZARMRST_IT9315_P = 7
    eZMRS0016 = 8
    eCJI3 = 9


class clsPaquete():
    status: str = ""
    strJob: str = ""
    strFile: str = ""
    strPath: str = ""
    booFileTXT: bool = False
    booFileTXTCopy: bool = False
    session: object
    Minutos: int = 0
    douSpool: int = 0

    class clsCamposSMX():
        def __init__(self, strJob: str, strStatus: str, strFecha: str, strHora: str, intMinutos: int, intPosX: int,
                     intPosY: int):
            self.strJob: str = strJob
            self.strStatus: str = strStatus
            self.strFecha: str = strFecha
            self.strHora: strHora
            self.intMinutos: int = intMinutos
            self.intPosX: int = intPosX
            self.intPosY: int = intPosY

    def __init__(self, session: object, eTransaccion: enumTransaccion, datInicio: date, datFin: date,
                 strTitle: str, objTransaccion: clsSAP, lngLineasProcFondo: int):
        self.eTransaccion: enumTransaccion = eTransaccion
        self.datInicio: date = datInicio
        self.datFin: date = datFin
        self.datEjecucion: datetime = datetime.now()
        self.session: object = session
        self.strTitle: str = strTitle
        self.sapTransaccion: clsSAP = objTransaccion
        self.lngLineasProcFondo: int = lngLineasProcFondo

    def Start_1(session: object, eTransaccion: enumTransaccion, colTransacciones: list, strTitle: str,
                lngLineasProcFondo: int,
                datInicio: date = 0, datFin: date = 0, eUnidadTiempo: enumUnidadTiempo = 1,
                sngUnidadTiempo: float = 0.0, LayOutSAP: str = '') -> list:

        objPaquete: clsPaquete
        objTransaccion: clsSAP
        # booPeriodo: bool
        booStart: bool = True

        arrayPeriodos = clsPaquete.__GenerarArrayPeriodos(datInicio, datFin, eUnidadTiempo, sngUnidadTiempo)

        for subPeriodo in arrayPeriodos:

            if strTitle == "":
                strTitle = eTransaccion.name[1:] + '_' + datInicio.strftime('%Y%mm%dd') + '_' + datFin.strftime(
                    '%Y%mm%dd')
            else:
                strTitle = eTransaccion.name[1:]

            objTransaccion = clsSAP(booStart, LayOutSAP)
            objPaquete = clsPaquete(session, eTransaccion, subPeriodo[0], subPeriodo[1], strTitle, objTransaccion,
                                    lngLineasProcFondo)

            colTransacciones.append(objPaquete)
            booStart = False

        return colTransacciones

    def __GenerarArrayPeriodos(self, datStart: date, datEnd: date, eUnidadTiempo: enumUnidadTiempo,
                               sngUnidadTiempo: float) -> list[tuple[date, date]]:

        arrayDat: list[tuple[date, date]] = []
        ajuste: relativedelta = relativedelta()

        datInicioSubPeriodo = datStart

        match eUnidadTiempo:
            case enumUnidadTiempo.dia:
                ajuste = relativedelta(days=sngUnidadTiempo)
            case enumUnidadTiempo.mes:
                ajuste = relativedelta(months=sngUnidadTiempo)
            case enumUnidadTiempo.quarter:
                ajuste = relativedelta(months=3 * sngUnidadTiempo)
            case enumUnidadTiempo.anio:
                ajuste = relativedelta(years=sngUnidadTiempo)

        i = 0
        while datEnd >= datInicioSubPeriodo:

            datInicioSubPeriodo = datStart + (ajuste * i)
            datFinSubPeriodo = datEnd + (ajuste * (i + 1)) - 1

            if datInicioSubPeriodo >= datEnd:
                datInicioSubPeriodo = datEnd

            if datFinSubPeriodo > datEnd:
                datFinSubPeriodo = datEnd

            arrayDat.append((datInicioSubPeriodo, datFinSubPeriodo))
            i += 1

        return arrayDat

    def booTry(self):

        match self.status:
            case "cancelado":
                return False
            case "terminado":
                if self.booFileTXT and not self.booFileTXTCopy:
                    return True
                else:
                    return False
            case "":
                return True

    def FinalizacionPaquetes(colPaquete: list) -> bool:

        objPaquete: clsPaquete

        for objPaquete in colPaquete:
            if objPaquete.booTry():
                continue
            else:
                return False

        return True

    def BucleSMX(colPaquete: list, session: object, strPath: str):

        objPaquete: clsPaquete

        for objPaquete in colPaquete:
            if objPaquete.booTry():
                pass

    def SMX(session: object, booStart: bool, strPath: str, colPaquete: list):

        def SMX_Filtrar(session: object, datDesde: datetime, datHasta: datetime):

            session.FindById("wnd[0]/usr/lbl[48,1]").SetFocus()
            session.FindById("wnd[0]").SendVKey(2)
            session.FindById("wnd[0]/usr/lbl[67,1]").SetFocus()
            session.FindById("wnd[0]").SendVKey(2)
            session.FindById("wnd[0]/usr/lbl[78,1]").SetFocus()
            session.FindById("wnd[0]").SendVKey(2)

            session.FindById("wnd[0]").SendVKey(38)
            # filtro
            session.FindById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN001-LOW").Text = "liberado"
            session.FindById("wnd[1]").SendVKey(2)
            session.FindById("wnd[2]/usr/cntlOPTION_CONTAINER/shellcont/shell").SetCurrentCell(5, "TEXT")
            session.FindById("wnd[2]/usr/cntlOPTION_CONTAINER/shellcont/shell").SelectedRows = "5"
            session.FindById("wnd[2]/usr/cntlOPTION_CONTAINER/shellcont/shell").DoubleClickCurrentCell()

            session.FindById(
                "wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN002-LOW").Text = datDesde.strftime(
                "dd.mm.yyyy")
            session.FindById(
                "wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN002-HIGH").Text = datHasta.strftime(
                "dd.mm.yyyy")

            session.FindById(
                "wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN003-LOW").Text = datDesde.strftime(
                "hh:nn:ss")
            session.FindById(
                "wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN003-HIGH").Text = datHasta.strftime(
                "hh:nn:ss")

            session.FindById("wnd[1]").SendVKey(0)

        def SMX_SelectorLayout(session: object, strLayout: str):

            session.FindById("wnd[0]/mbar/menu[4]/menu[0]/menu[1]").Select()

            for i in range(3, 11):
                if session.FindById(f"wnd[1]/usr/lbl[1,{i}]").Text == strLayout:
                    session.FindById(f"wnd[1]/usr/lbl[1,{i}]").SetFocus()
                    session.FindById("wnd[1]").SendVKey(2)
                    break

        def SMX_InstanciarRegScreen(session: object) -> list[clsPaquete.clsCamposSMX]:

            regCamposSMX: clsPaquete.clsCamposSMX
            listRegistros: list[clsPaquete.clsCamposSMX] = []
            lngPosSpool: int = 0
            lngPosStatus: int = 0
            lngPosJob: int = 0
            lngPosFecha: int = 0
            lngPosHora: int = 0
            lngPosMin: int = 0

            session.FindById("wnd[0]").SendVKey(8)
            for oComponent in session.children(0).children(4).children:
                strID: str = oComponent.ID

                temp = strID[strID.find(",") + 1: strID.find(",") + 11]
                lngLinea = temp[:-1]

                temp = strID[strID.find(",") - 4: strID.find(",") - 4 + 10]
                temp = temp[temp.find("[") + 1: temp.find("[") + 1 + 10]
                lngPosX = temp[:temp.find(",")]

                #  Ubicar a las posiciones de los campos
                if lngLinea == 1:
                    match oComponent.Text:
                        case "Lista SPOOL":
                            lngPosSpool = lngPosX
                        case "Status":
                            lngPosStatus = lngPosX
                        case "Nº job":
                            lngPosJob = lngPosX
                        case "Fe.inicio":
                            lngPosFecha = lngPosX
                        case "H.inicio":
                            lngPosHora = lngPosX
                        case "Duración(seg.)":
                            lngPosMin = lngPosX

                if oComponent.Type == 'GuiCheckBox':
                    listRegistros.append(
                        clsPaquete.clsCamposSMX(
                            strJob=session.FindById(f"wnd[0]/usr/lbl[{lngPosJob},{lngLinea}]").Text,
                            strStatus=session.FindById(f"wnd[0]/usr/lbl[1,{lngPosStatus}]").Text,
                            strFecha=session.FindById(f"wnd[0]/usr/lbl[1,{lngPosFecha}]").Text,
                            strHora=session.FindById(f"wnd[0]/usr/lbl[1,{lngPosHora}]").Text,
                            intMinutos=session.FindById(f"wnd[0]/usr/lbl[{lngPosMin},{lngLinea}]").Text / 60,
                            intPosX=int(lngPosX),
                            intPosY=int(lngLinea)
                        )
                    )
            return listRegistros

        def LecturaSPOOLPasos(session: object) -> str:

            session.FindById("wnd[0]/tbar[1]/btn[45]").Press()

            SMX_SelectorLayout(session, "/SMX_SPOOL")

            LecturaSPOOLPasos = session.children(0).children(4).children(1).Text
            session.FindById("wnd[0]").SendVKey(3)
            return LecturaSPOOLPasos

        def DownloadFileSP02(session: object, strPath: str, colPaquete: list) -> str:

            def CopiarPaquete(carpetaDestino, strTitle, strPathTXT):
                try:
                    archivo_destino = os.path.join(carpetaDestino, strTitle + ".txt")

                    # Si el archivo de destino ya existe, eliminarlo
                    if os.path.exists(archivo_destino):
                        os.remove(archivo_destino)

                    # Copiar el archivo
                    shutil.copy2(strPathTXT, archivo_destino)

                    # Eliminar el archivo original
                    os.remove(strPathTXT)

                    return True
                except Exception as e:
                    print(str(e))
                    print("Atención: Archivo no copiado")
                    return False

            objPaquete: clsPaquete

            strFecha = session.FindById("wnd[0]/usr/lbl[19,3]").Text
            strHora = session.FindById("wnd[0]/usr/lbl[30,3]").Text
            datTemp: datetime = datetime(strFecha[:-4], strFecha[4:5], strFecha[:1], strHora[:1], strHora[:-2], 0)
            datTemp = datTemp + relativedelta(minutes=1)

            strStatus = str(session.FindById("wnd[0]/usr/lbl[36,3]").Text).strip()

            DownloadFileSP02 = str(session.FindById("wnd[0]/usr/lbl[51,3]").Text).strip()

            for objPaquete in colPaquete:
                if objPaquete.strTitle == DownloadFileSP02 and datTemp > objPaquete.datEjecucion:
                    if strStatus == '-':
                        strSpool = str(session.FindById("wnd[0]/usr/lbl[3,3]").Text).strip()
                        session.FindById("wnd[0]/usr/chk[1,3]").Selected = True
                        session.FindById("wnd[0]/mbar/menu[0]/menu[2]/menu[1]").Select()

                        if session.Info.ScreenNumber == 200: session.FindById("wnd[0]").SendVKey(0)

                        sbar = session.ActiveWindow.FindByName("sbar", "GuiStatusbar").Text

                        objPaquete.douSpool = int(strSpool)
                        objPaquete.strFile = sbar[57:]
                        objPaquete.strPath = sbar[8:16]

                        objPaquete.booFileTXTCopy = CopiarPaquete(strPath, objPaquete.strTitle, objPaquete.strPath)
                        objPaquete.booFileTXT = True

                    else:
                        # 'Si el archivo no esta para bajar
                        objPaquete.booFileTXTCopy = False
                        objPaquete.booFileTXT = True

            session.FindById("wnd[0]").SendVKey(3)
            return DownloadFileSP02


        datDesde: datetime
        datHasta: datetime
        colPaquete: list[clsPaquete]

        if booStart:
            session.StartTransaction("SMX")
            if session.Info.Transaccion != 'SMX':
                messagebox.showinfo(message="No tiene acceso a la transacción SMX", title="Falta acceso SAP")
                # finalizar la ejecución
                exit()

            SMX_SelectorLayout(session, "/SMX_BOT")
            datDesde = colPaquete[0].datEjecucion - relativedelta(seconds=15)
            datHasta = colPaquete[-1].datEjecucion + relativedelta(minute=1)

            SMX_Filtrar(session, datDesde, datHasta)

        session.FindById("wnd[0]").SendVKey(80)

        strJobScreenFirst = ''
        strJobScreenLast = ''
        while True:
            listRegistros: [clsPaquete.clsCamposSMX] = SMX_InstanciarRegScreen(session)

            for registro in listRegistros:

                strJob = registro.strJob
                strStatus = registro.strStatus
                intMinutos = registro.intMinutos
                lngPosX = registro.intPosX
                lngPosY = registro.intPosY

                if registro.strJob == listRegistros[0].strJob:
                    strJobScreenFirst = strJob

                # Controlar si se repite pantalla cuando llega al final
                if strJob == strJobScreenLast: break

                # Controlar si el Job tiene asociado un paquete
                booTemp = True
                for objPaquete in colPaquete:
                    if objPaquete.strJob == strJob and not objPaquete.booTry():
                        booTemp = False
                        break

                if booTemp:
                    session.FindById(f"wnd[0]/usr/lbl[{lngPosX},{lngPosY}]").SetFocus()

                    match strStatus:
                        case "terminado":
                            session.FindById("wnd[0]").SendVKey(2)
                            # Si termino sin dato para bajar
                            if session.ActiveWindow.FindByName("sbar",
                                                               "GuiStatusbar").Text == "No existe ninguna lista":
                                session.FindById(f"wnd[0]/usr/lbl[{lngPosX},{lngPosY}]").SetFocus()
                                temp = LecturaSPOOLPasos(session)

                                for objPaquete in colPaquete:
                                    if objPaquete.strTitle == temp and objPaquete.booTry():
                                        objPaquete.booFileTXTCopy = False
                                        objPaquete.booFileTXT = False
                                        objPaquete.status = "terminado"
                                        objPaquete.strJob = strJob
                                        objPaquete.Minutos = intMinutos
                                        objPaquete.douSpool = 0
                                        break
                            else:
                                # Si se baja el TXT
                                temp = DownloadFileSP02(session, strPath, colPaquete)

                                for objPaquete in colPaquete:
                                    if objPaquete.strTitle == temp:
                                        objPaquete.status = "terminado"
                                        objPaquete.strJob = strJob
                                        objPaquete.Minutos = intMinutos

                        case "cancelado":
                            session.FindById(f"wnd[0]/usr/lbl[{lngPosX},{lngPosY}]").SetFocus()
                            session.FindById("wnd[0]").SendVKey(3)
                            temp = LecturaSPOOLPasos(session)

                            for objPaquete in colPaquete:
                                if objPaquete.strTitle == temp:
                                    objPaquete.status = "cancelado"
                                    objPaquete.strJob = strJob
                                    objPaquete.Minutos = intMinutos
                                    objPaquete.douSpool = 0
                                    objPaquete.booFileTXTCopy = False
                                    objPaquete.booFileTXT = False

            strJobScreenLast = strJobScreenFirst
            session.FindById("wnd[0]").SendVKey(82)



    def __SMX_CalcularJobScreen(session: object, intChildrenUltimoCampo: int):

        intChildren = 0

        for oSubComponent in session.children(0).children(4).children:
            children = f".Children({intChildren})"
            intChildren = + 1

            booContType = oSubComponent.ContainerType
            ID = oSubComponent.ID
            strType = oSubComponent.Type
