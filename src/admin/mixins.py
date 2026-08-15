from fastapi import Request


class RoleMixin:
    allowed_roles: set[str] = set()
    write_roles: set[str] = set()

    @staticmethod
    def _role(request: Request) -> str | None:
        return request.session.get("role")

    def is_visible(self, request: Request) -> bool:
        return self._role(request) in self.allowed_roles

    def is_accessible(self, request: Request) -> bool:
        return self._role(request) in self.allowed_roles

    async def check_can_create(self, request: Request) -> bool:
        return self._role(request) in self.write_roles

    async def check_can_edit(self, request: Request, model) -> bool:
        return self._role(request) in self.write_roles

    async def check_can_delete(self, request: Request, model) -> bool:
        return self._role(request) in self.write_roles
