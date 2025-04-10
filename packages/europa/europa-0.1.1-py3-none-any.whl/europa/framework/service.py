from abc import ABC, abstractmethod
import time
from threading import Thread
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from europa.framework.endpoint import expose

class _BaseService(ABC):
    """
    Base class for microservices with a calculation loop and REST endpoints.
    """

    SLEEP_INTERVAL = 5.0

    def __init__(self):
        self._running = False
        self._loop_thread = None

        self.app = FastAPI(title=self.__class__.__name__)  # Use class name as title
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # List of allowed origins
            allow_credentials=True,  # Allow cookies
            allow_methods=["*"],    # Allow all methods
            allow_headers=["*"],    # Allow all headers
        )

        # Automatically register methods decorated with @expose.<METHOD>
        self._register_exposed_methods()

    def _register_exposed_methods(self):
        """
        Scan for methods decorated with @expose.<METHOD> in the class and register 
        them as REST endpoints in FastAPI's router
        """

        self.router = APIRouter()

        for attr_name in dir(self):  # Inspect the class, not the instance
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "_http_method"):
                path = f"/{attr_name}"  # Derive path from method name (e.g., "get_status" -> "/get_status")
                method = getattr(
                    attr, "_http_method"  # Retrieve HTTP method from metadata
                )
                print(f"Registering route: {method} {path}")
                self.router.add_api_route(path, attr, methods=[method])

        self.app.include_router(self.router)  # Attach the router to the app

    def _start(self):
        """
        Start the calculation loop in a separate thread.
        """
        self._running = True

        # run custom startup before the calc loop starts
        self.custom_startup()

        self._loop_thread = Thread(target=self._run_calculation_loop, daemon=True)
        if not self._loop_thread.is_alive():
            self._loop_thread.start()

    def stop(self):
        """
        Stop the calculation loop.
        """
        self._running = False

    def launch(self, port: int):
        """
        Launch the FastAPI app using Uvicorn.
        Automatically starts the calculation loop before launching.
        """
        import uvicorn

        self._start()  # Start calculation loop in a seperate thread
        uvicorn.run(self.app, host="0.0.0.0", port=port, log_level='debug')

    def _run_calculation_loop(self):
        """
        Continuous calculation loop running synchronously.
        Calls the `calculate()` method and sleeps for the specified interval.
        """
        while self._running:
            try:
                self._pre_calculate()
                self._calculate()
                self._post_calculate()
            except Exception as e:
                print(f"Error in calculation loop: {e}")
            time.sleep(self.SLEEP_INTERVAL)  # Sleep for the configured interval

    def _pre_calculate(self):
        """ """
        pass

    @abstractmethod
    def _calculate(self):
        """
        This method needs to be implemented by the different TYPES of services
        classes (eg CalculationService, QueueService, etc)
        """

    def _post_calculate(self):
        """ """
        pass

    def custom_startup(self):
        """
        This function can be overriden to have a custom logic
        """
        pass

    @expose.GET
    async def get_status(self):
        return {"status": "running"}

    @expose.POST
    async def post_data(self, data: dict):
        return {"received": data}


class CalculationService(_BaseService):
    def __init__(self):
        super().__init__()

    def _calculate(self):
        """ """
        start_time = time.time()
        self.calculate()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function 'calculate' executed in {elapsed_time:.4f} seconds")

    @abstractmethod
    def calculate(self):
        """
        This method needs to be implemented by the type of Calculation Service
        """
