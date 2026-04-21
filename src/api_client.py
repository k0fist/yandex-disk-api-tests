from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class ApiConfig:
    base_url: str
    token: str
    timeout: int = 10


class ApiClient:
    def __init__(self, config: ApiConfig, session: requests.Session | None = None):
        self.config = config
        self.session = session or requests.Session()
        self.session.headers.update({
            "Authorization": f"OAuth {self.config.token}",
            "Accept": "application/json",
        })

    def _url(self, path):
        """Сформировать полный URL для запроса к API Яндекс Диска."""
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get_root(self):
        """Получить общую информацию о диске пользователя в Яндекс Диске."""
        return self.session.get(
            self._url(""),
            timeout=self.config.timeout,
        )
    
    def get_upload_link(self, remote_path, overwrite=True):
        """Получить ссылку для загрузки файла на Яндекс Диск."""
        return self.session.get(
            self._url("resources/upload"),
            params={
                "path": remote_path,
                "overwrite": str(overwrite).lower(),
            },
            timeout=self.config.timeout,
        )

    def upload_file(self, local_path, remote_path, overwrite=True):
        """Загрузить локальный файл на Яндекс Диск."""
        link_response = self.get_upload_link(remote_path=remote_path)
        link_response.raise_for_status()

        upload_url = link_response.json()["href"]

        with open(local_path, "rb") as f:
            return requests.put(
                upload_url,
                data=f,
                timeout=self.config.timeout
            )
    
    def delete_resource(self, remote_path, permanently=True):
        """Удалить файл или папку с Яндекс Диска."""
        return self.session.delete(
            self._url("resources"),
            params={
                "path": remote_path,
                "permanently": str(permanently).lower(),
            },
            timeout=self.config.timeout,
        )
    
    def copy_file(self, from_path, to_path, overwrite=True):
        """Скопировать файл на Яндекс Диске."""
        return self.session.post(
            self._url("resources/copy"),
            params={
                "from": from_path,
                "path": to_path,
                "overwrite": str(overwrite).lower(),
            },
            timeout=self.config.timeout,
        )
    
    def get_resource(self, remote_path):
        """Получить метаинформацию о файле или папке на Яндекс Диске."""
        return self.session.get(
            self._url("resources"),
            params={"path": remote_path},
            timeout=self.config.timeout,
        )