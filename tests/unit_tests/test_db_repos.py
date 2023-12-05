import pytest

from app.repositories.db_repository import (CRUDRepository, DishRepository,
                                            MenuRepository, SubmenuRepository)
from tests import conftest as c
from tests.fixtures.data import Model
from tests.utils import get_method


class TestCRUDRepository:
    crud: CRUDRepository

    @pytest.fixture
    def init(self, get_test_session: c.AsyncSession) -> None:
        self.crud = CRUDRepository(Model, get_test_session)

    @pytest.mark.parametrize('method_name',
                             ('is_update_allowed', 'is_delete_allowed')
                             )
    def test_is_allowed_methods_return_True(self, init, method_name: str) -> None:
        method = get_method(self.crud, method_name)
        assert method() is True


class TestMenuRepository:
    NOT_FOUND = 'menu not found'
    OBJECT_ALREADY_EXISTS = 'Меню с таким заголовком уже существует.'
    repo_db: MenuRepository

    @pytest.fixture
    def init(self, get_test_session: c.AsyncSession) -> None:
        self.repo_db = MenuRepository(get_test_session)

    def test_messages(self, init) -> None:
        assert self.NOT_FOUND == self.repo_db.NOT_FOUND
        assert self.OBJECT_ALREADY_EXISTS == self.repo_db.OBJECT_ALREADY_EXISTS


class TestSubmenuRepository:
    NOT_FOUND = 'submenu not found'
    OBJECT_ALREADY_EXISTS = 'Подменю с таким заголовком уже существует.'
    repo_db: SubmenuRepository

    @pytest.fixture
    def init(self, get_test_session: c.AsyncSession) -> None:
        self.repo_db = SubmenuRepository(get_test_session)

    def test_messages(self, init) -> None:
        assert self.NOT_FOUND == self.repo_db.NOT_FOUND
        assert self.OBJECT_ALREADY_EXISTS == self.repo_db.OBJECT_ALREADY_EXISTS

    def test_perform_create_method(self, init) -> None:
        create_data = {}
        self.repo_db.perform_create(create_data, 'menu.id')
        assert create_data['menu_id'] == 'menu.id'


class TestDishRepository:
    NOT_FOUND = 'dish not found'
    OBJECT_ALREADY_EXISTS = 'Блюдо с таким заголовком уже существует.'
    repo_db: DishRepository

    @pytest.fixture
    def init(self, get_test_session: c.AsyncSession) -> None:
        self.repo_db = DishRepository(get_test_session)

    def test_messages(self, init) -> None:
        assert self.NOT_FOUND == self.repo_db.NOT_FOUND
        assert self.OBJECT_ALREADY_EXISTS == self.repo_db.OBJECT_ALREADY_EXISTS

    def test_perform_create_method(self, init) -> None:
        create_data = {}
        self.repo_db.perform_create(create_data, 'submenu.id')
        assert create_data['submenu_id'] == 'submenu.id'
