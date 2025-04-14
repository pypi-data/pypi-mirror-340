import xfox
from Amisynth.utils import options_slash


@xfox.addfunc(xfox.funcs, name="addSlashChoiceOption")
async def add_choice(nombre_opcion: str, name_choice: str, value_choice: str, *args, **kwargs):
    """
    Agrega un choice a una opción existente.

    Uso:
        $add_choice[mensaje;josue;Josuehee]
    """
    for opcion in options_slash:
        if opcion["name_option"] == nombre_opcion:
            opcion.setdefault("choices", []).append({
                "name_choice": name_choice,
                "value_choice": value_choice
            })
            print("[DEBUG ADDCHOICEOPTION] Choice Agregado correctamente.")
            return ""
    print("[SLASH] No se encontró una opción con nombre '{nombre_opcion}' para agregar choice.")
    raise ValueError(f":x: No se encontró una opción con nombre '{nombre_opcion}' para agregar choice.")