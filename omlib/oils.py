# TODO - ERROR HANDLING
# TODO - Check column names, throw exceptions if cols not found in dataframes
# TODO - Add product blending equations(absolute lowest priority)

class CrudeOil:
    def __init__(self):
        self.api_gravity = None

    def get_api_gravity(self, specific_gravity):
        self.api_gravity = 141 / specific_gravity - 131.5
        return
