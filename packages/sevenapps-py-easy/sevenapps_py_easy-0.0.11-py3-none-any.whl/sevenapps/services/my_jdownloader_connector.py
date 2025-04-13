import myjdapi


class MyJDownloaderConnector:

    def __init__(self, user, password, device, app_key):
        self.jdownloader_connection = self.connect_to_jdownloader(user, password, device, app_key)

    def connect_to_jdownloader(self, user, password, device, app_key):

        jd = myjdapi.Myjdapi()
        jd.set_app_key(app_key)
        jd.connect(user, password)

        # Obtener los dispositivos disponibles
        jd.update_devices()

        # Retornamos el device
        return jd.get_device(device)