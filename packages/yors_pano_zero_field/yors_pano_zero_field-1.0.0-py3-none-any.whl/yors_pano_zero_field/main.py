# 定义常量来替代 sys.float_info.max 和 sys.maxsize
MAX_FLOAT = 1.7976931348623157e+308
MAX_INT = 9223372036854775807

class ZeroAnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

ZERO_ANY = ZeroAnyType("*")

class ZeroField:
    @staticmethod
    def field(field: str | list, data: dict = None) -> tuple[str | list, dict] | tuple[str | list]:
        if data:
            return (field, data,)
        return (field,)

    @staticmethod
    def boolean(
            default: float = False, force: bool = False
    ) -> tuple[str, dict]:
        field_data = {"default": default, "force": force}
        return ZeroField.field("BOOLEAN", field_data)

    @staticmethod
    def float(
            default: float = 1, min: float = -MAX_FLOAT, max: float = MAX_FLOAT, step: float = 0.01,
            force: bool = False
    ) -> tuple[str, dict]:
        field_data = {"default": default, "min": min, "max": max, "step": step, "forceInput": force}
        return ZeroField.field("FLOAT", field_data)

    @staticmethod
    def int(
            default: int = 1, min: int = -MAX_INT, max: int = MAX_INT, step: int = 1, force: bool = False
    ) -> tuple[str, dict]:
        field_data = {"default": default, "min": min, "max": max, "step": step, "forceInput": force}
        return ZeroField.field("INT", field_data)

    @staticmethod
    def string(
            default: str = '',
            multiline: bool = False,
            force: bool = False,
            dynamicPrompts: bool = False,
            description: str = '',
    ) -> tuple[str, dict]:
        field_data = {"default": default, 'multiline': multiline, "forceInput": force, "dynamicPrompts": dynamicPrompts,"description":description}
        return ZeroField.field("STRING", field_data)

    @staticmethod
    def any(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field(ZERO_ANY, field_data)

    @staticmethod
    def latent(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("LATENT", field_data)

    @staticmethod
    def image(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("IMAGE", field_data)

    @staticmethod
    def mask(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("MASK", field_data)

    @staticmethod
    def model(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("MODEL", field_data)

    @staticmethod
    def lora(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("LORA", field_data)

    @staticmethod
    def vae(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("VAE", field_data)

    @staticmethod
    def conditioning(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("CONDITIONING", field_data)

    @staticmethod
    def clip(force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field("CLIP", field_data)

    @staticmethod
    def combo(data: list, force: bool = False):
        field_data = {"forceInput": force}
        return ZeroField.field(data, field_data)