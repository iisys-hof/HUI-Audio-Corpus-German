from typing import Dict


class DependencyInjectionError(Exception):

    def __init__(self, exception: Exception, classConfig: Dict[str,str] , className : str, requestedClassName : str):
        self.exception = exception
        self.classConfig = classConfig
        self.className= className
        self.requestedClassName = requestedClassName

        super().__init__(f'Dependent object {self.className} could not be injected for {self.requestedClassName}')

    def __str__(self):
        return self.getString()

    def getString(self):
        string = f'\n+++++++++++++++++++++++++\n'
        string += 'Error during creation of dependencys. Maybe your config is wrong. \n'
        string += f'Dependent object "{self.className}" could not be injected for "{self.requestedClassName}" \n'
        string += f'with error message: {self.exception} \n'
        string += f'config parameter used are: {self.classConfig}\n'
        string += f'+++++++++++++++++++++++++\n'
        return string