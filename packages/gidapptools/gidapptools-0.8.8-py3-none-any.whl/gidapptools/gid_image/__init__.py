from gidapptools.errors import MissingOptionalDependencyError


MissingOptionalDependencyError.check_is_importable("PIL", "Pillow")
