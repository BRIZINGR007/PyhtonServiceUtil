import pytest
from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


@pytest.fixture
def app():
    app = FastAPI()
    app.state.process_pool = ProcessPoolExecutor()
    app.state.thread_pool = ThreadPoolExecutor()
    return app

@pytest.fixture
def sample_payload():
    