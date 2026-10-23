from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings

class MarioLandProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Super Mario Land"
    hash = "b259feb41811c7e4e1dc200167985c84"
    patch_file_ending = ".apsml"
    result_file_ending = ".gb"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().marioland_settings.rom_file, "rb") as f:
            return f.read()

def write_tokens(world, patch: MarioLandProcedurePatch) -> None:
    # so the client can tell a patched ROM from a vanilla one.
    patch.write_token(APTokenTypes.WRITE, 0x3FEB, b"SMLAP")

    patch.write_file("token_data.bin", patch.get_token_binary())